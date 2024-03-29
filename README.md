<h1 align="center">XPOSE Bot</h1>

<div align="center">
  <strong><i>A discord bot used to know if a coc player/clan is banned by a specific league or not.</i></strong>
  <br>
  <br>
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Made%20With-Python%203.8-blue.svg?style=for-the-badge&logo=Python" alt="Made with Python 3.8">
  <br>
  <a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/Code%20Style-Black-black?style=for-the-badge">
  </a>

  <a href="https://github.com/officialakhil/xpose-bot/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/license-mit-e74c3c.svg?style=for-the-badge" alt="MIT License">
  </a>
</div>
<br>

## About XPOSE Bot
XPOSE Bot is based on clash of clans and is designed specifically to help the leagues present out there encourage fair play. 
The bot helps you scan a clan/player or even scan your roster to see if there are any players banned by the league before. The bot also provides player's clan history and checks if any clan banned by the league is visited by the player in the past ... giving you info about how many days the player stayed in the clan , what role etc. 

This bot is developed by the WCL Tech Team
## Installation Instructions

### Pre-requisites
* Python v3.8.0+
* Git

### Installing Python3.8 (For Ubuntu 18.04)
Run the following as root/user with sudo access
* ```sudo apt update```
* ```sudo apt install software-properties-common```
Add the deadsnakes PPA to your system’s sources list:
* ```sudo add-apt-repository ppa:deadsnakes/ppa```
Once it's installed, install python3.8
* ```sudo apt install python3.8```

### Installing Python3.8 (For Ubuntu 20.04)
Ubuntu 20.04 is what we currently use to host the bot. 
* ```sudo apt update```
* ```sudo apt -y upgrade```
* ```python3 -v```
Returns 3.8.x (Ubuntu 20.04 gets python3.8 pre installed.)

### Installing pip
Run the following to install pip:
* ```sudo apt install python3-pip ```

### Basic Config
* Copy `config.py.example` and create a new file `config.py` and fill in all the  credentials

### Install Python Dependencies
* Navigate to the root directory
* Run `python3 -m pip install -r requirements.txt`

## Running the Bot
Start a tmux session using `tmux` and run the following:
* `python3 bot.py`

## Adding a new league Ban List
To add a ban list of any other league, the only file you would want to edit is `cogs/bancheck.py`. 
Check out the existing league's code to understand how to add a new one

### Author(s)
* Akhil Tulluri
