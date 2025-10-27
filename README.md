# Bot para discord

Este projeto contem um simples bot para discord baseado em python pronto para deploy, o bot é feito focado em linux, porém pode ser executado em windows já que todos os requisitos também estão disponíveis para windows, irei detalhar a instalação de requisitos para o windows também porém como não é o foco não detalharei a instalação.

## Instalação de requisitos Linux

```bash
apt update & apt upgrade -y
apt install python3 python3-venv ffmpeg -y
```
## Instalação de requisitos windows
```shell
winget install ffmpeg
```
## Instalação do bot linux
```bash
cd /home
git clone https://github.com/felipegomes12/Discord-bot
cd Discord-bot
python3 -m venv venv
pip install -r requirements.txt
sudo chmod +x /home/Discord-bot/main.py
```
## Criação do token
Antes de criar o serviço é necessário o token do bot, para isso é necessário que já tenha criado uma aplicação no discord, caso não tenha criado [clique aqui](https://discord.com/developers/applications), o bot deve ser público, deve ter Message Content Intent habilitado, e as seguintes permições devem ser dadas:
* View Channels
* Send Messages
* Read Message History
* Connect
* Speak
* Use Voice Activity

Ao salvar será criado o token, guarde tanto o token como o id da aplicação.
## Adicionar o bot ao servidor
Pegue o Client ID do bot e gere o link de convite usando o modelo abaixo:
```link
https://discord.com/oauth2/authorize?client_id=SEU_CLIENT_ID_AQUI&permissions=3147776&scope=bot%20applications.commands
```
Esteja logado no discord no navegador com uma conta com permissão no servidor para adicionar aplicações.
## Configuração do .env
Cole o token ao arquivo .env
```bash
nano /home/Discord-bot/.env
```
Cole a frente da variavel:
```bash
DISCORD_TOKEN=
```
## Criação do serviço
```bash
nano /etc/systemd/system/discord-bot.service
```
```bash
[Unit]
Description=Discord Music Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/Discord-bot
ExecStart=/home/Discord-bot/venv/bin/python3 /home/Discord-bot/main.py
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```
```bahs
sudo systemctl daemon-reload
sudo systemctl enable discord-bot.service
sudo systemctl start discord-bot.service
```
## Comandos disponíveis
```bash
!play
``` 
Digite na frente o nome ou url da música que deseja tocar.
```bash
!stop
```
Para de tocar e limpa a lista de reprodução.
```bash
!skip
```
Pula a música que está sendo tocada.
```bash
!clear
```
Limpa a lista de reprodução.
```bash
!repeat song
```
Repete a música que está sendo reproduzida.
```bash
!repeat queue
```
Coloca a lista de reprodução em loop.
```bash
!rickroll
```
Toca "never gonna give you up".
## Permições
Qualquer um é livre para baixar os arquivos e alterar para suprir suas necessidades. Nenhum crédito é necessário.