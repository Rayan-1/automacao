#!/usr/bin/env python3
import os
import subprocess

def validate_os():
    if not os.path.exists('/etc/os-release'): return "unknown"
    with open('/etc/os-release', "r") as file:
        content = file.read().lower()
        if "rhel" in content or "centos" in content: return "rhel"
        if "debian" in content: return "debian"
        if "ubuntu" in content: return "ubuntu"

def update_apt():
    # Removi o 1>/dev/null para você ver se o update deu erro
    subprocess.run(["apt-get", "update"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    
    # Pegamos a lista, mas sem filtros agressivos primeiro para garantir que vemos algo
    cmd = 'apt list --upgradable 2>/dev/null'
    saida = subprocess.getoutput(cmd)
    
    if "Listing..." in saida and len(saida.splitlines()) <= 1:
        print("SISTEMA_OK: Nenhum pacote pendente no Debian/Ubuntu")
    else:
        print("PACOTES_PARA_ATUALIZAR:")
        print(saida)

def update_yum():
    cmd = "yum list updates -q 2>/dev/null"
    saida = subprocess.getoutput(cmd)
    
    if not saida.strip():
        print("SISTEMA_OK: Nenhum pacote pendente no RHEL")
    else:
        print("PACOTES_PARA_ATUALIZAR:")
        print(saida)

if __name__ == "__main__":
    os_type = validate_os()
    print(f"--- Verificando atualizações em: {os_type.upper()} ---")
    if os_type in ["debian", "ubuntu"]:
        update_apt()
    elif os_type == "rhel":
        update_yum()