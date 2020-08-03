## Publishing a ReScience C article

Congrats on accepting a ReScience article for publication! Follow the steps below to complete the metadata, submit to Zenodo, and get the final article published.

### What you will need to begin
- The article metadata file (`metadata.yaml`) from the author's repository.   At this time the metadata file should **will be missing** the article DOI, number and URL.  This is expected and something you will fix over the coming steps.
- The final article itself (`article.pdf`)

Have these two files ready before cloning this repository. 

### Publishing the article

There are 5 parts to publishing the article. 

| Step | What it does |
|:--|:--|
| Set up credentials  | Get setup to programmatically submit to Zenodo |
| Pre-publish the paper | Reserves the DOI  |
| Update the metadata | Add volume, issue, page, doi to the paper & generate new pdf |
| Publish the paper | Make the final Zenodo deposit |
| Update the website | Enter bib information for the website  |



### 14 steps to publish a ReScience article

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
If you copy these in your bash profile you wont have to look for them again. We advise you to **first test the procedure** on the sandbox server using the `--sandbox` switch. More on this in the next step.


### Pre-publish the paper

This step reserves the DOI for the paper, allowing you to update metadata before final publication. 

Run the [process.py](process.py) script using the provided metadata
file. It requires Python 3 plus the libraries [PyYAML](https://pyyaml.org/), [Requests](https://requests.kennethreitz.org/), and [dateutil](https://dateutil.readthedocs.io/en/stable/).

First run on the sandbox server to check everything is OK:

```bash
$ ./process.py --sandbox --metadata metadata.yaml --pdf article.pdf
Article ID: xxxxx
Article DOI: 10.xxxx/zenodo.xxxxx
Article URL: https://sandbox.zenodo.org/record/xxxxxx/file/article.pdf
```

Did this work? Were there any problems? If there were no problems, then use the production server using the `--zenodo` switch instead of the `--sandbox` switch.

```bash
$ ./process.py --zenodo --metadata metadata.yaml --pdf article.pdf
Article ID: xxxxx
Article DOI: 10.xxxx/zenodo.xxxxx
Article URL: https://zenodo.org/record/xxxxxx/file/article.pdf
```

6\. If no errors were returned, you have successfully reserved a DOI! Next we’ll grab an issue, volume and article numbers.

```
NOTE: This DOI will not resolve anywhere. This behavior is expected
```

### Update the metadata

In this step, you'll update `metadata.yaml`, pull request the file back to the author, generate a new PDF (which will now contain the volume, issue, page, doi information), and copy that back here.

7\. Look at the last number on  [this GitHub issue](https://github.com/ReScience/ReScience/issues/48) and choose the next one in the series. Post a comment to claim that issue for your article. This comment
serves to avoid that two editors assign the same numbers to two
different articles.

8\. Then add these two bits of information (volume and article number) along with the Zenodo DOI and URL to `metadata.yaml`. 

You should complete the missing information and verify the whole file before moving on. The information you must add is:
  - DOI (from Zenodo)
  - article URL (from Zenodo)
  - contributors (reviewers and editors), with ORCIDs
  - acceptance and publication date
  - issue, volume, and article numbers.

9\.  Pull request just the `metadata.yaml` back to the author's repo (this will mean copying this file back to the author repo fork). Once the pull-request is merged, have them `Make` a new `article.pdf`. The PDF will now contain the volume, article number and DOI.

10\. Copy the newly updated `article.pdf` and `metadata.yaml` back to this repo.

  
### Publish the paper

11\. In order to publish the **final** article, you'll need to run the
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


12\. Discard any changes on the master branch.

### Website update

To have the new article to appear on the website, you'll need to prepend the newly created bibtex entry.

13\. Finally, copy the contents of `article.bib` from the doi folder for this paper into [rescience.github.io/_bibliography/published.bib](https://github.com/ReScience/rescience.github.io/blob/sources/_bibliography/published.bib) and send a final pull request (You can do this from the web). 

14\. Now you’re done! 🎉 🚀
