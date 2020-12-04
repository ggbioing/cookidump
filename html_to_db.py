#!/usr/bin/env python
from bs4 import BeautifulSoup
import json
from PIL import Image
import urllib.request
import io
from pathlib import Path
import copy

save_path = Path('jsons')


def url_to_img(url, show=False):
    with urllib.request.urlopen(url) as u:
        f = io.BytesIO(u.read())
    img = Image.open(f)
    if show:
        img.show()
    return img


def html_to_json(html_file, save_img=False):

    with open(html_file) as f:
        soup = BeautifulSoup(f, 'html.parser')

    tags = soup.head.find_all('script')
    data = [t.string for t in tags if t.string and t.has_attr('type')]

    jdata = json.loads(data[0])
    dataLayer = json.loads(data[1].replace('dataLayer = ', ''))[0]
    jdata['dataLayer'] = dataLayer

    jid = jdata['dataLayer']['product']['id']

    with open(f'{save_path}/{jid}.json', 'w') as outfile:
        json.dump(jdata, outfile, indent=4)

    print('ok')

    lowres_url = jdata['image']
    highres_url = lowres_url.split('/')
    highres_url.pop(5)
    highres_url = '/'.join(highres_url)

    if save_img:

        imglr = url_to_img(url=lowres_url)
        imglr.save(f'{save_path}/{jid}_lr.jpg', "JPEG")

        imghr = url_to_img(url=highres_url)
        imghr.save(f'{save_path}/{jid}_hr.jpg', "JPEG")



html_files = []

with open('rlist.txt', 'r') as rlist:
    for _, r in enumerate(rlist):
        html_files.append(r.rstrip('\n'))


for _, h in enumerate(html_files):
    print(f'Processing {_}/{len(html_files)}')
    html_to_json(html_file=h, save_img=True)


print("See you!")