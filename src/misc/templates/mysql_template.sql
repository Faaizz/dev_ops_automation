-- CREATE DATABASE
CREATE DATABASE ${db_name};

-- CREATE USER AND GRANT PERMISSIONS
CREATE USER "${db_user}"@"localhost" IDENTIFIED BY "${db_pass}";
GRANT all ON ${db_name}.* TO "${db_user}"@"localhost";