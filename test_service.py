from botocore.exceptions import ClientError

from service import get_entries, handler


def test_get_entries():
    """Reads from the `test_get_entries` cassette and processes the entries.
    """
    assert get_entries()


def test_handler_handles_s3_client_error(mocker):
    """Ensures any S3 client errors get handled"""
    mocker.patch("service.S3_CLIENT.put_object", side_effect=ClientError({}, "failure"))
    assert handler(None, None) is False
