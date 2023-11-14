#!/usr/bin/env python3

import os, sys, colorama, telebot, time, requests, json
import buttons as btn
from telebot import types
from dbase import Database


colorama.init()
CURRENT_PATH = os.path.dirname(__file__)
if not os.path.exists(CURRENT_PATH + '/config.py'):
    print('\033[31mYou haven\'t configured the bot yet.\033[0m')
    sys.exit(1)
from config import TOKEN, PUBLIC_CHANNEL_ID, PRIVATE_CHANNEL_ID,  STICKER_ID, ADMIN_ID, CRYPTO_ADDRESS, TRANSACTION_AMOUNT, DISCOUNTED_TRANSACTION_AMOUNT, EXPIRATION


bot = telebot.TeleBot(TOKEN)
db = Database(CURRENT_PATH + '/bot_dbase.db')

def checkTOKEN():
    try:
        bot_id = bot.get_me().id
        return bot_id
    except:
        return False

def checkAdmin():
    try:
        public_member = bot.get_chat_member(PUBLIC_CHANNEL_ID, checkTOKEN())
        private_member = bot.get_chat_member(PRIVATE_CHANNEL_ID, checkTOKEN())
        if public_member.status == 'administrator' and private_member.status == 'administrator':
            return True
        else:
            return False
    except:
        return False

def chat_member_status(chat_member):
    if not chat_member.status == 'left':
        return True
    else:
        return False

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == ADMIN_ID:
            bot.send_sticker(message.chat.id, STICKER_ID)
            bot.send_message(message.chat.id, '👋*Welcome to Admin menu*\n\nChoose an action below:', reply_markup=btn.AdminMenu, parse_mode='Markdown')
        else:
            chat_member = bot.get_chat_member(chat_id=PUBLIC_CHANNEL_ID, user_id=message.from_user.id)
            if chat_member_status(chat_member) == True:
                bot.send_sticker(message.chat.id, STICKER_ID)
                bot.send_message(message.chat.id, '👋*Welcome*\n\nThis bot accepts crypto payments and gives you access to private Telegram channel\n\nChoose an action below:', reply_markup=btn.UserMenu, parse_mode='Markdown')
            else:
                bot.reply_to(message, 'You are not a channel member\nYou can join it by pressing the button below', reply_markup=btn.JoinMenu)
    else:
        bot.send_message(message.chat.id, '_This bot cannot be used in this chat_', parse_mode='Markdown')


@bot.message_handler()
def restart(message: types.Message):
    if message.text == '/restart':
        if message.chat.type == 'private':
            restart_msg = bot.send_message(message.chat.id, 'Restarting')
            time.sleep(1)
            bot.edit_message_text(chat_id=message.chat.id, message_id=restart_msg.message_id, text='Restarting.')
            time.sleep(1)
            bot.edit_message_text(chat_id=message.chat.id, message_id=restart_msg.message_id, text='Restarting..')
            time.sleep(1)
            bot.edit_message_text(chat_id=message.chat.id, message_id=restart_msg.message_id, text='Restarting...')
            time.sleep(1)
            bot.delete_message(message.chat.id, restart_msg.message_id)
            start(message)
        else:
            bot.send_message(message.chat.id, '_This bot cannot be used in this chat_', parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, '_Unknown command_', parse_mode='Markdown')


@bot.callback_query_handler(func=lambda callback: callback.data == 'check')
def checkJoin(callback):
    chat_member = bot.get_chat_member(chat_id=PUBLIC_CHANNEL_ID, user_id=callback.from_user.id)
    if chat_member_status(chat_member) == True:
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        start(callback.message)
    else:
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'You are still not a channel member', reply_markup=btn.JoinMenu)


@bot.callback_query_handler(func=lambda callback: callback.data == 'access')
def access(callback):
    address_msg = bot.send_message(callback.message.chat.id, 'Enter *USDT TRC20* address from which you are going to make transaction\n\nℹ️Users who have ever bought access before receive a discount\n\n/stop - cancel the operation', parse_mode='Markdown')
    bot.register_next_step_handler(address_msg, access2)

def access2(message: types.Message):
    if not message.text == '/stop':
        if not db.check_if_blocked(user_id=message.from_user.id) == True:
            try:
                link = 'https://apilist.tronscan.org/api/account?address=' + message.text
                get_link = requests.get(link).text
                check_address = json.loads(get_link)
                if check_address == {} or check_address == {"message":"some parameters are invalid or out of range"}:
                    bot.send_message(message.chat.id, '_Address not found_', parse_mode='Markdown')
                else:
                    if db.check_address(address=message.text) == True:
                        if db.check_user(user_id=message.from_user.id) == True:
                            if not db.check_user_access_status(user_id=message.from_user.id) == 'yes':
                                if db.get_user_address(user_id=message.from_user.id) == message.text:
                                    if not db.check_user_hash(user_id=message.from_user.id) == None:
                                        bot.send_message(message.chat.id, 'Send *' + DISCOUNTED_TRANSACTION_AMOUNT + ' USDT* from your address `' + message.text + '`\nto `' + CRYPTO_ADDRESS + '`\n\n*TRC20*', parse_mode='Markdown', reply_markup=btn.PaymentMenu)
                                    else:
                                        bot.send_message(message.chat.id, 'Send *' + TRANSACTION_AMOUNT + ' USDT* from your address `' + message.text + '`\nto `' + CRYPTO_ADDRESS + '`\n\n*TRC20*', parse_mode='Markdown', reply_markup=btn.PaymentMenu)
                                else:
                                    bot.send_message(message.chat.id, '_This address is already in use_', parse_mode='Markdown')
                            else:
                                bot.send_message(message.chat.id, '_You already have access_', parse_mode='Markdown')
                        else:
                            bot.send_message(message.chat.id, '_This address is already in use_', parse_mode='Markdown')
                    else:
                        if not db.check_user(user_id=message.from_user.id) == True:
                            db.add_user(user_id=message.from_user.id, address=message.text, access='no')
                            bot.send_message(message.chat.id, 'Send *' + TRANSACTION_AMOUNT + ' USDT* from your address `' + message.text + '`\nto `' + CRYPTO_ADDRESS + '`\n\n*TRC20*', parse_mode='Markdown', reply_markup=btn.PaymentMenu)
                        else:
                            db.add_user_address(user_id=message.from_user.id, address=message.text)
                            if not db.check_user_hash(user_id=message.from_user.id) == None:
                                bot.send_message(message.chat.id, 'Send *' + DISCOUNTED_TRANSACTION_AMOUNT + ' USDT* from your address `' + message.text + '`\nto `' + CRYPTO_ADDRESS + '`\n\n*TRC20*', parse_mode='Markdown', reply_markup=btn.PaymentMenu)
                            else:
                                bot.send_message(message.chat.id, 'Send *' + TRANSACTION_AMOUNT + ' USDT* from your address `' + message.text + '`\nto `' + CRYPTO_ADDRESS + '`\n\n*TRC20*', parse_mode='Markdown', reply_markup=btn.PaymentMenu)
            except:
                bot.send_message(message.chat.id, '_Something went wrong_', parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, '_You are blocked and not allowed to buy accesses_', parse_mode='Markdown')
    else:
        cancel_msg = bot.reply_to(message, 'You have canceled the operation')
        time.sleep(1)
        bot.delete_message(message.chat.id, cancel_msg.message_id)
        start(message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'payment')
def transaction(callback):
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    hash_msg = bot.send_message(callback.message.chat.id, 'Enter transaction *hash*\n\n/stop - cancel the operation', parse_mode='Markdown')
    bot.register_next_step_handler(hash_msg, transaction2)

def transaction2(message: types.Message):
    if not message.text == '/stop':
        if not db.check_if_blocked(user_id=message.from_user.id) == True:
            try:
                if not db.check_user_access_status(user_id=message.from_user.id) == 'yes':
                    link = 'https://apilist.tronscan.org/api/transaction-info?hash=' + message.text
                    get_link = requests.get(link).text
                    get_hash = json.loads(get_link)
                    if get_hash == {}:
                        bot.send_message(message.chat.id, '_Transaction not found_\n\nTry again later', parse_mode='Markdown', reply_markup=btn.TransactionMenu)
                    else:
                        if not db.check_hash(hash=message.text) == True:
                            token = get_hash['contractType']
                            if not token == 31:
                                bot.send_message(message.chat.id, '_Wrong token sent_', parse_mode='Markdown', reply_markup=btn.TransactionMenu)
                            else:
                                status = get_hash['contractRet']
                                if not status == 'SUCCESS':
                                    bot.send_message(message.chat.id, '_Unable to receive payment_\nMaybe transaction is pending\n\nTry again later', parse_mode='Markdown', reply_markup=btn.TransactionMenu)
                                else:
                                    owner_address_result = get_hash['ownerAddress']
                                    deposit_address_result = get_hash['tokenTransferInfo']['to_address']
                                    amount_result = get_hash['tokenTransferInfo']['amount_str']
                                    owner_address = db.get_user_address(user_id=message.from_user.id)
                                    if not db.check_user_hash(user_id=message.from_user.id) == None:
                                        if owner_address_result == owner_address and deposit_address_result == CRYPTO_ADDRESS and amount_result == DISCOUNTED_TRANSACTION_AMOUNT + '000000':
                                            save_user_id = message.from_user.id
                                            db.add_user_hash(hash=message.text, user_id=save_user_id)
                                            db.add_user_access_status(access='yes', user_id=save_user_id)
                                            db.add_hash(hash=message.text)
                                            bot.unban_chat_member(chat_id=PRIVATE_CHANNEL_ID, user_id=save_user_id)
                                            channel_link = bot.create_chat_invite_link(chat_id=PRIVATE_CHANNEL_ID, member_limit=1)
                                            access_msg = bot.send_message(message.chat.id, '*Payment received!*\n\nHere is your link: ' + channel_link.invite_link + '\n\n*INFO*\n•After your access expires this link will also expire and you will be kicked from private channel\n•Only 1 user can join via this link and then it will become inactive', parse_mode='Markdown')
                                            time.sleep(EXPIRATION)
                                            db.add_user_access_status(access='no', user_id=save_user_id)
                                            bot.edit_message_text(chat_id=message.chat.id, message_id=access_msg.message_id, text='_Link expired_', reply_markup=btn.UserMenu, parse_mode='Markdown')
                                            bot.ban_chat_member(chat_id=PRIVATE_CHANNEL_ID, user_id=save_user_id)
                                        else:
                                            bot.send_message(message.chat.id, '_Some transaction parameters are wrong_', parse_mode='Markdown', reply_markup=btn.TransactionMenu)
                                    else:
                                        if owner_address_result == owner_address and deposit_address_result == CRYPTO_ADDRESS and amount_result == TRANSACTION_AMOUNT + '000000':
                                            save_user_id = message.from_user.id
                                            db.add_user_hash(hash=message.text, user_id=save_user_id)
                                            db.add_user_access_status(access='yes', user_id=save_user_id)
                                            db.add_hash(hash=message.text)
                                            bot.unban_chat_member(chat_id=PRIVATE_CHANNEL_ID, user_id=save_user_id)
                                            channel_link = bot.create_chat_invite_link(chat_id=PRIVATE_CHANNEL_ID, member_limit=1)
                                            access_msg = bot.send_message(message.chat.id, '*Payment received!*\n\nHere is your link: ' + channel_link.invite_link + '\n\n*INFO*\n•After your access expires this link will also expire and you will be kicked from private channel\n•Only 1 user can join via this link and then it will become inactive', parse_mode='Markdown')
                                            time.sleep(EXPIRATION)
                                            db.add_user_access_status(access='no', user_id=save_user_id)
                                            bot.edit_message_text(chat_id=message.chat.id, message_id=access_msg.message_id, text='_Link expired_', reply_markup=btn.UserMenu, parse_mode='Markdown')
                                            bot.ban_chat_member(chat_id=PRIVATE_CHANNEL_ID, user_id=save_user_id)
                                        else:
                                            bot.send_message(message.chat.id, '_Some transaction parameters are wrong_', parse_mode='Markdown', reply_markup=btn.TransactionMenu)
                        else:
                            bot.send_message(message.chat.id, '_Invalid transaction_', reply_markup=btn.TransactionMenu, parse_mode='Markdown')
                else:
                    bot.send_message(message.chat.id, '_You already have access_', parse_mode='Markdown')
            except:
                bot.send_message(message.chat.id, '_Something went wrong_', parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, '_You are blocked and not allowed to buy accesses_', parse_mode='Markdown')
    else:
        cancel_msg = bot.reply_to(message, 'You have canceled the operation')
        time.sleep(1)
        bot.delete_message(message.chat.id, cancel_msg.message_id)
        start(message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'msg_to_admin')
def adminMessage(callback):
    if bool(db.check_user_msg(user_id=callback.message.chat.id)) == False:
        msg_to_admin = bot.send_message(callback.message.chat.id, 'Enter your message to Admin\n\n/stop - cancel the operation')
        bot.register_next_step_handler(msg_to_admin, adminMessage2)
    else:
        bot.send_message(callback.message.chat.id, 'You already have a queued message to Admin\nWait for the response before sending a new one')

def adminMessage2(message: types.Message):
    if not message.text == '/stop':
        if not db.check_if_blocked(user_id=message.from_user.id) == True:
            try:
                if message.content_type == 'text':
                    message_text = '*New message received:*\n' + message.text + '\n\n👤' + message.from_user.username + ' (' + str(message.from_user.id) + ')'
                    bot.send_message(ADMIN_ID, message_text, reply_markup=btn.MessageMenu, parse_mode='Markdown')
                    db.add_user_msg(user_id=message.from_user.id, username=message.from_user.username)
                    bot.send_message(message.chat.id, 'Message has been sent to bot\'s Admin')
                else:
                    bot.send_message(message.chat.id, 'You\'ve sent: '+message.content_type+'\nExpected: text')
            except:
                bot.send_message(message.chat.id, '_Something went wrong_', parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, '_You are blocked and not allowed to send messages to Admin_', parse_mode='Markdown')
    else:
        cancel_msg = bot.reply_to(message, 'You have canceled the operation')
        time.sleep(1)
        bot.delete_message(message.chat.id, cancel_msg.message_id)
        start(message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'reply')
def replyToMessage(callback):
    global username
    global user_id
    username = callback.message.text.split()[5][1:]
    user_id = callback.message.text.split()[6][1:-1]
    bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
    reply_text = bot.send_message(callback.message.chat.id, 'Enter your reply to ' + username + '\n\n/stop - cancel the operation')
    bot.register_next_step_handler(reply_text, replyToMessage2)

def replyToMessage2(message: types.Message):
    if not message.text == '/stop':
        try:
            if message.content_type == 'text':
                message_text = '*Reply received:*\n' + message.text + '\n\n👤Admin'
                bot.send_message(user_id, message_text, parse_mode='Markdown')
                bot.send_message(message.chat.id, 'Reply has been sent to ' + username)
                db.remove_user_msg(user_id=user_id)
            else:
                bot.send_message(message.chat.id, 'You\'ve sent: '+message.content_type+'\nExpected: text')
        except:
            bot.send_message(message.chat.id, '_Something went wrong_', parse_mode='Markdown')
    else:
        cancel_msg = bot.reply_to(message, 'You have canceled the operation')
        time.sleep(1)
        bot.delete_message(message.chat.id, cancel_msg.message_id)
        start(message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'delete')
def deleteMessage(callback):
    user_id = callback.message.text.split()[6][1:-1]
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    db.remove_user_msg(user_id=user_id)


@bot.callback_query_handler(func=lambda callback: callback.data == 'payments')
def payments(callback):
    count = db.payments_count()
    bot.send_message(callback.message.chat.id, 'Number of payments: *' + str(count) + '*', parse_mode='Markdown')


@bot.callback_query_handler(func=lambda callback: callback.data == 'public')
def publicMessage(callback):
    msg_to_all = bot.send_message(callback.message.chat.id, 'Enter your public message\n\n/stop - cancel the operation')
    bot.register_next_step_handler(msg_to_all, publicMessage2)

def publicMessage2(message: types.Message):
    if not message.text == '/stop':
        try:
            if message.content_type == 'text':
                message_text = '*Public message received:*\n' + message.text + '\n\n👤Admin'
                all_users = db.get_all_users()
                for ids in all_users:
                    bot.send_message(ids[0], message_text, parse_mode='Markdown')
                bot.send_message(message.chat.id, 'Public message has been sent to all saved bot\'s users')
            elif message.content_type == 'photo':
                global photo
                photo = message.photo[-1].file_id
                caption_msg = bot.send_message(message.chat.id, 'Add a caption to your photo\n\n/no_caption - send photo without caption')
                bot.register_next_step_handler(caption_msg, publicMessage3)
            else:
                bot.send_message(message.chat.id, 'You\'ve sent: '+message.content_type+'\nExpected: text or photo')                
        except:
            bot.send_message(message.chat.id, '_Something went wrong_', parse_mode='Markdown')
    else:
        cancel_msg = bot.reply_to(message, 'You have canceled the operation')
        time.sleep(1)
        bot.delete_message(message.chat.id, cancel_msg.message_id)
        start(message)

def publicMessage3(message: types.Message):
    try:
        if message.content_type == 'text':
            message_text = '*Public message received:*\n' + message.text + '\n\n👤Admin'
            all_users = db.get_all_users()
            if not message.text == '/no_caption':
                for ids in all_users:
                    bot.send_photo(ids[0], photo, caption=message_text, parse_mode='Markdown')
            else:
                for ids in all_users:
                    bot.send_photo(ids[0], photo)
            bot.send_message(message.chat.id, 'Public message has been sent to all saved bot\'s users')
        else:
            bot.send_message(message.chat.id, 'You\'ve sent: '+message.content_type+'\nExpected: text')
    except:
        bot.send_message(message.chat.id, '_Something went wrong_', parse_mode='Markdown')


@bot.callback_query_handler(func=lambda callback: callback.data == 'block')
def blockUser(callback):
    id_msg = bot.send_message(callback.message.chat.id, 'Enter id of a user you want to block\n\nℹ️Blocked user will no longer be able to send messages to you and buy accesses\n\n/stop - cancel the operation')
    bot.register_next_step_handler(id_msg, blockUser2)

def blockUser2(message: types.Message):
    if not message.text == '/stop':
        if str(message.text).isnumeric() == True:
            if not db.check_if_blocked(user_id=message.text) == True:
                db.block_user(user_id=message.text)
                bot.send_message(message.chat.id, 'User blocked', reply_markup=btn.AdminMenu)
            else:
                bot.send_message(message.chat.id, '_This user is already blocked_', reply_markup=btn.AdminMenu, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, '_Incorrect id_', parse_mode='Markdown')
    else:
        cancel_msg = bot.reply_to(message, 'You have canceled the operation')
        time.sleep(1)
        bot.delete_message(message.chat.id, cancel_msg.message_id)
        start(message)


@bot.callback_query_handler(func=lambda callback: callback.data == 'unblock')
def unblockUser(callback):
    id_msg = bot.send_message(callback.message.chat.id, 'Enter id of a user you want to unblock\n\nℹ️Unblocked user will be able to send messages to you and buy accesses again\n\n/stop - cancel the operation')
    bot.register_next_step_handler(id_msg, unblockUser2)

def unblockUser2(message: types.Message):
    if not message.text == '/stop':
        if str(message.text).isnumeric() == True:
            if db.check_if_blocked(user_id=message.text) == True:
                db.unblock_user(user_id=message.text)
                bot.send_message(message.chat.id, 'User unblocked', reply_markup=btn.AdminMenu)
            else:
                bot.send_message(message.chat.id, '_This user is not blocked_', reply_markup=btn.AdminMenu, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, '_Incorrect id_', parse_mode='Markdown')
    else:
        cancel_msg = bot.reply_to(message, 'You have canceled the operation')
        time.sleep(1)
        bot.delete_message(message.chat.id, cancel_msg.message_id)
        start(message)


if __name__ == "__main__":
    if not checkTOKEN() == False:
        if checkAdmin() == True:
            print('\033[32mBot is ready for use.\033[0m')
            bot.polling(none_stop=True)
        else:
            print('\033[31mGive admin rights to bot in specified Telegram channels first.\033[0m')
            sys.exit(1)
    else:
        print('\033[31mInvalid bot\'s TOKEN.\033[0m')
        sys.exit(1)
