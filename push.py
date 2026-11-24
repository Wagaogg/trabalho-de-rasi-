#!/usr/bin/env python3
"""Commita e envia (push) este projeto para o GitHub.

Uso:  python3 push.py
Na primeira vez ele pede um token do GitHub (o link para criar aparece na tela).
O token NÃO é salvo em lugar nenhum.
"""
import base64
import getpass
import os
import subprocess
import sys

USUARIO = "Wagaogg"
EMAIL = "guedes.filho@aluno.ifsp.edu.br"
REPO = os.environ.get("REPO_URL", "https://github.com/Wagaogg/trabalho-de-rasi-.git")
BRANCH = "main"
MENSAGEM = " ".join(sys.argv[1:]) or "Adiciona projeto Flask com Docker e Docker Compose"

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def git(*args, header=None, check=True):
    cmd = ["git"]
    if header:
        cmd += ["-c", f"http.extraHeader={header}"]
    cmd += list(args)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.stdout.strip():
        print(r.stdout.strip())
    if r.returncode != 0 and r.stderr.strip():
        print(r.stderr.strip().replace(header or "\0", "***"))
    if check and r.returncode != 0:
        sys.exit(f"\nErro ao rodar: git {args[0]}")
    return r


# 1) pede o token
if REPO.startswith("http"):
    print("Precisa de um token do GitHub (Personal Access Token).")
    print("Crie em: https://github.com/settings/tokens/new?scopes=repo&description=push-rasi")
    print("(marque 'repo', clique em Generate token e copie o valor)\n")
    token = os.environ.get("GITHUB_TOKEN") or input("Cole o token aqui (botão direito do mouse = colar) e aperte Enter: ").strip()
    basic = base64.b64encode(f"{USUARIO}:{token}".encode()).decode()
    header = f"Authorization: Basic {basic}"
else:
    header = None

# 2) repositório local
if not os.path.isdir(".git"):
    git("init", "-b", BRANCH)
git("config", "user.name", USUARIO)
git("config", "user.email", EMAIL)
git("checkout", "-B", BRANCH, check=False)

# 3) garante que o .env (senhas) nunca vai
if os.path.exists(".env"):
    git("rm", "--cached", "-q", ".env", check=False)

# 4) commit
git("add", "-A")
if git("diff", "--cached", "--quiet", check=False).returncode != 0:
    git("commit", "-m", MENSAGEM)
else:
    print("Nada novo para commitar.")

# 5) remoto + junta com o que já existe no GitHub (ex.: README criado lá)
if git("remote", "get-url", "origin", check=False).returncode == 0:
    git("remote", "set-url", "origin", REPO)
else:
    git("remote", "add", "origin", REPO)
if git("fetch", "origin", BRANCH, header=header, check=False).returncode == 0:
    git("merge", f"origin/{BRANCH}", "--allow-unrelated-histories", "-X", "ours",
        "--no-edit", check=False)

# 6) push
git("push", "-u", "origin", BRANCH, header=header)
print("\nPronto! Enviado para", REPO.removesuffix(".git"))