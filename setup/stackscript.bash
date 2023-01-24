#!/bin/bash
if [ -f /etc/apt/sources.list ]; then
   apt update
   apt -y upgrade
   apt install -y python3-pip git
   apt-get install -y systemd
else
   echo "Your distribution is not supported by this StackScript"
   exit
fi

# <UDF name="SERVER_IP_ADDRESS" label="The host server IP address" default="localhost:3000" example="0.0.0.0:3000" />

if [ ! -d /root/ddos ]; then 
        git clone https://github.com/DhrumanGupta/mini-ddos-emulator /root/ddos 
else 
        git --git-dir="/root/ddos/.git" pull origin master 
fi

pip install -r /root/ddos/requirements.txt

echo "[Unit]
Description=Python DDoS Client
After=multi-user.target
[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /root/ddos/client/main.py

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/ddos-emulator.service


echo "SERVER_IP_ADDRESS=$SERVER_IP_ADDRESS" > /root/ddos/client/.env

systemctl daemon-reload

systemctl enable ddos-emulator.service
systemctl start ddos-emulator.service
