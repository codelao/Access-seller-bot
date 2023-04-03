from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


RestartMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
Check = KeyboardButton('Check')
Restart = KeyboardButton('Restart bot')
RestartMenu.add(Check, Restart)

JoinMenu = InlineKeyboardMarkup()
Join = InlineKeyboardButton(text='Join', url='https://t.me/dsfbbgnbg')
JoinMenu.add(Join)

TransactionMenu = InlineKeyboardMarkup()
Transaction = InlineKeyboardButton(text='Check transaction', callback_data='transaction')
TransactionMenu.add(Transaction)

Action = InlineKeyboardMarkup()
BuyAccess = InlineKeyboardButton(text = 'Buy access', callback_data='access')
MsgToAdmin = InlineKeyboardButton(text = 'Message to Admin', callback_data='admin_message')
Action.add(BuyAccess, MsgToAdmin)

AdminMenu = InlineKeyboardMarkup()
ReplyToUser = InlineKeyboardButton(text='Reply user', callback_data='reply')
Payments = InlineKeyboardButton(text='Number of received payments')
BlockUser = InlineKeyboardButton(text='Block user')
AdminMenu.add(ReplyToUser, Payments, BlockUser)

MessageType = InlineKeyboardMarkup()
Public = InlineKeyboardButton(text='Public', callback_data='public')
Private = InlineKeyboardButton(text='Private', callback_data='private')
MessageType.add(Public, Private)