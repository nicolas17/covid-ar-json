# SPDX-FileCopyrightText: 2020 Nicolás Alvarez <nicolas.alvarez@gmail.com>
#
# SPDX-License-Identifier: MIT

import unittest
import re

from textparser import *

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
        self.assertEqual(parse("El total de casos confirmados en Argentina es de 4, de los cuales 2 fallecieron."), Report(4,2))
        self.assertEqual(parse("El total de casos confirmados en Argentina es de treinta y seis (36), de los cuales dos (2) fallecieron."), Report(36,2))
        self.assertEqual(parse("El total de casos confirmados en Argentina es de cuatro (4), de los cuales uno (1) falleció."), Report(4,1))
        self.assertEqual(parse("A la fecha, se registran un total de 17 casos importados confirmados de COVID-19 entre los que se encuentra un (1) fallecido."), Report(17,1))
        self.assertEqual(parse("A la fecha, se registran un total de diecisiete (17) casos importados confirmados de COVID-19 entre los que se encuentra un (1) fallecido."), Report(17,1))
        self.assertEqual(parse("A la fecha, se registran un total de diecisiete (17) casos importados confirmados de COVID-19 entre los que se encuentran dos (2) fallecidos."), Report(17,2))

if __name__ == '__main__':
    unittest.main()
