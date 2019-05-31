import requests
from requests_html import HTMLSession
from collections import deque
import copy
import json

def main(base, start):
    session = HTMLSession()
    frontear = deque([start])
    viseted = set(start)
    c = 0
    while True:
        print("On iteraion", c, end="\r")
        if c > 100:
            break
        link = frontear.popleft()
        #print(link)
        res  = session.get(base+link)
        for link in res.html.links:
            if link[0:5] == "/wiki" and "." not in link and link not in viseted:
                #print(link)
                viseted.add(link)
                frontear.append(link)
        c += 1
    for link in list(viseted):
        print(link)  
    print("found", len(viseted),"uniq links with in depth", c)



if __name__ == "__main__":
    base = "https://sv.wikipedia.org"
    start = "/wiki/Alan_Turing"
    main(base, start)