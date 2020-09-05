#!/usr/bin/env python3
import io, sys, base64
from Crypto.Cipher import AES

with io.open('./target', 'rb') as fp:
    # first 8 bytes is useless
    # strip 8 bytes: https://tools.ietf.org/html/rfc2406#section-2.4
    c = fp.read()[8:]

    # rest of data:
    #   16 byte iv
    #   payload encrypted
    iv, ct = c[:16], c[16:]

    # known key
    key = b'13vu94r6643rv19u'
    aes = AES.new(key, AES.MODE_CBC, iv)

    # decrypt
    plaintext = aes.decrypt(ct)

    sys.stdout.buffer.write(plaintext)
