## OWASP Top 10 
This write-up is going to be based on the [OWASP Top 10](https://tryhackme.com/room/owasptop10) room on TryHackMe. The challenges to this room are going to be released on a daily basis so that for 10 days one can focus on one of the Top 10 vulnerabilities whichever has been released for that day. I will try to add every vulnerability task to this article as soon as I complete it.

### What is OWASP and what are the Top 10???
Open Web Application Security Project or better known as [OWASP](https://owasp.org/) is an online community that produces tools, documentations, technologies and many other things related to web security which can be accessed by anyone and at a cost-free rate. Some of the major OWASP projects that I know are [ZAP](https://www.zaproxy.org/), [Juice Shop](https://github.com/bkimminich/juice-shop), obviously the [Top 10](https://owasp.org/www-project-top-ten/) and many others.

Coming to OWASP Top 10, OWASP releases this document called OWASP Top 10 which consists of most critical security risks to web applications. There are many versions of this document released in the past as well. Going through this document would help any individual to develop a better insight regarding some of the major vulnerabilities on the web and not only how to exploit them but also how to protect yourself from those vulnerabilities.

Coming to this room, it does not require any prerequisite knowledge related to these vulnerabilities but one can easily develop some knowledge regarding them. Moving on let's get started with the `OWASP Top 10` room!

`July 14, 2020`
### [Task 1] Introduction
This task just provides a list of all the vulnerabilities that are going to be covered in this room.

1. [Injection](#task-1-introduction)
2. [Broken Authentication](#task-7-broken-authentication)
3. [Sensitive Data Exposure](#task-9-sensitive-data-exposure-introduction)
4. [XML External Entity](#task-13-xml-external-entity)
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

![EvilCorp](./.images/home_page.png)

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

With this the Day 1 Injection Challenge completes and I'll be back again tomorrow after the 24 hour buffer ends for `Broken Authentication` challenge!!!

`July 15, 2020`

The challenge we are provided with today is related to `Broken Authentication`. The task is very simple and easy to perform. So, let's just begin!

### [Task 7] Broken Authentication
The main purpose of this task was mainly just to let us know what exactly does Broken Authentication means, how can it affect, how it is usually performed and how can you protect yourself from this attack. Some of the major points in this task are:

* Authentication is the basic method that uses username and password to allow users access to the web application. Along with that session cookies are used to track users and their activities.

* Some of the major issues that lead to flaws in the authentication mechanism are:
	* Bruteforce attacks
	* Use of weak passwords
	* Weak session cookies

* When such attacks are performed, an attacker can gain access to the user's personal data including personal files, financial details and others.

* Some steps that can be taken to mitigate this kind of attack are:
	* Setting up an account lockout in case of multiple login failures.
	* Implementing multi-factor authentication.

### [Task 8] Broken Authentication Practical
Moving on to the practical task for Broken Authentication, they have explained about one of the basic flaws related to user authentication database which is if not handled properly we can register a user with the same username and prepend it with a blank space(` `). Doing so, and then logging in with the newly registered username we can gain access to the account of the original user. This can turn into a really serious issue if found in any real-world web application.

Now, we can start with the questions where we just need to register a new user as explained above on the deployed machine at `hhtp://<machine_ip:8888` and get the flag. The login page would look something like this:

![image](./.images/broken_auth_login.png)

1. What is the flag that you found in darren's account?
* For this question, we just simply need to visit go to the user registration page and register with the username as ` darren`. Once registered, we need to log in with the same username and the password used while registering the new user. Doing so will lead us to the user's homepage from where we can get the flag.

2. What is the flag that you found in arthur's account?
* Again we need to perform the same steps as we did in the previous step but with the username as ` arthur`.

With this, we can wrap up the Broken Authentication challenge. This challenge was really simple as there were no steps that were very difficult. 

The next challenge is related to Sensitive Data Exposure, I will add the write-up for the same immediately after the 24-hour buffer ends for that!

`July 16, 2020`

Today, the tasks related to `Sensitive Data Exposure` were released and to be honest they were very easy. A lot of supporting material is provided which makes it further easy to complete the tasks. First, we will go through some important points from all the informative tasks.

### [Task 9] Sensitive Data Exposure (Introduction)
As the task name suggests, it is going to be an intro to today's topic. Sensitive data exposure is nothing but can be explained in simple terms as leakage of some personal or confidential information from a web app. This can range from basic user details such as name, age, contact details to some confidential details like financial credentials, security numbers and others.

### [Task 10] Sensitive Data Exposure (Supporting Material 1)
This task tells us about the two ways in which data is generally stored in a web app which are:
1. Database (eg. MySQL, MariaDB)
2. Stored as files (called as "flat-files")

In this challenge, we are going to work with flat-files. And, also one hint is provided that this flat-file is stored underneath the root directory. 

Along with that, a few commands are provided that can be used to solve this challenge:
1. `file <filename>`: Provides information regarding the file-type. In the context of this task, we need to find a file of file-type SQLite.
2. `sqlite3 <filename>`: Access the SQLite file.
3. SQLite commands:
	* `.tables`: Gives a list of tables present in the database
	* `PRAGMA table_info(<tablename>);`: Provides the details of the columns in the mentioned table
	* `SELECT * FROM <tablename>;`: Print all the content of the table

### [Task 11] Sensitive Data Exposure (Supporting Material 2)
This task talks about password hashes. From the previous task, we understood how we can access the content of a table in the database. But this is a known fact that passwords are never stored as plaintext in any database. And the same case is over here, but to keep things easy, passwords are hashed using MD5 hashes. 

Along with that, they have mentioned a tool called [Crackstation](https://crackstation.net/) which can be used to break this hash and retrieve the original password from the hash.

### [Task 12] Sensitive Data Exposure (Challenge)
Beginning with the actual practical part of this challenge we can move on to the task questions!

1. We need to find a directory where information regarding some sensitive data is leaked.
* For this task, we need to deploy the machine and try to look around the web app to find some sort of information leakage. The first point of information leakage on a website that should come to our mind should be comments in the source code of the web app. We can try going through different web pages and look for some comments. The homepage would look like:

![sense_and_sensitivity](./.images/sensitive_data_exposure.png)

We can check the source code by right-clicking on the webpage and selecting the inspect element option. 
On the homepage, we don't find anything that would prove to be helpful so we can move on to the login page and see that in the source code there is a comment that mentions the directory where changes are meant to be made. And this directory itself is the answer to the first question.

2. Navigate to the directory you found in question one. What file stands out as being likely to contain sensitive data? 
* This task is pretty simple, we just need to navigate to the directory we found in the previous question. Over there, there is only one file that appears to be odd from the rest of the files and obviously, the name of that file is our answer.

Hint: It is a database file.

3. Use the supporting material to access sensitive data. What is the password hash of the admin user?
* We can download that odd file and then try to perform all the database operations explained in task 9 on it. So, let's begin with that:
	* To open the file we can use the command:
		`sqlite3 <filename>`
	* The next task would be to check the tables in the database:
		`.tables`
		
		Output:
		```
		sqlite> .tables
		sessions  users 
		```
	* We can see two tables over there but only one is of our use which is `users`.
	* Now, we need to know in what order data is arranged in the table, so we can use the command:
		`PRAGMA table_info(users);`
		
		Output:
		```
		sqlite> PRAGMA table_info(users);
		0|userID|TEXT|1||1
		1|username|TEXT|1||0
		2|password|TEXT|1||0
		3|admin|INT|1||0
		```
	* From these details, we can see that the third column would be containing the password hashes that we need.
	* To extract the password we need to print the table 'users'. And we can do that by using the query:
		`sqlite> SELECT * FROM users;`
	* From the printed table, we need the hash in the third column that belongs to 'admin' and submit it as the answer for the third question.

4. Crack the hash. What is the admin's plaintext password?
* This question is pretty simple as we just need to copy the hash value paste it at [CrackStation](https://crackstation.net/) and obtain the decrypted password which can be submitted as the password for this question.

5. Login as the admin. What is the flag?
* As the question suggests, we just need to use the cracked password with the username 'admin' and log in. Once, logged in we can see the flag right in front of us!!!

With this, we complete the Sensitive Data Exposure challenge. As I said earlier, this challenge was pretty simple and didn't take much time to solve as well.

Wait till tomorrow, when I'll add the walkthrough XML External Entity challenge!!!

`July 17, 2020`

In today's challenge, it was all related to the basics of the XXE attack. As this series is meant for beginners, the challenge was pretty easy to solve. Just required some payload manipulations.

### [Task 13] XML External Entity
This task broadly enumerates various attacks that an XXE attack can lead to such as Denial of Service(DoS), Server Side Request Forgery(SSRF), Remote Code Execution (RCE) and port scanning. It also describes to types of XXE attacks:

1. In-band attack: Attacker gets an immediate response to XXE payload
2. Out-of-band attack (blind XXE): Attacker has to reflect the output of the attack to some other file or their server

### [Task 14] XML External Entity - eXtensible Markup Language
This task talks about basics on an XML file. Following are some of the major points from the task:

1. XML consists of rules for encoding documents in a human and machine-readable format.
2. It is platform independent.
3. Changes can be made to an XML document without affecting data presentation.
4. XML allows validations using DTD's and Schema ensuring XML document is free from any syntax error.
5. Syntax:
	* Every XML document starts with a XML Prolog
	`<?xml version="1.0" encoding="UTF-8"?>`
	* This determines the XML version and the encoding used, also this line is not compulsory.
	* Every XML document must have a ROOT element without which it would be considered invalid.
	* Every opening tag must be closed with an identical tag with a preceding `/`.
	
		Eg. `<tag>Example</tag>`

For the first time, in this task certain questions are added based on the theory which are given below:

1. Full form of XML
* The answer lies in the task's name itself :P
2. Is it compulsory to have XML prolog in XML documents?
* It's optional
3. Can we validate XML documents against a schema?
* That is how we ensure the XML document is free from any errors.
4. How can we specify XML version and encoding in XML document?
* This is defined at the first line of the XML document and a specific term is given to that line

### [Task 15] XML External Entity - DTD
As the task name suggests, this task provides some brief information on Document Type Definition (DTD) which is used to define the structure and legal elements of an XML file.

DTD Example:
```
<!DOCTYPE note [ <!ELEMENT note (to,from,heading,body)> <!ELEMENT to (#PCDATA)> <!ELEMENT from (#PCDATA)> <!ELEMENT heading (#PCDATA)> <!ELEMENT body (#PCDATA)> ]>
```
Some terms that one must know from above payload:
1. The value next to `!DOCTYPE` is the ROOT element
2. The term `!ELEMENT` is used to define an element such as it's type (eg. #PCDATA which means parsable character data) or the sub-elements which it consists (`<!ELEMENT note (to,from,heading,body)>`)

This task also contains a few questions and answers to them are pretty simple as we just need to add a '!' before the term that is to be defined.

### [Task 16] XML External Entity - XXE Payload
In this task, two different payloads are presented. We can see each one of them and try to understand their sole purpose:

1. ENTITY assignment
```
<!DOCTYPE replace [<!ENTITY name "feast"> ]>
 <userInfo>
  <firstName>falcon</firstName>
  <lastName>&name;</lastName>
 </userInfo>
 ```
* In this payload, the main point that should be focused is the use of an entity for assignment purposes. It can understood as at the beginning of the payload the entity name has been defined as the value "feast". Later, the same value is used for the value of `lastName` using the term `&name;`.

2. Payload to read system files
```
<?xml version="1.0"?>
<!DOCTYPE root [<!ENTITY read SYSTEM 'file:///etc/passwd'>]>
<root>&read;</root>
```
* The main purpose of using this payload is to access system files. This is done by defining the path of the system file for a read action. We will be using this payload for solving the challenges in the next task.

### [Task 17] XML External Entity - Exploiting
To solve all the questions in this task we need to first deploy the machine and browse to `http://<machine_ip>` which would look something like:

![XXE_homepage](./.images/XML_homepage.png)

1. Try to display your own name using any payload.
* This question is pretty simple as we just need to print our name using XXE. For this, we can use the first payload and simply change various values and test the payload like values of `name'`, `firstName` or `lastName`.

2. See if you can read the /etc/passwd
* This task is also really simple and we can use the second payload from the previous task and just run it on the deployed website.

3. What is the name of the user in /etc/passwd
* This could be found out at the last line of the output from the previous question.

4. Where is falcon's SSH key located?
* For this question, we first need to know where the SSH key is stored on a Linux machine. After some googling, we can find the exact location and file in which this key is stored and that is `/home/<username>/.ssh/id_rsa`. We can change the username value and replace `/etc/passwd` in the second payload with this new path. And this new path itself is the answer to the question.

5. What are the first 18 characters for falcon's private key
* Once we execute the payload that we created in the last task, we can get falcon's SSH key and from the same key, we need to take out the first 18 characters from the key and use them as the answer to the question.
P.S. Don't make a silly mistake by copying those 18 characters from `-----BEGIN RSA PRIVATE KEY----- ` as the actual key begins after this!!!

So, one more challenge is over and I'll be back again tomorrow with the write-up for Broken Access Control!!!

P.S. As this is a live challenge I'll be adding the latest challenge write-up only 24 hours after it goes live!!!
