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
    assert len(entries) == 1
    assert entries[0] == {
        'accelerated_justification': 'Closing Time',
        'additional_text': 'Additional Text',
        'attachments': 'Attachments',
        'awarded_date': 'Awarded Value',
        'awarded_value': 'Supplier [Name|Address|Ref type|Ref Number|Is SME|Is VCSE]',
        'closing_date': 'Closing Date',
        'closing_time': 'Is sub-contract',
        'contact_address_1': 'Contact Address 1',
        'contact_address_2': 'Contact Address 2',
        'contact_country': 'Contact Country',
        'contact_email': 'Contact Email',
        'contact_name': 'Contact Name',
        'contact_postcode': 'Contact Postcode',
        'contact_telephone': 'Contact Telephone',
        'contact_town': 'Contact Town',
        'contact_website': 'Contact Website',
        'contract_end_date': 'OJEU Procedure Type',
        'contract_start_date': 'Contract end date',
        'cpv_codes': 'Cpv Codes',
        'description': 'Description',
        'end_date': 'End Date',
        'is_sub_contract': 'Parent Reference',
        'links': 'Links',
        'nationwide': 'Nationwide',
        'notice_identifier': 'Notice Identifier',
        'notice_type': 'Notice Type',
        'ojeu_contract_type': 'Value Low',
        'ojeu_procedure_type': 'Accelerated Justification',
        'organisation_name': 'Organisation Name',
        'parent_reference': 'Suitable for SME',
        'postcode': 'Postcode',
        'published_date': 'Published Date',
        'region': 'Region',
        'start_date': 'Start Date',
        'status': 'Status',
        'suitable_for_sme': 'Suitable for VCO',
        'suitable_for_vco': 'Supply Chain',
        'supplier_contact_name': 'Contract start date',
        'supplier_info': "Supplier's contact name",
        'supply_chain': 'OJEU Contract Type',
        'title': 'Title',
        'value_high': 'Awarded Date',
        'value_low': 'Value High',
    }


def test_handler_handles_s3_client_error(mocker):
    """Ensures any S3 client errors get handled"""
    mocker.patch("service.get_entries", return_value="{}")
    mocker.patch("service.S3_CLIENT.put_object", side_effect=ClientError({}, "failure"))
    assert handler(None, None) is False
