from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen
import urllib.request
import urllib.parse
import urllib.error
import os
import time
from selenium.webdriver import Chrome
from contextlib import closing
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re
import urllib
import sys



errors = 1


#First parameter is the replacement, second parameter is your input string
def remove(s):
    chars = "qwertyuiopasdfghjklzxcvbnm'WERTYUIOPASDFGHJKLZXCVBNM \n"
    txt = ""
    for letter in s:
        if letter in chars:
            txt += letter
        else:
            txt += " "
    return txt

with open('words.txt', 'r') as g:
    words = g.readlines()

for i in range(len(words)):
    words[i] = words[i].strip().lower()

chrome_options = Options()  
chrome_options.add_argument("--headless")
chrome_options.add_argument("--mute-audio")

with closing(Chrome(chrome_options=chrome_options)) as driver:
    wait = WebDriverWait(driver,50)

    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")
    source = requests.get("https://www.youtube.com/feed/trending").text
    soup = BeautifulSoup(source, 'lxml')#.text.encode("utf-8")



    for content in soup.findAll('div', class_= "yt-lockup-content"):
        
        title = content.h3.a.text
        print("#1 on trending is: " + title)
        link = content.h3.a['href']
        print("Link: https://www.youtube.com" + link)

            

        break
    link = ""
    while not (link.startswith("https://www.youtube.com/watch?v=")):
        link = input("Insert youtube link: ")
    amount = 3
    try:
        amount = int(input("Amount of reloads to search: "))
    except ValueError:
        amount = 3
    errors = 1
    try:
        errors = int(input("Amount of errors to be displayed: "))
    except ValueError:
        errors = 1

    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()

    # Creating a BeautifulSoup object of the html page for easy extraction of data.

    soup = BeautifulSoup(webpage, 'html.parser')
    html = soup.prettify('utf-8')

    for span in soup.findAll('span',attrs={'class': 'watch-title'}):
        print("Reading from: " + span.text.strip())
        

    

    driver.get(link)
    
    for item in range(amount): #by increasing the highest range you can get more content
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(3)
    if sys.platform == "win32":
        os.system("cls")
    else:
        os.system("clear")
    mistakes = 0

    
    


    for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#comment #content-text"))):
        other = []
        cs = []
        find = comment.text.replace("’", "'")
        find = find.replace(chr(10), "\n")
        
        find = remove(find)
        for line in find.split("\n"):
            for i,word in enumerate(line.split(" ")):
                if i == 0:
                    try:
                        if not (word[0] in "QWERTYUIOPASDFGHJKLZXCVBNM") and word != "" and word != " ":
                            other.append("[Does Not Start With A Capital]")
                    except:
                        pass
                if i > 0:
                    if word == line.split(" ")[i-1] and word != "" and word  != " " and not (word.strip().lower() + "-" + word.strip().lower() in words) :

                        cs.append("[Double Word ("+ word +")]")
                if len(word) > 0:
                    if word[0] in "QWERTYUIOPASDFGHJKLZXCVBNM":
                        pass

                    else:
                        wsp = False
                        if (word.lower() in words) or (word.replace("'","").lower() in words):
                            wsp = True

                        if wsp == False:
                            cs.append("(" + word + ")")
                            

        if len(cs) >= errors:
            for mistake in sorted(other):
                print(mistake)
            for mistake in sorted(cs):
                print(mistake)
            print(comment.text)
            print("-------------------"
            mistakes += 1
        
        #print(comment.text)

    

