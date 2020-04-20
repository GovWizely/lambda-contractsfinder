import vcr
from botocore.exceptions import ClientError
from freezegun import freeze_time

from service import get_entries, handler


@freeze_time("2020-04-16")
@vcr.use_cassette()
def test_get_entries():
    """Reads from the `test_get_entries` cassette and processes the entries.
    """
    entries = get_entries()
    assert len(entries) == 977
    assert entries[0] == {
        "notice_identifier": "Notice Identifier",
        "notice_type": "Notice Type",
        "organisation_name": "Organisation Name",
        "status": "Status",
        "published_date": "Published Date",
        "title": "Title",
        "description": "Description",
        "nationwide": "Nationwide",
        "postcode": "Postcode",
        "region": "Region",
        "cpv_codes": "Cpv Codes",
        "contact_name": "Contact Name",
        "contact_email": "Contact Email",
        "contact_address_1": "Contact Address 1",
        "contact_address_2": "Contact Address 2",
        "contact_town": "Contact Town",
        "contact_postcode": "Contact Postcode",
        "contact_country": "Contact Country",
        "contact_telephone": "Contact Telephone",
        "contact_website": "Contact Website",
        "attachments": "Attachments",
        "links": "Links",
        "additional_text": "Additional Text",
        "start_date": "Start Date",
        "end_date": "End Date",
        "closing_date": "Closing Date",
        "is_sub_contract": "Is sub-contract",
        "parent_reference": "Parent Reference",
        "suitable_for_sme": "Suitable for SME",
        "suitable_for_vco": "Suitable for VCO",
        "supply_chain": "Supply Chain",
        "ojeu_contract_type": "OJEU Contract Type",
        "value_low": "Value Low",
        "value_high": "Value High",
        "awarded_date": "Awarded Date",
        "awarded_value": "Awarded Value",
        "supplier_info": "Supplier [Name|Address|Ref type|Ref Number|Is SME|Is VCSE]",
        "supplier_contact_name": "Supplier's contact name",
        "contract_start_date": "Contract start date",
        "contract_end_date": "Contract end date",
        "ojeu_procedure_type": "OJEU Procedure Type",
        "accelerated_justification": "Accelerated Justification",
    }


def test_handler_handles_s3_client_error(mocker):
    """Ensures any S3 client errors get handled"""
    mocker.patch("service.get_entries", return_value="{}")
    mocker.patch("service.S3_CLIENT.put_object", side_effect=ClientError({}, "failure"))
    assert handler(None, None) is False
