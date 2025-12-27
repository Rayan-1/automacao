#!/usr/bin/env python3
import os
import subprocess
import configparser

# Lógica de leitura de config
cfg = configparser.ConfigParser()
cfg_path = '/etc/cloud-autoupdate/cloud-autoupdate.conf'
if os.path.exists(cfg_path):
    cfg.read(cfg_path)

def validate_os():
    with open('/etc/os-release', "r") as file:
        content = file.read()
        if "rhel" in content: return "rhel"
        if "debian" in content: return "debian"
        if "ubuntu" in content or "Ubuntu" in content: return "ubuntu"

def update_apt():
    os.system("apt-get update 1>/dev/null")
    # Aqui vai a lógica de listar pacotes do seu script original...
    cmd = 'apt list --upgradable 2>/dev/null | cut -d "/" -f 1'
    print(subprocess.getoutput(cmd))

def update_yum():
    cmd = "yum list updates 2>/dev/null | awk '{print $1}'"
    print(subprocess.getoutput(cmd))

if __name__ == "__main__":
    os_type = validate_os()
    if os_type in ["debian", "ubuntu"]:
        update_apt()
    elif os_type == "rhel":
        update_yum()
