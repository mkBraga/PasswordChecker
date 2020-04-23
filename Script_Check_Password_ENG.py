#################################################################     Password Checker   ###################################################################
#                               
#           INSTAL:             pip install requests
#           Activate:                             
#           DEFINITION:             
#           DOCUMENTATION:      https://pypi.org/project/requests/
#           Alternative Site:   https://haveibeenpwned.com/Passwords (for check password)
#           CMD:                python3 Scrpit_Check_Pasword_Eng.py "password"     (without quotes)                  
############################################################################################################################################################

import requests
import hashlib
import sys


def request_api_data(query_char):

    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)

    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res

def get_password_leaks_count(hashes, has_to_check):

    hashes = (line.split(':') for line in hashes.text.splitlines())

    for h, count in hashes:
        if h == has_to_check:
            return count
    return 0

def pwned_api_check(password):
    
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    print('\n', first5_char, tail)
    return get_password_leaks_count(response, tail)

def main(args):
    
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} it was found {count} times... you must change the pass')
        else:
            print(f'{password} not found.  :D !')
    return '\nDone Boss....'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
