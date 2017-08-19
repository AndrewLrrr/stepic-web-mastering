#!/usr/bin/env bash

sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart

if [ ! -d /etc/gunicorn.d ]; then
	sudo mkdir -p /etc/gunicorn.d;
fi

sudo ln -sf /home/box/web/etc/hello.py /etc/gunicorn.d/hello.py

sudo /etc/init.d/gunicorn restart
