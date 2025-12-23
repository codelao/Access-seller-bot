<h1 align="center">
    Access Seller Bot
</h1>

* [Usage](#usage)
* [Installation](#installation)


## Screenshots
#### As user:
<p>
  <img src="https://i.imgur.com/fOisKRp.png" width="30%"></br>
  <img src="https://i.imgur.com/WqgijTO.png" width="30%"></br>
  <img src="https://i.imgur.com/zZ5RMOb.png" width="30%"></br>
  <img src="https://i.imgur.com/z5nxXeo.png" width="30%"></br>
  <img src="https://i.imgur.com/iDU2yQl.png" width="30%"></br>
  <img src="https://i.imgur.com/AgRN7KJ.png" width="30%"></br>
</p>

#### As admin:
<p>
  <img src="https://i.imgur.com/kkj4Og4.png" width="30%"></br>
  <img src="https://i.imgur.com/cokzXTy.png" width="30%"></br>
  <img src="https://i.imgur.com/YAJtRQ6.png" width="30%"></br>
</p>

#### Other:
<p>
  <img src="https://i.imgur.com/xQBXcPC.png" width="50%"></br>
  <img src="https://i.imgur.com/IfMqxVf.png" width="50%"></br>
</p>


## Usage
This bot can be used to accept crypto payments and give an access to the private channel in Telegram. It can be also used for communication between users and bot's admin.</br>Make sure that you configured bot correctly before reporting a bug.</br>
**! Important note !**</br>
This bot uses [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/) library which doesn't directly support asynchronous running. If you need your bot to work asynchronously, I would recommend migrating to [aiogram](https://pypi.org/project/aiogram/).


## Installation
### macOS/Linux
*Note:* you need to have Python3 and Git installed in your system before moving to the bot installation steps.
1. Copy and paste this command into the Terminal:
```
git clone https://github.com/codelao/Access-seller-bot.git && cd Access-seller-bot && chmod +x configure.sh && ./configure.sh
```
2. After completing the configuration steps you'll be able to run the bot from this directory everytime by using this command:
```
./bot.py
```
*Note 2:* if you want to reconfigure your bot, you can use `./configure.sh` command in bot's directory again.

### Windows 10, 11
*Note:* you need to have Python3 and Git installed in your system before moving to the bot installation steps.
1. Copy and paste this command into the Command Prompt:
```
git clone https://github.com/codelao/Access-seller-bot.git && cd Access-seller-bot && configure
```
2. After completing the configuration steps you'll be able to run the bot from this directory everytime by using this command:
```
python3 bot.py
```
*Note 2:* if you want to reconfigure your bot, you can use `configure` command in bot's directory again.
