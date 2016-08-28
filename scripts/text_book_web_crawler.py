import urllib3
import BeautifulSoup
import re, csv

url = "http://www.textfiles.com/etext/"

links = [url+"AUTHORS",url+"MODERN", url+"FICTION",url+"NONFICTION",url+"REFERENCE"]
books = []

def get_links(url):
    l = []
    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False)
    response = r.read()
    soup = BeautifulSoup.BeautifulSoup(response)
    for a in soup.findAll('a'):
        s = re.match(".*\..*$",a['href'])
        if not s:
            l.append(url+"/"+a['href'])
    return l

def get_table(url):
    data = []
    http = urllib3.PoolManager()
    r = http.request('GET', url, preload_content=False)
    response = r.read()
    if r.status != 200:
        return data
    soup = BeautifulSoup.BeautifulSoup(response)
    table = soup.find("table")

    rows = table.findAll('tr')
    for row in rows:
        cols = row.findAll('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) # Get rid of empty values
    return data

while len(links) > 0:
    l = links.pop()
    t = get_table(l)
    for row in t:
        if len(row)==3:
            books += [[l + "/" + row[0]] + row]
        else:
            links += [l + "/" + row[0]]

print books

with open("../data/books.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(books)


