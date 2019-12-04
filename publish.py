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
    """ Upload content to the server """
        
    data = {'filename': filename}
    files = {'file': open(filename, 'rb')}
    url = 'https://%s/api/deposit/depositions/%s/files' % (server, article_id)
    response = requests.post(url, params={'access_token': token},
                              data=data, files=files)
    if response.status_code != 201:
        raise IOError("%s: " % response.status_code + response.json()["message"])

    
def update_metadata(server, token, article_id, article):
    """ Upload metadata to the server """

    # Any empty entry will make the upload to fail with a cryptic error message
    
    headers = {"Content-Type": "application/json"}
    url = 'https://%s/api/deposit/depositions/%s' % (server, article_id)

    data = {
        'metadata': {
            'title': article.title,
            'upload_type': 'publication',
            'publication_type': 'article',
            'description' : article.type,
            'creators': [],
            'access_right' : 'open',
            'license' : 'cc-by',
            'keywords' : article.keywords.split(','),
            'contributors' : [
#                {'name': article.editors[0].name, 'type': 'Editor' },
#                {'name': article.reviewers[0].name, 'type': 'Other' },
#                {'name': article.reviewers[1].name, 'type': 'Other' }
            ],
            'related_identifiers' : [
#                {'relation': 'isSupplementedBy', 'identifier': article.code.doi},
#                {'relation': 'cites',     'identifier': article.replication.doi}
            ],
            'journal_title' : "ReScience C",
            'journal_volume' : "%s" % article.journal_volume,
            'journal_issue' : "%s" % article.journal_issue,
            'journal_pages' : "#%s" % article.article_number,
# communities (rescience) will be populated for actual server only
            'communities' : [], 
        }
    }

    for author in article.authors:
        name = author.name
        orcid = author.orcid
        author = {'name' : name}
        if len(orcid) > 0:
            author['orcid'] = orcid
        data['metadata']['creators'].append(author)
    
    if article.type in ["replication", "Replication"]:
        if article.code.doi is not None:
            data['metadata']['related_identifiers'].append(
                {'relation': 'isSupplementedBy', 'identifier': article.code.doi})
#        if article.replication.doi is not None:
#            data['metadata']['related_identifiers'].append(
#                {'relation': 'cites',     'identifier': article.replication.doi})

    if server == "zenodo.org":
        data['metadata']["communities"].append({'identifier': 'rescience'})
    if len(article.editors) > 0:
        data['metadata']['contributors'].append(
            {'name': article.editors[0].name, 'type': 'Editor' } )
#    if len(article.editors) > 0 and len(article.reviewers[0].name) > 0:
#        data['metadata']['contributors'].append(
#            {'name': article.reviewers[0].name, 'type': 'Other' } )
#    if len(article.editors) > 1 and len(article.reviewers[1].name) > 0:
#        data['metadata']['contributors'].append(
#            {'name': article.reviewers[1].name, 'type': 'Other' } )


    response = requests.put(url, params={'access_token': token},
                            data=json.dumps(data),  headers=headers)
    if response.status_code != 200:
        if "errors" in response.json().keys():
            print(response.json()["errors"])
        raise IOError("%s: " % response.status_code +
                      response.json()["message"])

    
def publish(server, token, article_id):
    """ Make entry public (DANGER ZONE) """
    
    url = 'https://%s/api/deposit/depositions/%s/actions/publish' % (server, article_id)
    response = requests.post(url, params={'access_token': token})
    if response.status_code != 202:
        raise IOError("%s: " % response.status_code +
                      response.json()["message"])

    
def git_branch(metadata_file, article_file, article_doi):
    """
    Create a git branch to store the file and the metadata in a dedicated
    directory.
    """
    
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
    os.system("git stash apply")
    os.system("git stash drop")
    os.system("git checkout master")
    return branch

     
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    import argparse

    # Argument parsing
    parser = argparse.ArgumentParser(description='Publishing on Zenodo')
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
    if args.zenodo:
        server     = "zenodo.org"
        token_name = "ZENODO_TOKEN"
    else:
        server     = "sandbox.zenodo.org"
        token_name = "ZENODO_SANDBOX_TOKEN"
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
        print("Metadata is newer than PDF, probably PDF needs to be rebuilt")
        sys.exit(0)

    # Read article metadata
    with open(metadata_file) as file:
        article = Article(file.read())

    # Extract doi from metadata
    article_doi = article.article_doi
    article_id = article_doi.split('.')[-1]

    # Upload content
    print("Uploading content to Zenodo... ", end="")
    upload_content(server, token, article_id, article_file)
    print("done!")
        
    # Update metadata
    print("Updating metadata to Zenodo... ", end="")
    update_metadata(server, token, article_id, article)
    print("done!")

    # Publish entry
    print("Publishing on Zenodo... ", end="")
    publish(server, token, article_id)
    print("done!")

    print("Entry is online at ", end="")
    print("https://%s/record/%s" % (server, article_id))
    print()

    if args.zenodo:
        # Create a new local directory containing article and metadata
        print("Creating local directory...")
        branch = git_branch(metadata_file, article_file, article_doi)
        print()
        print("---------------------------------------------------")
        print("You can now merge {0} into master".format(branch))
        print("---------------------------------------------------")
    


