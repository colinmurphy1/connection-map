import re
import json
from geolite2 import geolite2
import argparse

files = dict()
gjson = list()


def geoJSONTemplate(ip, service, coords, color):
    """ Creates the relevent data needed to build a GeoJSON file """
    return {
        'type': 'Feature',
        'properties': {
            'ip': ip,
            'service': service,
            'color': color
        },
        'geometry': {
            'type': 'Point',
            'coordinates': coords
        }
    }

def obfuscateIPAddress(ip):
    """ Replaces the last octet of the IPv4 address with an X """
    return re.sub('(\d{1,3})$', 'x', ip)

def loadConfig(file):
    """ Loads the configuration file and puts it into a dictionary """
    try:
        with open(file, "r") as json_file:
            config = json.load(json_file)
        return config
    except:
        print("Error loading configuration file.")
        quit()

class LogFile:
    """
        LogFile class
        Opens and parses the log files
    """
    # By default, ignore local as well as private IPs, as they cannot be geolocated
    # There is no option to wildcard yet, just type in the beginning (or entire) part
    # of the IP you want to ignore.
    # TODO: Make this an option in the configuration file.
    ignoredIPs = ("0.0.0.0", "192.168.", "10.", "172.16.", "127.")

    def __init__(self, filename, service = "", hideIP = False, color = "#FFFFFF"):
        self.filename = filename
        self.service = service
        self.hideIP = hideIP
        self.color = color
        self.rawData = list()
        self.ipList = list()

    def openFile(self):
        """ Loads log file for parsing """
        try:
            with open(self.filename, 'r') as fh:
                return [line.rstrip() for line in fh]
        except Exception as e:
            print(e)
            quit()

    def parseFile(self):
        """ Parses a log file and returns IP addresses """

        # Open the log file
        self.rawData = self.openFile()

        # Iterate over each line in the log file, looking for IP addresses
        for line in self.rawData:
            search = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", line)
            for match in search:
                # Ignore certain IPs or IP ranges (need to improve this, probably)
                if match.startswith(self.ignoredIPs):
                    pass
                # Only add the IP address to the list if it's not already in it yet
                elif match not in self.ipList:
                    self.ipList.append(match)
        return self.ipList

    def geoJSON(self):
        """ Generates the relevent GeoJSON data needed for the map """
        jsonList = list()

        # Load GeoIP
        reader = geolite2.reader()

        for ip in self.ipList:
            # Get GeoIP information for IP
            try:
                ipgeo = reader.get(ip)
                lat = ipgeo["location"]["latitude"]
                lon = ipgeo["location"]["longitude"]
            except TypeError:
                # Some IPs don't have geolocation information for some reason,
                # and can't be included on the map, so skip them. 
                print("No geoip information for", ip)
                pass

            # Obfuscate IP (this can used for public map pages)
            if self.hideIP == True:
                ip = obfuscateIPAddress(ip)

            jsonList.append(geoJSONTemplate(ip, self.service, [lon,lat], self.color))
        geolite2.close() # Close geoip db
        return jsonList

def writeFile(outfile, data):
    """ Saves the GeoJSON file to disk """
    try:
        with open(outfile, 'w') as fh:
            json.dump(data, fh)
    except Exception as e:
        print(e)
        quit()


# Main program
if __name__ == "__main__":

    # Add command-line arguments
    parser = argparse.ArgumentParser(description="Connection Map")
    parser.add_argument("configFile", metavar="config_file", type=str, help="Configuration file (in JSON)")

    # Parse arguments
    args = parser.parse_args()

    # Load configuration file 
    config = loadConfig(args.configFile)

    # Go through each log file listed in configuration file 
    for service in config["logfiles"]:
        print("Opening logfile for", service)

        # Parse log file 
        files[service] = LogFile(config["logfiles"][service]["path"], service, config["hideip"], config["logfiles"][service]["color"])
        files[service].parseFile()

        # Get the generated GeoJSON
        gjson = gjson + files[service].geoJSON()

    # Write generated GeoJSON to disk
    writeFile(config["output"], gjson)
