#!/usr/bin/python3

# SPDX-FileCopyrightText: 2020 Nicolás Alvarez <nicolas.alvarez@gmail.com>
#
# SPDX-License-Identifier: MIT

import os
import re

import attr

def coalesce(*args):
    return next(x for x in args if x is not None)

@attr.s
class Report:
    cases = attr.ib()
    deaths = attr.ib()
    pdf_filename = attr.ib(default=None)


def handle_match(m):
    print(m.group(1))
    cases = int(coalesce(m.group('c1'), m.group('c2')))
    deaths = int(coalesce(m.group('d1'), m.group('d2')))
    return Report(cases=cases, deaths=deaths)

def num_regex(capture_name):
    # handles '45' and 'cuarenta y cinco (45)' and 'veintiún (21)'
    return r'((?P<{0}1>\d+)|[a-záéíóú ]+ \((?P<{0}2>\d+)\))'.format(capture_name)

def parse(filename):
    with open(filename, "r") as f:
        text = f.read().replace('\n',' ')
        m = re.search('El total de casos confi?rmados en Argenti?na es de '+num_regex('c')+'( casos)?, de los cuales '+num_regex('d')+' (fallecieron|falleció)', text)
        if m:
            return handle_match(m)

        m = re.search('se registran un total de '+num_regex('c')+' casos importados confirmados de COVID-19 entre los que se encuentran? '+num_regex('d')+' fallecidos?', text)
        if m:
            return handle_match(m)

        return None

for fn in os.listdir('.'):
    if fn.endswith('.txt'):
        print(fn)
        print(parse(fn))
        print()
