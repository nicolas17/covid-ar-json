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
    cases = attr.ib(default=None)
    deaths = attr.ib(default=None)
    new_cases = attr.ib(default=None)
    pdf_filename = attr.ib(default=None)

def num_regex(capture_name):
    # handles '45' and 'cuarenta y cinco (45)' and 'veintiún (21)'
    return r'((?P<{0}1>\d+)|[a-záéíóú ]+ \((?P<{0}2>\d+)\))'.format(capture_name)

def parse_main_totals(text, report):
    m = re.search('El total de casos confi?rmados en Argenti?na (a las \d+ horas de hoy )?es de '+num_regex('c')+'( casos)?(\*|\(*\)|, \(\*\))?, (de los cuales )?'+num_regex('d')+' (fallecieron|falleció)', text)
    if m:
        logging.info("Matched sentence: '{}'".format(m.group(0)))
        report.cases = int(coalesce(m.group('c1'), m.group('c2')))
        report.deaths = int(coalesce(m.group('d1'), m.group('d2')))
        return True

    m = re.search('se registran un total de '+num_regex('c')+' casos importados confirmados de COVID-19 entre los que se encuentran? '+num_regex('d')+' fallecidos?', text)
    if m:
        logging.info("Matched sentence: '{}'".format(m.group(0)))
        report.cases = int(coalesce(m.group('c1'), m.group('c2')))
        report.deaths = int(coalesce(m.group('d1'), m.group('d2')))
        return True

    return False

def parse(text):
    text = text.replace('\n', ' ')

    report = Report()

    if parse_main_totals(text, report):
        logging.info("Extracted info: cases:{}, deaths:{}".format(report.cases, report.deaths))
    else:
        logging.warning("No regex matched!")

    m = re.search('Hoy fueron confirmados '+num_regex('n')+' nuevos casos de COVID-19', text)
    if m:
        logging.info("Matched sentence: '{}'".format(m.group(0)))
        report.new_cases = int(coalesce(m.group('n1'), m.group('n2')))
        logging.info("Extracted info: new_cases:{}".format(report.new_cases))

    return report

def parse_text_file(filename):
    with open(filename, "r") as f:
        return parse(f.read())
