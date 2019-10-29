#!/usr/bin/env bash
# https://die-antwort.eu/techblog/2017-12-setup-raspberry-pi-for-kiosk-mode
{ # this ensures the entire script is downloaded #


#lifted from openframe.io
piframe_edit_or_add() {
  if grep -q "^$2" $1; then
    sudo bash -c "sed -i 's/^$2.*/$2$3/g' $1"
  else
    sudo bash -c "echo $2$3 >> $1"
  fi
}

#lifted from openframe.io
piframe_do_rotate() {
  echo "how much have you rotated it?"
  echo "enter '0' for no rotation"
  echo "'1' if you rotated your physical screen 90 degrees clockwise"
  echo "'2' for 180 degrees (upside down)"
  echo "'3' for 270 degrees (90 degrees counter-clockwise)"
  read ANSWER
  if [ "$ANSWER" -ge 0 -a "$ANSWER" -le 3 ]; then
    piframe_edit_or_add /boot/config.txt display_rotate= $ANSWER
  else
    echo "input not recognised, must be a number between 0 and 3"
    piframe_ask_rotate
  fi
}

#lifted from openframe.io
piframe_ask_rotate() {
  echo "have you rotated your screen from default (normally landscape)? (y/n)"
  read ANSWER
  ANSWER="$(echo $ANSWER | tr '[:upper:]' '[:lower:]')"
  if [ "$ANSWER" == "y" ] || [ "$ANSWER" == "yes" ]; then
    piframe_do_rotate
  elif [ "$ANSWER" == "n" ] || [ "$ANSWER" == "no" ]; then
    :
  else
    echo "input not recognised, must be yes or no"
    piframe_ask_rotate
  fi
}


# configure the nginx 
nginx_do_install() {
	apt-get install --no-install-recommends nginx -y
	cat > /etc/nginx/sites-available/piframe.conf << EOF
worker_processes 1;
events {
    worker_connections 1024;
}
http {
    sendfile on;
    gzip              on;
    gzip_http_version 1.0;
    gzip_proxied      any;
    gzip_min_length   500;
    gzip_disable      "MSIE [1-6]\.";
    gzip_types        text/plain text/xml text/css
                      text/comma-separated-values
                      text/javascript
                      application/x-javascript
                      application/atom+xml;
    server {
        listen 80;
        location ^~ /static/  {
            root /home/pi/piFrame/static/;
        }
        location = /favico.ico  {
            root /home/pi/piFrame/favico.ico;
        }
        location / {
            proxy_pass         http://127.0.0.1:8000;
            proxy_redirect     off;
            proxy_set_header   Host $host;
            proxy_set_header   X-Real-IP $remote_addr;
            proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header   X-Forwarded-Host $server_name;
        }
    }
}
EOF
	ln -s /etc/nginx/sites-available/piframe.conf /etc/nginx/sites-enabled/piframe.conf
	rm -rf /etc/nginx/sites-enabled/default
	nginx restart
}

#tools needed
tools_do_install() {
  echo "install git"
	apt-get install --no-install-recommends git -y

  echo "install vim"
	apt-get install --no-install-recommends vim -y

  echo "install screen"
  apt-get install --no-install-recommends screen -y
}

piframe_configure_pi(){
  # if gpu_mem is not set, set gpu memory to 96
  grep -qxF 'gpu_mem=' /boot/config.txt || echo 'gpu_mem=96' >> /boot/config.txt

  # if display rotate is not set, set display rotate to 1 
  # grep -qxF 'display_rotate=' /boot/config.txt || echo 'display_rotate=1' >> /boot/config.txt
}

openbox_do_config(){
# configure the openbox 
cat > /etc/xdg/openbox/autostart << EOF
# Disable any form of screen saver / screen blanking / power management
xset s off
xset s noblank
xset -dpms

# Allow quitting the X server with CTRL-ATL-Backspace
setxkbmap -option terminate:ctrl_alt_bksp

# Start Chromium in kiosk mode
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' ~/.config/chromium/'Local State'
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/; s/"exit_type":"[^"]\+"/"exit_type":"Normal"/' ~/.config/chromium/Default/Preferences
chromium-browser --disable-infobars --kiosk 'http://localhost:3000/display'
EOF
}

piFrame_systemd_config(){
# configure the openbox 
cat > /etc/xdg/openbox/autostart << EOF

EOF
}

piframe_do_install() {
	# disable terminal screen blanking
  openframe_edit_or_add ~/.bashrc "setterm -powersave off -blank 0"

	# update the system
	echo "update system"
	apt-get update

	echo "upgrade system packages"
	apt-get upgrade -y

	# add the necessary packages
	echo "install server x11 utils"
	apt-get install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox -y

	echo "install chromium"
	apt-get install --no-install-recommends chromium-browser -y

  echo "configure openbox"
  openbox_do_config

  echo "install tools"
  tools_do_install

	echo "install openframe"

	echo "cloning piframe repo"
  cd /home/pi
	git clone https://github.com/adriangoris/piFrame /home/pi/piFrame
	cd /home/pi/piFrame

	echo "installing python modules"
	pip3 install -r /home/pi/piFrame/requirements.txt

	echo "creating and configuring database"
	python3 /home/pi/piFrame/manage.py migrate
	# uwsgi --http :8000 --module piframe.wsgi
  
  # interactive prompt for configuration
  piframe_ask_rotate

  echo ""
  echo "If you have changed your display rotation, you must restart the Pi by typing: sudo reboot"
  echo ""
  echo "If not, you must run the following command: source ~/.bashrc"
  echo ""
  echo "After restarting or reloading .bashrc, you can launch the frame by just typing:"
  echo ""
  echo "openframe"

}



piframe_do_install

# add the autostart when running
cat > /home/pi/.bash_profile << EOF
[[ -z $DISPLAY && $XDG_VTNR -eq 1 ]] && startx -- -nocursor
EOF

#enable ssh
# cat > /boot/ssh << EOF
# EOF


# start the item running
#startx -- -nocursor

} # this ensures the entire script is downloaded #