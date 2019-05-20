---
id: 465
title: 'BeagleBone: Making a Home Media Server'
date: 2012-05-24T01:07:36+00:00
author: Everett
layout: post
guid: http://everettsprojects.com/?p=465
permalink: /2012/05/24/beaglebone-making-a-home-media-server/
twitter_cards_summary_img_size:
  - 'a:6:{i:0;i:929;i:1;i:518;i:2;i:3;i:3;s:24:"width="929" height="518"";s:4:"bits";i:8;s:4:"mime";s:9:"image/png";}'
dsq_thread_id:
  - "6140711662"
image: /wp-content/uploads/2012/05/rtorrent-startup-script-672x372.png
categories:
  - BeagleBone
  - Electronics
  - Linux
tags:
  - ARM
  - rtorrent
  - rutorrent
  - samba
  - Ubuntu
comments: true
---
There are plenty of products available to the person who wants a functioning NAS out of the box, though I&#8217;ve never really been that type. By using a versatile board like the BeagleBone as a home media server, I can make a project that is more than a simple networked storage solution. It also affords me the opportunity to learn about administration of a Linux server. While I could teach myself these skills by implementing a home media server using an old desktop, the amount of electricity consumed would be at least an order of magnitude higher and in any case my old desktop recently gave up the ghost. The information contained here is specifically intended for use on a BeagleBone, though I wouldn&#8217;t be the least bit surprised if it was useful to someone trying to achieve the same effect with a different platform. It is also important to not that I accept no liability for damages or issues that occur as a result of following my directions either on a BeagleBone or other hardware. I am very sorry if such an event should take place however, and would appreciate knowing about it so that I could correct this guide asap.

This guide is broken into major steps for the convenience of anyone wishing to follow it:

  1. [Installing Ubuntu and some basic configuration](#installingUbuntu)
  2. [Locking down SSH](#sshLockdown)
  3. [Getting rtorrent and rutorrent running](#rtorrent)
  4. [Installing and configuring Samba](#samba)
  5. [Updating and maintaining the system](#maintenance)

<div id="installingUbuntu"></div>
<p style="text-align:center;">
  *****
</p>


### Installing Ubuntu and some basic configuration

To start it&#8217;s necessary to get your preferred Linux distribution running on the BeagleBone. I chose Ubuntu mainly because I found an easy and ready to install image, though the fact that it is compiled to take advantage of the hard float capabilities in this arm processor was also a factor. The following instructions were up to date when I utilized them, though it&#8217;s entirely possible that a newer image has been created in the meantime and you should use that one if possible. You will also need a microSD card to write the image to (I used a 4GB card, though a 2GB card or greater should work).

Credit goes to <a href="http://elinux.org/BeagleBoardUbuntu#Demo_Image">http://elinux.org/BeagleBoardUbuntu#Demo_Image</a> as the basis for this portion of my guide.

The first thing we need to do is download the operating system image that we will write to the microSD card:

<blockquote>
  wget http://rcn-ee.net/deb/rootfs/precise/ubuntu-12.04-r1-minimal-armhf.tar.xz
</blockquote>


This image needs to be unpacked before we write it to the SD card:<em><br /> </em>

<blockquote>
  tar xJf ubuntu-12.04-r1-minimal-armhf.tar.xz<br /> cd ubuntu-12.04-r1-minimal-armhf
</blockquote>

We need to know where to install this image , and even though it is likely /dev/mmcblk0 we should check anyway:

<blockquote>
  sudo ./setup_sdcard.sh &#8211;probe-mmc
</blockquote>

In the output a line like <strong>Disk /dev/mmcblk0: 3957 MB, 3957325824 bytes </strong>should be seen. If there is only one line starting with <strong>Disk /dev/mmcblk</strong>&#8230; then that is the SD card we want, and that&#8217;s the location you should use. If there are more than one of these <strong>/dev/mmcblk</strong> lines, then you must figure out which one belongs to the SD card you want to write to, otherwise you may overwrite something important.

Having figured out where the SD card is mounted, we will run the script to write the contents of our image to it:

<blockquote>
  sudo ./setup_sdcard.sh &#8211;mmc /dev/mmcblk0 &#8211;uboot bone
</blockquote>

Where <strong>/dev/mmcblk0</strong> may be something else if you found the SD card to be mounted somewhere else in the previous step.<br /> At this point you only have to insert the microSD card and plug it into the BeagleBone to get started. Because the board lacks a way to hook up a display it is easiest to insert an ethernet cable and remotely SSH into it with <strong>the user &#8220;ubuntu&#8221; and the password &#8220;temppwd&#8221;</strong>

<blockquote>
  ssh ubuntu@_Local IP Address_
</blockquote>

I have managed to use the DHCP reservation functionality on my home router to ensure that the BeagleBone has a fixed local IP address, and I strongly encourage you to do the same if possible. Because this process varies by router manufacturer and model, I cannot offer much guidance in this regard. <a href="http://lifehacker.com/5822605/how-to-set-up-dhcp-reservations-so-you-never-have-to-check-an-ip-address-again">This guide</a> may be of some help.

Our first step after logging in should be to change the password for this account:

<blockquote>
  passwd
</blockquote>

This will ask for the current password, and the one you wish replace it with twice. The next two steps will create a new user account with a better name (just replace _username_ with your preference) and give it administrative privileges. These steps are cosmetic, and are unnecessary if you just wish to use the account &#8220;ubuntu&#8221;.

<blockquote>
  sudo adduser _username_
  sudo usermod -aG admin _username_
</blockquote>

The next two commands will allow us to change the host name for the BeagleBone to something other than &#8220;omap&#8221; and are also optional as they are purely cosmetic.

<blockquote>
  sudo nano /etc/hostname
</blockquote>

You should change the first line of this file to whatever you&#8217;d like as a new host name (don&#8217;t use spaces) and then press CTRL-o to save the changes and CTRL-x to exit. We will also need to change the following file:

<blockquote>
  sudo nano /etc/hosts
</blockquote>

The word <strong>omap</strong> in the second line of this file should be replaced with the same host name we just used.

I encountered perl locale errors when I tried doing various things later on, which may still be an issue. To fix them you want to check that <strong>/etc/default/locale</strong> contains a few things:

<blockquote>
  sudo nano /etc/default/locale
</blockquote>

You should find the following lines within, though they do not necessarily need to be US english:

{% highlight plaintext %}
LANG=en_US.UTF-8
LANGUAGE=en_US.UTF-8:en
LC_ALL=en_US.UTF-8
{% endhighlight %}

If any of these lines are not present, then you should add them (substituting in another language pack such as en_GB if you&#8217;re so inclined.)

Before proceeding, it is also a good idea to make sure all of the packages on your system are up to date:

<blockquote>
  sudo apt-get update<br /> sudo apt-get upgrade
</blockquote>

<blockquote>
  sudo reboot
</blockquote>

<div id="sshLockdown"></div>
<p style="text-align:center;">
  *****
</p>

### Locking down SSH

Credit goes to <a href="http://www.debian-administration.org/articles/530">http://www.debian-administration.org/articles/530</a> as the basis for this portion of my guide.<br /> We need to generate a set of public and private keys on the computer you wish to SSH into the BeagleBone from. It is important to make sure you are running this locally on the client computer, not through SSH on the BeagleBone:

<blockquote>
  ssh-keygen
</blockquote>

You will then be prompted for a password to protect the key we just generated. This password is not transmitted in any way to the system were are using SSH to access, but rather to decrypt the key on your local machine. If you leave the password blank it will not encrypt this key and make it so that anyone with the right file permissions can see it.<br /> Now we want to install the key on the BeagleBone:

<blockquote>
  ssh-copy-id -i .ssh/id_rsa.pub _username_@_Local IP adress_
</blockquote>

If this was successful, we should be able to SSH into the BeagleBone without entering a password.<br /> We should then check that we only installed the key we intended to:

<blockquote>
  nano ~/.ssh/authorized_keys
</blockquote>

You should see only one line in the file.

Next, it is a good idea to disable password authentication and limit the users who can access the board via SSH.<br /> You <strong>do not</strong> want to do this by disabling password authentication for the chosen account as outlined in the debian-administration.org article; this runs the risk of breaking your ability to use sudo and can leave you without root access. I may or may not have made this error first hand. It&#8217;s not fun. We achieve the desired effect by editing <strong>/etc/ssh/sshd_config</strong> .

<blockquote>
    sudo nano /etc/ssh/sshd_config
</blockquote>

First things first, it&#8217;s never a bad idea to disable root login. This isn&#8217;t really necessary on an Ubuntu system since there is no functioning root password and everything is done using sudo, but we&#8217;re better safe than sorry. Find the line beginning with <strong>PermitRootLogin</strong> and change it to <strong>no</strong>:

{% highlight plaintext %}
  PermitRootLogin no
{% endhighlight %}

We also want to disable password authentication by finding the line <strong>#PasswordAuthentication yes</strong>, changing it to <strong>no</strong>, and uncommenting it by removing the <strong>#</strong>:

{% highlight plaintext %}
  PasswordAuthentication no
{% endhighlight %}

Because we do not need X11-forwarding for our purposes you may also wish to change that line to:

{% highlight plaintext %}
  X11Forwarding no
{% endhighlight %}

And to limit the users allowed to SSH into the BeagleBone we want to add the following line to the end of the file, using the username we created earlier in the place of _username_:


{% highlight plaintext %}
  AllowUsers _username_
{% endhighlight %}


Finally, to finish our lockdown of SSH, we need to restart it so that the changes can take effect:


<blockquote>
    sudo service ssh restart

</blockquote>

<div id="rtorrent"></div>
<p style="text-align:center;">
  *****
</p>

### Getting rtorrent and rutorrent running

This portion of my guide has been mainly adapted from <a href="http://forums.rutorrent.org/index.php?topic=256.0">http://forums.rutorrent.org/index.php?topic=256.0</a>.


First we want to install a large number of packages:


<blockquote>
    sudo apt-get install apache2 apache2.2-common apache2-utils autoconf automake autotools-dev binutils build-essential bzip2 ca-certificates comerr-dev cpp cpp-4.6 dpkg-dev file g++ g++-4.6 gawk gcc gcc-4.6 libapache2-mod-php5 libapache2-mod-scgi libapr1 libaprutil1 libc6-dev libcppunit-dev libcurl3 libcurl4-openssl-dev libexpat1 libidn11 libidn11-dev libkdb5-6 libgssrpc4 libkrb5-dev libmagic1 libncurses5 libncurses5-dev libneon27 libpcre3 libpq5 libsigc++-2.0-dev libsqlite0 libsqlite3-0 libssl-dev libstdc++6-4.6-dev libsvn1 libtool libxml2 linux-libc-dev lynx m4 make mime-support ntp ntpdate openssl patch perl perl-modules php5 php5-cgi php5-cli php5-common php5-curl php5-dev php5-geoip php5-sqlite php5-xmlrpc pkg-config python-scgi screen sqlite ssl-cert subversion ucf unrar zlib1g-dev pkg-config unzip htop screen libwww-perl curl

</blockquote>

Several of these packages are probably already installed, though it does not hurt to make sure. Some of the packages in this long list have been updated to newer versions since the guide I have adapted thus from was written. If any appreciable length of time has passed since I wrote this, then you are well advised to check if any of these packages need to have their version numbers changed. If this is the case, then apt-get is likely to spit out some error messages about certain packages being missing. The specific packages I updated were: <strong>cpp-4.6, g++-4.6, gcc-4.6, libstdc++6-4.6-dev, libkdb5-6, and libneon27</strong>. Here&#8217;s a quick way to check the version numbers for <a href="http://packages.ubuntu.com/">packages in the ubuntu repository online</a>.


Having everything we need, our next step is to configure apache:


<blockquote>
    a2enmod ssl<br /> a2enmod auth_digest<br /> a2enmod scgi

</blockquote>

We need to make sure that apache has SCGI support enabled so that the rutorrent webui will work:


<blockquote>
    sudo nano /etc/apache2/apache2.conf

</blockquote>

You then need to paste the following at the end of the file:


{% highlight plaintext %}
  SCGIMount /RPC2 127.0.0.1:5000
  servername localhost
{% endhighlight %}


To make sure everything we&#8217;ve done takes effect it is a good idea to restart the server:


<blockquote>
    sudo reboot

</blockquote>

To make sure everything is working, on your client machine type the local ip address assigned to your BeagleBone into the address bar of your browser:


<blockquote>
    http:// < Local IP Address>

</blockquote>

You should see the following:


<a href="/wp-content/uploads/2012/05/working-apache.png"><img class="aligncenter size-medium wp-image-522" title="working apache" src="/wp-content/uploads/2012/05/working-apache.png?w=300" alt="The landing page that indicates apache is working" width="300" height="167" srcset="/wp-content/uploads/2012/05/working-apache.png 929w, /wp-content/uploads/2012/05/working-apache-300x167.png 300w, /wp-content/uploads/2012/05/working-apache-672x372.png 672w" sizes="(max-width: 300px) 100vw, 300px" /></a>


Because our rutorrent front end to rtorrent will be password protected, we need to have HTTPS functionality eneabled. To achieve this we need an SSL certificate. This process will ask for a lot of information which you can fill in however you see fit, though it&#8217;s a good idea to use the domain name your BeagleBone will be connected to if you have one:


<blockquote>
    openssl req $@ -new -x509 -days 365 -nodes -out /etc/apache2/apache.pem -keyout /etc/apache2/apache.pem<br /> chmod 600 /etc/apache2/apache.pem

</blockquote>

This is a self signed certificate, meaning your browser will probably spit out a warning the first time you connect. Just ignore the warning and store the exception, and this won&#8217;t happen again. Our next step is to protect our apache webserver with a username and password:


<blockquote>
    sudo htdigest -c /etc/apache2/passwords gods _webusername_

</blockquote>

This username, _webusername_, and password can be whatever you like. It can even be the same user and password we used earlier when setting sup the system. I personally decided to use a different username and password because it offers a slight security advantage in that if someone figures out the password to our rutorrent and apache setup, they still don&#8217;t have the password for root privileges through the operating system account we made earlier. It is unlikely that this scenario would ever happen since we made access through ssh only possible using key authentication, though it&#8217;s not much of a hassle for a little added security (Besides, I know you&#8217;ll just save the webusername and password in your browser anyway).


We also need to configure apache using the <strong>/etc/apache2/sites-available/default</strong> file:


<blockquote>
    sudo nano /etc/apache2/sites-available/default

</blockquote>

You want to replace the contents of this file with the following, where the two instances of _Local IP address_ are replaced by the address of your BeagleBone on the local network:


{% highlight xml %}
  <VirtualHost *:80>
    ServerAdmin webmaster@localhost

    DocumentRoot /var/www/
    <Directory />
        Options FollowSymLinks
        AllowOverride None
    </Directory>
    <Directory /var/www/>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride None
        Order allow,deny
        allow from all
    </Directory>

    ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
    <Directory "/usr/lib/cgi-bin">
        AllowOverride None
        Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
        Order allow,deny
        Allow from all
    </Directory>

    ErrorLog /var/log/apache2/error.log

    # Possible values include: debug, info, notice, warn, error, crit,
    # alert, emerg.
    LogLevel warn

    CustomLog /var/log/apache2/access.log combined

    Alias /doc/ "/usr/share/doc/"
    <Directory "/usr/share/doc/">
        Options Indexes MultiViews FollowSymLinks
        AllowOverride None
        Order deny,allow
        Deny from all
        Allow from 127.0.0.0/255.0.0.0 ::1/128
    </Directory>

    <Location /rutorrent>
        AuthType Digest
        AuthName "gods"
        AuthDigestDomain /var/www/rutorrent/ http://<Local IP Address>/rutorrent

        AuthDigestProvider file
        AuthUserFile /etc/apache2/passwords
        Require valid-user
        SetEnv R_ENV "/var/www/rutorrent"
    </Location>

</VirtualHost>

<VirtualHost *:443>
    ServerAdmin webmaster@localhost

    SSLEngine on
    SSLCertificateFile /etc/apache2/apache.pem

    DocumentRoot /var/www/
    <Directory />
        Options FollowSymLinks
        AllowOverride None
    </Directory>
    <Directory /var/www/>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride None
        Order allow,deny
        allow from all
    </Directory>

    ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
    <Directory "/usr/lib/cgi-bin">
        AllowOverride None
        Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
        Order allow,deny
        Allow from all
    </Directory>

    ErrorLog /var/log/apache2/error.log

    # Possible values include: debug, info, notice, warn, error, crit,
    # alert, emerg.
    LogLevel warn

    CustomLog /var/log/apache2/access.log combined

    Alias /doc/ "/usr/share/doc/"
    <Directory "/usr/share/doc/">
        Options Indexes MultiViews FollowSymLinks
        AllowOverride None
        Order deny,allow
        Deny from all
        Allow from 127.0.0.0/255.0.0.0 ::1/128
    </Directory>
    <Location /rutorrent>
        AuthType Digest
        AuthName "gods"
        AuthDigestDomain /var/www/rutorrent/ http://<Local IP Address>/rutorrent

        AuthDigestProvider file
        AuthUserFile /etc/apache2/passwords
        Require valid-user
        SetEnv R_ENV "/var/www/rutorrent"
    </Location>
</VirtualHost>
{% endhighlight %}

We then want to run the following to get apache running https:


<blockquote>
    sudo a2ensite default-ssl<br /> sudo /etc/init.d/apache2 reload

</blockquote>

If everything worked as intended, then going to <strong>https://< Local IP Address></strong> should show us the same page we saw earlier.


Unlike the guide I adapted these instructions from, I have decided not to install the Webmin configuration utilities for a couple of reasons. The first is that I wanted this project to help develop my skills as a Linux administrator, and a graphical GUI to change everything does not really fit that goal. The second reason is that the BeagleBone is not a powerful computer, and so I would prefer not to weigh it down with things that are not absolutely necessary.


Now that we have apache up and running with all the necessary bells and whistles, we can proceed to install and configure rtorrent and the rutorrent webui. At the time the guide I used as my starting point was written, the version of rtorrent in the Ubuntu repositories wasn&#8217;t complied with xmlrpc support, which was needed for rutorrent to work. This has long been fixed, and so you can probably just install the packages <strong>libxmlrpc-core-c3-dev</strong> and <strong>rtorrent</strong>. I can&#8217;t offer any guidance in this regard because I decided to compile the latest versions of these packages from source, mostly because I could. The compilation process will take a fair amount of time; likely more than an hour.


First things first, we need the sources for each of these packages:


<blockquote>
    cd ~/
    mkdir source
    cd source
    svn co https://xmlrpc-c.svn.sourceforge.net/svnroot/xmlrpc-c/advanced/ xmlrpc-c
    wget http://libtorrent.rakshasa.no/downloads/libtorrent-0.13.2.tar.gz
    wget http://libtorrent.rakshasa.no/downloads/rtorrent-0.9.2.tar.gz
    tar -xvzf libtorrent-0.13.2.tar.gz<br /> tar -xvzf rtorrent-0.9.2.tar.gz
    rm \*.tar.gz
</blockquote>

This simply downloads the sources, unpacks the archives and deletes the archive files once we have. These packages may be updated to newer versions by the time you read this, and you can change version numbers accordingly.


The first package we need to build is xmlrpc-c:


<blockquote>
    cd xmlrpc-c<br /> ./configure &#8211;disable-cplusplus<br /> make<br /> sudo make install

</blockquote>

Once this has completed we will do the same for libtorrent, the backend of rtorrent:


<blockquote>
    cd ../libtorrent-0.13.2<br /> ./autogen.sh<br /> ./configure<br /> make<br /> sudo make install

</blockquote>

And finally, we will compile rtorrent itself:


<blockquote>
    cd ../rtorrent-0.9.2<br /> ./autogen.sh<br /> ./configure &#8211;with-xmlrpc-c<br /> make<br /> sudo make install


    sudo ldconfig

</blockquote>

Next we need an rtorrent configuration file, which we will save as ~/.rtorrent.rc:


<blockquote>
    nano ~/.rtorrent.rc

</blockquote>

and replace any contents with the following:


{% highlight plaintext %}
# This is an example resource file for rTorrent. Copy to
# ~/.rtorrent.rc and enable/modify the options as needed. Remember to
# uncomment the options you wish to enable.
#
# Based on original .rtorrent.rc file from http://libtorrent.rakshasa.no/
# Modified by Lemonberry for rtGui http://rtgui.googlecode.com/
#
# This assumes the following directory structure:
#
# /Torrents/Downloading - temporaray location for torrents while downloading (see "directory")
# /Torrents/Complete - Torrents are moved here when complete (see "on_finished")
# /Torrents/TorrentFiles/Auto - The 'autoload' directory for rtorrent to use.  Place a file
#           in here, and rtorrent loads it #automatically.  (see "schedule = watch_directory")
# /Torrents/Downloading/rtorrent.session - for storing rtorrent session information
#

# Maximum and minimum number of peers to connect to per torrent.
#min_peers = 40
max_peers = 100

# Same as above but for seeding completed torrents (-1 = same as downloading)
min_peers_seed = -1
max_peers_seed = -1

# Maximum number of simultanious uploads per torrent.
max_uploads = 10

# Global upload and download rate in KiB. "0" for unlimited.
download_rate = 0
upload_rate = 0

# Default directory to save the downloaded torrents.
directory = _directory torrents will download to by default_

# Default session directory. Make sure you don't run multiple instance
# of rtorrent using the same session directory. Perhaps using a
# relative path? (We disregard this because of our startup script later)
session = /home/_username_/.session

# Watch a directory for new torrents, and stop those that have been
# deleted.
#schedule = watch_directory,5,5,load_start=/home/downloads/_username_/watch/*.torrent
#schedule = untied_directory,5,5,stop_untied=

# Close torrents when diskspace is low. */
schedule = low_diskspace,5,60,close_low_diskspace=100M

# Stop torrents when reaching upload ratio in percent,
# when also reaching total upload in bytes, or when
# reaching final upload ratio in percent.
# example: stop at ratio 2.0 with at least 200 MB uploaded, or else ratio 20.0
#schedule = ratio,60,60,stop_on_ratio=200,200M,2000

# When the torrent finishes, it executes "mv -n  ~/Download/"
# and then sets the destination directory to "~/Download/". (0.7.7+)
# on_finished = move_complete,"execute=mv,-u,$d.get_base_path=,/home/downloads/_username_/complete/ ;d.set_directory=/home/downloads/_username_/complete/"

# The ip address reported to the tracker.
#ip = 127.0.0.1
#ip = rakshasa.no

# The ip address the listening socket and outgoing connections is
# bound to.
#bind = 127.0.0.1
#bind = rakshasa.no

# Port range to use for listening.
port_range = 55995-56000

# Start opening ports at a random position within the port range.
#port_random = yes

scgi_port = 127.0.0.1:5000

# Check hash for finished torrents. Might be usefull until the bug is
# fixed that causes lack of diskspace not to be properly reported.
#check_hash = no

# Set whetever the client should try to connect to UDP trackers.
#use_udp_trackers = no

# Alternative calls to bind and ip that should handle dynamic ip's.
#schedule = ip_tick,0,1800,ip=rakshasa
#schedule = bind_tick,0,1800,bind=rakshasa

# Encryption options, set to none (default) or any combination of the following:
# allow_incoming, try_outgoing, require, require_RC4, enable_retry, prefer_plaintext
#
# The example value allows incoming encrypted connections, starts unencrypted
# outgoing connections but retries with encryption if they fail, preferring
# plaintext to RC4 encryption after the encrypted handshake
#
encryption = allow_incoming,try_outgoing

# Enable DHT support for trackerless torrents or when all trackers are down.
# May be set to "disable" (completely disable DHT), "off" (do not start DHT),
# "auto" (start and stop DHT as needed), or "on" (start DHT immediately).
# The default is "off". For DHT to work, a session directory must be defined.
#
dht = disable

# UDP port to use for DHT.
#
# dht_port = 6881

# Enable peer exchange (for torrents not marked private)
#
peer_exchange = no

#
# Do not modify the following parameters unless you know what you're doing.
#

# Hash read-ahead controls how many MB to request the kernel to read
# ahead. If the value is too low the disk may not be fully utilized,
# while if too high the kernel might not be able to keep the read
# pages in memory thus end up trashing.
#hash_read_ahead = 10

# Interval between attempts to check the hash, in milliseconds.
#hash_interval = 100

# Number of attempts to check the hash while using the mincore status,
# before forcing. Overworked systems might need lower values to get a
# decent hash checking rate.
#hash_max_tries = 10

# Max number of files to keep open simultaniously.
#max_open_files = 128

# Number of sockets to simultaneously keep open.
#max_open_sockets =

# Example of scheduling commands: Switch between two ip's every 5
# seconds.
#schedule = "ip_tick1,5,10,ip=torretta"
#schedule = "ip_tick2,10,10,ip=lampedusa"

# Remove a scheduled event.
#schedule_remove = "ip_tick1"
{% endhighlight %}

There are a couple of lines you must replace with your own specific information. The first is <strong>directory = _directory torrents will download to by default_</strong> and the second is <strong>session = /home/_username_/.session</strong> . I also encourage you to do a little research so that you can change other settings to suit your purposes.


We need to make sure the directories we just told rtorrent to use exist. Because it would be silly to have your media stored on the same SD card containing the OS, I&#8217;ve attached an external USB hard drive to the BeagleBone and set my <em>directory = _directory torrents will download to by default_</em> line to point towards there. Since this is external media, we&#8217;ll need it to auto mount whenever the board reboots so that rtorrent will always be able to find it. We&#8217;ll start by making the directories for rtorrent and for the drive to be mounted to:


<blockquote>
    cd ~<br /> sudo mkdir .session<br /> sudo mkdir /media/_mount directory name_

</blockquote>

I am mounting it in <strong>/media</strong> because that is the standard place to place such things in ubuntu, though you could just as well mount it in <strong>/mnt</strong> or another directory you have made. To achieve automagical mounting we will edit <strong>/etc/fstab</strong> after backing up the original:


<blockquote>
    sudo cp /etc/fstab /etc/fstab.backup

</blockquote>

We&#8217;re going to mount the usb hard drive using the <strong>uuid</strong> rather than the /dev/sda path because it is a better way of identifying the drive we actually want. To find this uuid we need to run:


<blockquote>
    ls -l /dev/disk/by-uuid

</blockquote>

One of the lines should have something like <strong>../../sda1</strong> listed in yellow, and a corresponding alphanumeric code in blue. The blue code is the uuid, which you should copy. We can now go ahead and edit <strong>/etc/fstab</strong> :


<blockquote>
    sudo nano /etc/fstab

</blockquote>

We want to add a specific line to the end:


{% highlight plaintext %}
  UUID=_uuid_ /media/_mount directory name_ auto defaults 0 0
{% endhighlight %}


where <strong>\_uuid\_</strong> is the value we copied earlier, and <strong>/media/_mount directory name_</strong> is where we decided to mount the drive. If you happen to know the file system in use on your usb drive you may wish to change the <strong>auto</strong> in the above line to the proper filesystem. For ext4 this is just &#8220;<strong>ext4</strong>&#8221; and for ntfs (<em>oh god, why?</em>) it would be &#8220;<strong>ntfs-3g</strong>&#8220;, each without quotes. If using ntfs it may be necessary to install the ntfs-3g package.


Now that fstab has been modified, we want Ubuntu to recognize the changes:


<blockquote>
    sudo mount -a

</blockquote>

And we will also make ourselves the owner of the external drive mount point:


<blockquote>
    sudo chown -R _username_:_username_ /media/_mount directory name_

</blockquote>

If everything went well, then we should find that rtorrent starts up without any issues:


<blockquote>
    rtorrent

</blockquote>

Any problems should be noted in rtorrent with an error that should help direct you towards a solution. I got a warning about xmlrpc, though a little research showed this was just an advisory and nothing to actually be worried about. You can now quit rtorrent by pressing CTRL-q.


We also want rtorrent to start up automatically in such a way that it will also keep running when we are not logged in via ssh. This is accomplished using a startup script (which I have left unmodified for the original guide) that makes use of screen.


<blockquote>
    sudo nano /etc/init.d/rtorrent

</blockquote>

Paste the follwing into that file. The only change necessary is to replace <strong>_username_</strong> in the <strong>line user=&#8221;_username_&#8221;</strong> with the user we created earlier:



{% highlight bash %}
#!/bin/sh
#############
###<Notes>###
#############
# This script depends on screen.
# For the stop function to work, you must set an
# explicit session directory using ABSOLUTE paths (no, ~ is not absolute) in your rtorrent.rc.
# If you typically just start rtorrent with just "rtorrent" on the
# command line, all you need to change is the "user" option.
# Attach to the screen session as your user with
# "screen -dr rtorrent". Change "rtorrent" with srnname option.
# Licensed under the GPLv2 by lostnihilist: lostnihilist _at_ gmail _dot_ com
##############
###</Notes>###
##############

#######################
##Start Configuration##
#######################
# You can specify your configuration in a different file
# (so that it is saved with upgrades, saved in your home directory,
# or whateve reason you want to)
# by commenting out/deleting the configuration lines and placing them
# in a text file (say /home/user/.rtorrent.init.conf) exactly as you would
# have written them here (you can leave the comments if you desire
# and then uncommenting the following line correcting the path/filename
# for the one you used. note the space after the ".".
# . /etc/rtorrent.init.conf

#Do not put a space on either side of the equal signs e.g.
# user = user
# will not work
# system user to run as
user="_username_"

# the system group to run as, not implemented, see d_start for beginning implementation
# group=`id -ng "$user"`

# the full path to the filename where you store your rtorrent configuration
config="`su -c 'echo $HOME' $user`/.rtorrent.rc"

# set of options to run with
options=""

# default directory for screen, needs to be an absolute path
base="`su -c 'echo $HOME' $user`"

# name of screen session
srnname="rtorrent"

# file to log to (makes for easier debugging if something goes wrong)
logfile="/var/log/rtorrentInit.log"
#######################
###END CONFIGURATION###
#######################
PATH=/usr/bin:/usr/local/bin:/usr/local/sbin:/sbin:/bin:/usr/sbin
DESC="rtorrent"
NAME=rtorrent
DAEMON=$NAME
SCRIPTNAME=/etc/init.d/$NAME

checkcnfg() {
  exists=0
  for i in `echo "$PATH" | tr ':' '\n'` ; do
      if [ -f $i/$NAME ] ; then
          exists=1
          break
      fi
  done
  if [ $exists -eq 0 ] ; then
      echo "cannot find rtorrent binary in PATH $PATH" | tee -a "$logfile" >&2
      exit 3
  fi
  if ! [ -r "${config}" ] ; then
      echo "cannot find readable config ${config}. check that it is there and permissions are appropriate" | tee -a "$logfile" >&2
      exit 3
  fi
  session=`getsession "$config"`
  if ! [ -d "${session}" ] ; then
      echo "cannot find readable session directory ${session} from config ${config}. check permissions" | tee -a "$logfile" >&2
      exit 3
  fi
}

d_start() {
[ -d "${base}" ] && cd "${base}"
stty stop undef && stty start undef
su -c "screen -ls | grep -sq "\.${srnname}[[:space:]]" " ${user} || su -c "screen -dm -S ${srnname} 2>&1 1>/dev/null" ${user} | tee -a "$logfile" >&2
# this works for the screen command, but starting rtorrent below adopts screen session gid
# even if it is not the screen session we started (e.g. running under an undesirable gid
#su -c "screen -ls | grep -sq "\.${srnname}[[:space:]]" " ${user} || su -c "sg \"$group\" -c \"screen -fn -dm -S ${srnname} 2>&1 1>/dev/null\"" ${user} | tee -a "$logfile" >&2
su -c "screen -S "${srnname}" -X screen rtorrent ${options} 2>&1 1>/dev/null" ${user} | tee -a "$logfile" >&2
}

d_stop() {
  session=`getsession "$config"`
  if ! [ -s ${session}/rtorrent.lock ] ; then
      return
  fi
  pid=`cat ${session}/rtorrent.lock | awk -F: '{print($2)}' | sed "s/[^0-9]//g"`
  if ps -A | grep -sq ${pid}.*rtorrent ; then # make sure the pid doesn't belong to another process
      kill -s INT ${pid}
  fi
}

getsession() {
  session=`cat "$1" | grep "^[[:space:]]*session[[:space:]]*=" | sed "s/^[[:space:]]*session[[:space:]]*=[[:space:]]*//" `
  echo $session
}

checkcnfg

case "$1" in
start)
  echo -n "Starting $DESC: $NAME"
  d_start
  echo "."
  ;;
stop)
  echo -n "Stopping $DESC: $NAME"
  d_stop
  echo "."
  ;;
restart|force-reload)
  echo -n "Restarting $DESC: $NAME"
  d_stop
  sleep 1
  d_start
  echo "."
  ;;
*)
  echo "Usage: $SCRIPTNAME {start|stop|restart|force-reload}" >&2
  exit 1
  ;;
esac

exit 0
{% endhighlight %}

Finally we will make the owner of the file the root, make it executable, and have it startup at boot.


<blockquote>
    sudo chown root:root /etc/init.d/rtorrent<br /> sudo chmod a+x /etc/init.d/rtorrent<br /> cd /etc/init.d<br /> sudo update-rc.d rtorrent defaults

</blockquote>

If everything has worked out then running the following should startup rtorrent in a screen session:


<blockquote>
    sudo /etc/init.d/rtorrent start

</blockquote>

Which we will verify by running htop. We should find a few rtorrent processes and a screen process which belong to the user we created earlier. To quit htop hit the &#8220;q&#8221; key on your keyboard.


The last step is to get rutorrent up and running. rutorrent is just a web interface, and so we will put it in <strong>/var/www</strong> so that the apache webserver we installed and configured earlier can serve it up to us.


<blockquote>
    cd /var/www<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/rutorrent

</blockquote>

We will also install a bunch of plugins to extend to functionality of rutorrent and to make it more like a native program running on the client machine itself:


<blockquote>
    cd rutorrent/plugins<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/erasedata<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/create<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/trafic<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/edit<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/retrackers<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/cookies<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/search<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/scheduler<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/autotools<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/datadir<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/tracklabels<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/geoip<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/ratio<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/seedingtime<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/diskspace<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/data<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/rss<br /> sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins/throttle

</blockquote>

The diskspace plugin watches the root directory by default, and that is no good since we&#8217;re using an external drive for our torrent download location. To fix this we need to edit one line in the file <strong>/var/www/rutorrent/conf/config.php</strong>:


<blockquote>
    sudo nano /var/www/rutorrent/conf/config.php

</blockquote>

We need to find the line that begins <strong>$topDirectory</strong> and change it to the following:


{% highlight plaintext %}
  $topDirectory = "/media/_mount directory name_";
{% endhighlight %}

Finally, we have to change the ownership of these files and folders so that the web server can make use of them:


<blockquote>
    cd /var/www<br /> sudo chown -R www-data:www-data rutorrent<br /> sudo chmod -R 777 rutorrent

</blockquote>

If everything went as expected, then going to <strong>https://_Local IP address_/rutorrent</strong> should prompt us for a username and password (this is the one we created for the webserver, _webusername_, and is not necessarily the user account we created for the OS). After logging in, we should see the empty rutorrent webgui:


<a href="/wp-content/uploads/2012/05/rutorrentwebui.png"><img class="aligncenter size-medium wp-image-550" title="rutorrentWebui" src="/wp-content/uploads/2012/05/rutorrentwebui.png?w=300" alt="The rutorrent web user interface" width="300" height="187" srcset="/wp-content/uploads/2012/05/rutorrentwebui.png 1440w, /wp-content/uploads/2012/05/rutorrentwebui-300x187.png 300w, /wp-content/uploads/2012/05/rutorrentwebui-1024x640.png 1024w" sizes="(max-width: 300px) 100vw, 300px" /></a>


At this point we&#8217;re essentially finished with this part of the guide unless you wish to install an FTP server. For my purposes I am content with using sftp, which is built into SSH, though the <a href="http://forums.rutorrent.org/index.php?topic=256.0">original source for this portion of the guide</a> also includes instructions for setting up a true FTP server using Pure-FTPd. There are also instructions to enable a multi-user rtorrent setup, though I have not pursued those either since I don&#8217;t have any need for it. Since we are finished with rtorrent and rutorrent, you can now start adding your torrents to it. You should make sure to point rutorrent to the right directory  if you add any torrents that you already have the data for and are seeding so that it won&#8217;t redownload the entire thing.


<div id="samba"></div>
<p style="text-align:center;">
  *****
</p>


### Installing and configuring Samba

Samba is a very convenient application to have running for a home media server as it allows us to have very easy access to the files from other computers on the local network. To install samba:


<blockquote>
    sudo apt-get install samba

</blockquote>

We also need to make a samba password for our samba user (the same Ubuntu user we made earlier):


<blockquote>
    smbpasswd -a _username_

</blockquote>

The next step in setting samba up is to change some things in the configuration file, <strong>/etc/samba/smb.conf</strong>:


<blockquote>
    sudo nano /etc/samba/smb.conf

</blockquote>

The first thing to ensure is that the following line is present and uncommented (it should be below ####### Authentication #######):


{% highlight plaintext %}
  security = user
{% endhighlight %}


This will ensure that the only people who can access samba shares are those with a valid ubuntu account on the BeagleBone. The next step is to ensure that only people on the local network can access the samba shares which we achieve by adding the following lines under #### Networking ####:


{% highlight plaintext %}
  # Added for extra security, only addresses on the local network can connect.
  hosts allow = 127.0.0.1 192.168.1.0/24
  hosts deny = 0.0.0.0/0
{% endhighlight %}


You may need to change 192.168.1.0/24 to something else depending on your router and local area network addresses (192.168.0.0/24 is another common one).


The last things we need to do in this config file are to setup the shares themselves. We will comment out any of the lines pertaining to printers because the BeagleBone is not attached to any. The end result is that those lines should appear as follows:


{% highlight plaintext %}
;[printers]
;   comment = All Printers
;   browseable = no
;   path = /var/spool/samba
;   printable = yes
;   guest ok = no
;   read only = yes
;   create mask = 0700

# Windows clients look for this share name as a source of downloadable
# printer drivers
;[print$]
;   comment = Printer Drivers
;   path = /var/lib/samba/printers
;   browseable = yes
;   read only = yes
;   guest ok = no
{% endhighlight %}

We also want to enable a share for our attached usb drive by adding the following lines to the end of the file with _mount directory name_ and _username_ are replaced by the appropriate values we used earlier:


{% highlight plaintext %}
# Share for the external media hard drive
[media]
      comment = External Drive connected to BeagleBone.
      path = /media/<mount directory name>
      read only = no
      browseable = yes
      valid users = <username>
{% endhighlight %}

This makes the entire usb hard drive available to the user we created earlier and no one else.


That&#8217;s it for samba, and we can enable the changes by restarting the samba processes:


<blockquote>
    sudo restart smbd<br /> sudo restart nmbd

</blockquote>

<div id="maintenance"></div>
<p style="text-align:center;">
  *****
</p>


### Updating and maintaining the system

There are a few basic things we need to do to keep our new home media server functioning in tiptop shape, and the first is keeping it up to date. For the most part, this can be done through the ubuntu repositories:


<blockquote>
    sudo apt-get update<br /> sudo apt-get upgrade

</blockquote>

The kernel is a slightly more difficult matter because the one that works with the TI omap processors isn&#8217;t upstreamed to the repositories yet. To update the kernel you need to get the one built by <a href="https://github.com/RobertCNelson/stable-kernel">Robert C Nelson.</a> Luckily you shouldn&#8217;t need to do this very often, except in the case of security patches and important bug fixes. To make this process as easy as possible someone has already created a simple script to do all of the work for you. I have made the necessary changes to configure it to work with the BeagleBone running Ubuntu 12.04.<br /> First we will create a scripts directory to store it, then create the file using nano:


<blockquote>
    mkdir ~/scripts<br /> cd scripts<br /> nano update-kernel-bone.sh

</blockquote>

You then want to paste the following into this file:


{% highlight bash %}
############################################################################
## This is a script obtained from http://elinux.org/BeagleBoardUbuntu     ##
## It updates the kernel on the BeagleBone using Robert C Nelsons Sources ##
## https://github.com/RobertCNelson/stable-kernel                         ##
############################################################################

export DIST=precise #(options are lucid/maverick/natty/oneiric/precise/squeeze/wheezy)
export ARCH=armhf   #(options are armel/armhf (armhf only for precise))

#Beagle/Panda
#export BOARD=omap

#BeagleBone
export BOARD=omap-psp

wget http://rcn-ee.net/deb/${DIST}-${ARCH}/LATEST-${BOARD}
wget $(cat ./LATEST-${BOARD} | grep STABLE | awk '{print $3}')
/bin/bash install-me.sh
{% endhighlight %}

Using this script is a simple as moving into the scripts directory and running it:


<blockquote>
    cd ~/scripts<br /> sudo bash update-kernel-bone.sh

</blockquote>

Before updating the kernel, it is a good idea to make a backup of the system so it can be restored if something goes amiss. The easiest way I have found of backing up the operating system itself is to use <strong>dd</strong> to clone the microSD card. To do this you need to remove the microSD card from the BeagleBone after shutting it down:


<blockquote>
    sudo poweroff

</blockquote>

After removing the card you want to insert it into another computer, the one you used to write the card in the first place should work just fine. Running the following command will copy the entire contents of the card to a file called sdcard.img into the home directory of this computer:


<blockquote>
    sudo dd if=/dev/mmcblk0 of=~/sdcard.img

</blockquote>

If there are other SD cards inserted into this computer, then the location /dev/mmcblk0 may be incorrect. Make sure you are copying the contents of the correct SD card before you assume you have a valid backup. You can also change the location the image is copied to some other directory if you wish. This process will take a few minutes to complete, and when it is done you should have an image that can be copied back to the card using the command:


<blockquote>
    sudo dd if=~/sdcard.img of=/dev/mmcblk0

</blockquote>

Hopefully this will never be necessary, though we&#8217;re always better off safe than sorry.


If you have another USB hard drive, you may wish to backup the contents of the one on the BeagleBone to it. The easiest way to do this is through rsync using SSH. On your computer (not the BeagleBone, the one we use to ssh into it) you just run the following command with necessary changes to fit your system:


<blockquote>
    rsync -avv &#8211;progress -e ssh _username_@_Local IP Adress_:/media/_mount directory name_/_the path to the backup drive on the local computer_

</blockquote>

The amount of time this takes will depend on the amount of data that is present on the BeagleBone&#8217;s drive but not on the destination drive.


<p style="text-align:center;">
*****
</p>

And with all that we should be done. I&#8217;ve tried my very best to keep this guide free of any errors, but some are sure to have snuck through. If you notice any, then I will be very grateful if you point them out so I can get them fixed. Once again, I accept no liability for damages or issues that occur as a result of following my directions either on a BeagleBone or other hardware.

<p style="text-align:center;">
*****
</p>
