#!/usr/bin/python3

# SPDX-FileCopyrightText: 2020 Nicolás Alvarez <nicolas.alvarez@gmail.com>
#
# SPDX-License-Identifier: MIT

import tempfile
import json
import logging
import os

import request
import pdfconvert
import textparser

logging.getLogger().setLevel(logging.INFO)

aws = os.getenv('LAMBDA_TASK_ROOT')

if aws:
    import boto3
    s3 = boto3.client('s3')
    def get_file(path):
        logging.debug('reading from S3 file {}'.format(path))
        obj = s3.get_object(Bucket='nicolas17', Key=path)
        data = obj['Body'].read()
        return data
    def put_file(path, data, public=False):
        if public:
            acl='public-read'
        else:
            acl='private'
        logging.debug('uploading to S3 key {} with ACL {}'.format(path, acl))
        s3.put_object(Bucket='nicolas17', Key=path, ACL=acl, ContentType='application/json', Body=data)
else:
    def get_file(path):
        logging.debug('reading from local file {}'.format(path))
        with open(path, 'rb') as f:
            return f.read()

    def put_file(path, data, public=False):
        logging.debug('writing to local file {}'.format(path))
        with open(path, 'wb') as f:
            f.write(data)

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

    logging.info("Getting current file")
    current_data = get_file('covid-ar.json')
    if current_data == output_json:
        logging.info("File is already up to date")
    else:
        logging.info("Storing new file")
        put_file('covid-ar.json', data=output_json, public=True)
        logging.info("Done!")

    return {'result': output}

if __name__ == '__main__':
    print(handler({},{}))
