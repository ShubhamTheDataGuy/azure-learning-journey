#!/bin/bash

# Update packages
sudo apt-get update -y

# Install NGINX
sudo apt-get install -y nginx

# Create simple default page
sudo bash -c 'cat > /var/www/html/index.html <<EOF
<html>
  <head><title>Custom Script Extensions Demo</title></head>
  <body>
    <h1>We now have NGINX running as a web server</h1>
  </body>
</html>
EOF'

# Ensure NGINX starts on boot
sudo systemctl enable nginx
sudo systemctl restart nginx