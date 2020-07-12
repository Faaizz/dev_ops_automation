#!/usr/bin/python3
import subprocess, os, time
import pexpect

# new_proc= pexpect.spawn("mysql -uroot -p <./misc/templates/mysql_template.sql")
# new_proc.expect("Password:")
# new_proc.sendline("Nkwr7596_")
# print(new_proc.before)
# new_proc.interact()

new_proc= subprocess.Popen("mysql -uroot -p{0} <./misc/templates/mysql_template.sql"
                            .format("Nkwr7596_"), 
                            shell=True,
                            stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.STDOUT
)


(out, err)= new_proc.communicate()

print(str(out))
print(str(err))
