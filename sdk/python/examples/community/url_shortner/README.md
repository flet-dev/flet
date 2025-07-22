# url shortner using flet

a simple shortner made with flet. A URL shortener is a simple tool that takes a long URL and turns it into whatever URL you would like it to be.

# Modules

"pyshorteners" is a Python library that provides functionality for shortening URLs using various URL shortening services such as bit.ly, tinyurl.com, etc. It allows users to programmatically create shortened versions of long URLs, which are typically used for sharing links on social media, email, or other platforms where long URLs can be inconvenient or visually unappealing.

Once the "pyshorteners" library is imported, you can use its functions and classes to generate shortened URLs. For example, you can use the "Shortener" class to create a new shortening service object, and then call the "short" method to generate a shortened URL.

Here is an example code snippet that demonstrates how to use "pyshorteners" to shorten a URL using the bit.ly service:

```
import pyshorteners

url = "https://www.example.com/some/long/url/that/needs/to/be/shortened"

shortener = pyshorteners.Shortener('Bitly', bitly_token='your_bitly_token')

short_url = shortener.short(url)
print(short_url)

```
