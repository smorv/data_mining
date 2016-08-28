import re
import os
import urllib3

BASE_DIR = "C:\cygwin\home\Francesc\code\data_mining\data"
def get_dir(d):
    check_dir = BASE_DIR
    path = d.split("/")
    for p in path[:-1]:
        check_dir = check_dir + "\\" + p
        if not os.path.exists(check_dir):
            os.makedirs(check_dir)
        return check_dir, path[-1]

def get_dest_dir(link):
    url = "http://www.textfiles.com/etext/"
    ptrn = url + "(.*)"
    t = re.match(ptrn,link)
    if t:
        return get_dir(t.group(1))
    else:
        return None, None


def download_file(link):
    dname,fname = get_dest_dir(link)
    http = urllib3.PoolManager()
    r = http.request('GET', link, preload_content=False)
    response = r.read()
    fout = open(dname + "\\" + fname,"w")
    fout.write(response)
    fout.close()

f = open("../data/books.csv","r")
flin = f.readlines()
downloaded = 0
for l in flin:
    downloaded += 1
    print "Downloading: " , downloaded
    download_file(l.split(",")[0])

print "Total downloaded: " , downloaded