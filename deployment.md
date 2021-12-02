# Steps to Deploy App to Linux Server (Ubuntu 20.04)
* Before beginning make sure to have a strong root password.
* Have a backup server for production.
* Choose location close to clients.
* You need to have ssh daemon setup in your server if using ssh.

### SSH into your remote server as root
```bash
ssh root@<your_server_ip>
```

### Update software
```bash
apt -y update && apt -y upgrade
```

### Setup hostname 
```bash
hostnamectl set-hostname flask-server
```

In the file `/etc/hosts` add `<your_ipv4_address>  flask-server` under `127.0.0.1 localhost`

## Setup regular user (limited user)

### Create new user with very strong password
```bash
adduser <test-user>
```

### Add user to sudo group
```bash
adduser <test-user> sudo
```

### SSH into your remote server as your newly-created user
```bash
ssh <test-user>@<your_server_ip>
```

## Setup SSH key-based authentication

On your local machine's terminal (NOT YOUR REMOTE SERVER'S TERMINAL) do the following:

### Make ssh directory within the home directory
```bash
mkdir ~/.ssh
```

### Generate SSH key pair
```bash
ssh-keygen -b 4096
```

### Copy public key to server
```bash
scp ~/.ssh/<your_public_key>.pub <test-user>@<your_server_ip>:~/.ssh/authorized_keys
```

On your remote server verify that the keys copied over, do the following::

```bash
ls .ssh
```

### Set permissions in server
```bash
sudo chmod 700 ~/.ssh/
sudo chmod 600 ~/.ssh/*
```

Now open a new terminal window in your local machine.
The rest of the commands in this deployment will be issued in this new terminal window.

### SSH into server using ssh keys
```bash
ssh <test-user>@<your_server_ip>
```

### Disallow root logins through ssh
In the file `/etc/ssh/sshd_config` uncomment and set `PermitRootLogin no` and `PasswordAuthentication no`

```bash
sudo systemctl restart sshd
```

### Setup firewall, follow these carefully as a wrong command can lock you out of your server.
```bash
sudo apt -y install ufw
sudo ufw default allow outgoing
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow 5000
sudo ufw enable
```

### Check status of firewall
```bash
sudo ufw status
```

### Copy/clone the project's repository into your web server
```bash
cd ~
git clone https://github.com/adrianmuino/Flask-Blog.git
```

### Setup python and virtual environment
```bash
sudo apt -y install python3-pip
sudo apt -y install python3-venv
python3 -m venv Flask-Blog/venv
cd Flask-Blog
source venv/bin/activate
./dependencies/pip_dep_install.sh
```

### Setup environment variables
Create the file `/etc/config.json` with all environment variables used when running the flask-blog site.
```json
{
    "SECRET_KEY" : "<Your flask secret key>",
    "SQLALCHEMY_DATABASE_URI" : "<Your DB uri>",
    "MAIL_USERNAME" : "<Your email>",
    "MAIL_PASSWORD" : "<Your email password>"
}
```

If you need to generate a new secret key, run the python interpreter:
```bash
python
```

Then run the following:
```python
import secrets
secrets.token_hex(16)
```

### Run flask app in release mode using the development server
```bash
export FLASK_APP=run.py
flask run --host=0.0.0.0
```

Test that everything works!

## Using production server.
We will use `nginx` to handle our static content, and `gunicorn` to handle our Python code.

### Install Nginx and gunicorn (make sure to be inside venv)
```bash
sudo apt -y install nginx
./dependencies/pip_install.sh gunicorn
```

### Remove default Nginx config and create new config file
```bash
sudo rm /etc/nginx/sites-enabled/default
```

Create a file called `/etc/nginx/sites-enabled/flaskblog` with the following configuration:
```
server {
    listen 80;
    server_name <your_ipv4_address>;

    location /static {
        alias /home/<test-user>/Flask-Blog/flaskblog/static;
    }

    location / {
        proxy_pass http://localhost:8000;
        include /etc/nginx/proxy_params;
        proxy_redirect off;
    }
}
```

### Allow HTTP traffic in firewall and disallow port 5000
```bash
sudo ufw allow http/tcp
sudo ufw delete allow 5000
sudo ufw enable
```

### Restart the Nginx server
```bash
sudo systemctl restart nginx
```

Now our static files should be working, such as `http://<your_ipv4_address>/static/main.css`, but dynamic content should not be working.
For the dynamic content we need to setup Gunicorn.

### Find out number of processor cores (Linux)
```bash
CORES=$(nproc --all)
```

### Start Gunicorn Python WSGI
Gunicorn recommends in their docs to run 2*CORES + 1 worker processes when used as production Python WSGI.
For example, if you have 1 core, then you should use 3 worker processes to handle requests.

```bash 
WORKERS=$((2*$CORES+1))
gunicorn -w $WORKERS run:app
```

We use `run:app` because our application variable is called `app` and is inside the `run.py` file.

Now we have a fully working application but if we CTRL+C, we kill our server. Not ready for production just yet!

### Setup supervisor to automate monitoring our flask server
```bash
sudo apt -y install supervisor
```
Create file `sudo nano /etc/supervisor/conf.d/flaskblog.conf` with the following content:
```
[program:flaskblog]
directory=/home/<test-user>/Flask-Blog
command=/home/<test-user>/Flask-Blog/venv/bin/gunicorn -w <WORKERS> run:app
user=<test-user>
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/flaskblog/flaskblog.err.log
stdout_logfile=/var/log/flaskblog/flaskblog.out.log
```

Create the log file's path and files.
```bash
sudo mkdir -p /var/log/flaskblog
sudo touch /var/log/flaskblog/flaskblog.err.log 
sudo touch /var/log/flaskblog/flaskblog.out.log 
```

Restart the supervisor program
```bash
sudo supervisorctl reload
```

Done. Test all functionality!!!
*** You might notice that trying to upload a large profile picture will make our server throw a 413 error (Nginx).
This is an Nginx default that we need to chage in our nginx configuration.
Hence, we should be very familiar with our web server before launching anything into production!!!***

PS, to fix the image upload size default in `/etc/nginx/nginx.conf` go inside the `http` brackets and add the `5M` line below:
```bash
http {
    ...
    types_hash_max_size 2048;
    client_max_body_size 5M;
}
```
Then run:
```bash
sudo systemctl restart nginx
```



Additionally, we can improve this by using custom DNS, HTTPS, adding unit tests, creating custom error pages for nginx errors, migrating to other DBs (perhaps PostgreSQL), adding DB indexes, etc etc etc.