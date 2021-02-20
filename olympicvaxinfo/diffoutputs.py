import os
import sys    

basedir = os.path.dirname(os.path.realpath(__file__))
tmpdir = basedir + '/website-dumps/'

bodylength = 500

def make_sample(diff_list = None):
    if diff_list == None:
        return ""
    ret = ""
    for iter in range(min(len(diff_list), 2)):
        body = diff_list[iter]
        truncated_str = (body[:bodylength - 3] + '...') if len(body) > bodylength else body
        ret = ret + '\n\n' + truncated_str
    return ret

def diffoutputs(oldstr, newstr, margin):
    oldList = [string.strip() for string in oldstr.splitlines()]
    oldSet = set([x for x in oldList if not x.startswith('This page was last updated')])

    newList = [string.strip() for string in newstr.splitlines()]
    newSet = set([x for x in newList if not x.startswith('This page was last updated')])

    outputSet = list(newSet.difference(oldSet))

    if len(outputSet) == 0:
        print('exact match')
        return ('exact match', "")
    elif len(outputSet) <= margin:
        print('close enough')
        return ('close enough', "")
    else:
        print('significant change')
        print("number of lines that diff: %d" % (len(outputSet)))
        ret = make_sample(sorted(outputSet, key=len, reverse=True))
        return ('significant change', ret)
    print('error')
    return ('error')

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
