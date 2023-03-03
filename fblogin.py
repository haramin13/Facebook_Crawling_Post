from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import sys
from crawl import CollectPosts
import random
import argparse

file = open('setup.txt', 'r')
email, password, cookie = file.readlines()
email = email.strip()
password = password.strip()
cookie = cookie.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--pages', nargs='+',
                        dest="pages",
                        help="List the pages you want to scrape for recent posts")

    parser.add_argument("-d", "--depth", action="store",
                        dest="depth", default=5, type=int,
                        help="How many recent posts you want to gather -- in multiples of (roughly) 8.")

    args = parser.parse_args()

    if not args.pages:
        print("Something went wrong!")
        print(parser.print_help())
        exit()

    else:
        C = CollectPosts(ids=args.pages, file=args.pages, depth=args.depth)

        # login with account's profile
        # C.login(email, password)
        # C.collect("pages")
        # print('done')

        # login with account's cookie
        isLive = C.checkLiveCookie(cookie)
        if (isLive):
            C.collect("pages")
            print("done")
