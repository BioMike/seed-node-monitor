#!/usr/bin/env python3

#    seed-node-monitor: a monitor system for cryptocurrency seed nodes
#    Copyright (C) 2015  Myckel Habets
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import sqlite3
import os.path
import random, string
import time

class Database:
   def __init__(self, dbfile):
      self.db = sqlite3.connect(dbfile)
      self.cur = self.db.cursor()

   def create_database(self):
      self.cur.execute("CREATE TABLE seeds (ip_address TEXT UNIQUE, password TEXT, name TEXT, timepoint INTEGER, blocks INTEGER, connections INTEGER, difficulty REAL, nethashrate INTEGER)")
      self.cur.execute("CREATE TABLE seeds_ma (ip_address TEXT UNIQUE, password TEXT, name TEXT, timepoint INTEGER, blocks INTEGER, connections INTEGER, difficulty_sha256d REAL, difficulty_scrypt REAL, difficulty_groestl REAL, difficulty_qubit REAL, difficulty_skein REAL)")
      self.cur.execute("CREATE TABLE config (confkey TEXT UNIQUE, confval TEXT)")
      self.db.commit()
      self.set_conf("version", 2)
      self.set_conf("nettype", 0) # 0 = default, 1 = multi-algo
      self.set_conf("hooks-slack-timeout", 0)

   def update_database(self):
      version = self.get_conf("version")
      if version is False:
         print("Increasing database version to 1.")
         self.cur.execute("CREATE TABLE config (confkey TEXT UNIQUE, confval TEXT)")
         self.db.commit()
         self.set_conf("hooks-slack-timeout", 0)
         self.set_conf("version", 1)
      if version is '1':
         print("Increasing database version to 2.")
         self.cur.execute("CREATE TABLE seeds_ma (ip_address TEXT UNIQUE, password TEXT, name TEXT, timepoint INTEGER, blocks INTEGER, connections INTEGER, difficulty_sha256d REAL, difficulty_scrypt REAL, difficulty_groestl REAL, difficulty_qubit REAL, difficulty_skein REAL)")
         self.db.commit()
         # Copy over node data to the new table.
         node_data = self.get_nodes()
         now = int(time.time())
         for node in node_data:
            self.cur.execute("INSERT INTO seeds_ma (ip_address, password, name, timepoint, blocks, connections, difficulty_sha256d, difficulty_scrypt, difficulty_groestl, difficulty_qubit, difficulty_skein) VALUES (?, ?, ?, ?, 0, 0, 0, 0, 0, 0, 0)", (str(node[0]), str(node[1]), str(node[2]), now))
         self.db.commit()
         self.set_conf("version", 2)
         self.set_conf("slack-hook", 0)
      updated_version = self.get_conf("version")
      print("Database updated to version %s" % (updated_version))

   def get_conf(self, key):
      try:
         self.cur.execute('SELECT confval FROM config WHERE confkey=?', (key, ))
      except:
         # Table does not exist
         return(False)
      result = self.cur.fetchone()
      if result is None:
         return(False)
      else:
         return(result[0])
   
   def set_conf(self, key, value):
      if self.get_conf(key) is not False:
         self.cur.execute("UPDATE config SET confval=? WHERE confkey=?", (value, key))
      else:
         self.cur.execute("INSERT INTO config (confkey, confval) VALUES (?, ?)", (key, value))
      self.db.commit()

   def get_nodes(self):
      if self.get_conf("nettype") == '0':
         self.cur.execute('SELECT * FROM seeds')
      elif self.get_conf("nettype") == '1':
         self.cur.execute('SELECT * FROM seeds_ma')
      return(self.cur.fetchall())

   def insert_node(self, ip_address, name):
      search_string = string.ascii_letters + string.digits
      word1=''.join(random.choice(search_string) for i in range(10))
      word2=''.join(random.choice(search_string) for i in range(10))
      word3=''.join(random.choice(search_string) for i in range(10))
      password="%s-%s-%s" % (word1, word2, word3)
      now = int(time.time())
      self.cur.execute("INSERT INTO seeds (ip_address, password, name, timepoint, blocks, connections, difficulty, nethashrate) VALUES (?, ?, ?, ?, 0, 0, 0, 0)", (ip_address, password, name, now))
      self.cur.execute("INSERT INTO seeds_ma (ip_address, password, name, timepoint, blocks, connections, difficulty_sha256d, difficulty_scrypt, difficulty_groestl, difficulty_qubit, difficulty_skein) VALUES (?, ?, ?, ?, 0, 0, 0, 0, 0, 0)", (ip_address, password, name, now))
      self.db.commit()

   def delete_node(self, ip_address):
      self.cur.execute("DELETE FROM seeds WHERE ip_address=?", (ip_address, ))
      self.cur.execute("DELETE FROM seeds_ma WHERE ip_address=?", (ip_address, ))
      self.db.commit()

def new_node(db):
   name = input("Node name: ")
   ip_address = input("Node IP address: ")
   db.insert_node(ip_address, name)

def delete_node(db):
   name = input("Node ip address: ")
   db.delete_node(name)

def change_settings(db):
   setting = input("Setting name (nettype): ")
   value = input("New value: ")
   db.set_conf(setting, value)


parser = argparse.ArgumentParser(description='seed-node-monitor database utility')
parser.add_argument('--database', required=True, help='Database file to work on')

args = parser.parse_args()

if(os.path.isfile(args.database)):
   db = Database(args.database)
   # Update the database
   db.update_database()
   db.get_nodes()
else:
   command=''
   while(str.upper(command) != 'Y' and str.upper(command) != 'N'):
      print("Database '%s' does not exist. Do you want to create it? [Y/n]" % (args.database))
      command = input("[Y/n] ")
      if(command == ""):
         command = "Y"
   if(str.upper(command) == "Y"):
      db = Database(args.database)
      db.create_database()
      db.get_nodes()
   if(str.upper(command) == "N"):
      exit()

# start the main loop

while(True):
   command=''
   nodes = db.get_nodes()
   print("Name                       IP address       Password")
   print('-'*79)
   for node in nodes:
      if(len(node[2]) > 25):
         seed_name = node[2][0:22] + "...  "
      else:
         padding = 27 - len(node[2])
         seed_name = node[2] + (padding*' ')
      padding_ip = 17 - len(node[0])
      ip_address = node[0] + (padding_ip*' ')
      print("%s%s%s" % (seed_name, ip_address, node[1]))
   print("\n")
   command = input("Enter \'H\' for help or a command > ")
   if(str.upper(command) == "Q"):
      exit()
   if(str.upper(command) == "N"):
      new_node(db)
   if(str.upper(command) == "D"):
      delete_node(db)
   if(str.upper(command) == "S"):
      change_settings(db)
   if(str.upper(command) == "H"):
      print("\n\nHelp screen:")
      print("H\tThis help screen")
      print("N\tAdd a new node")
      print("D\tDelete a node")
      print("S\tChange a setting (use with caution!)")
      print("Q\tQuit the util\n\n")