#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
from contextlib import closing

url = 'http://gz.ews.sellercube.com/content/eapk.apk'

with closing(requests.get(url,stream=True)) as r:
    print(int(r.headers['Content-Length'])/1024, 'kb')
    i = 0
    with open('file','wb') as f:
        for data in r.iter_content(10*1024):
            i += len(data)
            f.write(data)
            print('已下载：{}Kb'.format(i/1024))
