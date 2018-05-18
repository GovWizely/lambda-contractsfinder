# UK Trade Leads Lambda

This is a scraper of [UK Trade Leads](https://www.contractsfinder.service.gov.uk/Search/Results) data that builds 
a single JSON document and stores it in S3. The data isn't provided via an API endpoint, so this script pretends to
be a web browser and maintains the cookie needed to get the subsets of data and then reassemble them. The CSV download
functionality only returns ~1000 trade events at a time, and there are generally more than 1000. The approach taken
here is to get as much as possible per batch while moving the time window accordingly. This generates duplicates on the
border dates, so the accrued list of dicts gets de-duped before going to S3.  

## Prerequisites

Follow instructions from [python-lambda](https://github.com/nficano/python-lambda) to ensure your basic development 
environment is ready, including:

* Python 2.7
* Pip
* Virtualenv
* Virtualenvwrapper
* AWS credentials

## Getting Started

	git clone git@github.com:GovWizely/lambda-contractsfinder.git
	cd lambda-contractsfinder
	mkvirtualenv -r requirements.txt lambda-contractsfinder

## Configuration

* Define AWS credentials in either `config.yaml` or in the [default] section of ~/.aws/credentials.
* Edit `config.yaml` if you want to specify a different AWS region, role, and so on.
* Make sure you do not commit the AWS credentials to version control

## Invocation

	lambda invoke -v
 
## Deploy

	lambda deploy
