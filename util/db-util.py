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

class Database:
   def __init__(self, dbfile):
      self.db = sqlite3.connect(dbfile)
      self.cur = conn.cursor()

   def get_nodes(self):
      self.cur.execute('SELECT * FROM seeds')
      print(c.fetchall())


parser = argparse.ArgumentParser(description='seed-node-monitor database utility')
parser.add_argument('--database', required=True, help='Database file to work on')

args = parser.parse_args()

if(os.path.isfile(args.database)):
   db = Database(args.database)
   db.get_nodes()
else:
   print("Database '%s' does not exist. Do you want to create it? [Y/n]" % (args.database))
   command = input("[Y/n] ")
