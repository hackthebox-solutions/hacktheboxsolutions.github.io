![](../img/Jerry Writeup/1_u5geW2CkzLfUj3TlqvmN1A.png)

## Hack The Box — Jerry Write-up

*This is my write-up for the ‘Jerry’ box found on [Hack The Box](https://www.hackthebox.eu).*

*In short: Default credentials and authenticated RCE using metasploit module, Apache was running as root so no privilege escalation required.*

## Part 1: User

The information we start with is that it’s IP is 10.10.10.95, and it runs Windows. Of course, this is hardly enough information! So we use nmap to see what this machine has to offer.

![nmap -sV 10.10.10.95](../img/Jerry Writeup/1_qddW5evThv4QR1uIfYC0XQ.png)

We see that it’s running Apache Tomcat on port 8080, so our first instinct would be to visit the page.

![Apache Tomcat/7.0.88](../img/Jerry Writeup/1_Olb5uXwNM92oCBygfkpQOg.png)

Manager App sounds interesting!

![Authentication Required :(](../img/Jerry Writeup/1_lCfwB6aVsQ_W_cJHb2By7A.png)

Looks like we need login information, or we could just try ‘admin’ and ‘admin’?

![403 Access Denied](../img/Jerry Writeup/1__QUdfV9LTdD2yx9emGZ9vw.png)

Well, something happened.

If we have a read of this, we can see it’s showing us how to set up an account that can access the Manager App, with the username ‘tomcat’ and the password ‘s3cret’. So we tried ‘admin’ and ‘admin’, it didn’t work, but we are presented with new login credentials now, so let’s try them!

However we’re already logged in, so I quickly close Firefox and open it again, this will wipe the cookies as we’re in Private Browsing mode, thus logging us out. We then log back in with the new credentials and…

![Tomcat Web Application Manager](../img/Jerry Writeup/1_EMBW32Y1rr70rGY4WHsopQ.png)

This looks promising! Let’s have a gander at what we can do.

![Interesting names…](../img/Jerry Writeup/1_ajMx8pYJ-_PWiU8gLVvXxg.png)

Some of these names don’t look standard, indicating that this may be our way to getting user access.

![File upload? I smell an exploit…](../img/Jerry Writeup/1_rEKHJmy7itBA_833FyPEgg.png)

Scrolling further down, we see the reason for the strangely named apps. There’s an option to upload a WAR file, which is basically a JAR file for web apps. This sounds like our vulnerability to me, so we go to our best friend Google.

![Looking for some RCE](../img/Jerry Writeup/1_widJ3wepDp1HKwwTXBQGJw.png)

After chucking some random words together, we come across an exploit that makes use of authenticated upload, so the next step is to load up msfconsole

*Side note: The module I’m using is multi/http/tomcat_mgr_upload which uses a POST to /manager/html/upload to get the payload on the server, there is another similar module called multi/http/tomcat_mgr_deploy which uses a PUT to upload the payload, from testing the deploy payload has given limited success, so I’d suggest using the upload payload.*

![We’re gonna need a full-screen terminal this time!](../img/Jerry Writeup/1_qTGGjYVRGkK9QcMzeVGXOA.png)

We set our exploit by typing in use multi/http/tomcat_mgr_upload .

![](../img/Jerry Writeup/1_baGMIwt-NfcU5dJ_LQp0sA.png)

We then configure our exploit with the login credentials, the host, the payload, and the target. Once that is all set up all we need to do type is exploit , fingers-crossed!

![](../img/Jerry Writeup/1_QD-dpSIa949wnaEtgpy6SA.png)

Ta-da!

![](../img/Jerry Writeup/1_D4mlji2I80uQpift-Ad8mA.png)

I drop into a shell, and… what? I guess we’re already System, that was easy!

![2 flags for the price of 1!](../img/Jerry Writeup/1_ZyFkJzALAwvVTg9N5rCPDA.png)

After we navigate to the Administrator’s desktop, we find a directory named flags, which contains a text file called 2 for the price of 1.txt , which contains both of the flags we need to submit.

## Part 2: Root

Well, we already have System, and the root flag, so this section is pretty useless.

*Jerry was my first own on HTB, mainly because it was rated as ‘Piece of cake’ by a large majority of those who owned it. And, whilst it’s pretty easy (Especially because you get System as soon as you get a shell!), we all start somewhere.*

