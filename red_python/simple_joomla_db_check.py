#!/usr/bin/python
# -*- coding: utf-8 -*-
# 2019/01/24
# Author: Red Shen <red@noc.tw>
# You have to install mysql-connector-python first.
import os, sys, re
import mysql.connector
import json

DEFAULT_TARGET = "/home/"
DEFAULT_DIR = "public_html"

class Log:
    def __init__(self):
        self.log_path = "joomla_check_result.log"
        self.msgs = []
        log_file = open(self.log_path, "w")
        log_file.close()

    def add(self, msg):
        self.msgs.append(msg)
        print(msg)
    
    def write(self):
        log_file = open(self.log_path, "a")

        for msg in self.msgs:
            log_file.write("{0}\n".format(msg))

        log_file.close()
        self.msgs = []

class Database:
    def __init__(self, config_path):
        self.name = ""
        self.prefix = ""
        self.user = ""
        self.passwd = ""
        self.joomla = False
        self.available = False
        self.success = False

        if os.path.isfile(config_path):
            config = open(config_path, "r")
            content = config.read()
            config.close()
    
            if "JConfig" in content:
                self.joomla = True

                for line in content.splitlines():
                    self.set_value(line)
                 
            if self.is_joomla():
                try:
                    if self.user != "" and self.passwd != "" and self.name != "":
                        self.cnx = mysql.connector.connect(host="localhost", user=self.user, password=self.passwd, database=self.name)
                        self.cursor = self.cnx.cursor()
                        self.available = True
                except:
                    pass
        
    def get_value(self, text, regex):
        pattern = re.compile(regex)
        result = pattern.findall(text)

        if len(result) >= 1:
            return result[0]
        else:
            return ""
        
    def set_value(self, text):
        if self.name == "":
            self.name = self.get_value(text, " \$db = '(.*?)';")
        if self.prefix == "":
            self.prefix = self.get_value(text, " \$dbprefix = '(.*?)';")
        if self.user == "":
            self.user = self.get_value(text, " \$user = '(.*?)';")
        if self.passwd == "":
            self.passwd = self.get_value(text, " \$password = '(.*?)';")

    def is_joomla(self):
        return self.joomla

    def is_available(self):
        return self.available

    def is_success(self):
        return self.success

    def execute(self, cmd):
        self.success = False

        try:
            self.cursor.execute(cmd)
            self.success = True
        except:
            pass
        
    def get_users(self):
        self.execute("SELECT * FROM {0}users".format(self.prefix))

        if self.is_success():
            users = self.cursor.fetchall()
            return len(users)
        else:
            return "N/A"

    def get_registrable(self):
        #The URL is something like: http://example.com/index.php?option=com_users&view=registration
        self.execute("SELECT params FROM {0}extensions WHERE name = 'com_users'".format(self.prefix))

        if self.is_success():
            params = self.cursor.fetchone()

            if params != None:
                json_data = json.loads(params[0])
                return json_data["allowUserRegistration"]
                
        #For Joomla 1.5:
        self.execute("SELECT params FROM {0}components WHERE `option` = 'com_users'".format(self.prefix))
        if self.is_success():
            params = self.cursor.fetchone()

            if params != None:
                return self.get_value(params[0], "allowUserRegistration=(.?)")

        return "N/A"

    def get_contacts(self):
        #The URL is something like: http://example.com/index.php/component/contact/contact/1
        self.execute("SELECT * FROM {0}contact_details WHERE published = '1' AND params LIKE '%show_email_copy%'".format(self.prefix))
        
        if self.is_success():
            contacts = self.cursor.fetchall()
            return len(contacts)
        else:
            return "N/A"

    def close(self):
        if self.is_available():
            self.cursor.close()

def simple_joomla_db_check(input_path):
    for dirname, dirnames, filenames in os.walk(input_path):
        for fn in filenames:
            if fn == "configuration.php":
                full_path = os.path.join(dirname, fn)
                db = Database(full_path)
                if db.is_joomla():
                    if db.is_available():
                        users = db.get_users()
                        registrable = db.get_registrable()
                        contacts = db.get_contacts()
                        db.close()
                        log.add("{0},{1},{2},{3},{4}".format(full_path, db.name, users, registrable, contacts))
                    else:
                        log.add("{0},{1},Failed to connect".format(full_path, db.name))

def main_loop():
    log.add("Location,Database,Users,Registrable,Contacts")
    
    if len(sys.argv) >= 2:
       input_path = os.path.expanduser(sys.argv[1])
       simple_joomla_db_check(input_path)
    else:
        for dirname in os.listdir(DEFAULT_TARGET):
            #input_path = os.path.join(DEFAULT_TARGET, dirname, DEFAULT_DIR)
            input_path = os.path.join(DEFAULT_TARGET, dirname)
            
            if os.path.isdir(input_path):
                simple_joomla_db_check(input_path)
    log.write()

if __name__ == "__main__":
    appdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(appdir)
    log = Log()
    main_loop()

