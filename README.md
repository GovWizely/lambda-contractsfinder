[![CircleCI](https://circleci.com/gh/GovWizely/lambda-contractsfinder/tree/master.svg?style=svg)](https://circleci.com/gh/GovWizely/lambda-contractsfinder/tree/master)
[![Maintainability](https://api.codeclimate.com/v1/badges/e050d41793856644c86a/maintainability)](https://codeclimate.com/github/GovWizely/lambda-contractsfinder/maintainability)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=GovWizely/lambda-contractsfinder)](https://dependabot.com)

# UK Trade Leads Lambda

This is a scraper of [UK Trade Leads](https://www.contractsfinder.service.gov.uk/Search/Results) data that builds 
a single JSON document and stores it in S3. The data isn't provided via an API endpoint, so this script pretends to
be a web browser and maintains the cookie needed to get the subsets of data and then reassemble them. The CSV download
functionality only returns ~1000 trade events at a time, and there are generally more than 1000. The approach taken
here is to get as much as possible per batch while moving the time window accordingly. This generates duplicates on the
border dates, so the accrued list of dicts gets de-duped before going to S3.  

## Prerequisites

- This project is tested against Python 3.7+ in [CircleCI](https://app.circleci.com/github/GovWizely/lambda-contractsfinder/pipelines).
- Docker

## Getting Started

	git clone git@github.com:GovWizely/lambda-contractsfinder.git
	cd lambda-contractsfinder
	mkvirtualenv -p /usr/local/bin/python3.8 -r requirements-test.txt contractsfinder

If you are using PyCharm, make sure you enable code compatibility inspections for Python 3.7/3.8.

### Tests

```bash
python -m pytest
```

## Configuration

* Define AWS credentials in either `config.yaml` or in the [default] section of `~/.aws/credentials`. To use another profile, you can do something like `export AWS_DEFAULT_PROFILE=govwizely`.
* Edit `config.yaml` if you want to specify a different AWS region, role, and so on.
* Make sure you do not commit the AWS credentials to version control.

## Invocation

	lambda invoke -v
 
## Deploy

This project uses `MechanicalSoup` to parse XML, which uses `lxml` under the hood. That library must be built with C extensions for `libxml2` and `libxslt` in a way that is compatible with the Amazon Lambda execution environment.

To build the necessary libraries for Amazon's Python 3.8 runtime:

    docker build -t contractsfinder .
    docker run -v $(pwd):/outputs -it contractsfinder pip install --upgrade -r requirements.txt -t /outputs/

To deploy:

	lambda deploy --requirements requirements-dev.txt

Clean up the locally created files and directories:

    git clean -fd
