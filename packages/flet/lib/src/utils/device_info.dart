import 'dart:ui';

import 'package:device_info_plus/device_info_plus.dart';
import 'package:flet/src/utils/locale.dart';
import 'package:flutter/services.dart';

import 'enums.dart';
import 'platform.dart';

/// Returns device information as a Map.
Future<Map<String, dynamic>> getDeviceInfo() async {
  BaseDeviceInfo deviceInfo = await DeviceInfoPlugin().deviceInfo;
  return deviceInfo.asMap();
}

List<Map<String, String?>> getDeviceLocales() =>
    PlatformDispatcher.instance.locales
        .map((locale) => locale.toMap())
        .toList();

extension DeviceInfoExtension on BaseDeviceInfo {
  Map<String, dynamic> asMap() {
    var deviceInfo = this;
    final deviceLocales = getDeviceLocales();
    if (isWebPlatform()) {
      deviceInfo = (deviceInfo as WebBrowserInfo);
      return {
        "browser_name": deviceInfo.browserName.name,
        "app_code_name": deviceInfo.appCodeName,
        "app_name": deviceInfo.appName,
        "app_version": deviceInfo.appVersion,
        "device_memory": deviceInfo.deviceMemory,
        "language": deviceInfo.language,
        "languages": deviceInfo.languages,
        "platform": deviceInfo.platform,
        "product": deviceInfo.product,
        "product_sub": deviceInfo.productSub,
        "user_agent": deviceInfo.userAgent,
        "vendor": deviceInfo.vendor,
        "vendor_sub": deviceInfo.vendorSub,
        "max_touch_points": deviceInfo.maxTouchPoints,
        "hardware_concurrency": deviceInfo.hardwareConcurrency,
        "locales": deviceLocales,
      };
    } else {
      if (isAndroidMobile()) {
        deviceInfo = (deviceInfo as AndroidDeviceInfo);
        return {
          "available_ram_size": deviceInfo.availableRamSize,
          "board": deviceInfo.board,
          "bootloader": deviceInfo.bootloader,
          "brand": deviceInfo.brand,
          "device": deviceInfo.device,
          "display": deviceInfo.display,
          "fingerprint": deviceInfo.fingerprint,
          "free_disk_size": deviceInfo.freeDiskSize,
          "hardware": deviceInfo.hardware,
          "host": deviceInfo.host,
          "id": deviceInfo.id,
          "is_low_ram_device": deviceInfo.isLowRamDevice,
          "is_physical_device": deviceInfo.isPhysicalDevice,
          "manufacturer": deviceInfo.manufacturer,
          "model": deviceInfo.model,
          "name": deviceInfo.name,
          "physical_ram_size": deviceInfo.physicalRamSize,
          "product": deviceInfo.product,
          "supported_32_bit_abis": deviceInfo.supported32BitAbis,
          "supported_64_bit_abis": deviceInfo.supported64BitAbis,
          "supported_abis": deviceInfo.supportedAbis,
          "system_features": deviceInfo.systemFeatures,
          "tags": deviceInfo.tags,
          "total_disk_size": deviceInfo.totalDiskSize,
          "type": deviceInfo.type,
          "version": {
            'base_os': deviceInfo.version.baseOS,
            'sdk': deviceInfo.version.sdkInt,
            'release': deviceInfo.version.release,
            'code_name': deviceInfo.version.codename,
            'incremental': deviceInfo.version.incremental,
            'preview_sdk': deviceInfo.version.previewSdkInt,
            'security_patch': deviceInfo.version.securityPatch,
          },
          "locales": deviceLocales,
        };
      } else if (isIOSMobile()) {
        deviceInfo = (deviceInfo as IosDeviceInfo);
        return {
          "available_ram_size": deviceInfo.availableRamSize,
          "free_disk_size": deviceInfo.freeDiskSize,
          "is_ios_app_on_mac": deviceInfo.isiOSAppOnMac,
          "is_physical_device": deviceInfo.isPhysicalDevice,
          "localized_model": deviceInfo.localizedModel,
          "model": deviceInfo.model,
          "model_name": deviceInfo.modelName,
          "name": deviceInfo.name,
          "physical_ram_size": deviceInfo.physicalRamSize,
          "system_name": deviceInfo.systemName,
          "system_version": deviceInfo.systemVersion,
          "total_disk_size": deviceInfo.totalDiskSize,
          "utsname": {
            "machine": deviceInfo.utsname.machine,
            "node_name": deviceInfo.utsname.nodename,
            "release": deviceInfo.utsname.release,
            "sys_name": deviceInfo.utsname.sysname,
            "version": deviceInfo.utsname.version,
          },
          "identifier_for_vendor": deviceInfo.identifierForVendor,
          "locales": deviceLocales,
        };
      } else if (isLinuxDesktop()) {
        deviceInfo = (deviceInfo as LinuxDeviceInfo);
        return {
          "name": deviceInfo.name,
          "id": deviceInfo.id,
          "pretty_name": deviceInfo.prettyName,
          "version": deviceInfo.version,
          "id_like": deviceInfo.idLike,
          "version_code_name": deviceInfo.versionCodename,
          "version_id": deviceInfo.versionId,
          "build_id": deviceInfo.buildId,
          "variant": deviceInfo.variant,
          "variant_id": deviceInfo.variantId,
          "machine_id": deviceInfo.machineId,
          "locales": deviceLocales,
        };
      } else if (isMacOSDesktop()) {
        deviceInfo = (deviceInfo as MacOsDeviceInfo);
        return {
          "active_cpus": deviceInfo.activeCPUs,
          "arch": deviceInfo.arch,
          "computer_name": deviceInfo.computerName,
          "cpu_frequency": deviceInfo.cpuFrequency,
          "host_name": deviceInfo.hostName,
          "kernel_version": deviceInfo.kernelVersion,
          "major_version": deviceInfo.majorVersion,
          "memory_size": deviceInfo.memorySize,
          "minor_version": deviceInfo.minorVersion,
          "model": deviceInfo.model,
          "model_name": deviceInfo.modelName,
          "os_release": deviceInfo.osRelease,
          "patch_version": deviceInfo.patchVersion,
          "system_guid": deviceInfo.systemGUID,
          "locales": deviceLocales,
        };
      } else if (isWindowsDesktop()) {
        deviceInfo = (deviceInfo as WindowsDeviceInfo);
        return {
          "computer_name": deviceInfo.computerName,
          "number_of_cores": deviceInfo.numberOfCores,
          "system_memory": deviceInfo.systemMemoryInMegabytes,
          "user_name": deviceInfo.userName,
          "major_version": deviceInfo.majorVersion,
          "minor_version": deviceInfo.minorVersion,
          "build_number": deviceInfo.buildNumber,
          "platform_id": deviceInfo.platformId,
          "csd_version": deviceInfo.csdVersion,
          "service_pack_major": deviceInfo.servicePackMajor,
          "service_pack_minor": deviceInfo.servicePackMinor,
          "suit_mask": deviceInfo.suitMask,
          "product_type": deviceInfo.productType,
          "reserved": deviceInfo.reserved,
          "build_lab": deviceInfo.buildLab,
          "build_lab_ex": deviceInfo.buildLabEx,
          // "digital_product_id": deviceInfo.digitalProductId,
          "display_version": deviceInfo.displayVersion,
          "edition_id": deviceInfo.editionId,
          "install_date": deviceInfo.installDate,
          "product_id": deviceInfo.productId,
          "product_name": deviceInfo.productName,
          "registered_owner": deviceInfo.registeredOwner,
          "release_id": deviceInfo.releaseId,
          "device_id": deviceInfo.deviceId,
          "locales": deviceLocales,
        };
      }
      return {};
    }
  }
}

DeviceOrientation? parseDeviceOrientation(String? value,
    [DeviceOrientation? defaultValue]) {
  return parseEnum(DeviceOrientation.values, value, defaultValue);
}
