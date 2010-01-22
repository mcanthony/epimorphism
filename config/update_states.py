import os
import sys
import re


files = os.listdir('image')

idx = 0
files.sort()
print str(files)
for f in files:
    if(f.index(".png")):
        num = re.search("(\d)+", f).group(0)
        name = "config/state/state_%s.est" % num
        padded = ("%5d" % idx).replace(' ', '0')
        os.system("mv %s archive/state/fractal%s.est" % (name, padded)

        idx += 1
        print "processed", num, padded
        

