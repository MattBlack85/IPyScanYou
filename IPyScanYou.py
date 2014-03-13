import socket

import datetime

import os

import sys


def exception_handler(error):
    print("\nUh-oh, we got an error: %s") % error
    sys.exit("\nProgram terminated.")

def main():
    ip = False
    ports = False

    while not ip:
        ip = raw_input("\nPlease write the host you want to scan: ")
    
        try:
            ip = socket.gethostbyname(ip) if ip else False
            # OpenDNS check
            if ip == '67.215.65.132':
                raise socket.gaierror(-2,"Name or service not known")

        except socket.gaierror as e:
            exception_handler(e[1])

    while not ports:
        ports_input = raw_input("\nWrite the number of port you want to scan, " \
                                "if you want to scan a range, write the lower range and upper range " \
                                "separated by '-' symbol, if you want to scan more than one port " \
                                "write all the ports separated by ',': ")

        try:
            if not ports_input:
                continue

            elif "," in ports_input:
                try:
                    ports = [int(port) for port in ports_input.split(",") if isinstance(int(port), int)]
                except ValueError as e:
                    exception_handler(e)

            elif "-" in ports_input:
                try:
                    port_range = ports_input.split("-")
                    ports = range(int(port_range[0]), int(port_range[1])+1)
                except ValueError as e:
                    exception_handler(e)

            elif isinstance(int(ports_input), int):
                try:
                    if 0 <= int(ports_input) <= 65535:
                        ports = int(ports_input)
                    else:
                        err = "The port you enetered does not exist."
                        exception_handler(err)

                except ValueError as e:
                    exception_handler(e)

        except ValueError as e:
            exception_handler(e)

    if isinstance(ports, list):
        for port in ports:
            new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_socket.settimeout(1)

            if new_socket.connect_ex((ip, port)) == 0:
                print("\nPort %s: opened") % port

            new_socket.close()


    else: # We are going to scan just 1 port
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_socket.settimeout(1)

        if new_socket.connect_ex((ip, ports)) == 0:
            print("\nPort %s: opened") % ports

        new_socket.close()

if __name__ == "__main__":
    main()
