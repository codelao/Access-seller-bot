from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


JoinMenu = InlineKeyboardMarkup()
Join = InlineKeyboardButton(text='Join', url='https://t.me/dsfbbgnbg')
Check = InlineKeyboardButton(text='Check', callback_data='check')
JoinMenu.add(Join, Check)

AdminMenu = InlineKeyboardMarkup(row_width=2)
Payments = InlineKeyboardButton(text='Number of received payments', callback_data='payments')
Public = InlineKeyboardButton(text='Send a public message', callback_data='public')
Block = InlineKeyboardButton(text='Block user', callback_data='block')
Unblock = InlineKeyboardButton(text='Unblock user', callback_data='unblock')
AdminMenu.add(Payments)
AdminMenu.add(Public)
AdminMenu.add(Block, Unblock)

UserMenu = InlineKeyboardMarkup(row_width=1)
Access = InlineKeyboardButton(text = 'Buy access', callback_data='access')
MsgToAdmin = InlineKeyboardButton(text = 'Send a message to Admin', callback_data='msg_to_admin')
UserMenu.add(Access, MsgToAdmin)

PaymentMenu = InlineKeyboardMarkup()
Payment = InlineKeyboardButton(text='Check payment', callback_data='payment')
PaymentMenu.add(Payment)

MessageMenu = InlineKeyboardMarkup()
Reply = InlineKeyboardButton(text='Reply', callback_data='reply')
Delete = InlineKeyboardButton(text='Delete', callback_data='delete')
MessageMenu.add(Reply, Delete)
