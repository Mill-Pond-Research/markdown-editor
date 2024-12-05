# Deploying Markdown Editor on DigitalOcean

This guide will walk you through deploying the Markdown Editor application on DigitalOcean using a basic droplet setup.

## Prerequisites

- A DigitalOcean account
- Domain name (optional)
- SSH key pair for secure access

## Step 1: Create a Droplet

1. Log in to your DigitalOcean account
2. Click "Create" and select "Droplets"
3. Choose the following configuration:
   - **Image**: Ubuntu 22.04 LTS x64
   - **Plan**: Basic
   - **CPU option**: Regular with SSD
   - **Size**: $4/month (1GB RAM/1CPU) - Can scale up if needed
   - **Datacenter Region**: Choose closest to your target users
   - **Authentication**: SSH keys (recommended)
   - **Hostname**: markdown-editor (or your preference)

## Step 2: Initial Server Setup

SSH into your droplet:
```bash
ssh root@your_server_ip
```

Update the system and install required packages:
```bash
apt update && apt upgrade -y
apt install python3-pip python3-venv nginx supervisor -y
```

## Step 3: Clone and Setup Application

1. Create a deployment user:
```bash
adduser deploy
usermod -aG sudo deploy
```

2. Switch to deploy user and create application directory:
```bash
su - deploy
mkdir ~/markdown-editor
cd ~/markdown-editor
```

3. Clone the repository or upload the application files
4. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

5. Install dependencies:
```bash
pip install -r requirements.txt
pip install gunicorn  # For production server
```

## Step 4: Configure Gunicorn

Create a Gunicorn configuration file:
```bash
sudo nano /etc/supervisor/conf.d/markdown-editor.conf
```

Add the following configuration:
```ini
[program:markdown-editor]
directory=/home/deploy/markdown-editor
command=/home/deploy/markdown-editor/venv/bin/gunicorn app:app -b 127.0.0.1:8000
user=deploy
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/markdown-editor/gunicorn.err.log
stdout_logfile=/var/log/markdown-editor/gunicorn.out.log
```

Create log directory:
```bash
sudo mkdir -p /var/log/markdown-editor
sudo chown -R deploy:deploy /var/log/markdown-editor
```

## Step 5: Configure Nginx

Create Nginx configuration:
```bash
sudo nano /etc/nginx/sites-available/markdown-editor
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name your_domain.com;  # Replace with your domain or server IP

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/markdown-editor /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Remove default site
sudo nginx -t  # Test configuration
sudo systemctl restart nginx
```

## Step 6: Start the Application

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start markdown-editor
```

## Step 7: Setup SSL (Optional but Recommended)

Install Certbot:
```bash
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

Obtain SSL certificate:
```bash
sudo certbot --nginx -d your_domain.com
```

## Maintenance and Monitoring

- View application logs:
  ```bash
  tail -f /var/log/markdown-editor/gunicorn.out.log
  tail -f /var/log/markdown-editor/gunicorn.err.log
  ```

- Restart application:
  ```bash
  sudo supervisorctl restart markdown-editor
  ```

- Monitor system resources:
  ```bash
  htop
  ```

## Troubleshooting

1. If the application isn't accessible:
   - Check Nginx status: `sudo systemctl status nginx`
   - Check Gunicorn status: `sudo supervisorctl status markdown-editor`
   - Verify firewall settings: `sudo ufw status`

2. If you see 502 Bad Gateway:
   - Check if Gunicorn is running
   - Verify the socket configuration
   - Check application logs for errors

3. For permission issues:
   - Ensure proper ownership: `sudo chown -R deploy:deploy /home/deploy/markdown-editor`
   - Check log file permissions

## Security Considerations

1. Configure UFW firewall:
```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

2. Regular system updates:
```bash
sudo apt update && sudo apt upgrade
```

3. Monitor system logs:
```bash
sudo tail -f /var/log/auth.log
```

4. Consider setting up:
   - Fail2ban for brute force protection
   - Regular backup solution
   - Monitoring service (e.g., DigitalOcean Monitoring)

## Scaling Considerations

- Monitor resource usage and upgrade droplet specifications if needed
- Consider using DigitalOcean Spaces for file storage if implementing file uploads
- Set up a load balancer for high availability if required
- Implement caching if needed (e.g., Redis)

For any issues or questions, refer to:
- DigitalOcean documentation: https://docs.digitalocean.com/
- Flask deployment guide: https://flask.palletsprojects.com/en/2.3.x/deploying/
- Nginx documentation: https://nginx.org/en/docs/ 