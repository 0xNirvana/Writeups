# Solution for CTF challenge
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
for guess in itertools.product(chars, repeat=13):
    attempts += 1
    guess = 'PCTF{' + ''.join(guess) + '}'
    # print("Attempt: " + str(attempts) + " Password: " + guess)
    conn = remote('chal.pctf.competitivecyber.club', 4757)
    conn.recvuntil('What is the password: ')
    conn.sendline(guess)
    response = conn.recvline()
    if response != b'There\'s been an error\n':
        print(response)
        break
    conn.close()
    print("Attempt: " + str(attempts) + " Password: " + guess)
