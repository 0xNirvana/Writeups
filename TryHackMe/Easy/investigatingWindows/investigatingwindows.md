# Investigation Windows w/ PowerShell

In this writeup, I have tried to solve all the question in the [Investigating Windows](https://tryhackme.com/room/investigatingwindows) room on [TryHackMe.com](tryhackme.com).

As this is a Windows machine, the best way to access is via an RDP connection. So, once the machine boots up we can connect to it via RDP and get started with solving all the question.

Now, because we will try to solve all the question via PowerShell, as soon as we gain the RDP access the first thing that we need to do is start PowerShell.

1. **Whats the version and year of the windows machine?**

The answer to this question can be easily found out with the help of the command which provides all the details about the system i.e.
```powershell
systeminfo
```

2. **Which user logged in last?**

For this question, the first thing that we must know is the Event ID that is generated when a user logs in which is 4624. More information can be found at [Ultimate Windows Security](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventID=4624).

Using this event ID, a query can be created to get a list of all the users that logged on to the system.

```powershell
PS C:\Users\Administrator> Get-WinEvent -Computer $env:COMPUTERNAME -FilterHashtable @{Logname='Security';ID=4624} | select @{N='User'; E={$_.Properties[1].Value}}, TimeCreated
```

The issue with this query is that its output contains a lot of entries of username's `SYSTEM` and `Guest`. So, we can filter them out using the query:

```powershell
PS C:\Users\Administrator> Get-WinEvent -Computer $env:COMPUTERNAME -FilterHashtable @{Logname='Security';ID=4672} | where {$_.Properties[1].Value -notmatch "SYSTEM|Guest"} | select @{N='User'; E={$_.Properties[1].Value}}, TimeCreated
```

The first entry in the output of this query is the answer to our question.

3. **When did John log onto the system last?**

The information for any user including their last logon can be easily found using a simple command:
```powershell
net user john
```

4. **What IP does the system connect to when it first starts?**

Details for all the process that are executed when a system starts are can be found in one of the **Registry Entries** i.e. `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"`

And the details for those processes can be retrieved using the command:
```powershell
Get-Item "Registry::HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
```

5. **What two accounts had administrative privileges (other than the Administrator user)?**

Details for accounts with administrative rights can be retrieved easily with the command:
```powershell
net localgroup administrators
```

> This information can be retrieved only by administrators.

6. **Whats the name of the scheduled task that is malicous.**

- List of all the scheduled tasks can be found using the command: `Get-ScheduledTask`
- From this list, at the beginning itself we can find an odd process which is our answer.

7. **What file was the task trying to run daily?**

-   So, we can get details of the process using the command: `Get-ScheduledTaskInfo -TaskName "<scheduled_task_name>"`
- But this does not provide us with the actions that are being performed by the scheduled task. To get that information, we can use the command: `Get-ScheduledTask -TaskName "<scheduled_task_name>" | Select *`
- This query provides all the details of the scheduled task but again not the exact thing that is the command being executed by the task.
- To get the details of the action that are being performed by the scheduled task, the command that can be used is: `(Get-ScheduledTask -TaskName "<scheduled_task_name>").Actions`

8. **What port did this file listen locally for?**

From the details of the actions that are being performed by the suspicious scheduled task. In the arguments part we can see the port on which it was trying to listen.

9. **When did Jenny last logon?**

Again this can be found easily using a simple command that was used for John: `net user jenny`

10. **At what date did the compromise take place?**

It can be assumed that the system got infected when the file suspicious scheduled task was created on the machine. So, we need to get the details of the creation time of the suspicious task file.
- For this, first we can first go to the directory where the file is stored.
	```powershell
	PS C:\Users\Administrator> cd ..\
	PS C:\Users> cd ..\
	PS C:\> cd TMP
	PS C:\TMP> dir
	
	Directory: C:\TMP
	Mode                LastWriteTime         Length Name
	----                -------------         ------ ----
	-a----         3/2/2019   4:37 PM           9673 d.txt
	-a----         3/2/2019   4:37 PM           3389 mim-out.txt
	-a----         3/2/2019   4:37 PM         663552 mim.exe
	-a----         3/2/2019   4:45 PM         176148 moutput.tmp
	-a----         3/2/2019   4:37 PM          36864 nbtscan.exe
	-a----         3/2/2019   4:37 PM          37640 nc.ps1
	-a----         3/2/2019   4:37 PM         381816 p.exe
	-a----         3/2/2019   4:46 PM              0 scan1.tmp
	-a----         3/2/2019   4:46 PM              0 scan2.tmp
	-a----         3/2/2019   4:46 PM              0 scan3.tmp
	-a----         3/2/2019   4:37 PM           7022 schtasks-backdoor.ps1
	-a----         3/2/2019   4:45 PM       40464394 somethingwindows.dmp
	-a----         3/2/2019   4:46 PM          11950 sys.txt
	-a----         3/2/2019   4:37 PM          19998 WMIBackdoor.ps1
	-a----         3/2/2019   4:37 PM         843776 xCmd.exe
	```
	
	Here, it can be seen the date when the files were written but to be sure about the creation time of file, we can use the command: `(Get-ChildItem <suspicious_task_file>).CreationTime`

11. **At what time did Windows first assign special privileges to a new logon?**

The event ID generated when special privileges are assigned to a new logon is 4672. So, we can look for events associated with this event ID around the time when the system got compromised.

> Again, there are going to be a lot many entries for the username "SYSTEM" in the output so we can filter them out
```powershell
PS C:\Users\Administrator> Get-EventLog -LogName Security -After 3/2/2019 -InstanceId 4672 | where {$_.Message -notmatch "SYSTEM"} | select *
```
- This generates a lot many entries but we need to find the specific one when required for answering this question. 

> But even after trying a lot, I was not able to find the exact event. So, looked up in the hint and found an entry with similar entry in the output and that worked as the answer to the question as well.
	> `Get-EventLog -LogName Security -Index 151109 -InstanceId 4672 | select *`

12. **What tool was used to get Windows passwords?**

On exploring the files in the `C:\TMP` directory, we can find one file named as `mim-out.txt` which contains the output of the tool that is being used to extract Windows password.
```powershell
PS C:\TMP> .\mim-out.txt
```
13. **What was the attackers external control and command servers IP?**

Now, if the attacker is somehow able to connect to an external CnC server. Then the two most important things that need to be checked are the `hosts` file and the firewall rules.

The path to the `hosts` file can be found as:
```powershell
PS C:\> Get-ChildItem -Path C:\ -Include hosts -Recurse


    Directory: C:\Windows\System32\drivers\etc


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         3/2/2019   5:31 PM           1236 hosts
```

In the `hosts` file we can see an entry for `google.com` which appears to be suspicious and again that belongs to required CnC server.
14. **What was the extension name of the shell uploaded via the servers website?**

All the files associated with  a Web Server on a Windows server machine are stored at: `C:\inetpub\wwwroot`. So we can go to that directory and check for any suspicious file.

```powershell
PS C:\> cd C:\inetpub\wwwroot
PS C:\inetpub\wwwroot> dir


    Directory: C:\inetpub\wwwroot


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----         3/2/2019   4:37 PM          74853 b.jsp
-a----         3/2/2019   4:37 PM          12572 shell.gif
-a----         3/2/2019   4:37 PM            657 tests.jsp
```

15. **What was the last port the attacker opened?**

Details for the ports that are open or close can be found in the firewall rules. So, we can try to dump the contents of the inbound and outbound firewall rules to look for any odd port for which a rule has been specifically created.
```powershell
PS C:\\Windows> Get-NetFirewallRule -Direction Inbound | select DisplayName, DisplayGroup, @{Name='LocalPort';Expression={($PSItem | Get-NetFirewallPortFilter).LocalPort}}
```

When going through all the rules, we can come see an entry for the *leet* port which is the answer to this question.

16. Check for DNS poisoning, what site was targeted?

The answer to this question was found earlier when we checked the hosts file.

So, with this we completed the entire room with the help of PowerShell only!

## References:

1. TryHackMe-Investigating Windows: https://tryhackme.com/room/investigatingwindows
2. Event ID 4624: https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventID=4624
3. Event ID 4672: https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventID=4672