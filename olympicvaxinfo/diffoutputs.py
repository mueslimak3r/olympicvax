import os
import sys    
        
testoldstr = "testing this is working \n testing this is working 1 \n testing this isn't working \n testing this is working 3\n testing this isn't working 4"
testnewstr = "testing this is working \n testing this is working 1 \n testing this is working 2 \n testing this is working 3\n testing this is working 4"

basedir = os.path.dirname(os.path.realpath(__file__))
tmpdir = basedir + '/website-dumps/'


def diffoutputs(oldstr, newstr):
    oldSet = set(oldstr.split("\n"))
    newSet = set(newstr.split("\n"))

    outputSet = list(newSet.difference(oldSet))
    print("number of lines that diff: %d" % (len(outputSet)))
    diff = "\n\n\n\n ".join(outputSet)  # ' testing this is working 2, more things if there were...'
    print(diff)

def joind(l, sep):
    if not l:
        return ""
    li = iter(l)
    string = str(next(li))
    for i in li:
        string += str(sep) + str(i)
    return string

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

