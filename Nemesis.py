import argparse
import requests
import time
from colorama import init, Fore, Style
import pkg.file_loader

init(autoreset=True)

def logo():
        print(Fore.RED + "\n           +-----------------+")
        print(Fore.RED + "           |----- Nemesis ---|")
        print(Fore.RED + "           |-- Version 1.0 --|")
        print(Fore.RED + "           +-----------------+ -By HK\n")
        time.sleep(1)
        return None

def get_security_headers(url):
    try:
        response = requests.get(url)
        security_headers = response.headers
        return security_headers
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Error:", e)
        return None

def check_security_headers(headers):
    findings = []
    security_headers_to_check = {
        'Content-Security-Policy': 'Content Security Policy',
        'Referrer-Policy': 'Referrer Policy',
        'X-Content-Type-Options': 'X-Content-Type-Options',
        'Cache-Control' : 'Cache-Control',
        'Clear-Site-Data' : 'Clear-Site-Data'
    }

    for header_name, header_desc in security_headers_to_check.items():
        if header_name in headers and headers[header_name]:
            findings.append(Fore.GREEN + header_desc + " - Header is Found!")
        else:
            findings.append(Fore.RED + header_desc + " - Header is Missing!")

    return findings

def search_server_header(headers, response_text):
    server_header_findings = []
    server_headers = pkg.file_loader.load_server_headers_from_file('wordlist/serverheaders.txt')
    for header in server_headers:
        if header in headers:
            server_header_findings.append(Fore.GREEN  + " |- " + f"{header} header found: {headers[header]}")
    return server_header_findings

def search_keyword(headers, response_text):
    keywords_findings = []
    keywords = pkg.file_loader.load_keywords_from_file('wordlist/keywords.txt')
    for keyword in keywords:
        if keyword.lower() in response_text.lower():
            keywords_findings.append(Fore.GREEN + "|- " + f"Keyword '{keyword}' found in response.")
    return keywords_findings

def send_http_options_trace(url):
    try:
        # Send HTTP OPTIONS request
        options_response = requests.options(url)
        if options_response.status_code == 200:
            print(Fore.GREEN + "\n[+] HTTP OPTIONS request successful")
            allow_header = options_response.headers.get('Allow')
            if allow_header:
                print( " |- Allow header:", allow_header)
            else:
                print(Fore.RED + " |- Allow header not found in response")
        else:
            print(Fore.RED + "\n[+] HTTP OPTIONS request failed. Status code:", options_response.status_code)

        # Send HTTP TRACE request
        trace_response = requests.request("TRACE", url)
        if trace_response.status_code == 200:
            print(Fore.GREEN + "\n[+] HTTP TRACE request successful")
            print(Fore.BLUE + " |- Response content:")
            print( trace_response.text)
        else:
            print(Fore.RED + "\n[+] HTTP TRACE request failed. Status code:", trace_response.status_code)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + "Error occurred:", e)


def main():

    parser = argparse.ArgumentParser(description="DOOM V1.0")
    parser.add_argument("--url", type=str, help="URL of target", required=True)
    args = parser.parse_args()

    url = args.url
    headers = get_security_headers(url)

    if headers:
        logo()

        print(Fore.CYAN + "\n[+] Response from:", url + "\n")
        for header, value in headers.items():
            print(Fore.BLUE + header + ":", Fore.GREEN + value)
        
        findings = check_security_headers(headers)
        if findings:
            print(Fore.CYAN + "\n[+] Missing Security Headers:")
            for finding in findings:
                print(" |- " + finding)

        try:
            response = requests.get(url)
            response_text = response.text
        except requests.exceptions.RequestException as e:
            print(Fore.RED + "Failed to fetch response text:", e)
            response_text = ""

        header_findings = search_server_header(headers, response_text)
        if header_findings:
            print(Fore.CYAN + "\n[+] Platform name / Version Disclosure:")
            for server_header_findings in header_findings:
                print(server_header_findings)

        sensitive_keyword_findings = search_keyword(headers, response_text)
        if sensitive_keyword_findings:
            print(Fore.CYAN + "\n[+] Sensitive Keywords found:")
            for keywords_findings in sensitive_keyword_findings:
                print(keywords_findings)

        send_http_options_trace(url)

    else:
        print(Fore.RED + "Failed to fetch security headers for", url + "\n")


if __name__ == "__main__":
     main()