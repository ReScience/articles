## Publishing a ReScience C article

This document is intended for ReScience editors. Congrats on accepting a ReScience article for publication! If you're new at editing, this document will guide you through all the necessary steps. If you are a seasoned editor, this will be a handy reference to any steps you may have forgotten. Follow the steps below to complete the metadata, submit to Zenodo, and get the final article published.

### What you will need to begin
- The article metadata file (`metadata.yaml`) from the author's repository.   At this time the metadata file **will be missing** the article DOI, number and URL.  This is expected and something you will fix over the coming steps.
- The near final article itself (`article.pdf`)

Have these two files ready before cloning this repository. This would also be a good time to ask reviewers to share their [ORCIDs](https://orcid.org/) for the metadata. You can do this in the review issue.

### Publishing the article

There are 6 parts to publishing the article. 

| Part | What it does |
|:--|:--|
| [Set up credentials](#set-up-credentials)  | Get setup to programmatically submit to Zenodo |
| [Update the metadata 1](#update-the-metadata) | Add editor, reviewers, dates of submission, acceptance & publication |
| [Pre-publish the paper](#pre-publish-the-paper) | Reserve the DOI  |
| [Update the metadata 2](#update-the-metadata) | Add volume, issue, page, doi to the paper & generate new pdf |
| [Publish the paper](#publish-the-paper) | Make the final Zenodo deposit |
| [Update the website](#website-update) | Enter bib information for the website  |



### 15 steps to publishing a ReScience article

1\. Clone this repository locally.  
2\. Copy the authors `metadata.yaml` and `article.pdf` into this folder

### Set up Credentials

3\. To submit the paper and metadata to Zenodo, you will need to set up access tokens. Setting up your Zenodo sandbox and production tokens is a one time step. If you have done this before, skip over to step 4.

The first step is thus to request this information from Zenodo. Before
proceeding further, you'll need a Zenodo token that can be requested from the
[sandbox
server](https://sandbox.zenodo.org/account/settings/applications/tokens/new/)
and from the [actual
server](https://zenodo.org/account/settings/applications/tokens/new/). When creating tokens, be sure to check all three scopes.
The sandbox token is expected to be stored in the environment variable
`ZENODO_SANDBOX_TOKEN` while the true token must be stored in `ZENODO_TOKEN`, e.g.:
```bash
export ZENODO_SANDBOX_TOKEN="access token"
export ZENODO_TOKEN="access token"
```
And to check it was set correctly:
```bash
echo $ZENODO_SANDBOX_TOKEN
echo $ZENODO_TOKEN
```
If you copy these into your bash profile you won't have to look for them again. We advise you to **first test the procedure** on the sandbox server using the `--sandbox` switch. More on this in the next step.

### Update the metadata 1

4\. Complete the `metadata.yaml`: 
  - Add the submission (if not already there), as well as acceptance and publication dates in the dates section. This is mandatory for steps 5 to 7 to work properly.
  - Check that the code, data and replication sections have been correctly filled (for example, add the often missing DOI of the replicated paper).
  - Complete the information about the contributors (reviewers and editors), with ORCIDs.

### Pre-publish the paper

This step reserves the DOI for the paper, allowing you to update metadata before final publication. 

5\. Run the [process.py](process.py) script using the provided metadata
file. It requires Python 3 plus the libraries [PyYAML](https://pyyaml.org/), [Requests](https://requests.kennethreitz.org/), and [dateutil](https://dateutil.readthedocs.io/en/stable/).

First run on the sandbox server to check everything is OK:

```bash
$ ./process.py --sandbox --metadata metadata.yaml --pdf article.pdf
Article ID: xxxxx
Article DOI: 10.xxxx/zenodo.xxxxx
Article URL: https://sandbox.zenodo.org/record/xxxxxx/file/article.pdf
```

6\. Did this work? Were there any problems? If there were no problems, then use the production server using the `--zenodo` switch instead of the `--sandbox` switch.

```bash
$ ./process.py --zenodo --metadata metadata.yaml --pdf article.pdf
Article ID: xxxxx
Article DOI: 10.xxxx/zenodo.xxxxx
Article URL: https://zenodo.org/record/xxxxxx/file/article.pdf
```

7\. If no errors were returned, you have successfully reserved a DOI! Next we’ll grab an issue, volume and article numbers.

```
NOTE: This DOI will not resolve anywhere. This behavior is expected
```

### Update the metadata 2

In this step, you'll update `metadata.yaml`, pull request the file back to the author, generate a new PDF (which will now contain the volume, issue, page, doi information), and copy that back here.

8\. Look at the last number on  [this GitHub issue](https://github.com/ReScience/ReScience/issues/48) and choose the next one in the series. Post a comment to claim that issue for your article. This comment
serves to avoid that two editors assign the same numbers to two
different articles.

9\. Then add these two bits of information (volume and article number) along with the Zenodo DOI and URL to `metadata.yaml`. 

You should complete the missing information and verify the whole file before moving on. The information you must add are:
  - DOI (from Zenodo)
  - article URL (from Zenodo)
  - issue, volume, and article numbers.

10\.  Pull request just the `metadata.yaml` back to the author's repo (this will mean copying this file back to the author repo fork). Once the pull-request is merged, ask them to prepare a new `article.pdf`. The PDF will now contain the volume, article number and DOI.

11\. Copy the newly updated `article.pdf` and `metadata.yaml` back to this repo.

  
### Publish the paper

12\. In order to publish the **final** article, you'll need to run the
[publish.py](publish.py) script:

```bash
$ ./publish.py --sandbox --metadata metadata.yaml --pdf article.pdf
Uploading content... done!
Uploading metadata... done!
Publishing... done!
Entry is online at https://zenodo.org/record/xxxxx

Saved working directory and index state WIP on master: 30cd860 Typo
Switched to a new branch '10.5072_zenodo.xxxxx'
[10.5072_zenodo.248588 2e613e7] Created local entry for 10.5072/zenodo.xxxxx
 3 files changed, 158 insertions(+)
 create mode 100644 10.5072_zenodo.xxxxx/article.bib
 create mode 100644 10.5072_zenodo.xxxxx/article.pdf
 create mode 100644 10.5072_zenodo.xxxxx/article.yaml
Switched to branch 'master'
Your branch is up to date with 'origin/master'.

Local entry has been created in 10.5072_zenodo.xxxxx
A new git branch (10.5072_zenodo.xxxxx) has been created.
```

This example uses the sandbox, replace `--sandbox` by `--zenodo` for
publishing to the Zenodo production site. 

This will create a new folder and branch in `Rescience/articles` named after the article's DOI that contains three files:
  - The article (`article.pdf`)
  - metadata (`article.yaml`)
  - bib file (`article.bib`)

- Now push this branch:

```
git push origin <DOI>
```


13\. Discard any changes on the master branch.

### Website update

To have the new article to appear on the website, you'll need to prepend the newly created bibtex entry.

14\. Finally, copy the contents of `article.bib` from the doi folder for this paper into [rescience.github.io/_bibliography/published.bib](https://github.com/ReScience/rescience.github.io/blob/sources/_bibliography/published.bib) and send a final pull request (You can do this from the web). 

15\. Now you’re done! 🎉 🚀

### Updating an already published article

On rare occasions, authors propose corrections to their already published articles. This section explains how to handle such updates technically. If you have doubts on whether or not publishing a correction is the right thing to do, i.e. if the corrections go beyond fixing typos or correcting references, please open an issue on [the ReScience repository](https://github.com/ReScience/ReScience) for discussion.

Since updates are rare, the procedure is less automated than for publishing new articles.

1\. Log in on [Zenodo](https://zenodo.org) using your personal account.
2\. Click on "upload" (in the blue bar on top) to see your prior uploads. Find the original upload of the article and click on it. Note: the article will be listed there only if you have associated your ORCID with your Zenodo account.
3\. Click on the green "New version" button, right under the "Edit" button near the top of the page.
4\. Find the section "Basic information", which starts with the DOI. Note that the displayed DOI is *not* the one assigned initially, but a new DOI for the new version. Click on the "Reserve DOI" button below the DOI. Send the DOI to the authors, and ask them to provide a PDF of their updated article containing this DOI.
5\. Delete the original PDF file on Zenodo, and upload the new one. Note: if you don't delete the original file, the new version will contain both files.
6\. Click the "Publish" button.
7\. Clone this repository on your computer, and update the files article.pdf, article.yaml, and article.bib in the directory for the article you are working on. In article.bib, add a note field explaining the correction, with a reference to the original DOI. For an example, click [here](https://github.com/ReScience/articles/tree/master/10.5281_zenodo.3763416).
8\. Update https://github.com/ReScience/rescience.github.io/blob/sources/_bibliography/published.bib, replacing the original entry with a copy of the updated article.bib.
