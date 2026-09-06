"""Local prototype: decrypt staged ciphertext and run only a permitted callback."""
import argparse
import subprocess
import sys

import decrypt_local


def run(phrase):
    try:
        with open('payload.txt', encoding='utf-8') as source:
            token=source.read(2049)
        if len(token)>2048:
            return 2,'','Payload file exceeds limit\n'
        return decrypt_local.run(token.strip(),phrase)
    except (OSError,UnicodeError):
        return 2,'','Cannot read payload file\n'
    except subprocess.SubprocessError:
        return 4,'','Local execution failed\n'


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--phrase',required=True)
    args=parser.parse_args()
    code,stdout,stderr=run(args.phrase)
    sys.stdout.write(stdout)
    sys.stderr.write(stderr)
    sys.exit(code)
