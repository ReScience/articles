#! /usr/bin/env python3
# -----------------------------------------------------------------------------
# Copyright 2018 ReScience C - BSD two-clauses licence
#
# This script takes care of uploading a new ReScience article to Zenodo.
# It requires the acticle (PDF) article and the metadata (YAML).
# Zenodo REST API at http://developers.zenodo.org
# -----------------------------------------------------------------------------
import json
import os
import os.path
import requests
from article import Article

def upload_content(server, token, article_id, filename):
    """ Upload content to server """
        
    data = {'filename': filename}
    files = {'file': open(filename, 'rb')}
    url = 'https://%s/api/deposit/depositions/%s/files' % (server, article_id)
    response = requests.post(url, params={'access_token': token},
                              data=data, files=files)
    if response.status_code != 201:
        raise IOError("%s: " % response.status_code + response.json()["message"])

    
def update_metadata(server, token, article_id, article):
    """ Upload content metadata to server """


    # ! Any empty entry will ake the upload to fail with a cryptic error message
    
    headers = {"Content-Type": "application/json"}
    url = 'https://%s/api/deposit/depositions/%s' % (server, article_id)

    data = {
        'metadata': {
            'title': article.title,
            'upload_type': 'publication',
            'publication_type': 'article',
            'description' : article.type,
            'creators': [ {'name': author.name,
                           'orcid': author.orcid} for author in article.authors],
            'access_right' : 'open',
            'license' : 'cc-by',
            'keywords' : article.keywords.split(),
            'contributors' : [
                {'name': article.editors[0].name, 'type': 'Editor' },
                {'name': article.reviewers[0].name, 'type': 'Other' },
                {'name': article.reviewers[1].name, 'type': 'Other' }
            ],
            'related_identifiers' : [
#                {'relation': 'isSupplementedBy', 'identifier': article.code.doi},
#                {'relation': 'cites',     'identifier': article.replication.doi}
            ],
            'journal_title' : "ReScience C",
            'journal_volume' : "%s" % article.journal_volume,
            'journal_issue' : "%s" % article.journal_issue,
            'journal_pages' : "%s" % article.article_number,
            'communities' : [{'identifier': 'rescience'}],
        }
    }

    if article.type in ["replication", "Replication"]:
        if article.code.doi is not None:
            data['related_identifiers'].append(
                {'relation': 'isSupplementedBy', 'identifier': article.code.doi})
        if article.replication.doi is not None:
            data['related_identifiers'].append(
                {'relation': 'cites',     'identifier': article.replication.doi})
    
    response = requests.put(url, params={'access_token': token},
                            data=json.dumps(data),  headers=headers)
    if response.status_code != 200:
        raise IOError("%s: " % response.status_code +
                      response.json()["message"])

    
def publish(server, token, article_id):
    """ Publish entry """
    
    url = 'https://%s/api/deposit/depositions/%s/actions/publish' % (server, article_id)
    response = requests.post(url, params={'access_token': token})
    if response.status_code != 202:
        raise IOError("%s: " % response.status_code +
                      response.json()["message"])


     
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    import argparse

    # Argument parsing
    parser = argparse.ArgumentParser(description='DOI pre-reservation on Zenodo')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--sandbox', action='store_true',
                       help='Use the sandbox server')
    group.add_argument('--zenodo',  action='store_true',
                       help='Use the production server')
    parser.add_argument('--metadata', action='store', required=True,
                        help="Article metadata (YAML format)")
    parser.add_argument('--pdf', action='store', required=True,
                        help="Article (PDF format)")
    args = parser.parse_args()


    # Check if we have connection information
    if args.sandbox:
        server     = "sandbox.zenodo.org"
        token_name = "ZENODO_SANDBOX_TOKEN"
    else:
        server     = "zenodo.org"
        token_name = "ZENODO_TOKEN"
    token = os.getenv(token_name)
    if token is None:
        url = "".format(server)
        print("No token found ({0})".format(token_name))
        print("You can request one from https://{0}/account/settings/applications/tokens/new/".format(server))
        sys.exit(0)


    # Check for metadata and article files
    metadata_file = args.metadata
    if not os.path.exists(metadata_file):
        print("Metadata file not found ({0}).".format(metadata_file))
        sys.exit(0)

    article_file = args.pdf
    if not os.path.exists(article_file):
        print("Article file not found ({0}).".format(article_file))
        sys.exit(0)
        
    # Check if metadata file is newer than pdf
    if os.path.getmtime(metadata_file) > os.path.getmtime(article_file):
        print("Metadata is newer than PDF, probably PDF needs to be rebuild")
        sys.exit(0)

    # Read article metadata
    with open(metadata_file) as file:
        article = Article(file.read())

    # Extract doi from metadata
    article_doi = article.article_doi
    article_id = article_doi.split('.')[-1]

    # Upload content
    print("Uploading content... ", end="")
    upload_content(server, token, article_id, article_file)
    print("done!")
        
    # Update metadata
    print("Updating metadata... ", end="")
    update_metadata(server, token, article_id, article)
    print("done!")

    # Publish entry
    print("Publishing... ", end="")
    publish(server, token, article_id)
    print("done!")

    print("Entry is online at ", end="")
    print("https://%s/record/%s" % (server, article_id))
    print()

    # Create a new local directory containing article and metadata
    # This is done in a new branch
    branch = article_doi.replace('/','_')
    directory = branch
    src_pdf = article_file
    dst_pdf = os.path.join(directory, "article.pdf")
    src_yaml = metadata_file
    dst_yaml = os.path.join(directory, "article.yaml")
    src_bib = metadata_file
    dst_bib = os.path.join(directory, "article.bib")

    
    os.system("git stash")
    os.system("git checkout -b {0}".format(branch))
    os.system("mkdir {0}".format(directory))
    os.system("cp {0} {1}".format(src_pdf, dst_pdf))
    os.system("cp {0} {1}".format(src_yaml, dst_yaml))
    os.system("./yaml-to-bibtex.py -i {0} -o {1}".format(src_bib, dst_bib))
    os.system("git add {0}".format(dst_pdf))
    os.system("git add {0}".format(dst_yaml))
    os.system("git add {0}".format(dst_bib))
    os.system("git commit -m 'Added entry {0}'".format(article_doi))
    os.system("git checkout master")
    print()

    print("Local entry has been created in {0}.".format(directory))
    print("A new git branch ({0}) has been created.".format(branch))

    


