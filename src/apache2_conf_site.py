#!/usr/bin/python3

#==============================================================================
# IMPORTS
import argparse, os, shutil, subprocess
# Manual
from misc import misc_funcs


#==============================================================================
# COMMAND-LINE HELP, OPTIONS, ARGUMENTS

cl_parser= argparse.ArgumentParser(
    description="Automated site configuration for Apache2"
    )

# Arguments
# SSL mode
cl_parser.add_argument(
    "-s", action="store_true", default="admin",
    help="Server admin"
)


# Site root directory
cl_parser.add_argument(
    "--dir", action="store", default="/var/www/html",
    help="root directory of site"
)
# Site Name
cl_parser.add_argument(
    "--name", action="store", default="mysite",
    help="Site name. Saves the configuration file as <name>.conf"
)
# Server Name
cl_parser.add_argument(
    "--server_name", action="store", default="localhost",
    help="Server hostname"
)
# Server Admin
cl_parser.add_argument(
    "--server_admin", action="store", default="admin",
    help="Server admin"
)

# SSL Certificate
cl_parser.add_argument(
    "--ssl_cert", action="store", default="ca.crt",
    help="SSL certificate file name. \
        Assumes the certificate file is located in /etc/ssl/"
)
# SSL Private Key
cl_parser.add_argument(
    "--ssl_priv_key", action="store", default="ca-key.key",
    help="SSL certificate file name. \
        Assumes the certificate private key is located in /etc/ssl/private/"
)
# SSL Certificate Chain
cl_parser.add_argument(
    "--ssl_cert_bundle", action="store", default="ca-bundle.crt",
    help="SSL certificate file name. \
        Assumes the certificate chain file is located in /etc/ssl/"
)


# Collect arguments
install_options= cl_parser.parse_args()


#==============================================================================
# CREATE TEMP DIRECTORY

# Temporary directory path
temp_path= "../temp/apache2"

# Log
print(
    "Creating temporary directory at {0}...\n".format(os.path.abspath(temp_path))
)
# Create temporary directory
misc_funcs.create_temp_dir(temp_path)

# Change working directory to new temp folder
os.chdir(temp_path)


#==============================================================================
# SETUP .conf FILE

# Template Path
conf_path= "./{0}.conf".format(install_options.name)


# Check if SSL Mode is enabled
if(install_options.s == True):
    # Log
    print("SSL Mode enabled...\n")
    # SSL Mode
    src_path= "../../src/misc/templates/apache2_ssl_site.conf"
    # Setup replacements
    reps={
        "server_name": install_options.server_name,
        "server_admin": install_options.server_admin,
        "site_dir": install_options.dir,
        "ssl_cert": install_options.ssl_cert,
        "ssl_priv_key": install_options.ssl_priv_key,
        "ssl_cert_bundle": install_options.ssl_cert_bundle,
        # FIX:
        "APACHE_LOG_DIR": "${APACHE_LOG_DIR}"
    }


else:
    # HTTP mode
    src_path= "../../src/misc/templates/apache2_site.conf"
    # Setup replacements
    reps={
        "server_name": install_options.server_name,
        "server_admin": install_options.server_admin,
        "site_dir": install_options.dir,
        # FIX:
        "APACHE_LOG_DIR": "${APACHE_LOG_DIR}"
    }

# Log
print(
    "Populating template..."
)
# Populate Template
misc_funcs.populate_template(src_path, conf_path, reps)


#==============================================================================
# COPY CONFIG FILE TO /etc/apache2/sites-available

# Destination directory
dst_dir= "/etc/apache2/sites-available"

# Log
print(
    "Copying config file {0} to {1}...\n"
    .format(os.path.abspath(conf_path), dst_dir)
)
# Copy operation
shutil.copy(conf_path, dst_dir)


#==============================================================================
# APACHE2 HOUSEKEEPING

# If SSL mode is selected, enable SSL in apache2
if(install_options.s == True):
    # Log
    print("Attempting to enable ssl on apache2... \n")
    # Enable mod_rewrite
    sub_proc= subprocess.Popen(
        "a2enmod ssl", shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT
    )
    # Set timeout
    try: 
        (out, err)= sub_proc.communicate(timeout=5)
        print(str(out) + "\n")
    except subprocess.TimeoutExpired:
        print("ssl enable command timed out...\n")

# Log
print("Attempting to enable mod_rewrite on apache2... \n")
# Enable mod_rewrite
sub_proc= subprocess.Popen(
    "a2enmod rewrite", shell=True, stdout=subprocess.PIPE, 
    stderr=subprocess.STDOUT
)
# Set timeout
try: 
    (out, err)= sub_proc.communicate(timeout=5)
    print(str(out) + "\n")
except subprocess.TimeoutExpired:
    print("mod_rewrite enable command timed out...\n")


# Log
print("Attempting to enable site... \n")
# Enable site
sub_proc= subprocess.Popen(
    "a2ensite {0}".format(install_options.name), shell=True, 
    cwd="/etc/apache2/sites-available",
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT
)
# Set timeout
try: 
    (out, err)= sub_proc.communicate(timeout=5)
    print(str(out) + "\n")
except subprocess.TimeoutExpired:
    print("Site enable command timed out...\n")


# Log
print("Attempting to restart apache2.service... \n")
# Restart service
sub_proc= subprocess.Popen(
    "systemctl restart apache2", shell=True, 
    cwd="/etc/apache2/sites-available",
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT
)
# Set timeout
try: 
    (out, err)= sub_proc.communicate(timeout=5)
    print(str(out) + "\n")
except subprocess.TimeoutExpired:
    print("apache2.service restart command timed out...\n")
