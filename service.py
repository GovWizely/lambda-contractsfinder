# -*- coding: utf-8 -*-
import csv
import datetime
import json

import boto3
import mechanize

JSON = 'application/json'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, ' \
             'like Gecko) Version/11.1 Safari/605.1.15'
URL_PREFIX = 'https://www.contractsfinder.service.gov.uk/Search/'
HTML_FORM = URL_PREFIX + 'Results'
CSV_DOWNLOAD = URL_PREFIX + 'GetCsvFile'
PUBLISHED_FROM = '2008-01-01'
KEY = 'uk.json'
NORMALIZED_FIELDNAMES = (
    "notice_identifier", "notice_type", "organisation_name", "status", "published_date", "title",
    "description", "nationwide", "postcode", "region", "cpv_codes", "contact_name", "contact_email",
    "contact_address_1", "contact_address_2", "contact_town", "contact_postcode", "contact_country",
    "contact_telephone", "contact_website", "attachments", "links", "additional_text", "start_date",
    "end_date", "closing_date", "is_sub_contract", "parent_reference", "suitable_for_sme",
    "suitable_for_vco", "supply_chain", "ojeu_contract_type", "value_low", "value_high",
    "awarded_date", "awarded_value", "supplier_info", "supplier_contact_name",
    "contract_start_date", "contract_end_date", "ojeu_procedure_type", "accelerated_justification")

s3 = boto3.resource('s3')


def handler(event, context):
    items = get_items()
    if len(items) > 0:
        s3.Object('trade-leads', KEY).put(Body=json.dumps(items), ContentType=JSON)
        return "Uploaded {} file with {} items".format(KEY, len(items))
    else:
        return "No entries loaded so there is no JSON file to upload"


def sane(row):
    return row['start_date'] and row['end_date'] and row['closing_date'] and row[
        'published_date'] and row['title'] and row['description']


def get_items():
    items = []
    running = True
    published_to = datetime.datetime.now().strftime('%Y-%m-%d')
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.set_header('User-Agent', USER_AGENT)
    len_with_dupes = 0
    while running:
        print "Loading HTML form from {}...".format(HTML_FORM)
        br.open(HTML_FORM)
        br.select_form(name="search")
        br['published_from'] = PUBLISHED_FROM
        br['published_to'] = published_to
        print "Submitting form for date range {} to {}".format(PUBLISHED_FROM, published_to)
        br.submit()
        print "Fetching CSV file of up to ~1000 items"
        doc = br.retrieve(CSV_DOWNLOAD)
        with open(doc[0], 'rb') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=NORMALIZED_FIELDNAMES)
            rows = [row for row in reader if sane(row)]
            print "Received {} items from {} to {}".format(len(rows), PUBLISHED_FROM, published_to)
            items.extend(rows)
            published_to = rows[-1]['published_date'][0:10]
            if len(rows) < 1000: running = False
        len_with_dupes = len(items)
        items = {v['notice_identifier']: v for v in items}.values()
    print('Length with dupes: {}; De-duped: {}'.format(len_with_dupes, len(items)))
    return items
