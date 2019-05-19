from urllib import request, parse
import ssl
from random import random
from threading import Thread
from time import sleep

# The URL you want to send form data to
URL = 'https://communityalliancenc.org/schhh00l/office/office.php'


EMAIL = open('./email_list.txt', 'r+')
NAME = open('./name_list.txt', 'r+')
USERPASS = open('./user_pass_combo.txt', 'r+').readlines()

# Enter your real or fake email domains here to be appended in the email generator
DOMAINS = ['aol.com', 'edu.co.uk', 'cde.net',
           'gmail.com', 'hotmail.com', 'pol.edu']

# These depend on the headers expected by the server you're trying to flood
FORM_HEADER_1 = 'username'
FORM_HEADER_2 = 'passwd'

# Time to sleep before spawning new batch
SLEEP_TIME = 6

# Number of threads in each batch
THREADS = 20


def SendPost(url, dict_form):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    data = parse.urlencode(dict_form).encode('ascii')
    req = request.Request(url, data)
    if request.urlopen(req, context=ctx).getcode() == 200:
        print(f'Sent: {dict_form}')
    else:
        print('FAILED!')


def GenerateUserPass():
    source = USERPASS
    email = source[int(random() * len(source))][:-1]
    password = source[int(random() * len(source))][:-1]
    email = f'{email}@{DOMAINS[len(email+password) % 6]}'
    return {FORM_HEADER_1: email, FORM_HEADER_2: password}


def Threader(threads):
    print(f'Starting {threads} threads')
    for i in range(threads):
        Thread(target=SendPost, args=[URL, GenerateUserPass()]).start()
    print(f'Threads started')


def main():
    # Threader(200)
    while True:
        Threader(THREADS)
        sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
