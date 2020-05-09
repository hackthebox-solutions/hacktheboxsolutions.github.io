![](../img/Tenten Writeup/1_Huf6GSeyRAL4uafwMUnVXg.png)

---

**Tools Used: \***NMAP
WPScan
Steghide
John\*

**Difficulty: 5/10**

**Network Enumeration
**Let’s start with a simple NMAP scan.

![](../img/Tenten Writeup/1_3MUMRukzq0t1r-H4f7vGaw.png)

We can see from the NMAP scan we can see that ports 22 (SSH) and 80 (HTTP) are open.

![](../img/Tenten Writeup/1_39D4AwwFb_eOCmjp0g7djw.png)

After running a more intense scan on port 80, a few things stick out. We can see Apache 2.4.18 and WordPress 4.7.3. After searching on Exploit-DB, there are no exploits for either of these applications.

![](../img/Tenten Writeup/1_klIKwAVecaodYFMHNTIAJw.png)

After browsing to port 80, we can see the WordPress site running.

![](../img/Tenten Writeup/1_GYAr7v4Ac72asD3ceOthIQ.png)

The first thing to do on a WordPress site is to run wpscan for any vulnerabilities.

![](../img/Tenten Writeup/1_viBP6-PrQGfke1O7d9qOlA.png)

WPScan results returned a vulnerability finding regarding the job manager.

![](../img/Tenten Writeup/1_peAl0T7wvhqm8RUVANKOnw.png)

The second reference links of the exploit findings give us a website with a PHP script for exploitation. In the script, it’s calling for two inputs website and file name. We already have the site we now need to find the file name.

![](../img/Tenten Writeup/1_Hmr13EY5qfu8VWxzemL1OQ.png)

If we go to the apply link on the jobs page title says Pen Tester.

![](../img/Tenten Writeup/1_azENi261z9zkA713Rof7aA.png)

If we change the number, we get a different job application. Let’s see what all of the titles say. We can do this with a simple bash script.

> for i in $(seq 1 20); do echo -n “$i: “; curl -s [http://10.10.10.10/index.php/jobs/apply/\$i/](http://10.10.10.10/index.php/jobs/apply/$i/) | grep ‘<h1 class=”entry-title”>’; done

![](../img/Tenten Writeup/1_FPO3k1sn9H8p8gDwgUYd6g.png)

The results look typical except for line 13 that says “HackerAccessGranted.”

We need to make a few changes to our script.

```
for year in range(2017,2018):
    for i in range(1,13):
        for extension in {'php','html','pdf','png','gif','jpg','jpeg'}:
```

![](../img/Tenten Writeup/1_L8Bg1AUHo_DHJiHjcvS-qQ.png)

After running the script, we get a file name returned. HackerAccessGranted.jpg

![](../img/Tenten Writeup/1_HwZFWWOOELM-9zK98zc-wA.png)

Looking at the photo, I don’t see anything unusual and being a CTF machine the first thing that comes to my mind is steganography.

![](../img/Tenten Writeup/1_yBfbse-Z3ST2C6hV9NuljA.png)

Using steghide to extract the hidden content we see there is an RSA Private key. Most likely this will be used to ssh into the server, however, we need to figure out the password for the key.

![](../img/Tenten Writeup/1_I2k_PCxixiT-bBY3VMudTg.png)

To brute force the key’s password we need sshng2john python script to get the hash in john format.

![](../img/Tenten Writeup/1_lNf8yM_j5ykmIsAfiFv_Hw.png)

![](../img/Tenten Writeup/1_KQ9aKdepeJs5Il7P1OU7iQ.png)

Running the hash through john, we find out the password is “superpassword”

![](../img/Tenten Writeup/1_y5KfbY0nPlhJ_rzmMi_4_g.png)

I tried using the key to SSH into the server, and it was not working. Looking back at the WPScan I remember seeing a username discovered.

![](../img/Tenten Writeup/1_P0pRYUTopN1y8x0XfQPxcw.png)

Using the user “takis,” the RSA key, and the passphrase we now have user-level SSH into tenten.

![user.txt](../img/Tenten Writeup/1_xklETMQ644h-VopA-f3PNQ.png)

We can read user.txt.

Privilege escalation
Now that we user access we need to elevate our permissions to root. Let’s start with getting system information.

> takis@tenten:~\$ cat /etc/issue
> Ubuntu 16.04.2 LTS \n \l

![](../img/Tenten Writeup/1_crhOsGjHpU822hNPL4pFNw.png)

Escalating to root shows that we have access to a file called “/bin/fuckin.” We need to find out what in this file.

![](../img/Tenten Writeup/1_whQdWTdi2AWwLNAF1Dz81Q.png)

fuckin seems to be a batch script that contains arguments that we can pass on.

![](../img/Tenten Writeup/1_cq97uQWm_TQtBLOQg_OOTg.png)

Adding an argument after the file while running it as sudo allows us to run commands as root.

![](../img/Tenten Writeup/1_YobiubxriG5EfVLVr2o6nQ.png)

Adding bash to the first argument gives us root shell.

![](../img/Tenten Writeup/1_G5RB2nOvXYaoXtXxNL2q8Q.png)

As root, we can view root.txt
