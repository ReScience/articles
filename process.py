#! /usr/bin/env python3
# -----------------------------------------------------------------------------
# Copyright 2018 ReScience C - BSD two-clauses licence
#
# This script reserves a DOI on zenodo and assign a new article number
# Zenodo REST API at http://developers.zenodo.org
# -----------------------------------------------------------------------------
import json
import yaml
import requests

def reserve_doi(server, token):
    """ Reserve a new DOI on Zenodo """
    
    headers = { "Content-Type": "application/json" }
    url = 'https://%s/api/deposit/depositions' % server
    response = requests.post(url, params={'access_token': token},
                             json={}, headers=headers)
    if response.status_c ode != 201:
        raise IOError("%s: " % response.status_code +
                      response.json()["message"])
    data = response.json() 
    return data["id"], data["metadata"]["prereserve_doi"]["doi"]




# -----------------------------------------------------------------------------
if __name__ == '__main__':
    import os
    import sys
    import argparse
    from article import Article

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

    # Check for metadata and article files
    metadata_file = args.metadata
    if not os.path.exists(metadata_file):
        print("Metadata file not found ({0}).".format(metadata_file))
        sys.exit(0)

    article_file = args.pdf
    if not os.path.exists(article_file):
        print("Article file not found ({0}).".format(article_file))
        sys.exit(0)

    # Read article metadata
    with open(metadata_file) as file:
        article = Article(file.read())

    # Assign server and token
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

    # Get DOI
    article_id, article_doi = reserve_doi(server, token)

    # Display information
    print("Article ID: ", article_id)
    print("Article DOI:", article_doi)
    print("Article URL: https://{0}/record/{1}/files/{2}".format(
        server, article_id, os.path.basename(article_file)))
