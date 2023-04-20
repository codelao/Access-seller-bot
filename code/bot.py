import telebot
import time
import requests
import json
import datetime
import markups as btn
from telebot import types
from dbase import Database
from config import TOKEN, PUBLIC_CHANNEL_ID, PRIVATE_CHANNEL_ID,  STICKER_ID, CRYPTO_ADDRESS, MANAGER_LINK, TRANSACTION_AMOUNT, ACCESS_EXPIRY, ADMIN_ID


bot = telebot.TeleBot(TOKEN)
db = Database('bot_dbase.db')


def chat_member_status(chat_member):
    if not chat_member.status == 'left':
        return True
    else:
        return False


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        bot.send_sticker(message.chat.id, STICKER_ID, reply_markup=btn.RestartMenu)
        bot.send_message(message.chat.id, '👋 Welcome to Admin menu\nChoose an action below:', reply_markup=btn.AdminMenu)
    else:
        chat_member = bot.get_chat_member(chat_id=PUBLIC_CHANNEL_ID, user_id=message.from_user.id)
        if chat_member_status(chat_member) == True:
            bot.send_sticker(message.chat.id, STICKER_ID, reply_markup=btn.RestartMenu)
            bot.send_message(message.chat.id, '👋 Welcome\nChoose an action below:', reply_markup=btn.Action)
        else:
            bot.send_message(message.chat.id, 'You are not member of the channel\nYou can join it by pressing the button below', reply_markup=btn.JoinMenu)


@bot.message_handler()
def restart(message: types.Message):
    if message.text == 'Check':
        chat_member = bot.get_chat_member(chat_id=PUBLIC_CHANNEL_ID, user_id=message.from_user.id)
        if chat_member_status(chat_member) == True:
            start(message)
        else:
            message.reply('You are not member of the channel\nYou can join it by pressing the button below', reply_markup=btn.JoinMenu)
    elif message.text == 'Restart bot':
        restart_msg = bot.send_message(message.chat.id, 'Restarting')
        time.sleep(1)
        bot.edit_message_text(chat_id=message.chat.id, message_id=restart_msg.message_id, text='Restarting.')
        time.sleep(1)
        bot.edit_message_text(chat_id=message.chat.id, message_id=restart_msg.message_id, text='Restarting..')
        time.sleep(1)
        bot.edit_message_text(chat_id=message.chat.id, message_id=restart_msg.message_id, text='Restarting...')
        time.sleep(1)
        bot.delete_message(chat_id=message.chat.id, message_id=restart_msg.message_id)
        start(message)
    else:
        bot.send_message(message.chat.id, 'Unknown command')


@bot.callback_query_handler(func=lambda callback: callback.data == 'access')
def access(callback):
    address_msg = bot.send_message(callback.message.chat.id, 'Enter USDT TRC20 address from which you are going to make transaction\nUsers who have ever bought access before receive a discount\n/stop - cancel the operation')
    bot.register_next_step_handler(address_msg, access2)

def access2(message: types.Message):
    if not message.text == '/stop':
        if not db.check_if_blocked(user_id=message.from_user.id) == True:
            link = 'https://apilist.tronscan.org/api/account?address=' + message.text
            get_link = requests.get(link).text
            check_address = json.loads(get_link)
            if check_address == {} or check_address == {"message":"some parameters are invalid or out of range"}:
                bot.send_message(message.chat.id, 'Incorrect address entered\nMaybe this address does not exist or it is not USDT or TRC20 address', parse_mode='Markdown')
            else:
                if db.check_address(address=message.text) == True:
                    if db.check_user(user_id=message.from_user.id) == True:
                        if db.get_user_address(user_id=message.from_user.id) == message.text:
                            if db.check_user_hash(user_id=message.from_user.id) == True:
                                bot.send_message(message.chat.id, 'Send 5 USDT to `' + CRYPTO_ADDRESS + '` from your `' + message.text + '` address\nTRC20', parse_mode='Markdown', reply_markup=btn.TransactionMenu)
                            else:
                                bot.send_message(message.chat.id, 'Send 10 USDT to `' + CRYPTO_ADDRESS + '` from your `' + message.text + '` address\nTRC20', parse_mode='Markdown', reply_markup=btn.TransactionMenu)
                        else:
                            bot.send_message(message.chat.id, 'This address is already in use')
                    else:
                        bot.send_message(message.chat.id, 'This address is already in use')
                else:
                    if not db.check_user(user_id=message.from_user.id) == True:
                        db.add_user(user_id=message.from_user.id, address=message.text)
                        bot.send_message(message.chat.id, 'Send 10 USDT to `' + CRYPTO_ADDRESS + '` from your `' + message.text + '` address\nTRC20', parse_mode='Markdown', reply_markup=btn.TransactionMenu)
                    else:
                        db.add_user_address(user_id=message.from_user.id, address=message.text)

        else:
            bot.send_message(message.chat.id, 'You are blocked and not allowed to buy access\nContact the [manager](' + MANAGER_LINK + ')', parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, 'You have canceled the operation')
        time.sleep(1)
        start(message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'transaction')
def transaction(callback):
    hash_msg = bot.send_message(callback.message.chat.id, 'Enter transaction hash')
    bot.register_next_step_handler(hash_msg, transaction2)

def transaction2(message: types.Message):
    link = 'https://apilist.tronscan.org/api/transaction-info?hash=' + message.text
    get_link = requests.get(link).text
    get_hash = json.loads(get_link)
    if get_hash == {}:
        bot.send_message(message.chat.id, 'Transaction not found\nTry again or contact the [manager](' + MANAGER_LINK + ')', parse_mode='Markdown', reply_markup=btn.TransactionMenu)
    else:
        if not db.check_hash(hash=message.text) == True:
            token = get_hash['contractType']
            if not token == 31:
                bot.send_message(message.chat.id, 'Wrong token sent\nTry again or contact the [manager](' + MANAGER_LINK + ')', parse_mode='Markdown', reply_markup=btn.TransactionMenu)
            else:
                status = get_hash['contractRet']
                if not status == 'SUCCESS':
                    bot.send_message(message.chat.id, 'Unable to receive payment. Maybe transaction is pending\nTry again or contact the [manager](' + MANAGER_LINK + ')', parse_mode='Markdown', reply_markup=btn.TransactionMenu)
                else:
                    owner_address_result = get_hash['ownerAddress']
                    deposit_address_result = get_hash['tokenTransferInfo']['to_address']
                    amount_result = get_hash['tokenTransferInfo']['amount_str']
                    owner_address = db.get_user_address(user_id=message.from_user.id)
                    if owner_address_result == owner_address and deposit_address_result == CRYPTO_ADDRESS and amount_result == TRANSACTION_AMOUNT + '000000':
                        if message.chat.type == 'private':
                            save_user_id = message.from_user.id
                            db.add_user_hash(hash=message.text, user_id=save_user_id)
                            db.add_hash(hash=message.text)
                            bot.unban_chat_member(chat_id=PRIVATE_CHANNEL_ID, user_id=save_user_id)
                            channel_link = bot.create_chat_invite_link(chat_id=PRIVATE_CHANNEL_ID, member_limit=1)
                            access_msg = bot.send_message(message.chat.id, 'Payment received!\nHere is your link: ' + str(channel_link)[17:-453] + '\n*REMEMBER*\n1.Link will expire soon and you will be kicked from the channel\n2.Only 1 user can join via this link, then it will become inactive', parse_mode='Markdown')
                            time.sleep(ACCESS_EXPIRY)
                            bot.edit_message_text(chat_id=message.chat.id, message_id=access_msg.message_id, text='Link expired')
                            bot.ban_chat_member(chat_id=PRIVATE_CHANNEL_ID, user_id=save_user_id)
                    else:
                        bot.send_message(message.chat.id, 'Some transaction parameters are incorrect\nTry again or contact the [manager](' + MANAGER_LINK + ')', parse_mode='Markdown', reply_markup=btn.TransactionMenu)
        else:
            bot.send_message(message.chat.id, 'Invalid transaction', reply_markup=btn.TransactionMenu)


@bot.callback_query_handler(func=lambda callback: callback.data == 'admin_message')
def adminMessage(callback):
    bot.send_message(callback.message.chat.id, 'Select the type of message:', reply_markup=btn.MessageType)


@bot.callback_query_handler(func=lambda callback: callback.data == 'public')
def publicMessage(callback):
    msg_to_admin = bot.send_message(callback.message.chat.id, 'Enter what you want to send to the bot\'s Admin')
    bot.register_next_step_handler(msg_to_admin, publicMessage2)

def publicMessage2(message: types.Message):
    if not db.check_if_blocked(user_id=message.from_user.id) == True:
        full_date = datetime.datetime.now()
        time = full_date.time()
        message_text = 'User "' + str(message.from_user.id) + '" sent you a message at ' + str(time)[0:5] + '\nMessage says: ' + message.text
        db.add_user_message(user_id=message.from_user.id, message=message_text)
        link = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + str(ADMIN_ID) + '&text=' + message_text
        requests.post(link)
        bot.send_message(message.chat.id, 'Public message has been sent to Admin')
    else:
        bot.send_message(message.chat.id, 'You are blocked and not allowed to send messages\nContact the [manager](' + MANAGER_LINK + ')', parse_mode='Markdown')


@bot.callback_query_handler(func=lambda callback: callback.data == 'private')
def privateMessage(callback):
    msg_to_admin = bot.send_message(callback.message.chat.id, 'Enter what you want to send to the bot\'s Admin')
    bot.register_next_step_handler(msg_to_admin, privateMessage2)

def privateMessage2(message: types.Message):
    if not db.check_if_blocked(user_id=message.from_user.id) == True:
        full_date = datetime.datetime.now()
        time = full_date.time()
        message_text = 'Anonymous user sent you a message at ' + str(time)[0:5] + '\nMessage says: ' + message.text
        db.add_user_message(user_id=message.from_user.id, message=message_text)
        link = 'https://api.telegram.org/bot' + TOKEN + '/sendMessage?chat_id=' + str(ADMIN_ID) + '&text=' + message_text
        requests.post(link)
        bot.send_message(message.chat.id, 'Private message has been sent to Admin')
    else:
        bot.send_message(message.chat.id, 'You are blocked and not allowed to send messages\nContact the [manager](' + MANAGER_LINK + ')', parse_mode='Markdown')


@bot.callback_query_handler(func=lambda callback: callback.data == 'payments')
def payments(callback):
    count = db.payments_count()
    bot.send_message(callback.message.chat.id, 'Number of payments: ' + count, reply_markup=btn.AdminMenu)


@bot.callback_query_handler(func=lambda callback: callback.data == 'block')
def blockUser(callback):
    id_msg = bot.send_message(callback.message.chat.id, 'Enter id of a user you want to block\nBlocked user will no longer be able to send messages to you and buy accesses\n/stop - cancel the operation')
    bot.register_next_step_handler(id_msg, blockUser2)

def blockUser2(message: types.Message):
    if not message.text == '/stop':
        if not db.check_if_blocked(user_id=message.text) == True:
            db.block_user(user_id=message.text)
            bot.send_message(message.chat.id, 'User blocked', reply_markup=btn.AdminMenu)
        else:
            bot.send_message(message.chat.id, 'This user is already blocked', reply_markup=btn.AdminMenu)
    else:
        if message.from_user.id == ADMIN_ID:
            bot.send_message(message.chat.id, 'You have canceled the operation')
            time.sleep(1)
            start(message)
        else:
            bot.send_message(message.chat.id, 'Unknown command')


@bot.callback_query_handler(func=lambda callback: callback.data == 'unblock')
def unblockUser(callback):
    id_msg = bot.send_message(callback.message.chat.id, 'Enter id of a user you want to unblock\nUnblocked user will be able to send messages to you and buy accesses again\n/stop - cancel the operation')
    bot.register_next_step_handler(id_msg, unblockUser2)

def unblockUser2(message: types.Message):
    if not message.text == '/stop':
        if db.check_if_blocked(user_id=message.text) == True:
            db.unblock_user(user_id=message.text)
            bot.send_message(message.chat.id, 'User unblocked', reply_markup=btn.AdminMenu)
        else:
            bot.send_message(message.chat.id, 'This user is not blocked', reply_markup=btn.AdminMenu)
    else:
        if message.from_user.id == ADMIN_ID:
            bot.send_message(message.chat.id, 'You have canceled the operation')
            time.sleep(1)
            start(message)
        else:
            bot.send_message(message.chat.id, 'Unknown command')
        

if __name__ == "__main__":
    bot.polling(none_stop=True)