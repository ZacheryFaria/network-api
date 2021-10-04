from fastapi import FastAPI
import nmap
from cachetools import TTLCache, cached
from threading import Thread
import time

nm = nmap.PortScanner()

app = FastAPI()

cache = {}


def get_nmap_data():
    results = nm.scan('192.168.1.*', arguments='-sn')
    return {k: results['scan'][k]['hostnames'][0]['name'] for k in results['scan'].keys()}


def update_nmap_results():
    global cache
    while True:
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
