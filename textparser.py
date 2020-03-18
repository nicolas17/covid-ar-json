# SPDX-FileCopyrightText: 2020 Nicolás Alvarez <nicolas.alvarez@gmail.com>
#
# SPDX-License-Identifier: MIT

import os
import re
import logging

import attr

def coalesce(*args):
    return next(x for x in args if x is not None)

@attr.s
class Report:
    cases = attr.ib()
    deaths = attr.ib()
    pdf_filename = attr.ib(default=None)


def handle_match(m):
    logging.info("Matched sentence: '{}'".format(m.group(0)))
    cases = int(coalesce(m.group('c1'), m.group('c2')))
    deaths = int(coalesce(m.group('d1'), m.group('d2')))
    logging.info("Extracted info: cases:{}, deaths:{}".format(cases, deaths))
    return Report(cases=cases, deaths=deaths)

def num_regex(capture_name):
    # handles '45' and 'cuarenta y cinco (45)' and 'veintiún (21)'
    return r'((?P<{0}1>\d+)|[a-záéíóú ]+ \((?P<{0}2>\d+)\))'.format(capture_name)

def parse(text):
    text = text.replace('\n', ' ')
    m = re.search('El total de casos confi?rmados en Argenti?na es de '+num_regex('c')+'( casos)?, de los cuales '+num_regex('d')+' (fallecieron|falleció)', text)
    if m:
        return handle_match(m)

    m = re.search('se registran un total de '+num_regex('c')+' casos importados confirmados de COVID-19 entre los que se encuentran? '+num_regex('d')+' fallecidos?', text)
    if m:
        return handle_match(m)

    logging.warning("No regex matched!")

    return None

def parse_text_file(filename):
    with open(filename, "r") as f:
        return parse(f.read())
