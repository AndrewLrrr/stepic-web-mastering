#!/usr/bin/env bash

sudo /etc/init.d/mysql start

mysql -uroot -e "CREATE DATABASE ask CHARACTER SET utf8 COLLATE utf8_general_ci;"