#!/usr/bin/python3

# SPDX-FileCopyrightText: 2020 Nicolás Alvarez <nicolas.alvarez@gmail.com>
#
# SPDX-License-Identifier: MIT

import tempfile
import json

import request
import pdfconvert
import textparser

print("Downloading list")
pdf_urls = list(request.get_pdf_urls())
pdf_url = pdf_urls[0]
print("PDF URL: {}".format(pdf_url))
with tempfile.NamedTemporaryFile(suffix='.pdf') as f:
    request.download_file(pdf_url, f)
    print("File downloaded into {}".format(f.name))
    text = pdfconvert.text_from_pdf(f.name)
    print("Converted into {} bytes of text".format(len(text)))

report = textparser.parse(text)
output = {'cases': report.cases, 'deaths': report.deaths, 'source_pdf': pdf_url}
print(json.dumps(output))
