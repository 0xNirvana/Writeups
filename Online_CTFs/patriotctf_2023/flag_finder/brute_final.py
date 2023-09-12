from pwn import *
import itertools
import string

chars = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
attempts = 0

pwf = 'pctf{'
pwb = '************}'

beginning_string = 'User input: 112\\nFlag input: 112\\nUser input: 99\\nFlag input: 99\\nUser input: 116\\nFlag input: 116\\nUser input: 102\\nFlag input: 102\\nUser input: 123\\nFlag input: 123\\n'
end_string = 'There\'s been an error\\n'
       

def attempt(guess, gchar):
    global beginning_string
    global end_string
    conn = remote('chal.pctf.competitivecyber.club', 4757)
    conn.recvuntil('What is the password: ')
    conn.sendline(bytes(guess, encoding='utf-8'))
    response = conn.recvall()
    print(response)
    conn.close()
    gdec = ord(gchar)
    # print(gdec)
    char_select_string = 'User input: {}\\nFlag input: {}\\n'.format(gdec, gdec)
    search_string = beginning_string + char_select_string + end_string
    # print(search_string)
    if search_string in str(response):
        print('FOUND')
        beginning_string = beginning_string + char_select_string
        return True
    elif 'is not long enough' in str(response):
        print('TOO SHORT')
        exit()
    return False


if __name__ == '__main__':
    for i in range(0, 13):
        for guess in chars:
            password = pwf + guess + pwb[i:]
            if attempt(password, guess) == True:
                pwf = pwf + guess
                break