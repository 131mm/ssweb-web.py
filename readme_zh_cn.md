## Shadowsocks/r web manager

[English](https://github.com/131mm/ssweb-web.py/blob/master/readme.md)|中文

#### 简介

本项目是一个用于shadowsocks/r单机多用户管理的web，旨在让shadowsocks的配置可视化，只需一次部署，其余的管理操作都可以在网页上完成

#### 功能

- [x] 1、一键添加用户，可随机设置一切配置，无需任何输入

- [x] 2、一键删除用户或端口，适用与端口被阻断等情况

- [x] 3、修改配置，支持几乎所有shadowsocks的配置修改

- [x] 4、查看所有用户使用情况

#### 操作系统支持

Debian 9最佳，Debian应该都行

#### 语言

Python3.6，Python3应该都可以

#### Web框架

web.py==0.40.dev1

django 版本 [here](https://github.com/131mm/shadowsocks-monitor)

#### 声明：

这个项目的安全性没有经过测试

#### 使用

本项目与doubi写的ssr多用户一键脚本配合使用，请先安装该脚本
click [here](https://github.com/ToyoDAdoubi/doubi#ssrmush) to install it.

切换到root用户  `sudo su`

##### Method 1

安装Git  `apt install git`

拉取本项目到 ’/usr/local‘ 目录 `git clone https://github.com/131mm/ssweb-web.py.git /usr/local/ssweb-web.py && cd /usr/local/ssweb-web.py`

网站部署：

1. 安装nginx  `apt install nginx` 
2. 修改nginx配置文件‘nginx’中的 server_name 为你的域名 
3. 安装apache2-utils来生成网站密码 `apt install apache2-utils`
4. 生成密码 `htpasswd -c /etc/nginx/passwd.db username`
5. 修改 'ssr.py' 文件第三行的域名为你的域名        
6. 把nginx配置文件’nginx‘复制到 ’/etc/nginx/sites-enabled/‘ `cp nginx /etc/nginx/sites-enabled/`                
7. 重启nginx  `nginx &&  nginx -s reload`                    
8. 安装python3 venv pip `apt install python3 python3-venv python3-pip`
9. 创建虚拟环境 `python3 -m venv venv`          
10. 启动 `bash run.sh` 

##### Or Method 2
如果想简单点，可以用下面的命令，和method1是一样的

1. 
```
apt install python3 python3-pip python3-venv git nginx apache2-utils -y;
git clone https://github.com/131mm/ssweb-web.py.git /usr/local/ssweb-web.py &&cd /usr/local/ssweb-web.py;
```
2. 修改nginx配置文件‘nginx’中的 server_name 为你的域名 
3. 修改 'ssr.py' 文件第三行的域名为你的域名        

```
cp nginx /etc/nginx/sites-enabled/;
htpasswd -c /etc/nginx/passwd.db username;
nginx && sudo nginx -s reload;
python3 -m venv venv;
bash run.sh;

```

#### 网站截图

主页: 显示用户信息

![深度截图_选择区域_20190214165157.png](https://i.loli.net/2019/02/14/5c652c78795e0.png)

点击用户可查看详细配置:

![深度截图_选择区域_20190214165217.png](https://i.loli.net/2019/02/14/5c652c7860e24.png)

修改用户配置:

![深度截图_选择区域_20190214165243.png](https://i.loli.net/2019/02/14/5c652c784084c.png)

