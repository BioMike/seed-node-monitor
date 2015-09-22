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



import random, string

def randomword(length):
   search_string = string.ascii_letters + string.digits
   return ''.join(random.choice(search_string) for i in range(length))

part1 = randomword(10)
part2 = randomword(10)
part3 = randomword(10)

print("\n%s-%s-%s\n" % (part1, part2, part3))

