
# 📑 Documentação: Automação de Patching e Remediação de Vulnerabilidades (AWX)

## 1. Visão Geral

Esta solução automatiza o ciclo de correção de vulnerabilidades críticas em servidores Linux (Ubuntu/Debian) hospedados em ambiente On-Premise (VMware/WSL). A automação utiliza **Ansible** via **AWX** para orquestrar a execução de scripts Python customizados que analisam e aplicam patches de segurança.

## 2. Componentes da Solução

A solução é composta por quatro pilares principais:

* **AWX (Ansible Tower Open Source):** Interface de gerenciamento, controle de inventário e execução de jobs.
* **Script de Análise (`get_packages.py`):** Coleta informações sobre pacotes pendentes de atualização.
* **Script de Remediação (`cloud_autoupdate.py`):** Executa o `apt-get upgrade` de forma segura e identifica a necessidade de reinicialização do kernel.
* **Playbook Ansible (`run_update.yml`):** Orquestra o envio dos scripts para os hosts e gerencia o reboot.

---

## 3. Fluxo de Execução (Workflow)

O processo segue os seguintes passos técnicos:

1. **Cópia de Arquivos:** O AWX transfere os scripts Python para o diretório `/tmp` do servidor alvo.
2. **Identificação:** O sistema identifica as vulnerabilidades de pacotes.
3. **Remediação:** Aplica-se o comando `dist-upgrade` para garantir que dependências críticas e patches de kernel sejam instalados.
4. **Verificação de Kernel:** O script verifica se o arquivo `/var/run/reboot-required` existe.
5. **Reboot Condicional:** O servidor é reiniciado **apenas se** houve atualização de Kernel ou bibliotecas do sistema (evitando downtime desnecessário).

---

## 4. Configuração no AWX

Para replicar este ambiente, foram configurados:

* **Inventory:** Criado um inventário dinâmico contendo os IPs dos servidores (Ex: `172.27.34.63`).
* **Credentials:** Armazenamento seguro de chaves SSH ou usuário/senha (sudo) para acesso aos hosts.
* **Project:** Sincronizado com o repositório Git contendo o Playbook.
* **Job Template:** Configurado com o parâmetro **Forks** (para execução em massa) e **Limit** (para filtrar por grupos como QA ou PROD).

---

## 5. Como Executar para Novos Servidores

Para escalar a solução:

1. Adicione o IP do novo servidor em **Inventories > Hosts**.
2. Associe o host a um grupo (`qa_group` ou `prod_group`).
3. No **Job Template**, clique no foguete 🚀.
4. No campo **Limit**, digite o nome do grupo ou IP específico para restringir a execução.

---

## 6. Comandos de Verificação (Troubleshooting)

Para validar se a automação funcionou manualmente:

* **Verificar logs de atualização:** `cat /var/log/apt/history.log`
* **Verificar uptime (se reiniciou):** `uptime`
* **Verificar versão do Kernel:** `uname -a`

---

### O que você acha de adicionarmos um item de "Próximos Passos"?

Eu sugeriria colocar:

* *Implementação de agendamento semanal (Schedules).*
* *Envio de relatórios pós-execução via E-mail/Slack.*

**Gostaria que eu formatasse essa documentação em um arquivo Markdown (.md) para você subir no seu GitHub?** Isso conta muito ponto em portfólio!