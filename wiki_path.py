from requests_html import HTMLSession
from collections import deque
from lib.pather import Pather
from time import sleep

import sys

MAX = 1000
def search(goal, frontier, viseted):
    # Create a session
    session = HTMLSession()
    c = 0
    while True:
        print(c,"links expanded", end="\r")
        # Max number hyper links expanded
        if c > MAX:
            break
        #dont go to fast
        sleep(0.5)
        # get next link for expantion
        link = frontier.popleft()
        # fetch the html page
        res  = session.get(base+link)
        # check all links in on the page
        for next_link in res.html.links:
            # if it dose not start with /wiki we migth leave the wikipedia
            # . is an indecation of fetching unwanted data like ".png"
            # we are not alowde to expand likes we have seen erlier (viseted)
            if next_link[0:5] == "/wiki" and "." not in next_link and "Category:" not in next_link and next_link not in viseted:
                # Add all links in current page as children
                viseted[link].children.append(next_link)

                # Add current link do viseted with the parent page
                viseted[next_link] = Pather(next_link, link)
                
                # Check if we hare reached the goal 
                if goal.lower() == next_link.lower():
                    print(f"expanded {c} links")
                    return next_link

                # Add the link on the queue for expandthon
                frontier.append(next_link)

            elif next_link in viseted:
                # Add the alternativ path for furture development
                viseted[next_link].parent.append(link)
        c += 1
    print(f"expanded {c} links")
    return None


def path(base, start, end):
    # Setup the datastuctures
    frontier = deque([start])
    viseted = {start: Pather(start)}
    result = search(end, frontier, viseted)

    # check if no path was found
    if result == None:
        print(f"unable to find a path with in {MAX} jumps")
        return

    # find an arbitrary path 
    curr = result
    depth = -1
    path = []
    while curr in viseted:
        depth += 1
        path.append(viseted[curr])
        if len(viseted[curr].parent) == 0:
            break
        curr = viseted[curr].parent[0]

    # Summury
    print(f"found {len(viseted)} uniq links")
    print(f"found at depth {depth}")
    print("\nPath: ")
    for p in reversed(path):
        print(p)
    return 


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("wiki_path <from> <to>")
    base = "https://en.wikipedia.org"
    start = "/wiki/"+sys.argv[1]
    end = "/wiki/"+ sys.argv[2]
    path(base, start, end)