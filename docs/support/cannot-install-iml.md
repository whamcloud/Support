# IML Installation Fails

[Support Table of Contents](TOC.md)

This document describes the steps to take when an IML installation fails.

## Basic Troubleshooting

The first thing that should be done following a failed IML installation is to check the installation log on the manager node at `/var/log/chroma/install.log`. Here are a few things to look for:

1. Did all of the dependencies install correctly? If the installation is being done offline make sure the epel and centos / rhel repos have been reposynced.
2. Did a service fail to start?

## Problems and Solutions

### Failed dependency

If a dependency failed to install run:

```bash
yum provides <package name>
```

This should indicate where the package is located. If yum cannot find the package, check the repos in the /etc/yum.repos.d folder and make sure they are correct.

If the installation is being done offline you will need to ensure that all necessary repos have been reposynced. Please read through [How to create offline repos for IML](https://intel-hpdd.github.io/Online-Help/docs/Contributor_Docs/cd_Create_Offline_Repos.html) to ensure that all necessary repos are reposynced. Remember that epel and the base centos / rhel repos may need to be reposynced as well.

[Top](#iml-installation-fails)

### Postgresql service will not start

In the event that postgresql does not start there are a few things that need to be checked. First, run the following:

```bash
ls -l /var/run
```

A `postgresql` folder should exist in this directory and both the group and owner should be `postgres`. If the folder does not exist then the postgresql service was not able to create the folder. Note that the problem may be able to be resolved by creating a `postgresql` directory in `/var/run` but this will not persist and is not a good solution. The `/var/run` directory is symlinked to the `/run` directory, which is a tempfs filesystem, meaning that it is more or less scrach space for services to operate on between reboots of the server. Checking the service logs will help determine the root cause. Run:

```bash
systemctl status postgresql.service
```

This should provide more information about why the service was not able to start. You may see errors such as the following:

```bash
failed at step USER spawning /usr/bin/postgresql-check-db-dir: No such process
postgresql could not create lock file "/var/run/postgresql/.s.PGSQL.5432.lock": Permission denied
```

The next step is to switch to the postgres user:

```bash
su - postgres
```

Look for any errors or warnings when switching to this user. Also, check the directory with `pwd`; it should be `/var/lib/pgsql`. Another thing to check is the environment variables. They should look similar to the following:

```bash
$ env
XDG_SESSION_ID=5
HOSTNAME=admin-hostname
SHELL=/bin/bash
TERM=xterm-256color
HISTSIZE=1000
USER=postgres
LS_COLORS=rs=0:di=38;5;27:ln=38;5;51:mh=44;38;5;15:pi=40;38;5;11:so=38;5;13:do=38;5;5:bd=48;5;232;38;5;11:cd=48;5;232;38;5;3:or=48;5;232;38;5;9:mi=05;48;5;232;38;5;15:su=48;5;196;38;5;15:sg=48;5;11;38;5;16:ca=48;5;196;38;5;226:tw=48;5;10;38;5;16:ow=48;5;10;38;5;21:st=48;5;21;38;5;15:ex=38;5;34:*.tar=38;5;9:*.tgz=38;5;9:*.arc=38;5;9:*.arj=38;5;9:*.taz=38;5;9:*.lha=38;5;9:*.lz4=38;5;9:*.lzh=38;5;9:*.lzma=38;5;9:*.tlz=38;5;9:*.txz=38;5;9:*.tzo=38;5;9:*.t7z=38;5;9:*.zip=38;5;9:*.z=38;5;9:*.Z=38;5;9:*.dz=38;5;9:*.gz=38;5;9:*.lrz=38;5;9:*.lz=38;5;9:*.lzo=38;5;9:*.xz=38;5;9:*.bz2=38;5;9:*.bz=38;5;9:*.tbz=38;5;9:*.tbz2=38;5;9:*.tz=38;5;9:*.deb=38;5;9:*.rpm=38;5;9:*.jar=38;5;9:*.war=38;5;9:*.ear=38;5;9:*.sar=38;5;9:*.rar=38;5;9:*.alz=38;5;9:*.ace=38;5;9:*.zoo=38;5;9:*.cpio=38;5;9:*.7z=38;5;9:*.rz=38;5;9:*.cab=38;5;9:*.jpg=38;5;13:*.jpeg=38;5;13:*.gif=38;5;13:*.bmp=38;5;13:*.pbm=38;5;13:*.pgm=38;5;13:*.ppm=38;5;13:*.tga=38;5;13:*.xbm=38;5;13:*.xpm=38;5;13:*.tif=38;5;13:*.tiff=38;5;13:*.png=38;5;13:*.svg=38;5;13:*.svgz=38;5;13:*.mng=38;5;13:*.pcx=38;5;13:*.mov=38;5;13:*.mpg=38;5;13:*.mpeg=38;5;13:*.m2v=38;5;13:*.mkv=38;5;13:*.webm=38;5;13:*.ogm=38;5;13:*.mp4=38;5;13:*.m4v=38;5;13:*.mp4v=38;5;13:*.vob=38;5;13:*.qt=38;5;13:*.nuv=38;5;13:*.wmv=38;5;13:*.asf=38;5;13:*.rm=38;5;13:*.rmvb=38;5;13:*.flc=38;5;13:*.avi=38;5;13:*.fli=38;5;13:*.flv=38;5;13:*.gl=38;5;13:*.dl=38;5;13:*.xcf=38;5;13:*.xwd=38;5;13:*.yuv=38;5;13:*.cgm=38;5;13:*.emf=38;5;13:*.axv=38;5;13:*.anx=38;5;13:*.ogv=38;5;13:*.ogx=38;5;13:*.aac=38;5;45:*.au=38;5;45:*.flac=38;5;45:*.mid=38;5;45:*.midi=38;5;45:*.mka=38;5;45:*.mp3=38;5;45:*.mpc=38;5;45:*.ogg=38;5;45:*.ra=38;5;45:*.wav=38;5;45:*.axa=38;5;45:*.oga=38;5;45:*.spx=38;5;45:*.xspf=38;5;45:
MAIL=/var/spool/mail/postgres
PATH=/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin
PWD=/var/lib/pgsql
LANG=en_US.UTF-8
HISTCONTROL=ignoredups
SHLVL=1
HOME=/var/lib/pgsql
LOGNAME=postgres
PGDATA=/var/lib/pgsql/data
```

If the `HOME` env variable doesn't match or there are other odd looking properties / values, it's possible that the postgres user's environment was not setup correctly. This can happen, for example, if the node is connected to an NAS server which also has a postgres user. If this is the case, the node should be disconnected from the NAS server and postgresql will need to be removed (using yum). Note that this will remove the chroma package as well and the installation process will need to be repeated. At this point, the IML installation should succeed.

[Top](#iml-installation-fails)