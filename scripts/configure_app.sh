#!/bin/bash
# scripts/configure_app.sh
# Note: Run this script as the default 'ubuntu' user from inside the cloned repository directory.

APP_DIR="/home/ubuntu/cs408-project"

echo "Setting up Virtual Environment and installing dependencies..."
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Creating .env file for production configurations..."
cat <<EOF > $APP_DIR/.env
DATABASE_URL=postgresql://recipeuser:recipepassword@localhost/recipedb
PORT=8000
EOF

echo "Initializing PostgreSQL Database tables..."
# Triggers SQLAlchemy to create tables based on models.py
python -c "from app.main import Base, engine; Base.metadata.create_all(bind=engine)"

echo "Configuring Systemd Service for FastAPI via Gunicorn..."
sudo bash -c "cat <<EOF > /etc/systemd/system/recipeshare.service
[Unit]
Description=Gunicorn instance serving RecipeShare FastAPI Application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=$APP_DIR
Environment=\"PATH=$APP_DIR/venv/bin\"
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/venv/bin/gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 127.0.0.1:8000 app.main:app

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl daemon-reload
sudo systemctl start recipeshare
sudo systemctl enable recipeshare

echo "Configuring Nginx Reverse Proxy..."
sudo bash -c "cat <<EOF > /etc/nginx/sites-available/recipeshare
server {
    listen 80;
    server_name _; # Accepts any domain name or IP

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \\\$host;
        proxy_set_header X-Real-IP \\\$remote_addr;
        proxy_set_header X-Forwarded-For \\\$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \\\$scheme;
    }
}
EOF"

sudo ln -sf /etc/nginx/sites-available/recipeshare /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl restart nginx

echo "Configuration complete. The Collaborative Recipe Sharing Platform is now live."