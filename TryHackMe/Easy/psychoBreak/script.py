import os
import subprocess
import sys

f = open("random.dic", "r")

keys = f.readlines()

for key in keys:
	key = str(key.replace("\n", ""))
	print (key)
	subprocess.run(["./program", key])
