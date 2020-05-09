## HackTheBox Writeup — Beep

![Pic Credits — Ippsec](../img/Beep Writeup/1_rxghvaZ377EBeGkxEI6SfQ.png)

### NMAP Results

So we run NMAP against the target 10.10.10.7 and get

![](../img/Beep Writeup/1_OXFpzS5FpeRV95uWOf_llQ.png)

### Web Services

We run the IP in the browser , but it redirects us to HTTPS websites

![](../img/Beep Writeup/1_-31vncEDjGGfVqmtKq7cFA.png)

We see that its running Elastix , running Gobuster on it , we get

![](../img/Beep Writeup/1_mYL0CW0KRoHDhdelSNwaVA.png)

Running searchsploit for elastix , we get

![](../img/Beep Writeup/1_Jte8eyXiK8PBlECC5YZeLw.png)

We get few exploits , the one which looks interesting is the LFI and Remote Code Execution one , let’s try the LFI one

![](../img/Beep Writeup/1_MkNoWaLzY2L8SnXhLTdraA.png)

We see it gave us the location of the LFI , which is the /vtigercrm directory , which we saw in the gobuster results too , let’s copy it and see the result

![](../img/Beep Writeup/1_-oEumlZZc-kpmFEive762A.png)

We get something , but its hard to read this rendered file , so we view the source code

![](../img/Beep Writeup/1_1VyhV3KJl5kXYvi4GMuhAQ.png)

We get many things like users and password for FreePBX which can be accessed through the /admin

![](../img/Beep Writeup/1_lHdAnLv0XB6I-0i7jD6GoA.png)

We get prompted for username and password , so we will enter the creds for admin as we got before and hit OK

![](../img/Beep Writeup/1_mQujPsL0dmS18YOjhWSO-Q.png)

We got successfully logged in and see that its running FreePBX version 2.8.1.4

I tried many exploits for this , but it didnt worked for me , so as we saw that ssh is open and we have password for admin from the config file we got , let’s try to connect to root through it

![](../img/Beep Writeup/1_gdr-LzUyPw_hxDBDW3-H1Q.png)

So we got it as root , it was a proper guess work here , coz I have encountered same thing on some other boxes too as well

Let’s get the user flag which is located at home folder of the user as user.txt

![](../img/Beep Writeup/1_j7Ey_H2UVTvDR69FMSD2QA.png)

The root flag is located at the root folder as root.txt

![](../img/Beep Writeup/1_HPNSyM1l7K9pQdSCx5V87Q.png)

That’s the box , really very CTF type from the perspective I solved this