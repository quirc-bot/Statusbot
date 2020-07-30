import QuIRC
import random
import requests
import re
import time
import random
nick = ''
username = ''
realname = ''
bot = QuIRC.IRCConnection()
room = ''
changer = ''
wiki = ''
admins = ['freenode-staff']
nspassword = ''


def getinfo():
    print('loadingconfig')
    global nick
    global username
    global realname
    global room
    global changer
    global wiki
    global admins
    global nspassword
    infofile = open('settings.csv', 'r')
    for line in infofile:
        setting = line.split(';')
        print(setting)
        if setting[0] == 'nick':
            nick = setting[1]
        if setting[0] == 'username':
           username = setting[1]
        if setting[0] == 'realname':
           realname = setting[1]
        if setting[0] == 'room':
            room = setting[1]
        if setting[0] == 'changer':
           changer = setting[1]
        if setting[0] == 'wiki':
           wiki = setting[1]
        if setting[0] == 'admins':
            admins = setting[1]
            admins = admins.split(',')
        if setting[0] == 'nspassword':
            nspassword = setting[1]

def on_connect(bot):
    bot.set_nick(nick)
    bot.send_user_packet(nick,realname)

def on_welcome(bot):
    global nspassword
    bot.send_message('NickServ', 'identify ' + nspassword)
    print('Authed to NickServ')
    time.sleep(10)
    bot.join_channel(room)
    print('Joined channels')

def on_message(
    bot,
    channel,
    sender,
    message
    ):
    global topic
    global nick
    global admins
    sendernick = sender.split('!')[0]
    senderhost = sender.split('@')[1]
    if message.lower().startswith('!online') and sendernick in admins:
        bot.send_message(changer, '\.status ' + wiki + ' online')
        bot.send_message(room, '\.topic online')
     if message.lower().startswith('!offline') and sendernick in admins:
        bot.send_message(changer, '\.status ' + wiki + ' offline')
        bot.send_message(room, '\.topic offline')
    if message.lower().startswith('!around') and sendernick in admins:
        bot.send_message(changer, '\.status ' + wiki + ' around')
        bot.send_message(room, '\.topic around')
    if message.lower().startswith('!busyon') and sendernick in admins:
        bot.send_message(changer, '\.status ' + wiki + ' busy on wiki')
        bot.send_message(room, '\.topic busy on wiki')
    if message.lower().startswith('!busyoff') and sendernick in admins:
        bot.send_message(changer, '\.status ' + wiki + ' busy off wiki')
        bot.send_message(room, '\.topic busy off wiki')
    if message.lower().startswith('!wikibreak') and sendernick in admins:
        bot.send_message(changer, '\.status ' + wiki + ' on wikibreak')
        bot.send_message(room, '\.topic on wikibreak')
    if message.lower() == '!getinfo' and sendernick in admins:
        bot.set_nick(nick + '-down')
        bot.send_message(sendernick, 'Rebuilding')
        nick = ''
        admins = ''
        nspassword = ''
        time.sleep(1)
        getinfo()
        time.sleep(1)
        bot.send_message(sendernick, 'Rebuilt')
        bot.set_nick(nick)


def on_pm(
    bot,
    sender,
    message
    ):
    global nick
    global admins
    print('Got PM')
    if message.lower().startswith('!online') and sender in admins:
        bot.send_message(changer, '\.status ' + wiki + ' online')
        bot.send_message(room, '\.topic online')
    if message.lower().startswith('!offline') and sender in admins:
        bot.send_message(changer, '\.status ' + wiki + ' offline')
        bot.send_message(room, '\.topic offline')
    if message.lower().startswith('!around') and sender in admins:
        bot.send_message(changer, '\.status ' + wiki + ' around')
        bot.send_message(room, '\.topic around')
    if message.lower().startswith('!busyon') and sender in admins:
        bot.send_message(changer, '\.status ' + wiki + ' busy on wiki')
        bot.send_message(room, '\.topic busy on wiki')
    if message.lower().startswith('!busyoff') and sender in admins:
        bot.send_message(changer, '\.status ' + wiki + ' busy off wiki')
        bot.send_message(room, '\.topic busy off wiki')
    if message.lower().startswith('!wikibreak') and sender in admins:
        bot.send_message(changer, '\.status ' + wiki + ' on wikibreak')
        bot.send_message(room, '\.topic on wikibreak')
    if message.lower() == 'getinfo' and sender in admins or message.lower() =="!getinfo" and sender in admins:
        bot.set_nick(nick + '-down')
        bot.send_message(sender, 'Rebuilding')
        nick = ''
        admins = ''
        nspassword = ''
        time.sleep(1)
        getinfo()
        time.sleep(1)
        bot.send_message(sender, 'Rebuilt')
        bot.set_nick(nick)

getinfo()
bot.on_private_message.append(on_pm)
bot.on_connect.append(on_connect)
bot.on_welcome.append(on_welcome)
bot.on_public_message.append(on_message)
print('Starting...')

bot.connect("chat.freenode.net")
print('Connected')
bot.run_loop()
