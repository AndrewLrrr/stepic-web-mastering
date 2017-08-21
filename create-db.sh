#!/usr/bin/env bash

sudo /etc/init.d/mysql start

mysql -uroot -e "DROP DATABASE IF EXISTS ask"

mysql -uroot -e "CREATE DATABASE ask CHARACTER SET utf8 COLLATE utf8_general_ci;"

cd ask && python3 manage.py migrate