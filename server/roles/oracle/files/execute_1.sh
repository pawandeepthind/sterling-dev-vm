source /home/vagrant/.bash_profile
sqlplus sys/manager as sysdba <<EOT
ALTER SYSTEM SET PROCESSES=200 SCOPE=spfile;
ALTER SYSTEM SET SESSIONS=225 SCOPE=spfile;
exit;
EOT