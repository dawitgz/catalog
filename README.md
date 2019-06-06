# Catalog Project

IP Address: 3.91.25.159
SSH PORT: 2200
URL: http://3.91.25.159
Software Installed: Flask, SQLAlchemy, psycopg2, requests, oauth2client, httplib2
Configuration: 
 1. Updated myapp.wsgi with sys.path.insert(0, '/var/www/html')
 2. Updated database_setup.py and sports_items.py to use the postgres sql db connection instead of sqlite.
    postgresql://user:password@localhost/database
 3. Configured VirtualHost in /etc/apache2/sites-available/000-default.conf with:
  - ServerName - to point to the AWS Lightsail server address
  - DocumentRoot - to point to /var/www/html
  - Alias to Template folder
  - WSGIScriptAlias to point to the myapp.wsgi file
  - WSGIDaemonProcess to point to the virtual env location
  - Gave the directories /var/www/html and /var/www/html/Templates global open access so they can be viewed online
 4. Searched a lot of third party resources to complete this project, some of the links can be found here:
 
  
  
