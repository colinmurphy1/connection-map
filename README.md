# Connection Map

Connection Map is a program that plots the location of incoming network connections to your server on a map. It searches through system log files for IP addresses, and then uses geolocation data to find the hosts’ approximate location.

You can see a live demonstration of Connection Map [here](https://map.colinmurphy.me). It updates every hour, showing connections to my SSH and HTTP server.

## Installation

Connection Map requires the following Python 3 modules: `python-geoip`, `maxminddb-geolite2`. Install them using pip or your distributions' package manager.

It is recommended to create a dedicated user for this program, as it will require access to your system log files. If you are using Debian/Ubuntu, you can add your user to the `adm` group to simplify this, like so:

    usermod -aG adm $USERNAME

Place the contents of `map` somewhere in your website directory. By default, this is `/var/www/map/`. Make sure the user you created has permissions to modify the contents of this directory, or at least the `data.geo.json` file. 

Next, set up the configuration file. An example configuration file is located at `settings.example.json`. By default, this configuration will use the log files for OpenSSH (`/var/log/auth.log`) and nginx (`/var/log/nginx/access.log`), but you can change these to your liking. The default output file is `/var/www/map/data.geo.json`.

## Running the program

To run it, run `python3 connmap.py settings.json`.