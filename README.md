### ReScience C published articles

In order to publish a new article (after acceptance), you'll need to have the
article metadata file (YAML format) and the corresponding article (PDF
format). The metadata file should be missing the article DOI, number and
URL. The first step is thus to request this information from Zenodo. Before
proceeding further, you'll need a Zenodo token that can be requested from the
[sandbox
server](https://sandbox.zenodo.org/account/settings/applications/tokens/new/)
and from the [actual
server](https://zenodo.org/account/settings/applications/tokens/new/).

The sandbox token is expected to be stored in the environment variable
`ZENODO_SANDBOX_TOKEN` while the true token must be stored in `ZENODO_TOKEN`.
We strongly advise you to **first test the procedure** on the sandbox server
using the `--sandbox` switch.


#### 1. Pre-Publication (article DOI, URL and number)

Run the [process.py](process.py) script using the provided metadata
file. It requires Python 3 plus the [PyYAML](https://pyyaml.org/) and [Requests](https://requests.kennethreitz.org/) libraries.

First run on the sandbox server to check everything is OK:

```bash
$ ./process.py --sandbox --metadata metadata.yaml --pdf article.pdf
Article ID: xxxxx
Article DOI: 10.xxxx/zenodo.xxxxx
Article URL: https://zenodo.org/record/xxxxxx/file/article.pdf
```

Then use the actual server using the `--zenodo` switch instead of the
`--sandbox` switch.

```bash
$ ./process.py --zenodo --metadata metadata.yaml --pdf article.pdf
Article ID: xxxxx
Article DOI: 10.xxxx/zenodo.xxxxx
Article URL: https://zenodo.org/record/xxxxxx/file/article.pdf
```

You must also assign the issue, volume, and article numbers. Have a
look on the published articles and assign the next available number in
the same issue and same volume if your article is still in the same
year.  Otherwise, increment the volume number and start with
issue 1. The issue number is only changed for accommodating special issues.
Post your numbers to [this GitHub issue](https://github.com/ReScience/ReScience/issues/48)
that serves to avoid that two editors assign the same numbers to two
different articles.


#### 2. Metadata update and creation of the final PDF

The `metadata.yaml` has a section (at the end) for information added during
the publication process. You should complete it and verify the whole file
before moving on. The information you must add is:
  - DOI (from Zenodo)
  - article URL (from Zenodo)
  - contributors (reviewers and editors), with ORCIDs
  - acceptance and publication date
  - issue, volume, and article numbers.

Next, there are two situations:

 - If the authors have used the [ReScience article template](http://github.com/rescience/template),
   you can fork their repository, copy the edited `metadata.yaml` to it, and create
   the final PDF by running `make`. Don't forget to submit a pull request to the
   authors' repository with the changes you made to `metadata.yaml`.

 - Otherwise, you give the authors the required information and
   ask them to update their article and produce the final PDF file. You should
   check that their PDF contains all the information you sent them.
   
You need to give this information back to author(s) such that they can update
the metadata file as well as the article that display the DOI in the left
margin (make sure they actually update this information). For the article
number, you can have a look on the published articles and assign the next
available number in the same issue and same volume.


#### 3. Publication (Zenodo and GitHub)

In order to publish the **final** article, you'll need to run the
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
publishing to the Zenodo production site! This will create a new
public record on Zenodo and also create a new local directory
corresponding to the entry. This means you need to push this new
branch on GitHub and make a pull request (the commit will have been
created automatically).


#### Website update

To have the new article to appear on the website, you'll need to prepend the
newly created bibtex entry (look into the local repository) to the
[published.bib](https://github.com/ReScience/rescience.github.io/blob/sources/_bibliography/published.bib)
file on the website (you can do it directly from the GitHub interface). If you
previously added the entry to the
[under_review.bib](https://github.com/ReScience/rescience.github.io/blob/sources/_bibliography/under-review.bib)
file, don't forget to remove it.


