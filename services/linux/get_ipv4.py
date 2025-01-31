#!/usr/bin/python3
import psutil
import socket


def get_ipv4_addresses():
    """
    Realiza a consulta dos endereços IPV4 da máquina.

    Returns
    -------
    ipv4_list : list
        A lista com os endereços IPV4 identificados na máquina.
    """

    ipv4_list = []
    for interface, addresses in psutil.net_if_addrs().items():
        for address in addresses:
            if address.family == socket.AF_INET:
                ipv4_list.append((interface, address.address))
    return ipv4_list

if __name__ == "__main__":
    ipv4_addresses = get_ipv4_addresses()
    for interface, ipv4 in ipv4_addresses:
        print(f"Link: http://{ipv4}:8502")