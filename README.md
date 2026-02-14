# Gojo Server Guardian Bot

Gojo is a powerful Discord bot designed to monitor and control your Linux server remotely.

It provides system monitoring, login alerts, remote control, and automatic startup.

---

## Features

• Server status monitoring
• Login detection alerts
• Restart server remotely
• Shutdown server remotely
• Execute Linux commands remotely
• Owner security protection
• Embed-based clean UI
• Auto start on server boot

---

## Commands

| Command        | Description                  |
| -------------- | ---------------------------- |
| !status        | Shows CPU, RAM, Disk, uptime |
| !info          | Shows bot information        |
| !helpgojo      | Shows help                   |
| !restart       | Restart server               |
| !shutdown      | Shutdown server              |
| !run <command> | Run Linux command            |

---

## Installation

### Clone repo

```
git clone https://github.com/ADEEP13/gojo-bot.git
cd gojo-bot
```

---

### Install dependencies

```
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

### Setup environment

Create .env file

```
TOKEN=your_token
OWNER_ID=your_id
ALERT_CHANNEL_ID=channel_id
```

---

### Run bot

```
python bot.py
```

---

## Auto Start Setup

Create service file

```
sudo nano /etc/systemd/system/gojo.service
```

Paste:

```
[Unit]
Description=Gojo Discord Bot
After=network.target

[Service]
User=adeep
WorkingDirectory=/home/adeep/gojo-bot
ExecStart=/home/adeep/gojo-bot/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable service:

```
sudo systemctl daemon-reexec
sudo systemctl enable gojo
sudo systemctl start gojo
```

---

## Check Status

```
sudo systemctl status gojo
```

---

## Security

Only OWNER_ID can:

• restart server
• shutdown server
• run commands

---

## Requirements

Ubuntu Server
Python 3.8+
Discord Bot Token

---

## License

Open source
