#! /usr/bin/python
import itertools
import datetime

zero = datetime.timedelta()
buckets = { "VIM" : { "" : zero, ".c" : zero, ".py" : zero, "gcc" : zero, "binutils" : zero, "avr-libc" : zero } ,"Vimperator" : { "JIRA" : zero, "" : zero } }

def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.zip_longest(a, b)

def parse(line):
     parts = line.split("   ")
     stime = parts[0]
     activity = "".join(parts[1:]).strip()
     return datetime.datetime.strptime(stime, "%a %b %d %H:%M:%S %Z %Y"), activity

def analyze (pair):
    l1, l2 = pair
    if l2 is None:
        return
    time1, activity = parse(l1)
    time2, activity2 = parse(l2)

    #print (activity + "\t : " + str(time2 - time1))
    for key in buckets:
        try:
            if str.endswith(activity, key):
                buckets[key] = buckets[key] + (time2 - time1)
        except:
            for subkey in buckets[key]:
                if subkey in activity:
                    buckets[key][subkey] = buckets[key][subkey] + (time2 - time1)


with open("/scratch/timelog") as f:
    for pair in pairwise(f):
        analyze (pair)

    for key in sorted(buckets.keys()):
        print (key.ljust(20) + " : ", end='')
        if isinstance(buckets[key], datetime.timedelta):
            v = str(buckets[key])
            print (v.rjust(20))
        else:
            print ()
            for subkey in sorted(buckets[key].keys()):
                text = subkey
                if text == '':
                    text = 'Total'
                val = buckets[key][subkey]
                print ("  " + text.ljust(18) + " : " + str(val).rjust(20))
                
 
