# SPDX-FileCopyrightText: 2020 Nicolás Alvarez <nicolas.alvarez@gmail.com>
#
# SPDX-License-Identifier: MIT

import unittest
import re

import textparser

class TestParser(unittest.TestCase):

    def test_numregex(self):
        regex = textparser.num_regex("foo")

        def do_test(text, exp1, exp2):
            m = re.match(regex, text)
            self.assertIsNotNone(m)
            self.assertEqual(m.group('foo1'), exp1)
            self.assertEqual(m.group('foo2'), exp2)

        do_test('42', '42', None)
        do_test('cuarenta y dos (42)', None, '42')
        do_test('veintiún (21)', None, '21')

if __name__ == '__main__':
    unittest.main()
