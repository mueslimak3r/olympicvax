import os
import sys    

basedir = os.path.dirname(os.path.realpath(__file__))
tmpdir = basedir + '/website-dumps/'

margin = 2

def diffoutputs(oldstr, newstr):
    oldList = [string.strip() for string in oldstr.splitlines()]
    oldSet = set([x for x in oldList if not x.startswith('This page was last updated')])

    newList = [string.strip() for string in newstr.splitlines()]
    newSet = set([x for x in newList if not x.startswith('This page was last updated')])

    outputSet = list(newSet.difference(oldSet))

    if len(outputSet) == 0:
        print('exact match')
        return (False)
    elif len(outputSet) < margin:
        print('close enough')
        return (False)
    else:
        print('significant change')
        print("number of lines that diff: %d" % (len(outputSet)))
        #print("\n\n\n\n ".join(outputSet))
        return (True)
    print('weird error')
    return (False)

def run_test(oldname, newname):
    oldfile = open(oldname, 'r')
    oldstr = "\n".join(oldfile.read().splitlines()[2:-2])
    
    newfile = open(newname, 'r')
    newstr = "\n".join(newfile.read().splitlines()[2:-2])
    diffoutputs(oldstr, newstr)

if __name__ == '__main__':
    print(f"Arguments count: {len(sys.argv)}")
    if len(sys.argv) != 3:
        print("see if files differ by more than a margin - usage: diffoutputs.py oldfile newfile")
        exit()

    oldfile = sys.argv[1]
    newfile = sys.argv[2]
    run_test(oldfile, newfile)
