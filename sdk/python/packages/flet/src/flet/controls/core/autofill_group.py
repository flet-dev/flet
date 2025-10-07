from enum import Enum

from flet.controls.base_control import control
from flet.controls.control import Control

__all__ = ["AutofillGroup", "AutofillGroupDisposeAction", "AutofillHint"]


class AutofillHint(Enum):
    ADDRESS_CITY = "addressCity"
    ADDRESS_CITY_AND_STATE = "addressCityAndState"
    ADDRESS_STATE = "addressState"
    BIRTHDAY = "birthday"
    BIRTHDAY_DAY = "birthdayDay"
    BIRTHDAY_MONTH = "birthdayMonth"
    BIRTHDAY_YEAR = "birthdayYear"
    COUNTRY_CODE = "countryCode"
    COUNTRY_NAME = "countryName"
    CREDIT_CARD_EXPIRATION_DATE = "creditCardExpirationDate"
    CREDIT_CARD_EXPIRATION_DAY = "creditCardExpirationDay"
    CREDIT_CARD_EXPIRATION_MONTH = "creditCardExpirationMonth"
    CREDIT_CARD_EXPIRATION_YEAR = "creditCardExpirationYear"
    CREDIT_CARD_FAMILY_NAME = "creditCardFamilyName"
    CREDIT_CARD_GIVEN_NAME = "creditCardGivenName"
    CREDIT_CARD_MIDDLE_NAME = "creditCardMiddleName"
    CREDIT_CARD_NAME = "creditCardName"
    CREDIT_CARD_NUMBER = "creditCardNumber"
    CREDIT_CARD_SECURITY_CODE = "creditCardSecurityCode"
    CREDIT_CARD_TYPE = "creditCardType"
    EMAIL = "email"
    FAMILY_NAME = "familyName"
    FULL_STREET_ADDRESS = "fullStreetAddress"
    GENDER = "gender"
    GIVEN_NAME = "givenName"
    IMPP = "impp"
    JOB_TITLE = "jobTitle"
    LANGUAGE = "language"
    LOCATION = "location"
    MIDDLE_INITIAL = "middleInitial"
    MIDDLE_NAME = "middleName"
    NAME = "name"
    NAME_PREFIX = "namePrefix"
    NAME_SUFFIX = "nameSuffix"
    NEW_PASSWORD = "newPassword"
    NEW_USERNAME = "newUsername"
    NICKNAME = "nickname"
    ONE_TIME_CODE = "oneTimeCode"
    ORGANIZATION_NAME = "organizationName"
    PASSWORD = "password"
    PHOTO = "photo"
    POSTAL_ADDRESS = "postalAddress"
    POSTAL_ADDRESS_EXTENDED = "postalAddressExtended"
    POSTAL_ADDRESS_EXTENDED_POSTAL_CODE = "postalAddressExtendedPostalCode"
    POSTAL_CODE = "postalCode"
    STREET_ADDRESS_LEVEL1 = "streetAddressLevel1"
    STREET_ADDRESS_LEVEL2 = "streetAddressLevel2"
    STREET_ADDRESS_LEVEL3 = "streetAddressLevel3"
    STREET_ADDRESS_LEVEL4 = "streetAddressLevel4"
    STREET_ADDRESS_LINE1 = "streetAddressLine1"
    STREET_ADDRESS_LINE2 = "streetAddressLine2"
    STREET_ADDRESS_LINE3 = "streetAddressLine3"
    SUB_LOCALITY = "subLocality"
    TELEPHONE_NUMBER = "telephoneNumber"
    TELEPHONE_NUMBER_AREA_CODE = "telephoneNumberAreaCode"
    TELEPHONE_NUMBER_COUNTRY_CODE = "telephoneNumberCountryCode"
    TELEPHONE_NUMBER_DEVICE = "telephoneNumberDevice"
    TELEPHONE_NUMBER_EXTENSION = "telephoneNumberExtension"
    TELEPHONE_NUMBER_LOCAL = "telephoneNumberLocal"
    TELEPHONE_NUMBER_LOCAL_PREFIX = "telephoneNumberLocalPrefix"
    TELEPHONE_NUMBER_LOCAL_SUFFIX = "telephoneNumberLocalSuffix"
    TELEPHONE_NUMBER_NATIONAL = "telephoneNumberNational"
    TRANSACTION_AMOUNT = "transactionAmount"
    TRANSACTION_CURRENCY = "transactionCurrency"
    URL = "url"
    USERNAME = "username"


class AutofillGroupDisposeAction(Enum):
    COMMIT = "commit"
    CANCEL = "cancel"


@control("AutofillGroup")
class AutofillGroup(Control):
    """
    Used to group autofill controls together.
    """

    content: Control
    """
    The content of this group.

    Must be visible.

    Raises:
        ValueError: If [`content`][(c).] is not visible.
    """

    dispose_action: AutofillGroupDisposeAction = AutofillGroupDisposeAction.COMMIT
    """
    The action to be run when this group is the topmost
    and it's being disposed, in order to clean up the current autofill context.
    """

    def before_update(self):
        super().before_update()
        if not self.content.visible:
            raise ValueError("content must be visible")
