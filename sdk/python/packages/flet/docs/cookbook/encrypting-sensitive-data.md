---
title: Encrypting sensitive data
sidebar_label: Encrypting sensitive data
---

Sensitive data such as tokens, keys, credit card numbers and other "secrets" must be stored at rest (database, files, [client storage](/docs/cookbook/client-storage)) in encrypted form to avoid data breaches.

Flet includes utility methods to encrypt and decrypt sensitive text data using symmetric algorithm (where the same key is used for encryption and decryption). They use [Fernet](https://github.com/fernet/spec/blob/master/Spec.md) implementation from [cryptography](https://pypi.org/project/cryptography/) package, which is AES 128 with some additional hardening, plus PBKDF2 to derive encryption key from a user passphrase.

## Secret key

Encryption secret key (aka password, or passphrase) is an arbitrary password-like string configured by a user and used for encrypting and decrypting data. Crypto algorithm uses secret key to "derive" encryption key (32 bytes).

/// admonition
    type: danger
Do not embed any secrets into the source code to avoid accidental exposure to the public!
///

You can provide a secret to your app via environment variable:

```python
import os
secret_key = os.getenv("MY_APP_SECRET_KEY")
```

Before running the app set the secret in a command line:

```
$ export MY_APP_SECRET_KEY="<secret>"
```

/// admonition
    type: note
While passing secrets via environment variables is a common practice amongst developers and service providers it does not fully prevent secrets leaking in some environments. Other mechanisms can be used
to inject secrets to your application such as mounting secret files or vault services.
///

## Encrypting data

Use `encrypt()` method to encrypt a string:

```python
import os
from flet.security import encrypt, decrypt

secret_key = os.getenv("MY_APP_SECRET_KEY")
plain_text = "This is a secret message!"
encrypted_data = encrypt(plain_text, secret_key)
```

`encrypted_data` is a URL-safe base64-encoded string.

`encrypt` accepts strings only, so any objects must be serialized to JSON, XML or other text-based format before encryption.

## Decrypting data

Use `decrypt()` method to decrypt the data:

```python
import os
from flet.security import encrypt, decrypt

secret_key = os.getenv("MY_APP_SECRET_KEY")
encrypted_data = "601llp2zpPp4QjBWe2cOwGdBQUFBQUJqTTFJbmgyWU5jblVp..."
plain_text = decrypt(encrypted_data, secret_key)
print(plain_text)
```
