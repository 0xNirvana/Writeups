## OWASP Top 10 
This writeup is going to be based on the [OWASP Top 10](https://tryhackme.com/room/owasptop10) room on TryHackMe. The challenges to this room are going to be released on a daily basis so that for 10 days one can focus on one of the Top 10 vulnerabilities whichever has been released for that day. I will try to add every vulnerability task to this article as soon as I complete it.

### What is OWASP and what are the Top 10???
Open Web Application Security Project or better known as [OWASP](https://owasp.org/) is an online community that produces tools, documentations, technologies and many other things related to web security which can be accessed by anyone and at a cost-free rate. Some of the major OWASP projects that I know are [ZAP](https://www.zaproxy.org/), [Juice Shop](https://github.com/bkimminich/juice-shop), obviously the [Top 10](https://owasp.org/www-project-top-ten/) and many others.

Coming to OWASP Top 10, OWASP releases this document called OWASP Top 10 which consists of most critical security risks to web applications. There are many versions of this document released in the past as well. Going through this document would help any individual to develop a better insight regarding some of the major vulnerabilities on the web and not only how to exploit them but also how to protect yourself from those vulnerabilities.

Coming to this room, it does not require any prerequisite knowledge related to these vulnerabilities but one can easily develop some knowledge regarding them. Moving on let's get started with the `OWASP Top 10` room!

### [Task 1] Introduction
This task just provides a list of all the vulnerabilities that are going to be covered in this room.

1. Injection
2. Broken Authentication
3. Sensitive Data Exposure
4. XML External Entity
5. Broken Access Control
6. Security Misconfiguration
7. Cross-Site Scripting
8. Insecure Deserialization
9. Components With Known Vulnerabilities
10. Insufficient Logging and Monitoring

#### Tasks 2 and 3 are just related to VPN access and daily prize. So, nothing important here.

### [Task 4] Injection
This is the point where all the interesting stuff begins. In this task, they have briefed about what an Injection is, how it can be performed and how to defend yourself from such attacks. Following are some major points from the description they have provided:

* There are broadly two types of injection attacks:
	* SQL Injection: When you exploit some weakness in SQL or database implementation in a web application.
	* Command Injection: When you exploit the web app implementation at the system level and run system-level command.
* Once such injection attacks are successfully performed, an attacker can easily access, modify or delete important data and sometimes confidential data as well.
* Considering the protection from such attacks, the best way is to sanitize all the data coming in from every possible entry-point before it gets processed or executed.

### [Task 5] Command Injection
This task provides a brief introduction to command injection. One important point described over here is that once an attacker gets access to the system it is not necessary that he/she will perform some simple malicious tasks like `whoami` or some other system-level commands but he/she can also try to pop a shell for themselves and virtually own all the data stored on that server which can be pretty dangerous in several ways.

### [Task 6] Command Injection Practical
This task is all about the practical implementation of Command Injection. Though one important thing to be noted here is that we can never find such an easy way to perform command injection out in the real world, this is just for basic practice and develop a simple mindset for such an attack.

The task talks about a simple code snippet that is running behind the URL through which we will be performing command injection. Also, a few Windows and Linux commands are provided which can be tested while performing command injection. 

Now, the most interesting part of THE PRACTICAL IMPLEMENTATION!!!!

First of all, deploy the machine and browse to the URL: `http://<machine_ip>/evilshell.php` which would look something like:

![EvilCorp](https://github.com/n00b-0x31/TryHackMe-Writeups/blob/master/OWASP_Top_10/.images/home_page.png)

1. What strange text file is in the website root directory?
* This question asks about an odd file present in the web root directory. Keep in mind it is asking about the `WEB ROOT` directory and not the `ROOT` directory. With the command, `pwd` we get the result as `/var/www/html` which is the `WEB ROOT` directory. All that needs to be done here is just to run the `ls` command to get a list of all the files present in this directory and find the odd file out.

2. How many non-root/non-service/non-daemon users are there?
* To determine the user on any Linux machine the best way is to take a look at the `/etc/passwd` file using the `cat` command. This file consists of all different accounts present on the system including root, service and daemon accounts. But the question is asking about non-root/non-service/non-daemon users on the system. To find such users we must understand the different account types that are present in the `/etc/passwd` file like root, users, services and daemons. Visit [this link] (https://stackoverflow.com/questions/28139377/daemon-and-service-difference) to understand the difference between service and daemon accounts. Moreover, in a passwd file, there are different types of shell assigned to user and many times no shell is assigned, we need to understand that as well. Read about such shell [over here](https://www.howtogeek.com/296637/why-do-some-system-users-have-usrbinfalse-as-their-shell/). Once, we understand all these things we can easily determine the number of non-root/non-service/non-daemon accounts on the system. Refer to [this link](https://computingforgeeks.com/how-to-list-users-in-linux/) to get an idea of various default accounts on the system. 

Hint: If you are still not able to find the answer try various single digit values and then try to correlate the correct value with the passwd file.

3. What user is this app running as? 
* This is a very simple question and can be checked using `whoami` command.

4. What is the user's shell set as?
* We just need to correlate the current user's shell details in the `/etc/passwd` file.

5. What version of Ubuntu is running?
* Another simple question that can be checked by a single command `ls_release -a`.

6. Print out the MOTD.  What favorite beverage is shown?
* This one was a bit confusing question as I did not know what MOTD meant. After some googling, I came to know MOTD stands for 'Message of The Day'. The issue that I faced with this challenge was before Ubuntu 16 the MOTD was saved in `/etc/motd` file which was not present in this system as it is not running on version 16. But on other versions, the files related to MOTD are stored in the directory `/etc/update-motd.d`. We just need to `cat` the files present in this folder and go through them to find the answer to this question.

Hint: Check for a file named `00-header`.

With this the Day 1 Injection Challenge completes and I'll be back again tomorrow when `Broken Authentication` challenge begins!!!
