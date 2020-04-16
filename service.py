# -*- coding: utf-8 -*-
import csv
import datetime
import io
import json
import logging

import boto3
import mechanicalsoup
from botocore.exceptions import ClientError

BUCKET = "trade-leads"
KEY = "uk.json"
JSON = "application/json"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, "
    "like Gecko) Version/11.1 Safari/605.1.15 "
)
URL_PREFIX = "https://www.contractsfinder.service.gov.uk/Search/"
HTML_FORM = URL_PREFIX + "Results"
CSV_DOWNLOAD = URL_PREFIX + "GetCsvFile"
PUBLISHED_FROM = "2008-01-01"
NORMALIZED_FIELDNAMES = (
    "notice_identifier",
    "notice_type",
    "organisation_name",
    "status",
    "published_date",
    "title",
    "description",
    "nationwide",
    "postcode",
    "region",
    "cpv_codes",
    "contact_name",
    "contact_email",
    "contact_address_1",
    "contact_address_2",
    "contact_town",
    "contact_postcode",
    "contact_country",
    "contact_telephone",
    "contact_website",
    "attachments",
    "links",
    "additional_text",
    "start_date",
    "end_date",
    "closing_date",
    "is_sub_contract",
    "parent_reference",
    "suitable_for_sme",
    "suitable_for_vco",
    "supply_chain",
    "ojeu_contract_type",
    "value_low",
    "value_high",
    "awarded_date",
    "awarded_value",
    "supplier_info",
    "supplier_contact_name",
    "contract_start_date",
    "contract_end_date",
    "ojeu_procedure_type",
    "accelerated_justification",
)

S3_CLIENT = boto3.client("s3")


def handler(event, context):
    entries = get_entries()
    response = True
    try:
        S3_CLIENT.put_object(
            Bucket=BUCKET, Key=KEY, Body=json.dumps(entries), ContentType=JSON
        )
        print(f"✅ Uploaded {KEY} file with {len(entries)} locations")
    except ClientError as e:
        logging.error(e)
        response = False
    return response


def sane(row):
    return (
        row["start_date"]
        and row["end_date"]
        and row["closing_date"]
        and row["published_date"]
        and row["title"]
        and row["description"]
    )


def get_entries():
    items = []
    running = True
    published_to = datetime.datetime.now().strftime("%Y-%m-%d")
    br = mechanicalsoup.StatefulBrowser(user_agent=USER_AGENT)
    len_with_dupes = 0
    while running:
        print(f"Loading HTML form from {HTML_FORM}...")
        br.open(HTML_FORM)
        br.select_form()
        br["published_from"] = PUBLISHED_FROM
        br["published_to"] = published_to
        print(f"Submitting form for date range {PUBLISHED_FROM} to {published_to}")
        br.submit_selected()
        print("Fetching CSV file of up to ~1000 items")
        doc = br.download_link(link=CSV_DOWNLOAD)
        str_io = io.StringIO(doc.text)
        reader = csv.DictReader(str_io, fieldnames=NORMALIZED_FIELDNAMES)
        rows = [row for row in reader if sane(row)]
        print(f"Received {len(rows)} items from {PUBLISHED_FROM} to {published_to}")
        items.extend(rows)
        published_to = rows[-1]["published_date"][0:10]
        if len(rows) < 1000:
            running = False
        len_with_dupes = len(items)
        items = list({v["notice_identifier"]: v for v in items}.values())
    print(f"Length with dupes: {len_with_dupes}; De-duped: {len(items)}")
    return items
