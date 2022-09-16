#!/bin/bash
if [ -f /etc/apt/sources.list ]; then
   apt update
   apt -y upgrade
   apt install -y python3-pip
   apt-get install -y systemd
else
   echo "Your distribution is not supported by this StackScript"
   exit
fi

git clone https://github.com/DhrumanGupta/mini-ddos-emulator
cd mini-ddos-emulator

pip install -r requirements.txt

echo "[Unit]
Description=Python DDoS Client
After=multi-user.target
[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 ${PWD}/client/main.py

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/ddos-emulator.service


echo "SERVER_IP_ADDRESS=${SERVER_IP_ADDRESS}" > ./client/.env

systemctl daemon-reload

systemctl enable ddos-emulator.service
systemctl start ddos-emulator.service



# python client/main.py

    