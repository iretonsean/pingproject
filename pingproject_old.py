"""

Author: Sean Ireton
Program Name: SuperPinger
Version: 1.0.0
CIS 201 Project (Fall 2024)

Description: Pinging tool for devices connected to my LAN and WAN.
Objective: Ping devices and websites successfully, then log responses to an external file.
Libraries to use:
    Ping Libraries
        ping3 (https://pypi.org/project/ping3/)
        subprocess
    Data Handling
        Pandas


"""

# LIBRARY IMPORTS
###############################################################################################

from ping3 import ping, verbose_ping
import subprocess

# FUNCTIONS
###############################################################################################


# RUN MAIN PROGRAM
###############################################################################################

f = open("output/pinglist.csv", "r")
lines = f.read()
f.close
pingList = []
response = ""


def createList():
    for line in lines:
        line = lines.strip()
        # print(line)

    for pingItem in line:
        pingItem = line.split(", ")
        # pingList.append(pingItem)
        # pingList.append(ping(pingItem))

    while True:
        for item in pingItem:
            if ping(item) is False:
                response = print("No response")
            else:
                response = print(verbose_ping(item))
        return response
        # pingList.append(pingItem)


def writeList():
    createList()


def main():
    print("*** START OF MAIN ***")
    createList()
    print("*** END OF MAIN ***")


if __name__ == "__main__":
    main()
