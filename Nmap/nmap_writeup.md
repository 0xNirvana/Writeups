## NMAP
Continuing with another box on TryHackMe, as the name suggests this time it is [Nmap](https://nmap.org/). In my last writeup ([Vulnversity](../Vulnversity/vulnversity_writeup.md)), there was a part where nmap was used but it had a brief role over there. With this room ([Nmap](https://tryhackme.com/room/rpnmap)) on THM we can develop our nmap skill further.

#### What is nmap?
As per Wikipedia (https://en.wikipedia.org/wiki/Nmap), it a free open-source network scanner which can be used to discover hosts and services on a computer network by sending packets and analyzing responses. But once we start using nmap to it's fullest, we can see that it can be used for many more things like OS detection, encryptions being used, testing scripts and many more things. Basically, it is one of the most used tools to perform reconnaissance on any given target/s.

So, let's begin with the room now!

### [Task 1] Deploy
We need to deploy the machine in order to gain access to it and nothing more is required in this task.

### [Task 2] Quiz
In this task, there are a number of questions that arranged in a way that we can get a better grip on the mostly used nmap switches. Remember for any help `man nmap` is always there.
As this room is pretty straightforward and there is not much to discuss, we can look into each switch's meaning at a somewhat detailed level.

1. Accessing the Help Menu: `-h`
	* With `nmap -h`, we can see all the various switches and their brief description. This can come in handy when we don't feel like going through the manual and just want to check the switch that we want.
  
2. Stealth Scan: `-sS`
	```
	nmap -sS <target_ip>
	```
	* It is the default and most popular type of scan. As the name suggests it can perform the scan in a stealth mode as it never opens a full TCP connection.

3. UDP Scan: `-sU`
	```
	nmap -sU <target_ip>
	```
	* With this switch, we can perform scan on the target machine's UDP port. This scan works by simply sending a UDP packet to every port on the target machine and analyzing the response.
	
4. Operating System Detection: `-O`
	```
	nmap -O <target_ip>
	```
	* With this switch, we can directly detect the OS that the target machine is running. Sometimes, nmap is not able to detect the exact OS but it might provide some suspected OSs that might be running on the target.

5. Service Version Detection: `-sV`
	```
	nmap -sV <target_ip>
	```
	* With this switch, we can detect the version of the service running on the open ports. Also, with the help of this information, we can differentiate between truly open ports and filtered ports.

6. Being Talky (Verbose): `-v`
	```
	nmap -v <target_ip>
	```
	* Sometimes we want to know what is going on in the background of the running scan and in such cases, the verbose switch turns out to be really helpful.

7. Very Verbose: `-vv`
	```
	nmap -vv <target_ip>
	```
	* This switch provides even greater verbosity and much more detailed insights into the processes running in the background of a scan.
	
8. Saving Output in XML File: `-oX`
	```
	nmap -oX <target_ip>
	```
	* When performing the scan it can be handy to save the output of the scan so that it can be used in the future to check some major or minor details of the scan.

9. Aggressive Scan: `-A`
	```
	nmap -A <target_ip>
	```
	* When want in-depth details of a scan we can use this switch as it is capable of performing OS detection, version detection, script scanning and traceroute all together.
	
10. Max Scan Speed: `-T5`
	```
	nmap -T<0-5> <target_ip>
	```
	* We can adjust the speed of the scan using the speed template. These range from 0 to 5 with 0 T4 being the slowest and T5 being the fastest. One thing to keep in mind here is that faster the scan, more are the chances that we can miss on some details in the scan.
	
11. Specific Port: `-p`
	```
	nmap -p<single port number or range> <target_ip>
	```
	* With this switch, we can perform scan on a single port like `-p80` or over a range of ports like `-p100-2000`.

12. Scanning All Ports: `-p-`
	```
	nmap -p- <target_ip>
	```
	* While running a scan to detect all the open ports, we need to perform a check on all the ports. And in such a case we can use the switch `-p-` to run the scan over all the ports.
	
13. Script Scan: `--script`
	```
	nmap --script <scrip_name> <target_ip>
	```
	* Nmap has a large variety of scripts that can check for various vulnerabilities and perform various detections.

14. Running Vulnerability Scripts: `--script vuln`
	```
	nmap --script vuln <target_ip>
	```
	* There are many categories of scripts in nmap that are segregated in various categories like auth, broadcast, exploit, fuzzer, vuln and many others.

15. Scan Without Ping: `-Pn`
	```
	nmap -Pn <target_ip>
	```
	* With this switch, nmap skips the discovery stage which is used to determine active machines for heavier scanning. When this switch is specified, nmap is forced to perform a scan against every target IP address specified.
	
### [Task 3] Nmap Scanning
This section consists of various tasks that are needed to be performed on the actual deployed machine. I've explained the switches that are used for each task:

Output for questions 1, 2 and 3. As it seems that the results for all these three questions can be obtained from only one search `tester@kali:~$ sudo nmap -sS 10.10.103.104` I've provided it before answering them.

```
tester@kali:~$ sudo nmap -sS 10.10.103.104
Nmap scan report for 10.10.103.104
Host is up (0.17s latency).
Not shown: 997 closed ports
PORT     STATE    SERVICE
22/tcp   open     ssh
80/tcp   open     http
8090/tcp filtered opsmessaging

Nmap done: 1 IP address (1 host up) scanned in 1128.53 seconds
```

1. Syn Scan
	* As explained above Syn Scan can be performed with `-sS` switch.

2. Open Ports
	 * On running the previous scan, we get a list of ports from which we can determine the number of open ports.

3. Communication Protocol
	* From the previous scan result itself, we can determine the protocol as it is provided right beside the port number.
	
For the next 3 questions 4, 5 and 6 as well, only one search would also work and the output of that search is provided below:

```
tester@kali:~$ sudo nmap -A --script vuln 10.10.103.104
[sudo] password for tester: 
Starting Nmap 7.80 ( https://nmap.org ) at 2020-07-14 01:14 IST
Nmap scan report for 10.10.103.104
Host is up (0.16s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.10 (Ubuntu Linux; protocol 2.0)
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
|_clamav-exec: ERROR: Script execution failed (use -d to debug)
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|       httponly flag not set
|   /login.php: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-csrf: Couldn't find any CSRF vulnerabilities.
|_http-dombased-xss: Couldn't find any DOM based XSS.
| http-enum: 
|   /login.php: Possible admin folder
|   /robots.txt: Robots file
|   /config/: Potentially interesting directory w/ listing on 'apache/2.4.7 (ubuntu)'
|   /docs/: Potentially interesting directory w/ listing on 'apache/2.4.7 (ubuntu)'
|_  /external/: Potentially interesting directory w/ listing on 'apache/2.4.7 (ubuntu)'
|_http-server-header: Apache/2.4.7 (Ubuntu)
| http-slowloris-check: 
|   VULNERABLE:
|   Slowloris DOS attack
|     State: LIKELY VULNERABLE
|     IDs:  CVE:CVE-2007-6750
|       Slowloris tries to keep many connections to the target web server open and hold
|       them open as long as possible.  It accomplishes this by opening connections to
|       the target web server and sending a partial request. By doing so, it starves
|       the http server's resources causing Denial Of Service.
|       
|     Disclosure date: 2009-09-17
|     References:
|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2007-6750
|_      http://ha.ckers.org/slowloris/
|_http-stored-xss: Couldn't find any stored XSS vulnerabilities.
| vulners: 
|   cpe:/a:apache:http_server:2.4.7: 
|     	CVE-2017-7679	7.5	https://vulners.com/cve/CVE-2017-7679
|     	CVE-2018-1312	6.8	https://vulners.com/cve/CVE-2018-1312
|     	CVE-2017-15715	6.8	https://vulners.com/cve/CVE-2017-15715
|     	CVE-2014-0226	6.8	https://vulners.com/cve/CVE-2014-0226
|     	CVE-2017-9788	6.4	https://vulners.com/cve/CVE-2017-9788
|     	CVE-2019-0217	6.0	https://vulners.com/cve/CVE-2019-0217
|     	CVE-2020-1927	5.8	https://vulners.com/cve/CVE-2020-1927
|     	CVE-2019-10098	5.8	https://vulners.com/cve/CVE-2019-10098
|     	CVE-2020-1934	5.0	https://vulners.com/cve/CVE-2020-1934
|     	CVE-2019-0220	5.0	https://vulners.com/cve/CVE-2019-0220
|     	CVE-2018-17199	5.0	https://vulners.com/cve/CVE-2018-17199
|     	CVE-2017-9798	5.0	https://vulners.com/cve/CVE-2017-9798
|     	CVE-2017-15710	5.0	https://vulners.com/cve/CVE-2017-15710
|     	CVE-2016-8743	5.0	https://vulners.com/cve/CVE-2016-8743
|     	CVE-2016-2161	5.0	https://vulners.com/cve/CVE-2016-2161
|     	CVE-2016-0736	5.0	https://vulners.com/cve/CVE-2016-0736
|     	CVE-2014-3523	5.0	https://vulners.com/cve/CVE-2014-3523
|     	CVE-2014-0231	5.0	https://vulners.com/cve/CVE-2014-0231
|     	CVE-2019-10092	4.3	https://vulners.com/cve/CVE-2019-10092
|     	CVE-2016-4975	4.3	https://vulners.com/cve/CVE-2016-4975
|     	CVE-2015-3185	4.3	https://vulners.com/cve/CVE-2015-3185
|     	CVE-2014-8109	4.3	https://vulners.com/cve/CVE-2014-8109
|     	CVE-2014-0118	4.3	https://vulners.com/cve/CVE-2014-0118
|     	CVE-2014-0117	4.3	https://vulners.com/cve/CVE-2014-0117
|     	CVE-2018-1283	3.5	https://vulners.com/cve/CVE-2018-1283
|_    	CVE-2016-8612	3.3	https://vulners.com/cve/CVE-2016-8612
No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).
TCP/IP fingerprint:
OS:SCAN(V=7.80%E=4%D=7/14%OT=22%CT=1%CU=40403%PV=Y%DS=2%DC=T%G=Y%TM=5F0CBB2
OS:3%P=x86_64-pc-linux-gnu)SEQ(SP=105%GCD=2%ISR=10A%TI=Z%CI=I%II=I%TS=8)OPS
OS:(O1=M508ST11NW6%O2=M508ST11NW6%O3=M508NNT11NW6%O4=M508ST11NW6%O5=M508ST1
OS:1NW6%O6=M508ST11)WIN(W1=68DF%W2=68DF%W3=68DF%W4=68DF%W5=68DF%W6=68DF)ECN
OS:(R=Y%DF=Y%T=40%W=6903%O=M508NNSNW6%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=A
OS:S%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R
OS:=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F
OS:=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%
OS:T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD
OS:=S)

Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 80/tcp)
HOP RTT       ADDRESS
1   161.35 ms 10.8.0.1
2   161.12 ms 10.10.103.104

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 379.87 seconds
```

4. Service Version Detection
	* Service detection can be performed using the `-sV` switch but we also know that `-A` search can perform multiple detections including service version detection and the output to that is provided above. From the details related to services running on various ports at the beginning of the output, we can see the version of service running on port 22.

5. Find the Flag Not Set
	* The output provided above contains the results of an aggressive `-A` scan and from that, we can easily see under the details for port 80 that there is the only flag that is not set.
	
6. Susceptible DoS Attack
	* Under the details for port 80 itself, we can see that nmap has performed some script tests and from that, we can determine the DoS attack to which the machine is susceptible.
	
With this, we can conclude the Nmap room. This room introduced us with several different switches that we can use with nmap to tweak our scans.
