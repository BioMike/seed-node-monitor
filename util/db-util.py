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
      self.db.commit()

   def get_nodes(self):
      self.cur.execute('SELECT * FROM seeds')
      return(self.cur.fetchall())

   def insert_node(self, ip_address, name):
      search_string = string.ascii_letters + string.digits
      word1=''.join(random.choice(search_string) for i in range(10))
      word2=''.join(random.choice(search_string) for i in range(10))
      word3=''.join(random.choice(search_string) for i in range(10))
      password="%s-%s-%s" % (word1, word2, word3)
      now = int(time.time())
      self.cur.execute("INSERT INTO seeds (ip_address, password, name, timepoint, blocks, connections, difficulty, nethashrate) VALUES (?, ?, ?, ?, 0, 0, 0, 0)", (ip_address, password, name, now))
      self.db.commit()

   def delete_node(self, name):
      self.cur.execute("DELETE FROM seeds WHERE name=?", (name, ))
      self.db.commit()

def new_node(db):
   name = input("Node name: ")
   ip_address = input("Node IP address: ")
   db.insert_node(ip_address, name)

def delete_node(db):
   name = input("Node name: ")
   db.delete_node(name)


parser = argparse.ArgumentParser(description='seed-node-monitor database utility')
parser.add_argument('--database', required=True, help='Database file to work on')

args = parser.parse_args()

if(os.path.isfile(args.database)):
   db = Database(args.database)
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

#start the main loop

while(True):
   command=''
   nodes = db.get_nodes()
   print("Name\tIP address\tPassword")
   for node in nodes:
      print("%s\t%s\t%s" % (node[2], node[0], node[1]))
   print("\n")
   command = input("Enter \'H\' for help or a command > ")
   if(str.upper(command) == "Q"):
      exit()
   if(str.upper(command) == "N"):
      new_node(db)
   if(str.upper(command) == "D"):
      delete_node(db)
   if(str.upper(command) == "H"):
      print("\n\nHelp screen:")
      print("H\tThis help screen")
      print("N\tAdd a new node")
      print("D\tDelete a node")
      print("Q\tQuit the util\n\n")

