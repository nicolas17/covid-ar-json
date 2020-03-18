#!/usr/bin/python3

# SPDX-FileCopyrightText: 2020 Nicolás Alvarez <nicolas.alvarez@gmail.com>
#
# SPDX-License-Identifier: MIT

import tempfile
import json
import logging
import boto3

import request
import pdfconvert
import textparser

logging.getLogger().setLevel(logging.INFO)

s3 = boto3.client('s3')

def handler(event, context):
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
    output_json = json.dumps(output).encode('utf8')

    logging.info("Getting current file from S3")
    current_obj = s3.get_object(Bucket='nicolas17', Key='covid-ar.json')
    current_data = current_obj['Body'].read()
    if current_data == output_json:
        logging.info("File is already up to date")
    else:
        logging.info("Uploading to S3")
        s3.put_object(Bucket='nicolas17', Key='covid-ar.json', ACL='public-read', ContentType='application/json', Body=output_json)
        logging.info("Done!")

    return {'result': output}

if __name__ == '__main__':
    print(handler({},{}))
