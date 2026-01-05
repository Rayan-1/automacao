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
        print("Iniciando atualização crítica...")
        # EM VEZ DE os.system(cmd), USE:
        try:
            # Isso captura a saída e manda para o stdout que o seu YAML lê
            resultado = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
            print(resultado) 
        except subprocess.CalledProcessError as e:
            print(e.output)

    elif os_type == "rhel":
        # Mesma lógica para RHEL
        resultado = subprocess.check_output("yum update -y", shell=True, text=True)
        print(resultado)

if __name__ == "__main__":
    run_update()
