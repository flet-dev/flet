from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

__all__ = [
    "AndroidBuildVersion",
    "AndroidDeviceInfo",
    "DeviceInfo",
    "IosDeviceInfo",
    "IosUtsname",
    "LinuxDeviceInfo",
    "MacOsDeviceInfo",
    "WebBrowserName",
    "WebDeviceInfo",
    "WindowsDeviceInfo",
]


@dataclass
class DeviceInfo:
    """
    Base class for device information.

    Platform-specific classes include:
    - [`AndroidDeviceInfo`][flet.]
    - [`IosDeviceInfo`][flet.]
    - [`LinuxDeviceInfo`][flet.]
    - [`MacOsDeviceInfo`][flet.]
    - [`WebDeviceInfo`][flet.]
    - [`WindowsDeviceInfo`][flet.]
    """


@dataclass
class MacOsDeviceInfo(DeviceInfo):
    active_cpus: int
    """Number of active CPUs."""

    arch: str
    """Machine CPU architecture.

    Note:
        Apple Silicon Macs can return `"x86_64"` if app runs via Rosetta.
    """

    computer_name: str
    """Name given to the local machine."""

    cpu_frequency: int
    """Device CPU frequency."""

    host_name: str
    """Operating system type."""

    kernel_version: str
    """Machine kernel version.

    Examples:
        - `"Darwin Kernel Version 15.3.0: Thu Dec 10 18:40:58 PST 2015; root:xnu-3248.30.4~1/RELEASE_X86_64"`
        - `"Darwin Kernel Version 15.0.0: Wed Dec 9 22:19:38 PST 2015; root:xnu-3248.31.3~2/RELEASE_ARM64_S8000"`
    """

    major_version: int
    """The major release number, such as `10` in version 10.9.3."""

    memory_size: int
    """Machine's memory size."""

    minor_version: int
    """The minor release number, such as `9` in version 10.9.3."""

    model: str
    """Device model identifier.

    For example: `"MacBookPro18,3"`, `"Mac16,2"`.
    """

    model_name: str
    """Device model name.

    For example: `"MacBook Pro (16-inch, 2021)"`, `"iMac (24-inch, 2024)"`.
    """

    os_release: str
    """Operating system release number."""

    patch_version: int
    """The update release number, such as `3` in `version 10.9.3`."""

    system_guid: Optional[str] = None
    """Device GUID."""


class WebBrowserName(Enum):
    """
    Represents commonly used browsers.
    """

    FIREFOX = "firefox"
    """Mozilla Firefox"""

    SAMSUNG_INTERNET = "samsungInternet"
    """Samsung Internet Browser"""

    OPERA = "opera"
    """Opera Web Browser"""

    MSIE = "msie"
    """Microsoft Internet Explorer"""

    EDGE = "edge"
    """Microsoft Edge"""

    CHROME = "chrome"
    """Google Chrome"""

    SAFARI = "safari"
    """Apple Safari"""

    UNKNOWN = "unknown"
    """Unknown web browser"""


@dataclass
class WebDeviceInfo(DeviceInfo):
    """
    Information derived from `navigator`.

    More info: https://developer.mozilla.org/en-US/docs/Web/API/Window/navigator
    """

    browser_name: WebBrowserName
    """The name of the browser in use."""

    app_code_name: Optional[str] = None
    """The internal 'code' name of the current browser.

    More info: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/appCodeName

    Note:
        Do not rely on this property to return the correct value.
    """

    app_name: Optional[str] = None
    """A string with the official name of the browser.

    More info: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/appName

    Note:
        Do not rely on this property to return the correct value.
    """

    app_version: Optional[str] = None
    """The version of the browser as a string.

    More info: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/appVersion

    Note:
        Do not rely on this property to return the correct value.
    """

    device_memory: Optional[float] = None
    """The amount of device memory in gigabytes.

    This value is an approximation given by rounding to the nearest power of `2` and
    dividing that number by `1024`.

    More info: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/deviceMemory
    """

    language: Optional[str] = None
    """A string representing the preferred language of the user, usually the language
    of the browser UI.

    Will be `None` if unknown.

    More info: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/language
    """

    languages: Optional[list[str]] = None
    """A list of strings representing the languages known to the user, by order of
    preference.

    More info: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/languages
    """

    platform: Optional[str] = None
    """A string representing the platform of the browser.

    More info: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/platform

    Note:
        Do not rely on this property to return the correct value.
    """

    product: Optional[str] = None
    """Always returns `"Gecko"`, on any browser.

    More info: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/product

    Note:
        Do not rely on this property to return the correct value. This property is
        kept only for compatibility purposes.
    """

    product_sub: Optional[str] = None
    """The build number of the current browser.

    More info: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/productSub

    Note:
        Do not rely on this property to return the correct value.
    """

    user_agent: Optional[str] = None
    """The user agent string for the current browser (e.g., 'Mozilla/5.0 ...').

    More info: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/userAgent
    """

    vendor: Optional[str] = None
    """The vendor name of the current browser.

    More info: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/vendor
    """

    vendor_sub: Optional[str] = None
    """Returns the vendor version number (e.g., '6.1').

    More info: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/vendorSub

    Note:
        Do not rely on this property to return the correct value.
    """

    max_touch_points: Optional[int] = None
    """The maximum number of simultaneous touch contact points supported
    by the current device.

    More info: https://developer.mozilla.org/en-US/docs/Web/API/Navigator/maxTouchPoints
    """

    hardware_concurrency: Optional[int] = None
    """The number of logical processor cores available.

    More info:
    https://developer.mozilla.org/en-US/docs/Web/API/Navigator/hardwareConcurrency
    """


@dataclass
class AndroidBuildVersion:
    code_name: str
    """
    The current development codename, or the string "REL" if this is a release build.
    """

    incremental: str
    """
    The internal value used by the underlying source control to represent this build.

    Note:
        Available only on Android M (API 23) and newer.
    """

    release: str
    """The user-visible version string."""

    sdk: int
    """The user-visible SDK version of the framework.

    Possible values are defined in:
    https://developer.android.com/reference/android/os/Build.VERSION_CODES.html
    """

    base_os: Optional[str] = None
    """The base OS build the product is based on.

    Note:
        Available only on Android M (API 23) and newer.
    """

    preview_sdk: Optional[int] = None
    """The developer preview revision of a pre-release SDK."""

    security_patch: Optional[str] = None
    """The user-visible security patch level.

    Note:
        Available only on Android M (API 23) and newer.
    """


@dataclass
class AndroidDeviceInfo(DeviceInfo):
    available_ram_size: int
    """Total available RAM size in bytes."""

    board: str
    """The name of the underlying board, like `"goldfish"`.

    More info: https://developer.android.com/reference/android/os/Build#BOARD
    """

    bootloader: str
    """The system bootloader version number.

    More info: https://developer.android.com/reference/android/os/Build#BOOTLOADER
    """

    brand: str
    """The consumer-visible brand with which the product/hardware will be associated,
    if any.

    More info: https://developer.android.com/reference/android/os/Build#BRAND
    """

    device: str
    """The name of the industrial design.

    More info: https://developer.android.com/reference/android/os/Build#DEVICE
    """

    display: str
    """A build ID string meant for displaying to the user.

    More info: https://developer.android.com/reference/android/os/Build#DISPLAY
    """

    fingerprint: str
    """A string that uniquely identifies this build.

    More info: https://developer.android.com/reference/android/os/Build#FINGERPRINT
    """

    free_disk_size: int
    """Free disk size in bytes."""

    hardware: str
    """The name of the hardware (from the kernel command line or /proc).

    More info: https://developer.android.com/reference/android/os/Build#HARDWARE
    """

    host: str
    """Hostname.

    More info: https://developer.android.com/reference/android/os/Build#HOST
    """

    id: str
    """Either a changelist number, or a label like `"M4-rc20"`.

    More info: https://developer.android.com/reference/android/os/Build#ID
    """

    is_low_ram_device: bool
    """`True` if the application is running on a low-RAM device, `False` otherwise."""

    is_physical_device: bool
    """`False` if the application is running in an emulator, `True` otherwise."""

    manufacturer: str
    """The manufacturer of the product/hardware.

    More info: https://developer.android.com/reference/android/os/Build#MANUFACTURER
    """

    model: str
    """The end-user-visible name for the end product.

    More info: https://developer.android.com/reference/android/os/Build#MODEL
    """

    name: str
    """The name of the device."""

    physical_ram_size: int
    """Total physical RAM size in bytes."""

    product: str
    """The name of the overall product.

    More info: https://developer.android.com/reference/android/os/Build#PRODUCT
    """

    supported_32_bit_abis: list[str]
    """An ordered list of 32 bit ABIs supported by this device.
    Available only on Android L (API 21) and newer.

    More info:
    https://developer.android.com/reference/android/os/Build#SUPPORTED_32_BIT_ABIS
    """

    supported_64_bit_abis: list[str]
    """An ordered list of 64 bit ABIs supported by this device.
    Available only on Android L (API 21) and newer.

    More info:
    https://developer.android.com/reference/android/os/Build#SUPPORTED_64_BIT_ABIS
    """

    supported_abis: list[str]
    """An ordered list of ABIs supported by this device.
    Available only on Android L (API 21) and newer.

    More info: https://developer.android.com/reference/android/os/Build#SUPPORTED_ABIS
    """

    system_features: list[str]
    """Describes what features are available on the current device.

    This can be used to check if the device has, for example, a front-facing
    camera, or a touchscreen. However, in many cases this is not the best
    API to use. For example, if you are interested in bluetooth, this API
    can tell you if the device has a bluetooth radio, but it cannot tell you
    if bluetooth is currently enabled, or if you have been granted the
    necessary permissions to use it. Please only use this if there is no
    other way to determine if a feature is supported.

    This data comes from Android's PackageManager.getSystemAvailableFeatures,
    and many of the common feature strings to look for are available in
    PackageManager's public documentation:
    https://developer.android.com/reference/android/content/pm/PackageManager
    """

    tags: str
    """Comma-separated tags describing the build, like `"unsigned,debug"`.

    More info: https://developer.android.com/reference/android/os/Build#TAGS
    """

    total_disk_size: int
    """Total disk size in bytes."""

    type: str
    """The type of build, like `"user"` or `"eng"`.

    More info: https://developer.android.com/reference/android/os/Build#TYPE
    """

    version: AndroidBuildVersion
    """
    Android operating system version values derived from `android.os.Build.VERSION`.
    """


@dataclass
class LinuxDeviceInfo(DeviceInfo):
    """
    Device information for a Linux system.

    More info:
        - https://www.freedesktop.org/software/systemd/man/os-release.html
        - https://www.freedesktop.org/software/systemd/man/machine-id.html
    """

    name: str
    """A string identifying the operating system, without a version component,
    and suitable for presentation to the user.

    Examples: `"Fedora"`, `"Debian GNU/Linux"`.

    If not set, defaults to `"Linux"`.
    """

    id: str
    """A lower-case string identifying the operating system, excluding any version
    information and suitable for processing by scripts or usage in generated filenames.

    The ID contains no spaces or other characters outside of 0–9, a–z, '.', '_' and '-'.

    Examples: `"fedora"`, `"debian"`.

    If not set, defaults to `"linux"`.
    """

    pretty_name: str
    """A pretty operating system name in a format suitable for presentation to the
    user. May or may not contain a release code name or OS version of some kind,
    as suitable.

    Examples: `"Fedora 17 (Beefy Miracle)"`.

    If not set, defaults to `"Linux"`.
    """

    version: Optional[str] = None
    """A string identifying the operating system version, excluding any OS name
    information, possibly including a release code name, and suitable for presentation
    to the user.

    Examples: `"17"`, `"17 (Beefy Miracle)"`.

    May be `None` on some systems.
    """

    id_like: Optional[list[str]] = None
    """A space-separated list of operating system identifiers in the same syntax as
    the id value. It lists identifiers of operating systems that are closely related
    to the local operating system in regards to packaging and programming interfaces,
    for example listing one or more OS identifiers the local OS is a derivative from.

    Examples: an operating system with id `"centos"`, would list `"rhel"`
    and `"fedora"`, and an operating system with id `"ubuntu"` would list `"debian"`.

    May be `None` on some systems.
    """

    version_code_name: Optional[str] = None
    """A lower-case string identifying the operating system release code name,
    excluding any OS name information or release version, and suitable for processing
    by scripts or usage in generated filenames.

    The codename contains no spaces or other characters outside of 0–9, a–z, '.', '_'
    and '-'.

    Examples: `"buster"`, `"xenial"`.

    May be `None` on some systems.
    """

    version_id: Optional[str] = None
    """A lower-case string identifying the operating system version, excluding any
    OS name information or release code name, and suitable for processing by scripts or
    usage in generated filenames.

    The version is mostly numeric, and contains no spaces or other characters outside
    of 0–9, a–z, '.', '_' and '-'.

    Examples: `"17"`, `"11.04"`.

    May be `None` on some systems.
    """

    build_id: Optional[str] = None
    """A string uniquely identifying the system image used as the origin for a
    distribution (it is not updated with system updates). The field can be identical
    between different version_id values as build_id is only a unique identifier to a
    specific version.

    Examples: `"2013-03-20.3"`, `"201303203"`.

    May be `None` on some systems.
    """

    variant: Optional[str] = None
    """A string identifying a specific variant or edition of the operating system
    suitable for presentation to the user. This field may be used to inform the user
    that the configuration of this system is subject to a specific divergent set of
    rules or default configuration settings.

    Examples: `"Server Edition"`, `"Smart Refrigerator Edition"`.

    Note: this field is for display purposes only. The variant_id field should be used
    for making programmatic decisions.

    May be `None` on some systems.
    """

    variant_id: Optional[str] = None
    """A lower-case string identifying a specific variant or edition of the operating
    system. This may be interpreted in order to determine a divergent default
    configuration.

    The variant ID contains no spaces or other characters outside of
    0–9, a–z, '.', '_' and '-'.

    Examples: `"server"`, `"embedded"`.

    May be `None` on some systems.
    """

    machine_id: Optional[str] = None
    """A unique machine ID of the local system that is set during installation or boot.
    The machine ID is hexadecimal, 32-character, lowercase ID. When decoded from
    hexadecimal, this corresponds to a 16-byte/128-bit value.
    """


@dataclass
class WindowsDeviceInfo(DeviceInfo):
    computer_name: str
    """The computer's fully-qualified DNS name, where available."""

    number_of_cores: int
    """Number of CPU cores on the local machine."""

    system_memory: int
    """The physically installed memory in the computer, in megabytes.

    This may not be the same as available memory.
    """

    user_name: str

    major_version: int
    """The major version number of the operating system.

    For example, for Windows 2000, the major version number is `5`.

    For more info, see the table in Remarks:
    https://docs.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/ns-wdm-_osversioninfoexw#remarks
    """

    minor_version: int
    """The minor version number of the operating system.

    For example, for Windows 2000, the minor version number is `0`.

    For more info, see the table in Remarks:
    https://docs.microsoft.com/en-us/windows-hardware/drivers/ddi/wdm/ns-wdm-_osversioninfoexw#remarks
    """

    build_number: int
    """The build number of the operating system.

    Examples:
        - `22000` or greater for Windows 11.
        - `10240` or greater for Windows 10.
    """

    platform_id: int
    """The operating system platform.

    For Win32 on NT-based operating systems,
    RtlGetVersion returns the value `VER_PLATFORM_WIN32_NT`.
    """

    csd_version: str
    """The service-pack version string.

    This member contains a string, such as "Service Pack 3",
    which indicates the latest service pack installed on the system.
    """

    service_pack_major: int
    """The major version number of the latest service pack installed on the system.

    For example, for Service Pack 3, the major version number is three.
    If no service pack has been installed, the value is zero.
    """

    service_pack_minor: int
    """The minor version number of the latest service pack installed on the system.

    For example, for Service Pack 3, the minor version number is zero.
    """

    suit_mask: int
    """The product suites available on the system."""

    product_type: int
    """The product type.

    This member contains additional information about the system.
    """

    reserved: int
    """Reserved for future use."""

    build_lab: str
    """Value of `HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\BuildLab`
    registry key.

    For example: `"22000.co_release.210604-1628"`.
    """

    build_lab_ex: str
    """Value of `HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\BuildLabEx`
    registry key.

    For example: `"22000.1.amd64fre.co_release.210604-1628"`.
    """

    # digital_product_id: str

    display_version: str
    """Value of `HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\DisplayVersion`
    registry key.

    For example: `"21H2"`.
    """

    edition_id: str
    """Value of `HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\EditionID`
    registry key.
    """

    install_date: datetime
    """Value of `HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\InstallDate`
    registry key.
    """

    product_id: str
    """Displayed as "Product ID" in Windows Settings.

    Value of the `HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProductId`
    registry key.

    For example: `"00000-00000-0000-AAAAA"`.
    """

    product_name: str
    """Value of `HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProductName`
    registry key.

    For example: `"Windows 10 Home Single Language"`.
    """

    registered_owner: str
    """Value of the `HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\RegisteredOwner`
    registry key.

    For example: `"Microsoft Corporation"`.
    """

    release_id: str
    """
    Value of the `HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ReleaseId`
    registry key.

    For example: `"1903"`.
    """

    device_id: str
    """Displayed as "Device ID" in Windows Settings.

    Value of `HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\SQMClient\\MachineId`
    registry key.
    """


@dataclass
class IosUtsname:
    """
    Information derived from `utsname`.

    More info: http://pubs.opengroup.org/onlinepubs/7908799/xsh/sysutsname.h.html
    """

    machine: str
    """Hardware type (e.g. `"iPhone7,1"` for iPhone 6 Plus)."""

    node_name: str
    """Network node name."""

    release: str
    """Release level."""

    sys_name: str
    """Operating system name."""

    version: str
    """Version level."""


@dataclass
class IosDeviceInfo(DeviceInfo):
    available_ram_size: int
    """Current unallocated RAM size of the device in megabytes."""

    free_disk_size: int
    """Free disk size in bytes."""

    is_ios_app_on_mac: bool
    """Indicates whether the process is an iPhone or iPad app running on a Mac.

    More info:
    https://developer.apple.com/documentation/foundation/nsprocessinfo/3608556-iosapponmac
    """

    is_physical_device: bool
    """`False` if the application is running in a simulator, `True` otherwise."""

    localized_model: str
    """Localized name of the device model.

    More info:
    https://developer.apple.com/documentation/uikit/uidevice/1620029-localizedmodel
    """

    model: str
    """Device model according to OS.

    More info:
    https://developer.apple.com/documentation/uikit/uidevice/1620044-model
    """

    model_name: str
    """Commercial or user-known model name.

    For example: `"iPhone 16 Pro"`, `"iPad Pro 11-Inch 3"`
    """

    name: str
    """The device name.

    Note:
        - On iOS < 16 returns user-assigned device name.
        - On iOS >= 16 returns a generic device name if project has
            no entitlement to get user-assigned device name.

    More info:
    https://developer.apple.com/documentation/uikit/uidevice/1620015-name
    """

    physical_ram_size: int
    """Total physical RAM size of the device in megabytes."""

    system_name: str
    """The name of the current operating system.

    More info:
    https://developer.apple.com/documentation/uikit/uidevice/1620054-systemname
    """

    system_version: str
    """The current operating system version.

    More info:
    https://developer.apple.com/documentation/uikit/uidevice/1620043-systemversion
    """

    total_disk_size: int
    """Total disk size in bytes."""

    utsname: IosUtsname
    """Operating system information derived from `sys/utsname.h`."""

    identifier_for_vendor: Optional[str] = None
    """Unique UUID value identifying the current device.

    More info:
    https://developer.apple.com/documentation/uikit/uidevice/1620059-identifierforvendor
    """
