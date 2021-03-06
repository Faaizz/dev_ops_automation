# DevOps Automation
Simple python scripts for automating common DevOps operations on Ubuntu 
(and other debian-based linux distributions).

-------------------------------------------------------------------------------
## Content
- [Wordpress Automated Setup](#Wordpress-Automated-Setup)  
- [Apache Automated Site Configuration](#Apache-Automated-Site-Configuration)  
- [NGINX Automated Reverse Proxy for Web Apps](#NGINX-Automated-Reverse-Proxy-for-Web-Apps)  

-------------------------------------------------------------------------------
## Wordpress Automated Setup
Automatically download and extract the latest release of wordpress, 
create MySQL database and user for use with wordpress, 
set up wordpress configuration file (wp-config.php) to use the created database 
and database user, 
copy wordpess installation to specified target directory, 
and clean up installation files afterwards.

### Basic Usage
```shell
sudo ./src/install_wordpress.py --target="/var/www/html" --mysql_root_pass="RootPass" --mysql_pass="MyPass"
```

### Flags and Arguments
- ```-h```: to view help
- ```--target```: Optional. Defaults to */var/www/html/wordpress*. Path to install wordpress
- ```--mysql_root_pass```: Required. Password for MySQL root user
- ```--mysql_pass```: Required. Password for MySQL wordpress user
- ```--mysql_db```: Optional. Defaults to *wordpress_db*. Wordpress database name
- ```--mysql_user```: Optional. Defaults to *wordpress_user*. Wordpress user name

### Requirements
- Run with root privileges (i.e. prefixed with *sudo*)
- Pyhton3
- Apache2 HTTP Server with *mod_rewrite* enabled
- MySQL Server
- PHP

-------------------------------------------------------------------------------
## Apache Automated Site Configuration
Automatically generate site config file, enable the site, 
and restart apache2 service.  
SSL support is also included. However, the certificate files must be 
stored in the default location */etc/ssl/* and the certificate private key must 
also be stored in the default location */etc/ssl/private*


### Basic Usage
```shell
sudo ./src/apache2_conf_site.py --name="main_site"  --dir="/var/www/html" --server_name="example.com"
```

### Flags and Arguments
- ```-h```: to view help
- ```-s```: Configure site with SSL
- ```--name```: Optional. Defaults to *myssite*. 
Site name, saves the configuration file as <name>.conf
- ```--dir```: Optional. Defaults to */var/www/html*. Site root directory
- ```--server_name```: Optional. Defaults to *localhost*. Server hostname
- ```--server_admin```: Optional. Defaults to *admin*. Server admin
- ```--ssl_cert```: Optional. Defaults to *ca.crt*. SSL certificate file name. 
Certificate file must be stored in */etc/ssl/*
- ```--ssl_priv_key```: Optional. Defaults to *ca-key.key*. SSL certificate 
private key file name. Must be stored in */etc/ssl/private/*
- ```--ssl_cert_bundle```: Optional. Defaults to *ca-bundle.crt*. SSL certificate 
chain file name. Certificate chain file must be stored in */etc/ssl/*

### Requirements
- Run with root privileges (i.e. prefixed with *sudo*)
- Pyhton3
- Apache2 HTTP Server 


-------------------------------------------------------------------------------
## NGINX Automated Reverse Proxy for Web Apps
Automatically set up reverse proxy for web apps and reload nginx service to effect changes.  

### Basic Usage
```shell
sudo ./src/nginx_conf.py --name="main_site"  --from_site="127.0.0.1:5000" --server_name="example.com"
```

In the above example, all incoming traffic to *example.com* are routed to *127.0.0.1:5000*. 
Similarly, all outgoing traffic from *127.0.0.1:5000* are routed through *example.com*.

### Flags and Arguments
- ```-h```: to view help
- ```--name```: Optional. Defaults to *myssite*. 
Site name, saves the configuration file as <name>
- ```--from_site```: Optional. Defaults to *localhost:5000*. Server hostname
- ```--server_name```: Optional. Defaults to *localhost*. Server hostname

### Requirements
- Run with root privileges (i.e. prefixed with *sudo*)
- Pyhton3
- Nginx Server
