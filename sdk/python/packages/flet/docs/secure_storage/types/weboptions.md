{{ class_all_options("flet_secure_storage.types.WebOptions") }}

## Important Security Considerations

SecureStorage uses an experimental implementation using WebCrypto API.
Use at your own risk. The browser creates the private key, and encrypted
strings in localStorage are not portable to other browsers or machines
and will only work on the same domain.

You MUST have HTTP Strict Forward Secrecy enabled and proper
headers applied to your responses, or you could be subject to JavaScript hijacking.

Required security measures:

- Enable HSTS (HTTP Strict Transport Security)
- Use proper security headers

References:

- https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security
- https://www.netsparker.com/blog/web-security/http-security-headers/

## Application-Specific Key Wrapping

On web, all keys are stored in LocalStorage. You can wrap this stored key
with an application-specific key to make it more difficult to analyze:

```python
storage = SecureStorage(
    web_options=WebOptions(
        wrap_key='your_application_specific_key',
        wrap_key_iv='your_application_specific_iv',
    ),
)
```
