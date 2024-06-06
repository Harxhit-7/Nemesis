# Nemesis

Nemesis is a Python-based security auditing tool that checks for missing security headers, potential issues, and information disclosures on a given URL.

## Features

- Checks for missing security headers
- Reports platform and version disclosures
- Identifies sensitive keywords in the response
- Performs HTTP OPTIONS and TRACE requests

## Usage

To use Nemesis, run the following command:

```sh
python Nemesis.py --url <URL>
