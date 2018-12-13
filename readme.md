## ssweb powered by web.py

#### System supported

Debian 9 only

#### Language

Python3.6 required

#### Framework

web.py==0.40.dev1

django version [here](https://github.com/131mm/shadowsocks-monitor)

#### Usage

Before you start this web, make sure you have installed another awesome shell 'ssrmu.sh'. 
If not, please click [here](https://github.com/ToyoDAdoubi/doubi#ssrmush) to install it.

Switch to super user root using `sudo su`

##### Method 1

Git is also required, using `apt install git`

Clone this project to `/usr/local`  using `git clone https://github.com/131mm/ssweb-web.py.git /usr/local/ssweb-web.py` 
and `cd` into it `cd /usr/local/ssweb-web.py`

Then

1. install nginx using `apt install nginx` 
2. change the server_name in file 'nginx' to your domain 
3. install apache2-utils using `apt install apache2-utils`
4. generate password using `htpasswd -c /etc/nginx/passwd.db username`
5. change the website in line 3 of file 'ssr.py' to your domain        
6. copy file `nginx` in to `/etc/nginx/sites-enabled/` using `cp nginx /etc/nignx/sites-enabled/`                
7. start nginx with `nginx && sudo nginx -s reload`                    
8. install venv and pip using `apt install python3-venv python3-pip`   
9. create virtual-env for web.py using `python3 -m venv venv`          
10.start it `bash run.sh` 

##### Or Method 2

1. change the server_name in file 'nginx' to your domain
2. change the website in line 3 of file 'ssr.py' to your domain
3. :

```
apt install python3 python3-pip python3-venv git nginx apache2-utils -y;
git clone https://github.com/131mm/ssweb-web.py.git /usr/local/ssweb-web.py;
cd /usr/local/ssweb-web.py;
cp nginx /etc/nignx/sites-enabled/;
htpasswd -c /etc/nginx/passwd.db username;
nginx && sudo nginx -s reload;
python3 -m venv venv;
bash run.sh;

```