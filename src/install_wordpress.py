#!/usr/bin/python3

#==============================================================================
# IMPORTS
import tarfile, requests, pathlib, os, shutil, argparse, subprocess
# Manual scripts
from misc import misc_funcs


#==============================================================================
# COMMAND-LINE HELP, OPTIONS, ARGUMENTS

cl_parser= argparse.ArgumentParser(
    description="Automated Wordpress installation"
    )

# Arguments
# Installation root path
cl_parser.add_argument(
    "--target", action="store", default="/var/www/html/wordpress", 
    help="path to install wordpress"
)
# MySQL root Password
cl_parser.add_argument(
    "--mysql_root_pass", action="store", required=True, 
    help="MySQL root password"
)
# MySQL Database
cl_parser.add_argument(
    "--mysql_db", action="store", default="wordpress_db", 
    help="wordpress MySQL database name"
)
# MySQL Database Username
cl_parser.add_argument(
    "--mysql_user", action="store", default="wordpress_user", 
    help="wordpress MySQL database user"
)
# MySQL User Password
cl_parser.add_argument(
    "--mysql_pass", action="store", required=True, 
    help="wordpress MySQL databse password"
)

## Collect installation options
install_options= cl_parser.parse_args()


#==============================================================================
# CREATE TEMP DIRECTORY

# Temporary directory path
temp_path= "./temp/wordpress"

# Create temporary directory
misc_funcs.create_temp_dir(temp_path)

# Change working directory to new temp folder
os.chdir(temp_path)


#==============================================================================
# DOWNLOAD PACKAGE

# Url
url= "https://wordpress.org/latest.tar.gz"

# Open temporary file to keep downloaded data
temp_file_path= os.getcwd() + '/wordpress.tar.gz'

# Download package
misc_funcs.download_package(temp_file_path, url)
    

#==============================================================================
# EXTRACT PACKAGE

# Temporary directory for extracted files
tar_temp_dir= os.getcwd() + "/extracted"

# Extract downloaded file
misc_funcs.extract_downloaded_file(temp_file_path, tar_temp_dir)


#==============================================================================
# SETUP WORDPRESS CONFIG FILE
# wp-config.php Template path
src_path= "../../src/misc/templates/wp-config.php"
dst_path= tar_temp_dir + "/wordpress/wp-config.php"

# Populate Template
# Log
print("Creating wp-config.php...")
reps={
    "wordpress_db": install_options.mysql_db,
    "wordpress_user": install_options.mysql_user,
    "wordpress_pass": install_options.mysql_pass,
    # FIX: $table_prefix is used in wp-config.php, thus string.Template sees
    # $table_prefix as a placeholder
    "table_prefix": '$table_prefix'
}
misc_funcs.populate_template(src_path, dst_path, reps)

#==============================================================================
# COPY INSTALLATION TO INSTALL DIRECTORY

# Source directory
src_dir= tar_temp_dir + "/wordpress"
dst_dir= install_options.target

# Copy files
misc_funcs.copy_files(src_dir, dst_dir)

#==============================================================================
# SET PERMISSIONS FOR www-data IN INSTALL DIRECTORY
pem_proc= subprocess.Popen(
    "chown -R www-data:www-data ./*",
    shell=True, cwd=dst_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
)

try:
    (out, err)=pem_proc.communicate(timeout=15)
    # Log output
    print(str(out))

except subprocess.TimeoutExpired:
    print("Permission changing command timeout...\nAborting...")


#==============================================================================
# DATABASE CONFIGURATION
# MySQL Template path
mysql_src_path= "../../src/misc/templates/mysql_template.sql"
mysql_dst_path= os.getcwd() + "/query.sql"

# Populate Template
# Log
print("Populating MySQL template...")
misc_funcs.populate_mysql_template(
    mysql_src_path, mysql_dst_path, install_options.mysql_db, 
    install_options.mysql_user, install_options.mysql_pass
)

# Run MySQL query
# Log
print("Creating MySQL database and user...")
# Spawn child process
mysql_proc= subprocess.Popen(
    "mysql -uroot -p{0} <{1}".format(install_options.mysql_root_pass, mysql_dst_path),
    shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
)

try:
    (out, err)=mysql_proc.communicate(timeout=15)
    # Log output
    print(str(out))

except subprocess.TimeoutExpired:
    print("MySQL command timeout...\nAborting...")


#==============================================================================
# CLEANUP
misc_funcs.cleanup("../wordpress")






    
