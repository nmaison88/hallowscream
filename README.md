# hallowscream

Fun little project for making a raspberry pi, trigger jump scares when a pir sensor is tripped. added bonus is the addition of a distance ir sensor which can tell the height of the victim, if its a small one we still trigger a sound but we don't scare the bejesus out of them, just the taller ones! 

## Pre-requisites
```
first need to install pygame
pip install pygame
second need to install etc mixer dependencies
sudo apt-get install libsdl2-mixer-2.0-0
```
run app with python hallowScream.py


can also add to rc.local for startup headless.
```
paste the below line before the exit:
in /etc/rc.local
sudo -H -u pi /usr/bin/python3 /home/pi/hallowscream/hallowScream.py &
```

### view logs via:
```  
tail -f /var/log/syslog
```


### If during testing you need to easily disable the daemon you can do either

``` 
# list running python services with:

ps aux |grep python
#grab the pid from the desired service name and enter:
kill -9 <pid>

# alternatively you can kill all python3 processes with:
sudo killall python3
```