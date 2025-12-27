#!/usr/bin/env python3
import os
import subprocess
import configparser

cfg = configparser.ConfigParser()
cfg.read('/etc/cloud-autoupdate/cloud-autoupdate.conf')

def validate_os():
    with open('/etc/os-release', "r") as file:
        content = file.read()
        if "rhel" in content: return "rhel"
        if "debian" in content or "ubuntu" in content or "Ubuntu" in content: return "debian"

def run_update():
    os_type = validate_os()
    if os_type == "debian":
        # Comando para forçar instalação sem pedir confirmação (Ideal para automação)
        cmd = 'export DEBIAN_FRONTEND=noninteractive ; apt-get upgrade -y -o Dpkg::Options::="--force-confold"'
        os.system(cmd)
    elif os_type == "rhel":
        os.system("yum update -y")

if __name__ == "__main__":
    run_update()
