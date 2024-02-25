#!/bin/zsh

# Update the package manager and upgrade the system
sudo apt update && sudo apt upgrade -y

# Install Apache2 and PHP for LAMP stack
sudo apt install -y apache2 php libapache2-mod-php php-mysql

# Install MySQL for LAMP stack
sudo apt install -y mysql-server
sudo mysql_secure_installation

# Enable and start Apache2 service
sudo systemctl enable apache2
sudo systemctl start apache2

# Optional: Install additional PHP extensions
sudo apt install -y php-curl php-gd php-cli php-json

# Restart Apache to apply PHP changes
sudo systemctl restart apache2

# For LEMP stack, replace Apache with Nginx and install PHP-FPM
if [[ "$1" == "LEMP" ]]; then
  # Remove Apache2 if installed
  sudo apt remove -y --purge apache2 libapache2-mod-php
  sudo apt autoremove -y

  # Install Nginx and PHP-FPM for LEMP stack
  sudo apt install -y nginx php-fpm

  # Enable and start Nginx service
  sudo systemctl enable nginx
  sudo systemctl start nginx

  # Configure Nginx to use PHP-FPM by editing /etc/nginx/sites-available/default
  cat << EOF | sudo tee /etc/nginx/sites-available/default
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /var/www/html;
    index index.php index.html index.htm index.nginx-debian.html;
    server_name _;

    location / {
        try_files \$uri \$uri/ =404;
    }

    location ~ \.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php$(php -r 'echo PHP_VERSION;')-fpm.sock;
        fastcgi_param SCRIPT_FILENAME \$document_root\$fastcgi_script_name;
        include fastcgi_params;
    }
}
EOF

  # Restart Nginx to apply the changes
  sudo systemctl restart nginx
fi

echo "LAMP/LEMP stack installation and configuration complete."
