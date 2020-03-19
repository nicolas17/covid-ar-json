# SPDX-FileCopyrightText: 2020 Nicolás Alvarez <nicolas.alvarez@gmail.com>
#
# SPDX-License-Identifier: MIT

import requests
from bs4 import BeautifulSoup

sess = requests.session()

def get_pdf_urls():
    resp = sess.get("https://www.argentina.gob.ar/coronavirus/informe-diario", headers={'User-Agent': 'CovidParser/0.1 (+nicolas.alvarez+covid@gmail.com)'})
    soup = BeautifulSoup(resp.content, 'html.parser')
    for elem in soup.find('div', class_='downloads').find_all('a'):
        yield elem["href"]

def download_file(url, fd):
    resp = sess.get(url, headers={'User-Agent': 'CovidParser/0.1 (+nicolas.alvarez+covid@gmail.com)'})
    for chunk in resp.iter_content(chunk_size=4096):
        fd.write(chunk)
    fd.flush()
