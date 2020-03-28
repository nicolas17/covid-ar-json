# SPDX-FileCopyrightText: 2020 Nicolás Alvarez <nicolas.alvarez@gmail.com>
#
# SPDX-License-Identifier: MIT

import unittest
import re

from textparser import *
from pdfconvert import *
from request import *

class TestParser(unittest.TestCase):

    def test_numregex(self):
        regex = num_regex("foo")

        def do_test(text, exp1, exp2):
            m = re.match(regex, text)
            self.assertIsNotNone(m)
            self.assertEqual(m.group('foo1'), exp1)
            self.assertEqual(m.group('foo2'), exp2)

        do_test('42', '42', None)
        do_test('cuarenta y dos (42)', None, '42')
        do_test('veintiún (21)', None, '21')

    def test_parser(self):
        def do_test(text, cases, deaths):
            report = parse(text)
            self.assertEqual((report.cases, report.deaths), (cases, deaths))

        do_test("El total de casos confirmados en Argentina es de 4, de los cuales 2 fallecieron.", 4,2)
        do_test("El total de casos confirmados en Argentina es de treinta y seis (36), de los cuales dos (2) fallecieron.", 36,2)
        do_test("El total de casos confirmados en Argentina es de cuatro (4), de los cuales uno (1) falleció.", 4,1)
        do_test("A la fecha, se registran un total de 17 casos importados confirmados de COVID-19 entre los que se encuentra un (1) fallecido.", 17,1)
        do_test("A la fecha, se registran un total de diecisiete (17) casos importados confirmados de COVID-19 entre los que se encuentra un (1) fallecido.", 17,1)
        do_test("A la fecha, se registran un total de diecisiete (17) casos importados confirmados de COVID-19 entre los que se encuentran dos (2) fallecidos.", 17,2)
        do_test("En nuestro país, el total de casos es de 690. Blah blah. La tasa de letalidad en el país es del 2,1%, habiéndose registrado un total de 17 fallecidos confirmados para COVID-19.",
                690, 17)
        do_test("El total de casos confirmados en Argentina es de 690, \u200bde los cuales 17 fallecieron.", 690, 17)

    def test_parse_new(self):
        report = parse("Hoy fueron confirmados 14 nuevos casos de COVID-19:")
        self.assertEqual(report.new_cases, 14)
        report = parse("Hoy fueron confirmados nueve (9) nuevos casos de COVID-19.")
        self.assertEqual(report.new_cases, 9)

    def test_pdf(self):
        # end-to-end test
        self.assertEqual(
            parse(text_from_pdf('16-03-20-reporte-diario-covid-19_0.pdf')),
            Report(cases=65, deaths=2, new_cases=9)
        )

    def test_html_header(self):
        import datetime
        self.assertEqual(date_from_header('Reporte Diario / 19-03-2020 (283.6 Kb)'), datetime.date(2020, 3, 19))

if __name__ == '__main__':
    unittest.main()
