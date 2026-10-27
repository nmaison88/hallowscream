# hallowscream

Fun little project for making a raspberry pi, trigger jump scares when a pir sensor is tripped. added bonus is the addition of a distance ir sensor which can tell the height of the victim, if its a small one we still trigger a sound but we don't scare the bejesus out of them, just the taller ones! 

## Pre-requisites

### Raspberry Pi OS 12 (bookworm) / 13 (trixie) and newer
Newer Pi OS blocks `pip install` system wide (`error: externally-managed-environment`),
and building pygame from source on a Pi usually fails. Install everything from apt instead:
```
sudo apt-get update
sudo apt-get install -y python3-pygame python3-numpy python3-opencv libsdl2-mixer-2.0-0 python3-rpi-lgpio
```
`python3-rpi-lgpio` provides `RPi.GPIO` on current Pi OS (it's usually already installed).
`numpy` and `opencv` are only needed for `test.py`.

If you'd rather use pip, do it inside a virtual environment:
```
python3 -m venv --system-site-packages ~/hallowscream/.venv
~/hallowscream/.venv/bin/pip install pygame
~/hallowscream/.venv/bin/python hallowScream.py
```

Quick check that everything is installed:
```
python3 -c "import pygame, RPi.GPIO; pygame.mixer.init(); print('ok')"
```

### Older Pi OS (buster / bullseye)
```
first need to install pygame
pip install pygame
second need to install etc mixer dependencies
sudo apt-get install libsdl2-mixer-2.0-0
```

run app with python3 hallowScream.py


## Start on boot (systemd)
Newer Pi OS doesn't ship `/etc/rc.local`, so use a systemd service instead.
Create `/etc/systemd/system/hallowscream.service`:
```
[Unit]
Description=HallowScream jump-scare sampler
After=sound.target local-fs.target
Wants=sound.target

[Service]
Type=simple
User=pi
Group=pi
SupplementaryGroups=audio gpio
WorkingDirectory=/home/pi/hallowscream
Environment=SDL_AUDIODRIVER=alsa
Environment=PYTHONUNBUFFERED=1
ExecStart=/usr/bin/python3 /home/pi/hallowscream/hallowScream.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```
then enable and start it:
```
sudo systemctl daemon-reload
sudo systemctl enable --now hallowscream
```

### view logs via:
```
journalctl -u hallowscream -f
```

### stop / start / disable during testing
```
sudo systemctl stop hallowscream      # stop until next boot
sudo systemctl start hallowscream     # start again
sudo systemctl restart hallowscream   # after editing the code
sudo systemctl disable hallowscream   # don't start on boot
```

### Older Pi OS: rc.local
can also add to rc.local for startup headless.
```
paste the below line before the exit:
in /etc/rc.local
sudo -H -u pi /usr/bin/python3 /home/pi/hallowscream/hallowScream.py &
```
view logs via:
```  
tail -f /var/log/syslog
```

If during testing you need to easily disable the daemon you can do either
``` 
# list running python services with:

ps aux |grep python
#grab the pid from the desired service name and enter:
kill -9 <pid>

# alternatively you can kill all python3 processes with:
sudo killall python3
```

## Troubleshooting
- **No sound:** sound goes to the 3.5mm jack (card 0) by default. List outputs with `aplay -l`
  and test with `aplay ~/hallowscream/dinoFx/bite1.wav`. Run `alsamixer` to check the volume.
- **`RuntimeWarning: ... neon capable`** from pygame can be ignored; it only affects graphics.
- **Logs stop at "Waiting For Sensor To Settle":** the script is waiting on the distance
  sensor's ECHO pin (GPIO 24). Check the TRIG (23) / ECHO (24) wiring.
