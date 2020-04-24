#!/usr/bin/python3
from os import path
from os import system
from os import getuid
from sys import argv

# Argument Parse Filter {Security from argbuster and decomPYle}
if(len(argv)<2 or len(argv)>3 or argv[1] == '-h' or argv[1] == '--help' or argv[1] == '' or argv[1] == ' ' or  (len(argv)==2 and (argv[1]=='-d' or argv[1]=='-domain'))):
    print('\nHelp\n----\n\nNOTE: Run This Program as Root\n\nUsage\n-----\n-d or --fqdn {arg}: \tPass Domain Name "FQDN" Arg\n-u or --user {arg}: \tprovide a users info file (space seperated usernames and password) ; please use it with and after -d/--domain only\n-h or --help : \t\tDisplay this help\n')

elif(argv[1] == '-d' or argv[1] == '--fqdn'):
    FQDN = argv[2]
    if(getuid()==0):
        ##-- Using seperate system calls to improve IPC --##
        # Upgrading and updating the packages
        system('apt-get update -y')
        system('apt-get upgrade -y')

        # Installing Dependencies and requirements {not upgrading php if already exists}
        if(path.isfile('/usr/bin/php') or path.isfile('/usr/local/bin/php')):
            system('apt-get install -y unzip apache2')
        else:
            system('apt-get install -y unzip apache2 php')

        # Installing Postfix Mail server with configs
        system(f'debconf-set-selections <<< "postfix postfix/mailname string {FQDN}"')
        system('debconf-set-selections <<< "postfix postfix/main_mailer_type string \'Internet Site\'"')
        system('apt-get install --assume-yes postfix')

        # Restarting postfix after auto-configuration
        system('service postfix restart')

        # Installing Dovecot imap and pop3 servers
        system('apt-get install -y dovecot-imapd dovecot-pop3d')

        # Restarting Dovecot service after auto configuration
        system('service dovecot restart')

        # Installing Squirrel webmail
        system('cd /tmp')
        system('wget https://sourceforge.net/projects/squirrelmail/files/stable/1.4.22/squirrelmail-webmail-1.4.22.zip')
        system('unzip squirrelmail-webmail-1.4.22.zip')
        system('mv squirrelmail-webmail-1.4.22 /var/www/html/')
        system('chown -R www-data:www-data /var/www/html/squirrelmail-webmail-1.4.22/')
        system('chmod 755 -R /var/www/html/squirrelmail-webmail-1.4.22/')
        system('mv /var/www/html/squirrelmail-webmail-1.4.22/ /var/www/html/squirrelmail')
        
        if(path.isdir('/var/local/squirrelmail/data')):
            system('chown -R www-data:www-data /var/local/squirrelmail/data/')
        else:
            system('mkdir -p /var/local/squirrelmail-webmail/data/')
            system('chown -R www-data:www-data /var/local/squirrelmail/data/')
        
        # Configuring Squirrel webmail
        print('Configure the Squirrel webmail manually')
        system('perl /var/www/html/squirrelmail/config/conf.pl')
        
        system('service apache2 restart')

        # Print Success
        print('\n\n-------\nSuccess\n-------\nSetting the Mail server\n\n')

    else:
        print('\n--- ---- ------- -- ----\nRun this program as root \n--- ---- ------- -- ----\n\n')


else:
    print("\n\nError : Something went wrong, Maybe you aren't connected to Internet\n\n")
