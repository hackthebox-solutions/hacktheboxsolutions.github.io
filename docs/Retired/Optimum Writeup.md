![](../img/Optimum Writeup/1_Eq2z6OoROOZgnfEsy_Tivw.png)

## Summary

This is a

## Recon

The first thing I do is run an nmap on the target to see which ports are open.

![](../img/Optimum Writeup/1_hlcfn1cVvreqQ__hmJNu5w.png)

This box only has one port open, and it seems to be running HttpFileServer httpd 2.3. Lets take a look in searchsploit and see if we find any known vulnerabilities.

![](../img/Optimum Writeup/1_iUR6RbIQXLMw3YMvm8mosQ.png)

We see a remote code execution exploit for our exact version, lets take a look.

![](../img/Optimum Writeup/1__xBszlA69yJPRd8p3zVa4Q.png)

For this RCE exploit to work, we need nc.exe to be reachable in our web server. Lets fire out our listener, and copy over the executable to the required location.

![](../img/Optimum Writeup/1_vlARMXQlAPGzcqdXho_dcg.png)

![](../img/Optimum Writeup/1_BPbT0j2NwlYC8hMBxwSlxw.png)

![](../img/Optimum Writeup/1_WwrV7ZXycvdXlRu105kwmg.png)

Now that we have met the pre-exploit requirements, lets download and run the exploit. It could take several attempts, so if you do not get a shell on your listener the first time, try it again.

![](../img/Optimum Writeup/1_w7aVfpU6MGsEyj85IaO3sQ.png)

![](../img/Optimum Writeup/1_XmbrPnkfGDf9F2_cRaENgg.png)

## Foothold/ Local Enumeration

Now that we got a shell, lets run the command systeminfo to enumerate this box.

![](../img/Optimum Writeup/1_u9-X81HltZgG8M3x92Hrzg.png)

There is a great tool in Kali called windows-exploit-suggester which we can use, now that we have the data from systeminfo . To utilize this tool we need to save the output of systeminfo and save it to a text file. You might also have to update the tool like me, which I did below.

![](../img/Optimum Writeup/1_wGBvs3ukR-v4TlGrUSqtzQ.png)

Now that the tool is updated, we can run the tool and see some suggested exploits.

![](../img/Optimum Writeup/1_vnlWXEpgOQpNzVW3Vj66WQ.png)

## Privilege Escalation

While this tool gave us some great suggestions, i found an easier exploit while looking around on Google.

![](../img/Optimum Writeup/1_twaXqTyLYQl9EUMAP_jOUQ.png)

![](../img/Optimum Writeup/1_F28muNENZxuxJyRQnZG-qw.png)

I found this executable that will elevate our privileges on this box. To get this executable on the target box, check out the Privilege Escalation section of my ‘Access’ walkthrough for a guide to build a powershell wget script.

![](../img/Optimum Writeup/1_NaNFdioVmf1psIrBBHySEw.png)

Now that we have the our executable on our target, we can run it to get nt authority\system shell.

![](../img/Optimum Writeup/1_VViF6nRlSBd3UUMVhaSzjA.png)

Pwned!!!

Lets go get our flags.

![](../img/Optimum Writeup/1_M1jM8d6MKCIx8m-Ll-BrtA.png)

![](../img/Optimum Writeup/1_PrS6ptM0eUH_prnuHsK9aA.gif)