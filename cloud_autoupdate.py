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
        # Usamos subprocess.check_output para capturar o texto da atualização
        cmd = 'export DEBIAN_FRONTEND=noninteractive ; apt-get update && apt-get dist-upgrade -y -o Dpkg::Options::="--force-confold"'
        print("Iniciando atualização crítica...")
        # O output captura todo o log da instalação (incluindo a palavra 'linux-image')
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(output) # Isso envia o texto para o update_result.stdout do Ansible
    elif os_type == "rhel":
        output = subprocess.check_output("yum update -y", shell=True, universal_newlines=True)
        print(output)
if __name__ == "__main__":
    run_update()
