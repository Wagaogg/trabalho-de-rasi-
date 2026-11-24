# Containerização de uma aplicação Flask com Docker e Docker Compose

Trabalho do 4º bimestre de Redes e Administração de Sistemas (RASI) — IFSP Campus Campos do Jordão.
Técnico em Informática Integrado ao Ensino Médio.

**Autores:** Wagner Guedes Filho e Anthony Machado da Silva
**Professor:** Cesar Augusto de Moraes Costa
**Repositório de referência:** https://github.com/CesarAugusto88/RAS-Docker

## Sobre o projeto

Aplicação web em Python Flask containerizada com Docker (imagem base `python:3.14-slim`) e depois orquestrada com Docker Compose em três serviços:

| Serviço | Container | Função |
|---|---|---|
| `mysql` | `banco-mysql` | Banco de dados MySQL 8.0, com volume `dados_mysql` e healthcheck |
| `flask` | `aplicacao-flask` | Aplicação Flask (porta 5000, só interna) |
| `server` | `servidor-apache` | Apache httpd 2.4 como proxy reverso, na porta 80 |

Fluxo: Navegador → Apache (80) → Flask (5000) → MySQL (3306)

## Estrutura

```
.
├── app.py
├── compose.yaml
├── Dockerfile
├── httpd.conf
├── requirements.txt
├── .env.example
└── .gitignore
```

## Rotas

- `/` – página inicial
- `/sobre` – sobre o projeto
- `/contato` – contato
- `/alunos` – lista de alunos buscada no MySQL

## Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/[SEU-USUARIO]/[SEU-REPOSITORIO].git
   cd [SEU-REPOSITORIO]
   ```
2. Crie o arquivo `.env` a partir do exemplo e defina as senhas:
   ```bash
   cp .env.example .env
   ```
3. Suba os containers:
   ```bash
   docker compose up -d --build
   ```
4. Acesse `http://<IP-DA-VM>/` (ou `http://localhost/`).
5. Veja o estado dos serviços e derrube a stack quando quiser:
   ```bash
   docker compose ps
   docker compose down
   ```

## Ambiente utilizado

- VirtualBox com Ubuntu Server 26.04.1 LTS (2 GB de RAM, 1 CPU, rede em modo Bridge)
- Acesso remoto por SSH
- Docker 29.1.3

## Observações

- O `.env` guarda as credenciais e **não é versionado** (está no `.gitignore`). Só o `.env.example` vai para o GitHub.
- Veja o relatório técnico completo em `Relatorio_RASI_Docker_e_Docker_Compose.pdf`.
