"""Decrypt and execute only the two fixed callbacks. No stored passphrase."""
import argparse
import base64
import hashlib
import json
import os
import subprocess
import tempfile

from cryptography.fernet import Fernet, InvalidToken

COMMANDS = {event: f"curl -fsS --max-time 2 'http://127.0.0.1:8855/?event={event}'"
            for event in ('ORCHID_17_A', 'ORCHID_17_B')}
ARGV = {command: ['/usr/bin/curl', '-fsS', '--max-time', '2',
                 f'http://127.0.0.1:8855/?event={event}'] for event, command in COMMANDS.items()}


def cipher(phrase, salt):
    if not isinstance(phrase, str) or not 1 <= len(phrase) <= 128 or len(salt) != 16:
        raise ValueError('Invalid key input')
    key = hashlib.scrypt(phrase.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
    return Fernet(base64.urlsafe_b64encode(key))


def encrypt(plaintext, phrase):
    salt = os.urandom(16)
    return base64.urlsafe_b64encode(salt).decode() + '.' + cipher(phrase, salt).encrypt(plaintext.encode()).decode()


def decrypt(token, phrase):
    if not isinstance(token, str) or not 1 <= len(token) <= 2048:
        raise ValueError('Invalid token length')
    salt, ciphertext = token.split('.')
    salt = base64.b64decode(salt, altchars=b'-_', validate=True)
    return cipher(phrase, salt).decrypt(ciphertext).decode('utf-8')


def run(token, phrase):
    try:
        command = decrypt(token, phrase)
    except (ValueError, InvalidToken, UnicodeError):
        return 2, '', 'Decryption failed\n'
    if command not in ARGV:
        return 3, '', 'Action not permitted\n'
    with tempfile.TemporaryDirectory(prefix='orchid-encrypted-') as directory:
        result = subprocess.run(ARGV[command], shell=False, cwd=directory,
                                env={'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'},
                                capture_output=True, text=True, timeout=3)
    return result.returncode, json.dumps({'decrypted': command, 'stdout': result.stdout}) + '\n', result.stderr


if __name__ == '__main__':
    import sys
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phrase', required=True)
    parser.add_argument('--token', required=True)
    args = parser.parse_args()
    try:
        code, stdout, stderr = run(args.token, args.phrase)
    except (OSError, subprocess.SubprocessError):
        code, stdout, stderr = 4, '', 'Local execution failed\n'
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)
    sys.exit(code)
