# SPDX-FileCopyrightText: 2020 Nicolás Alvarez <nicolas.alvarez@gmail.com>
#
# SPDX-License-Identifier: MIT

import requests
import logging
import datetime
import re
from bs4 import BeautifulSoup

sess = requests.session()

def date_from_header(header_text):
    match = re.match('Reporte Diario (?:\w+ )?/ (\d+)-(\d+)-(\d+) \(.*\)', header_text)
    if match:
        d = int(match.group(1))
        m = int(match.group(2))
        y = int(match.group(3))
        return datetime.date(y,m,d)

def get_pdfs():
    resp = sess.get("https://www.argentina.gob.ar/coronavirus/informe-diario?cache-bust=%d" % datetime.datetime.now().minute, headers={'User-Agent': 'CovidParser/0.1 (+nicolas.alvarez+covid@gmail.com)'})
    logging.info("Parsing HTML page")
    soup = BeautifulSoup(resp.content, 'html.parser')

    links = soup.find('div', class_='downloads').find_all('a')
    logging.info("Found {} links".format(len(links)))

    for elem in links:
        url = elem["href"]
        header = elem.parent.p
        header_text = header.text
        date = date_from_header(header_text)

        yield (url, date)

def download_file(url, fd):
    resp = sess.get(url, headers={'User-Agent': 'CovidParser/0.1 (+nicolas.alvarez+covid@gmail.com)'})
    for chunk in resp.iter_content(chunk_size=4096):
        fd.write(chunk)
    fd.flush()
