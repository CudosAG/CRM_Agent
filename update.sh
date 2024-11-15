#!/bin/bash

# Setze den Projektordner auf das aktuelle Verzeichnis
PROJECT_PATH=/root/CRM_Agent

cd $PROJECT_PATH

source venv/bin/activate
git pull
pip install -r requirements.txt

systemctl restart crmservice.service

