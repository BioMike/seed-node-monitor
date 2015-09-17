#!/usr/bin/env python3

import random, string

def randomword(length):
   search_string = string.ascii_letters + string.digits
   return ''.join(random.choice(search_string) for i in range(length))

part1 = randomword(10)
part2 = randomword(10)
part3 = randomword(10)

print("\n%s-%s-%s\n" % (part1, part2, part3))

