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
 4. Main third party resources used to complete this project, some of the links can be found here:
 - [Restart Apache] (https://www.cyberciti.biz/faq/star-stop-restart-apache2-webserver/)
 - [MOD_WSGI](https://modwsgi.readthedocs.io/en/develop/index.html)
 - [Secret Key issue](https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session-using-the-flask-session-extension)
 - [SQL Alchemy Engine Configuration](https://docs.sqlalchemy.org/en/13/core/engines.html#postgresql)
 - [postgresql issues and solutions](https://www.postgresql.org/docs/9.4/tutorial-createdb.html)
 - [PSQL Info](https://www.postgresql.org/docs/9.4)
 - [User access in postgres](https://tableplus.io/blog/2018/04/postgresql-how-to-grant-access-to-users.html)
 - [Apache error log location](https://blog.codeasite.com/how-do-i-find-apache-http-server-log-files/)
 - [Login without password as postgres user](https://serverfault.com/questions/110154/whats-the-default-superuser-username-password-for-postgres-after-a-new-install)
 - [MODWSGI configuration] (https://modwsgi.readthedocs.io/en/develop/user-guides/configuration-guidelines.html)
 
  
  
