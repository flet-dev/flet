import 'package:flutter/material.dart';

import '../models/control.dart';

List<String>? parseAutofillHints(dynamic value, [List<String>? defaultValue]) {
  if (value == null) return defaultValue;
  List<String> hints = [];
  if (value is List) {
    hints = value
        .map((e) => parseAutofillHint(e.toString()))
        .whereType<String>()
        .toList();
  } else if (value is String) {
    hints = [parseAutofillHint(value)].whereType<String>().toList();
  }

  return hints;
}

String? parseAutofillHint(String? value, [String? defaultValue]) {
  if (value == null) return defaultValue;

  const hints = <String, String>{
    'addresscity': AutofillHints.addressCity,
    'addresscityandstate': AutofillHints.addressCityAndState,
    'addressstate': AutofillHints.addressState,
    'birthday': AutofillHints.birthday,
    'birthdayday': AutofillHints.birthdayDay,
    'birthdaymonth': AutofillHints.birthdayMonth,
    'birthdayyear': AutofillHints.birthdayYear,
    'countrycode': AutofillHints.countryCode,
    'countryname': AutofillHints.countryName,
    'creditcardexpirationdate': AutofillHints.creditCardExpirationDate,
    'creditcardexpirationday': AutofillHints.creditCardExpirationDay,
    'creditcardexpirationmonth': AutofillHints.creditCardExpirationMonth,
    'creditcardexpirationyear': AutofillHints.creditCardExpirationYear,
    'creditcardfamilyname': AutofillHints.creditCardFamilyName,
    'creditcardgivenname': AutofillHints.creditCardGivenName,
    'creditcardmiddlename': AutofillHints.creditCardMiddleName,
    'creditcardname': AutofillHints.creditCardName,
    'creditcardnumber': AutofillHints.creditCardNumber,
    'creditcardsecuritycode': AutofillHints.creditCardSecurityCode,
    'creditcardtype': AutofillHints.creditCardType,
    'email': AutofillHints.email,
    'familyname': AutofillHints.familyName,
    'fullstreetaddress': AutofillHints.fullStreetAddress,
    'gender': AutofillHints.gender,
    'givenname': AutofillHints.givenName,
    'impp': AutofillHints.impp,
    'jobtitle': AutofillHints.jobTitle,
    'language': AutofillHints.language,
    'location': AutofillHints.location,
    'middleinitial': AutofillHints.middleInitial,
    'middlename': AutofillHints.middleName,
    'name': AutofillHints.name,
    'nameprefix': AutofillHints.namePrefix,
    'namesuffix': AutofillHints.nameSuffix,
    'newpassword': AutofillHints.newPassword,
    'newusername': AutofillHints.newUsername,
    'nickname': AutofillHints.nickname,
    'onetimecode': AutofillHints.oneTimeCode,
    'organizationname': AutofillHints.organizationName,
    'password': AutofillHints.password,
    'photo': AutofillHints.photo,
    'postaladdress': AutofillHints.postalAddress,
    'postaladdressextended': AutofillHints.postalAddressExtended,
    'postaladdressextendedpostalcode':
        AutofillHints.postalAddressExtendedPostalCode,
    'postalcode': AutofillHints.postalCode,
    'streetaddresslevel1': AutofillHints.streetAddressLevel1,
    'streetaddresslevel2': AutofillHints.streetAddressLevel2,
    'streetaddresslevel3': AutofillHints.streetAddressLevel3,
    'streetaddresslevel4': AutofillHints.streetAddressLevel4,
    'streetaddressline1': AutofillHints.streetAddressLine1,
    'streetaddressline2': AutofillHints.streetAddressLine2,
    'streetaddressline3': AutofillHints.streetAddressLine3,
    'sublocality': AutofillHints.sublocality,
    'telephonenumber': AutofillHints.telephoneNumber,
    'telephonenumberareacode': AutofillHints.telephoneNumberAreaCode,
    'telephonenumbercountrycode': AutofillHints.telephoneNumberCountryCode,
    'telephonenumberdevice': AutofillHints.telephoneNumberDevice,
    'telephonenumberextension': AutofillHints.telephoneNumberExtension,
    'telephonenumberlocal': AutofillHints.telephoneNumberLocal,
    'telephonenumberlocalprefix': AutofillHints.telephoneNumberLocalPrefix,
    'telephonenumberlocalsuffix': AutofillHints.telephoneNumberLocalSuffix,
    'telephonenumbernational': AutofillHints.telephoneNumberNational,
    'transactionamount': AutofillHints.transactionAmount,
    'transactioncurrency': AutofillHints.transactionCurrency,
    'url': AutofillHints.url,
    'username': AutofillHints.username,
  };

  return hints[value.toLowerCase()] ?? defaultValue;
}

AutofillContextAction? parseAutofillContextAction(String? value,
    [AutofillContextAction? defaultValue]) {
  switch (value?.toLowerCase()) {
    case 'commit':
      return AutofillContextAction.commit;
    case 'cancel':
      return AutofillContextAction.cancel;
    default:
      return defaultValue;
  }
}

extension AutofillParsers on Control {
  List<String>? getAutofillHints(String propertyName,
      [List<String>? defaultValue]) {
    return parseAutofillHints(get(propertyName), defaultValue);
  }

  String? getAutofillHint(String propertyName, [String? defaultValue]) {
    return parseAutofillHint(get(propertyName), defaultValue);
  }

  AutofillContextAction? getAutofillContextAction(String propertyName,
      [AutofillContextAction? defaultValue]) {
    return parseAutofillContextAction(get(propertyName), defaultValue);
  }
}
