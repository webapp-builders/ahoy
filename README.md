# README - Installation Instructions

---------------------------------

## Step One - Install Ansible

You can follow the instructions on the [Ansible website]
http://docs.ansible.com/intro_installation.html#installing-the-control-machine
or either of the options below:


### (if you have OSX)

first install homebrew if you dont have it installed

ruby -e "$(curl -fsSL https-//raw.github.com/Homebrew/homebrew/go/install)"

then run

```
brew update
brew install python
brew install ansible
pip install paramiko PyYAML Jinja2 httplib2
```

### OR (if you use ubuntu/debian)

```
sudo apt-get install python-yaml python-markupsafe nfs-kernel-server nfs-common portmap
sudo apt-get install software-properties-common
```
Test to see if ansible is installed using `ansible --version`  If it is not installed, do the following:
```
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible
```

### OR (if you have centos/redhat)

```
yum install ansible
```

---------------------------------

## Step Two - Virtualbox

Download [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and install.

---------------------------------

## Step Three - Vagrant

Download [Vagrant](http://www.vagrantup.com/downloads) and install.

---------------------------------

## Step Four - Repo

Go to directory you want clone into. For example, if you want to clone into `/someuser/myapps/`

You could do: `cd /someuser/myapps/`

Then type below:
```
git clone https://github.com/webapp-builders/ahoy.git
```

or this if using ssh:
```
git clone git@github.com:webapp-builders/ahoy.git
```

---------------------------------

## Step Five

```
cd ahoy
```

You can confirm that you are in the correct directory by typing `ls`.<br>
If you see a file `Vagrantfile` you are in the correct directory.

**_Note_**: If you are using ubuntu as your primary OS, uncomment line 22 to use the VirtualBox GUI.

**_Note_**: If your computer only supports 32-bit operating systems, after `cd groundwork`, open the file: `Vagrantfile`<br>
Comment out line 3 and uncomment line 5 to use "ubuntu/trusty64" <br>
(this will tell VirtualBox to run the "precise32" operating system).

---------------------------------

## Step Six

```
vagrant up
```
**__READ Below for possible "terminal messages":__**<br>
Numerous messages and errors may occur once typing `vagrant up`.<br>
Read the following _Terminal Message 1_ and _Terminal Message 2_, to make sure you are on the right track.

---------------------------------

**_Terminal Message 1_**:  If your terminal seems to be "stuck" at `TASK: rvm...` just wait.  This might take a while, because you are installing Ruby using RVM.  This is a good sign.  It means everything is installing properly.


**_Terminal Message 2_**:  You many receive an error if you already have Rail or Postgresql running on your machine. <br>
This means you need to *stop* Rails and/or Postgresql.

An error might look like the following:
```
Vagrant cannot forward the specified ports on this VM, since they
would collide with some other application that is already listening
on these ports. The forwarded port to 5432 is already in use
on the host machine.

To fix this, modify your current projects Vagrantfile to use another
port. Example, where '1234' would be replaced by a unique host port:

  config.vm.network :forwarded_port, guest: 5432, host: 1234

Sometimes, Vagrant will attempt to auto-correct this for you. In this
case, Vagrant was unable to. This is usually because the guest machine
is in a state which doesn't allow modifying port forwarding.
```
For Rails server, find the terminal window that is running Rails locally and
press `ctrl+c` together.

You may not realize it, but Postgres might have started automatically at
startup.
If Postgresql is running, to stop your:

**_For Ubuntu_**:
```
sudo service postgresql stop
```

**_For  OSX homebrew_**:<br>
Go online, search for "how to stop postgresql osx"<br>
(There will be different instructions depending on how your Mac is setup).


---------------------------------

## Step Seven (ON first host OS Terminal Tab)

```
vagrant ssh
```

Your terminal prompt should change from your normal one.
Now this tab becomes your Guest OS Terminal Tab


**For example**:<br>
(These are not exact, the will vary from computer to computer)<br>
Your terminal prompt _before_:   OSX@jennifer~/myworkfiles $<br>
Your terminal prompt _after_:   vagrant@vagrant-ubuntu-trusty-64:~$<br>

Once you have typed `vagrant ssh` and your terminal prompt has successfully
 changed to a new one such as `vagrant@vagrant-ubuntu-trusty-64:~$` this
 means you are now **using the terminal of another operating system!**

The whole reason you are using Vagrant is to have another operating system
(within your computer) to have a completely isolated environment for
development.


---------------------------------

## Step Eight(ON host OS Terminal Tab)

To work on the project

Type:

```
workon web
```

This will activate the virtual environment and cd into the
project directory.
You will now be in the web project directory with the virtual environment
named "web" activated as indicated by the (web) text before the prompt.
Also all packages defined in requirements.txt file in the project directory
are automatically
re-installed every time you type workon web
Also all environment variables exported in the .env file in the project
directory are sourced every time you type workon web

Go to STEP NINE.



---------------------------------

## Step Nine(ON host OS Terminal Tab)

create the database schema by typing the following:
(you should skip this step for now since
currently there is no database defined)

```
python ./tasks/createdb.py
```

Go to STEP TEN.

---------------------------------

## Step Ten(ON Guest OS Terminal Tab)

Start the flask develoment server by typing:

```
python manage.py -h 33.33.33.33
```

Go to your browser and open http://33.33.33.33:5000


You can stop the server by typing ctrl-c

--------------------------------------
## Step Eleven(ON Guest OS Terminal Tab)

At anytime you can deactivate the virtual environment simply by typing:

```
deactivate
```

and you can reactivate it again by again typing:

```
workon web
```

--------------------------------------
## Step Twelve
Open a second Host OS Terminal Tab
cd into project directory

You can run git commands for the project here.
Note: git is not installed on the guest OS so all git management
should be done on the Host os. Treat the Guest OS like a production
environment and the project files on the guest os as readonly.

--------------------------------------
## Step Fourteen
Open a third Host OS Terminal Tab
cd into project directory

You can type the command that launches your text editor here


---------------------------------
Vagrant Notes:

the initilal vagrant up command also runs the vagrant provision automiatically
subsequent vagrant up (or vagrant reload) commands will only run the changes in the vagrantfile
but will not run the ansible configuration specified in the vagrant file unless
the vagrant destroy command is run before it.
In order to run the changes in the ansible configuration
run the following command (ON first host OS Terminal Tab)

```
vagrant provision
```

Note vagrant prvision will only run the changes to the ansible configuration
but will not run changes in the vagrant file. for executing the changes in the
vagrant file type vagrant up or vagrant reload (ON first host OS Terminal Tab)



