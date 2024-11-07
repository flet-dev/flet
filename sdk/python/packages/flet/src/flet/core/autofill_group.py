from enum import Enum
from typing import Any, Optional

from flet.core.control import Control
from flet.core.ref import Ref


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


class AutofillGroup(Control):
    """
    This control is used to group autofill controls together.

    -----

    Online docs: https://flet.dev/docs/controls/autofillgroup
    """

    def __init__(
        self,
        content: Control = None,
        dispose_action: Optional[AutofillGroupDisposeAction] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            data=data,
        )

        self.content = content
        self.dispose_action = dispose_action

    def _get_control_name(self):
        return "autofillgroup"

    def _get_children(self):
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

    def before_update(self):
        super().before_update()
        assert self.__content.visible, "content must be visible"

    # content
    @property
    def content(self) -> Control:
        return self.__content

    @content.setter
    def content(self, value: Control):
        self.__content = value

    # dispose_action
    @property
    def dispose_action(self) -> Optional[AutofillGroupDisposeAction]:
        return self.__dispose_action

    @dispose_action.setter
    def dispose_action(self, value: Optional[AutofillGroupDisposeAction]):
        self.__dispose_action = value
        self._set_enum_attr("disposeAction", value, AutofillGroupDisposeAction)
