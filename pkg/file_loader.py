def load_keywords_from_file(filename):
    try:
        with open(filename, 'r') as file:
            keywords = file.readlines()
        return [keyword.strip() for keyword in keywords]
    except FileNotFoundError:
        print(Fore.RED + f"File '{filename}' not found.")
        return []

def load_server_headers_from_file(filename):
    try:
        with open(filename, 'r') as file:
            server_headers = file.readlines()
        return [header.strip() for header in server_headers]
    except FileNotFoundError:
        print(Fore.RED + f"File '{filename}' not found.")
        return []
