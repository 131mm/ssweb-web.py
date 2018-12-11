# ssweb powered by web.py

## System supported

Debian 9 only

## Language

Python3.6 required

## Usage

Before you start this web, make sure you have installed another awesome shell 'ssrmu.sh'. 
If not, please click [here](https://github.com/ToyoDAdoubi/doubi#ssrmush) to install it.

Switch to super user root using `sudo su`

Git is also required, using `apt install git`

Clone this project to `/usr/local`  using `git clone https://github.com/131mm/ssweb-web.py.git /usr/local/ssweb-web.py` 
and `cd` into it `cd /usr/local/ssweb-web.py`

Then

1. install nginx using `apt install nginx` 
2. change the server_name in file 'nginx' to your domain 
3. change the website in line 3 of file 'ssr.py' to your domain
4. copy file `nginx` in to `/etc/nginx/sites-enabled/`               
5. start nginx with `nginx && sudo nginx -s reload`                  
6. install venv and pip using `apt install python3-venv python3-pip` 
7. create virtual-env for web.py using `python3 -m venv venv`        
8. start it `bash run.sh`                                            