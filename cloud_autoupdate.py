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
    if os_type in ["debian", "ubuntu"]:
        cmd = 'export DEBIAN_FRONTEND=noninteractive ; apt-get update && apt-get dist-upgrade -y -o Dpkg::Options::="--force-confold"'
        # MUDANÇA AQUI: subprocess captura o texto para o Ansible ler
        resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(resultado.stdout) # Isso joga o texto no .stdout que seu YAML procura
    elif os_type == "rhel":
        resultado = subprocess.run("yum update -y", shell=True, capture_output=True, text=True)
        print(resultado.stdout)

if __name__ == "__main__":
    run_update()
