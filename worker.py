#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import punctuation
import subprocess
from database import DataBase
import os
import urllib.request
from urllib.parse import urlencode
import settings

class MessageWorker:
    def __init__(self, db, stop_words = 'assets/stop-word.ru'):
        self.stop_words = stop_words
        self.db = db

    def handleUpdate(self, msg):
        try:
            if msg['message']['text'] == '/stat':
                conf_id = msg['message']['chat']['id']
                user_id = msg['message']['from']['id']
                chat_title = msg['message']['chat']['title']
                self.db.add_conf(conf_id, chat_title)

                message = """Here is your top:\n"""
                top = self.db.get_top(
                    user_id=user_id,
                    conf_id=conf_id
                )
                for word in top:
                    message += '*%s*: %s\n' % (word[1], word[0])
                self.send(id=conf_id, msg=message)
                return True
        except:
            return False
        try:
            text = msg['message']['text']
            username = msg['message']['from']['username']
            try:
                last_name = msg['message']['from']['last_name']
            except:
                last_name = '_null'
            try:
                first_name = msg['message']['from']['first_name']
            except:
                first_name = '_null'
            user_id = msg['message']['from']['id']
            chat_id = msg['message']['chat']['id']
            chat_title = msg['message']['chat']['title']
            #print(self.clean_text(text))
        except:
            return False
        
        collection = self.clean_text(text)
        
        self.db.add_user(username,
            user_id,
            first_name,
            last_name)

        self.db.add_conf(chat_id, chat_title)

        for word in collection:
            self.db.add_relation(word=word, user_id=user_id, conf_id=chat_id)
        
        
    def clean_text(self, s):
        file = open(self.stop_words, 'rt')
        sw = file.read().split('\n')
        file.close()
        # dirty hack with dat fucking file
        fh = open("tmp.txt","w")
        fh.write(s)
        fh.close()
        cmd = "./assets/mystem -nlwd < tmp.txt"
        ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        output = ps.communicate()[0]
        os.remove("tmp.txt")
        # end of the fuckin' dirty hack
        s = output.decode('utf8')
        s = s.replace('?', '')
        s = s.split('\n')
        collection = []
        for word in s:
            if len(word) >2:
                if word not in sw:
                    collection.append(word)
                else:
                    pass
            else:
                pass
        return collection

    def send(self, id, msg):
        url =  settings.parser.get('bot', 'telegram_api') + \
            'bot'+ settings.parser.get('bot', 'telegram_key') \
            + '/sendMessage'
        post_fields = {
            'text': msg,
            'chat_id': id,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': 1
            }
        urllib.request.Request(url, urlencode(post_fields).encode())
        request = urllib.request.Request(url, urlencode(post_fields).encode())
        json = urllib.request.urlopen(request).read().decode()
        return json
