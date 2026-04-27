#!/bin/bash
# scripts/setup_ec2.sh
# Note: Run this script with root privileges (sudo bash scripts/setup_ec2.sh)

echo "Updating system packages..."
apt-get update && apt-get upgrade -y

echo "Installing Python 3, pip, venv tools, PostgreSQL, and Nginx..."
apt-get install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx

echo "Configuring PostgreSQL Database and User..."
# Creates a database user 'recipeuser' and database 'recipedb'
sudo -u postgres psql -c "CREATE USER recipeuser WITH PASSWORD 'recipepassword';"
sudo -u postgres psql -c "CREATE DATABASE recipedb OWNER recipeuser;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE recipedb TO recipeuser;"

# Ensure the application directory exists and is owned by the default ubuntu user
APP_DIR="/home/ubuntu/cs408-project"
mkdir -p $APP_DIR
chown ubuntu:ubuntu $APP_DIR

echo "System setup complete. Switch to the ubuntu user to clone your repo, then run configure_app.sh."