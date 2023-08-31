@echo off

python3 --version
if not %errorlevel% == 0 (
	cls
	echo Bot requires Python3 to be installed in your system first.
	exit /b 1
) else (
	pip3 install colorama pyTelegramBotAPI requests

	call :configuration
	if not %errorlevel% == 0 (
		exit /b 1
	) else (
		echo Done.
		exit /b 0
	)
)

:configuration
cls
echo //Configuring your own Access Seller Bot.
echo ///You must enter only correct and valid data, otherwise your bot will not work correctly.
echo 1. Your bot's token:
echo ////You can get your own bot's token from @BotFather in Telegram.
set /p "TOKEN="
echo TOKEN = '%TOKEN%' >> "config.py"
echo 2. Public Telegram channel's id:
echo ////You can get any channel and user id's from @getmyid_bot in Telegram.
set /p "PUBLIC_CHANNEL_ID="
echo PUBLIC_CHANNEL_ID = '%PUBLIC_CHANNEL_ID%' >> "config.py"
echo 3. Private Telegram channel's id:
echo ////You can get any channel and user id's from @getmyid_bot in Telegram.
set /p "PRIVATE_CHANNEL_ID="
echo PRIVATE_CHANNEL_ID = '%PRIVATE_CHANNEL_ID%' >> "config.py"
echo 4. Welcome sticker's id:
echo ////You can get any sticker id from @idstickerbot in Telegram.
set /p "STICKER_ID="
echo STICKER_ID = '%STICKER_ID%' >> "config.py"
echo 5. Bot admin's id:
echo ////You can get any channel and user id's from @getmyid_bot in Telegram.
set /p "ADMIN_ID="
echo ADMIN_ID = %ADMIN_ID% >> "config.py"
echo 6. Crypto address for receiving payments:
echo ////You must enter only USDT TRC20 address.
set /p "CRYPTO_ADDRESS="
echo CRYPTO_ADDRESS = '%CRYPTO_ADDRESS%' >> "config.py"
echo 7. Price of private channel access:
echo ////Must be specified in USDT. For example: 10, 30, 100, 5000.
set /p "TRANSACTION_AMOUNT="
echo TRANSACTION_AMOUNT = '%TRANSACTION_AMOUNT%' >> "config.py"
echo 8. Discounted price of private channel access:
echo ////Must be specified in USDT. For example: 10, 30, 100, 5000.
set /p "DISCOUNTED_TRANSACTION_AMOUNT="
echo DISCOUNTED_TRANSACTION_AMOUNT = '%DISCOUNTED_TRANSACTION_AMOUNT%' >> "config.py"
echo 9. Private channel access will expire after:
echo ////Must be specified in seconds.
set /p "EXPIRATION="
echo EXPIRATION = %EXPIRATION% >> "config.py"
