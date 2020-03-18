#!/usr/bin/python3

# SPDX-FileCopyrightText: 2020 Nicolás Alvarez <nicolas.alvarez@gmail.com>
#
# SPDX-License-Identifier: MIT

import tempfile
import json
import logging

import request
import pdfconvert
import textparser

logging.basicConfig(level=logging.INFO)

logging.info("Downloading list")
pdf_urls = list(request.get_pdf_urls())
pdf_url = pdf_urls[0]
logging.info("PDF URL: %s", pdf_url)
with tempfile.NamedTemporaryFile(suffix='.pdf') as f:
    request.download_file(pdf_url, f)
    logging.info("File downloaded into %s", f.name)
    text = pdfconvert.text_from_pdf(f.name)
    logging.info("Converted into %d bytes of text", len(text))

report = textparser.parse(text)
output = {'cases': report.cases, 'deaths': report.deaths, 'source_url': pdf_url}
print(json.dumps(output))
