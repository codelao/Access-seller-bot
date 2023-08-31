#!/bin/bash

configuration() {
clear
printf "//Configuring your own Access Seller Bot.\n///You must enter only correct and valid data, otherwise your bot will not work correctly.\n"
printf "1. Your bot's token:\n////You can get your own bot's token from @BotFather in Telegram.\n"
read TOKEN
echo "TOKEN = '$TOKEN'" > "config.py"
printf "2. Public Telegram channel's id:\n////You can get any channel and user id's from @getmyid_bot in Telegram.\n"
read PUBLIC_CHANNEL_ID
echo "PUBLIC_CHANNEL_ID = '$PUBLIC_CHANNEL_ID'" >> "config.py"
printf "3. Private Telegram channel's id:\n////You can get any channel and user id's from @getmyid_bot in Telegram.\n"
read PRIVATE_CHANNEL_ID
echo "PRIVATE_CHANNEL_ID = '$PRIVATE_CHANNEL_ID'" >> "config.py"
printf "4. Welcome sticker's id:\n////You can get any sticker id from @idstickerbot in Telegram.\n"
read STICKER_ID
echo "STICKER_ID = '$STICKER_ID'" >> "config.py"
printf "5. Bot admin's id:\n////You can get any channel and user id's from @getmyid_bot in Telegram.\n"
read ADMIN_ID
echo "ADMIN_ID = $ADMIN_ID" >> "config.py"
printf "6. Crypto address for receiving payments:\n////You must enter only USDT TRC20 address.\n"
read CRYPTO_ADDRESS
echo "CRYPTO_ADDRESS = '$CRYPTO_ADDRESS'" >> "config.py"
printf "7. Price of private channel access:\n////Must be specified in USDT. For example: 10, 30, 100, 5000.\n"
read TRANSACTION_AMOUNT
echo "TRANSACTION_AMOUNT = '$TRANSACTION_AMOUNT'" >> "config.py"
printf "8. Discounted price of private channel access:\n////Must be specified in USDT. For example: 10, 30, 100, 5000.\n"
read DISCOUNTED_TRANSACTION_AMOUNT
echo "DISCOUNTED_TRANSACTION_AMOUNT = '$DISCOUNTED_TRANSACTION_AMOUNT'" >> "config.py"
printf "9. Private channel access will expire after:\n////Must be specified in seconds.\n"
read EXPIRATION
echo "EXPIRATION = $EXPIRATION" >> "config.py"
}

if ! python3 --version; then
	clear
	printf "Bot requires Python3 to be installed in your system first."
	exit 1
else
	pip3 install colorama pyTelegramBotAPI requests

	if ! configuration; then
		exit 1
	else
		chmod +x bot.py
		printf "Done.\n"
		exit 0
	fi
fi
