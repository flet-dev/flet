import pytest

from flet_local_auth.local_auth import LocalAuthentication
from flet_local_auth.types import LocalAuthErrorCode, LocalAuthException


def test_raise_for_error_success_is_noop():
    LocalAuthentication._raise_for_error(True)
    LocalAuthentication._raise_for_error(None)
    LocalAuthentication._raise_for_error({})


def test_raise_for_error_translates_known_code():
    with pytest.raises(LocalAuthException) as exc_info:
        LocalAuthentication._raise_for_error(
            {
                "error_code": "userCanceled",
                "error_description": "canceled",
            }
        )

    assert exc_info.value.code == LocalAuthErrorCode.USER_CANCELED
    assert exc_info.value.description == "canceled"


def test_raise_for_error_unknown_code_falls_back():
    with pytest.raises(LocalAuthException) as exc_info:
        LocalAuthentication._raise_for_error({"error_code": "futureUpstreamCode"})

    assert exc_info.value.code == LocalAuthErrorCode.UNKNOWN_ERROR
