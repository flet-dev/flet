import 'dart:convert';

import 'package:flutter/material.dart';

import '../models/control.dart';

List<String>? parseAutofillHints(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return autofillHintsFromJson(j1);
}

List<String> autofillHintsFromJson(dynamic json) {
  List<String> hints = [];
  if (json is List) {
    hints = json
        .map((e) => autofillHintFromString(e.toString()))
        .whereType<String>()
        .toList();
  } else if (json is String) {
    hints = [autofillHintFromString(json)].whereType<String>().toList();
  }

  return hints;
}

String? autofillHintFromString(String? hint, [String? defaultAutoFillHint]) {
  switch (hint?.toLowerCase()) {
    case 'addresscity':
      return AutofillHints.addressCity;
    case 'addresscityandstate':
      return AutofillHints.addressCityAndState;
    case 'addressstate':
      return AutofillHints.addressState;
    case 'birthday':
      return AutofillHints.birthday;
    case 'birthdayday':
      return AutofillHints.birthdayDay;
    case 'birthdayMonth':
      return AutofillHints.birthdayMonth;
    case 'birthdayyear':
      return AutofillHints.birthdayYear;
    case 'countrycode':
      return AutofillHints.countryCode;
    case 'countryname':
      return AutofillHints.countryName;
    case 'creditcardexpirationdate':
      return AutofillHints.creditCardExpirationDate;
    case 'creditcardexpirationday':
      return AutofillHints.creditCardExpirationDay;
    case 'creditcardexpirationmonth':
      return AutofillHints.creditCardExpirationMonth;
    case 'creditcardexpirationyear':
      return AutofillHints.creditCardExpirationYear;
    case 'creditcardfamilyname':
      return AutofillHints.creditCardFamilyName;
    case 'creditcardgivenname':
      return AutofillHints.creditCardGivenName;
    case 'creditcardmiddlename':
      return AutofillHints.creditCardMiddleName;
    case 'creditcardname':
      return AutofillHints.creditCardName;
    case 'creditcardnumber':
      return AutofillHints.creditCardNumber;
    case 'creditcardsecuritycode':
      return AutofillHints.creditCardSecurityCode;
    case 'creditcardtype':
      return AutofillHints.creditCardType;
    case 'email':
      return AutofillHints.email;
    case 'familyname':
      return AutofillHints.familyName;
    case 'fullstreetaddress':
      return AutofillHints.fullStreetAddress;
    case 'gender':
      return AutofillHints.gender;
    case 'givenname':
      return AutofillHints.givenName;
    case 'impp':
      return AutofillHints.impp;
    case 'jobtitle':
      return AutofillHints.jobTitle;
    case 'language':
      return AutofillHints.language;
    case 'location':
      return AutofillHints.location;
    case 'middleinitial':
      return AutofillHints.middleInitial;
    case 'middlename':
      return AutofillHints.middleName;
    case 'name':
      return AutofillHints.name;
    case 'nameprefix':
      return AutofillHints.namePrefix;
    case 'namesuffix':
      return AutofillHints.nameSuffix;
    case 'newpassword':
      return AutofillHints.newPassword;
    case 'newusername':
      return AutofillHints.newUsername;
    case 'nickname':
      return AutofillHints.nickname;
    case 'onetimecode':
      return AutofillHints.oneTimeCode;
    case 'organizationname':
      return AutofillHints.organizationName;
    case 'password':
      return AutofillHints.password;
    case 'photo':
      return AutofillHints.photo;
    case 'postaladdress':
      return AutofillHints.postalAddress;
    case 'postaladdressextended':
      return AutofillHints.postalAddressExtended;
    case 'postaladdressextendedpostalcode':
      return AutofillHints.postalAddressExtendedPostalCode;
    case 'postalcode':
      return AutofillHints.postalCode;
    case 'streetaddresslevel1':
      return AutofillHints.streetAddressLevel1;
    case 'streetaddresslevel2':
      return AutofillHints.streetAddressLevel2;
    case 'streetaddresslevel3':
      return AutofillHints.streetAddressLevel3;
    case 'streetaddresslevel4':
      return AutofillHints.streetAddressLevel4;
    case 'streetaddressline1':
      return AutofillHints.streetAddressLine1;
    case 'streetaddressline2':
      return AutofillHints.streetAddressLine2;
    case 'streetaddressline3':
      return AutofillHints.streetAddressLine3;
    case 'sublocality':
      return AutofillHints.sublocality;
    case 'telephonenumber':
      return AutofillHints.telephoneNumber;
    case 'telephonenumberareacode':
      return AutofillHints.telephoneNumberAreaCode;
    case 'telephonenumbercountrycode':
      return AutofillHints.telephoneNumberCountryCode;
    case 'telephonenumberdevice':
      return AutofillHints.telephoneNumberDevice;
    case 'telephonenumberextension':
      return AutofillHints.telephoneNumberExtension;
    case 'telephonenumberlocal':
      return AutofillHints.telephoneNumberLocal;
    case 'telephonenumberlocalprefix':
      return AutofillHints.telephoneNumberLocalPrefix;
    case 'telephonenumberlocalsuffix':
      return AutofillHints.telephoneNumberLocalSuffix;
    case 'telephonenumbernational':
      return AutofillHints.telephoneNumberNational;
    case 'transactionamount':
      return AutofillHints.transactionAmount;
    case 'transactioncurrency':
      return AutofillHints.transactionCurrency;
    case 'url':
      return AutofillHints.url;
    case 'username':
      return AutofillHints.username;
    default:
      return defaultAutoFillHint;
  }
}

AutofillContextAction? parseAutofillContextAction(String? action,
    [AutofillContextAction? defaultAction]) {
  switch (action?.toLowerCase()) {
    case 'commit':
      return AutofillContextAction.commit;
    case 'cancel':
      return AutofillContextAction.cancel;
    default:
      return defaultAction;
  }
}
