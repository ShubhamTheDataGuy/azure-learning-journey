#!/bin/bash

# Update packages
sudo apt-get update -y

# Install NGINX
sudo apt-get install -y nginx

VM_NAME="$(hostname -s || echo unknown)"

tee /var/www/html/index.html >/dev/null <<EOF
<html>
  <head><title>Custom Script Extensions Demo</title></head>
  <body>
    <h1>We now have NGINX running as a web server</h1>
    <p>This page is served from VM instance: <b>${VM_NAME}</b></p>
  </body>
</html>
EOF

# Ensure NGINX starts on boot
sudo systemctl enable nginx
sudo systemctl restart nginx