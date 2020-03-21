# SPDX-FileCopyrightText: 2020 Nicolás Alvarez <nicolas.alvarez@gmail.com>
#
# SPDX-License-Identifier: MIT

import subprocess
import os

os.environ['PATH'] = ".:"+os.environ['PATH']

def text_from_pdf(filename):
    proc = subprocess.run(['pdftotext', filename, '-'], capture_output=True)
    return proc.stdout.decode('utf8')
