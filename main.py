from fastapi import FastAPI
from threading import Thread
import time
import requests
import re

app = FastAPI()

cache = {}

exp = re.compile(r'Nmap scan report for (.*) \((.*)\)')


def get_nmap_data():
    result = requests.get('http://192.168.1.164/nmap')
    txt = result.text.strip()
    output = {}
    for row in txt.split('\n'):
        res = exp.match(row)
        output[res[2]] = res[1]


    return output


def update_nmap_results():
    global cache
    while True:
        cache = get_nmap_data()
        time.sleep(5)
        tmp = get_nmap_data()
        time.sleep(5)
        tmp.update(get_nmap_data())
        cache = tmp
        time.sleep(60)


thread = Thread(target=update_nmap_results, daemon=True)


@app.get("/")
def root():
    return cache


thread.start()
