#!/usr/bin/python3

#==============================================================================
# IMPORTS
import os, argparse, subprocess, shutil

from flask import Flask

from misc import misc_funcs


#==============================================================================
# COMMAND LINE ARGUMENTS

# Create parser object
cl_parser= argparse.ArgumentParser(
    description="automated site configuration for NGINX"
)

# ARGUMENTS
# IP and Port of Web App to reverse proxy
cl_parser.add_argument(
    "--from_site", action="store", default="localhost:8000",
    help="IP and port of web app to reverse proxy"
)

# Site Name
cl_parser.add_argument(
    "--name", action="store", default="mysite",
    help="Site name. Saves the configuration file as <name>"
)

# Server hostname
cl_parser.add_argument(
    "--server_name", action="store", default="localhost",
    help="Server hostname"
)

# Collect command-line arguments
install_options= cl_parser.parse_args()


#==============================================================================
# CREATE TEMPORARY DIRECTOY AND SET AS WORKING DIRECTORY
# Temporary directory location
temp_path= "../temp/nginx"

# Log
print(
    "Creating temporary directory at {0}...\n".format(os.path.abspath(temp_path))
)

# Create temporary directory
misc_funcs.create_temp_dir(temp_path)

# Change working directory to new temp directory
os.chdir(temp_path)


#==============================================================================
# SETUP SERVER CONFIG FILE

# Path to save config file
conf_path= "./{0}".format(install_options.name)

# Template path
src_path= "../../src/misc/templates/nginx_site"

# Setup string replacements
reps= dict(
    server_name= install_options.server_name,
    from_site= install_options.from_site,
    # FIX
    http_upgrade= "$http_upgrade",
    host= "$host"
)

# Log
print(
    "Populating template..."
)

# Populate template
misc_funcs.populate_template(src_path, conf_path, reps)

# COPY CONFIG FILE TO /etc/nginx/sites-available
# Copy config file to /etc/nginx/sites-available

# Destination directory
dst_dir= "/etc/nginx/sites-available"

# Log
print(
    "Copying config file {0} to {1}...\n"
    .format(os.path.abspath(conf_path), dst_dir)
)

# Copy operation
shutil.copy(conf_path, dst_dir)


#==============================================================================
# NGINX HOUSEKEEPING

# Create symbolic link in /etc/nginx/sites-enabled

# Log
print(
    "Attempting to create symbolic link in /etc/nginx/sites-enabled...\n"
)

# Create child process
sub_proc= subprocess.Popen(
    "sudo ln -s /etc/nginx/sites-available/{0} /etc/nginx/sites-enabled/"
    .format(install_options.name), shell=True, stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)

# Set timeout
try:
    (out, err)= sub_proc.communicate(timeout=5)
    print(str(out) + "\n")
except subprocess.TimeoutExpired:
    print("Failed to create symbolic link in sites-enabled folder...")

# Reload NGINX service

# Log
print(
    "Reloading NGINX service...\n"
)

sub_proc= subprocess.Popen(
    "sudo systemctl reload nginx", shell=True,
    stdout=subprocess.PIPE, stderr=subprocess.STDOUT
)

# Set timeout
try:
    (out, err)= sub_proc.communicate(timeout=5)
    print(str(out) + "\n")
except subprocess.TimeoutExpired:
    print("NGINX service reload failed...")


#==============================================================================
# CLEANUP

# Cleanup
misc_funcs.cleanup("../nginx")
