#!/usr/bin/env python
 #    textgen - utility for generating text
 #    This program is free software: you can redistribute it and/or modify
 #    it under the terms of the GNU General Public License as published by
 #    the Free Software Foundation, either version 3 of the License, or
 #    (at your option) any later version.

 #    This program is distributed in the hope that it will be useful,
 #    but WITHOUT ANY WARRANTY; without even the implied warranty of
 #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #    GNU General Public License for more details.

 #    You should have received a copy of the GNU General Public License
 #    along with this program.  If not, see <http://www.gnu.org/licenses/>.

 # Igor Tyukalov <tyukalov@bk.ru> 

from sys import argv
from re import findall
from collections import defaultdict
from random import choice
import gettext
import locale
import os

_ = gettext.gettext

VERSION      = "0.01"
PROGNAME     = "textgen"
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANG_DIR     = 'textgen/lang/'
DEFAULTPARAM = [('-d', 2),
                ('-c', 10),
                ('-e', 'utf-8')]
INTPARAM     = ('-d', '-c')
gettext.bindtextdomain(PROGNAME, os.path.join(BASE_DIR, LANG_DIR).replace('\\','/'))

gettext.textdomain(PROGNAME)

def help ():
    '''Displays help'''
    print(_("\tUsage: %s -f=filename -edchv\n")%(argv[0]))
    print(_("\tWhere:\n\
    \t -e file encoding (-e=cp1251). Default value - utf-8;\n\
\t -v or --version - displays version information;\n\
\t -h or --help - displays help;\n\
    \t -d - length of n-gram. Default value - 3;\n\
    \t -c - number of sentences. Default value - 10;\n"))
    exit(0)

def version ():
    """Displays version information"""
    print("\t%s v%s\n"%(PROGNAME, VERSION) + _('\tLicense GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>\n\
\tWritten by Igor \'sp_r00t\' Tyukalov.\n'))
    exit(0)

def fullgetpr(ws, size, count):
	ltup = list(zip(*[ws[x:] for x in range(size + 1)]))
	wdict = defaultdict(list)
	for x in ltup:
		wdict[tuple(x[:-1])].append(x[-1])
	starts = [x for x in wdict if (not '.' in x and x[0][0].upper() == x[0][0])]
	text = ""
	for _ in range(count):
		res = list(choice(starts))
		while True:
			if res[-1] == '.':
				break
			ks = tuple(res[- size:])
			res.append(choice(wdict[ks]))
		for x in res:
			text = text + x  + ' '
	return text

def argparse(arg):
    args   = [x.split('=') for x in arg[1:]]
    result = defaultdict(lambda x: x, DEFAULTPARAM)
    for x in args:
        result[x[0]] = None if len(x) < 2 else int(x[1]) if x[0] in INTPARAM else x[1]
    return result

if __name__ == '__main__':
    args=argparse(argv)
    if '-v' in args or '--version' in args:
        version()
        exit(0)
    if '-h' in args or '--help' in args:
        help()
        exit(0)
    if '-f' not in args:
        print(_("Please, enter filename (-f=filename)\n"))
        exit(-1)
    words = []
    try:
        with open(args['-f'], encoding=args['-e']) as fd:
            for s in fd:
                words += findall(r'\w+|\.', s)
    except UnicodeDecodeError:
        print(_("Please, specify the correct encoding of the file (-e=enc)\n"))
        exit(-1)
    except FileNotFoundError:
        print(_("File not found"))
        exit(-1)


    print(fullgetpr(words, args['-d'], args['-c']))
