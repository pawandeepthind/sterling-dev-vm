source /home/vagrant/.bash_profile
sqlplus sys/manager as sysdba <<EOT
EXEC DBMS_XDB.SETLISTENERLOCALACCESS(FALSE);
exit;
EOT