import os
import sys
from threading import Thread

import flask
from flask import make_response, send_file, render_template
import requests as r
import time
import random
import json
from urllib.request import Request, urlopen

nl = '\n'

def clr(txt='?', ri='w', fse=0):
    if fse == 2:
        return '\033[0m'
    clrs = 'drgybmcw'
    if len(ri) == 1:
        i = f'1{ri}d'
    elif len(ri) == 2:
        i = f'1{ri}'
    else:
        i = ri
    if fse == 1:
        return f'\033[{i[0]};{int(clrs.index(i[1].lower())) + (30 if i[1].isupper() else 90)};{int(clrs.index(i[2].lower())) + 40}m'
    return f'\033[{i[0]};{int(clrs.index(i[1].lower())) + (30 if i[1].isupper() else 90)};{int(clrs.index(i[2].lower())) + 40}m{txt}\033[0m'


def hit(txt, bc=' ', sa=5, cs=0, ol=False, font=0, rep=''):
    if rep == '':
        rep = '█╔╗╚╝═║╦'
    hitdata = [[
        [
            ' 000002 ', '0000002 ', ' 000002 ', '0000002 ', '00000002',
            '00000002', ' 0000002 ', '002  002', '002', '     002', '002  002',
            '002     ', '0002   0002', '0002  002', ' 000002 ', '0000002 ',
            ' 0000002 ', '0000002 ', ' 0000002', '000000002', '002   002',
            '002   002', '002       002', '002  002', '002   002', '00000002',
            ' 000002 ', '  0002  ', '0000002 ', '0000002 ', '  002002',
            '00000002', ' 000002 ', '00000002', ' 000002 ', ' 000002 ', '002',
            '002002', ' 00000002', '002 002', '  002', '002  ', '      ',
            '       ', '       ', '00002', '00002', '002', '002', '002',
            '   002 002 ', '   ', '   ', '  002', '002  ', '    002',
            ' 000002 '
        ],
        [
            '00155002', '00155002', '00155002', '00155002', '00155554',
            '00155554', '00155554 ', '006  006', '006', '     006', '006 0014',
            '006     ', '00002 00006', '00002 006', '00155002', '00155002',
            '001555002', '00155002', '00155554', '355001554', '006   006',
            '006   006', '006  002  006', '30020014', '3002 0014', '35555006',
            '00155002', ' 00006  ', '35555002', '35555002', ' 0014006',
            '00155554', '0015554 ', '35555006', '00155002', '00155002', '006',
            '306306', '001001554', '3540014', ' 0014', '3002 ', '      ',
            '0000002', '  002  ', '00154', '35006', '354', '354', '306',
            '00000000002', '   ', '   ', ' 0014', '3002 ', '   0014',
            '00155002'
        ],
        [
            '00000006', '00000074', '006  354', '006  006', '000002  ',
            '000002  ', '006  002 ', '00000006', '006', '     006', '0000054 ',
            '006     ', '00100001006', '001002006', '006  006', '00000014',
            '006002006', '00000014', '3000002 ', '   006   ', '006   006',
            '3002 0014', '3002000020014', ' 300014 ', ' 3000014 ', '  000154',
            '006  006', '001006  ', '  000154', ' 0000014', '0014 006',
            '0000002 ', '0000002 ', '    0014', '30000014', '30000006', '006',
            ' 34 34', '30000002 ', '  0014 ', '0014 ', ' 3002', '000002',
            '3555554', '0000002', '006  ', '  006', '   ', '   ', ' 34',
            '35001500154', '   ', '   ', '0014 ', ' 3002', '  0014 ',
            '35400014'
        ],
        [
            '00155006', '00155002', '006  002', '006  006', '001554  ',
            '001554  ', '006  3002', '00155006', '006', '002  006', '0015002 ',
            '006     ', '00630014006', '006300006', '006  006', '0015554 ',
            '300000014', '00155002', ' 3555002', '   006   ', '006   006',
            ' 3000014 ', ' 00001500006 ', ' 001002 ', '  30014  ', '001554  ',
            '006  006', '354006  ', '001554  ', ' 3555002', '00000006',
            '35555002', '00155002', '   0014 ', '00155002', ' 3555006', '354',
            '      ', ' 35001002', ' 0014  ', '3002 ', ' 0014', '355554',
            '0000002', '3500154', '006  ', '  006', '002', '   ', '   ',
            '00000000002', '002', '   ', '3002 ', ' 0014', ' 0014  ',
            '   3554 '
        ],
        [
            '006  006', '00000074', '30000014', '00000014', '00000002',
            '006     ', '300000014', '006  006', '006', '30000014', '006 3002',
            '00000002', '006 354 006', '006 30006', '30000014', '006     ',
            ' 3500154 ', '006  006', '00000014', '   006   ', '300000014',
            '  30014  ', ' 30014 30014 ', '00143002', '   006   ', '00000002',
            '30000014', '00000002', '00000002', '00000014', '35555006',
            '00000014', '30000014', '  0014  ', '30000014', ' 0000014', '002',
            '      ', '000000014', '0014002', ' 3002', '0014 ', '      ',
            '3555554', '  354  ', '00002', '00006', '306', '002', '   ',
            '30015001554', '306', '002', ' 3002', '0014 ', '0014   ',
            '   002  '
        ],
        [
            '354  354', '3555554 ', ' 355554 ', '3555554 ', '35555554',
            '354     ', ' 3555554 ', '354  354', '354', ' 355554 ', '354  354',
            '35555554', '354     354', '354  3554', ' 355554 ', '354     ',
            '   354   ', '354  354', '3555554 ', '   354   ', ' 3555554 ',
            '   354   ', '  354   354  ', '354  354', '   354   ', '35555554',
            ' 355554 ', '35555554', '35555554', '3555554 ', '     354',
            '3555554 ', ' 355554 ', '  354   ', ' 355554 ', ' 355554 ', '354',
            '      ', '35555554 ', '354 354', '  354', '354  ', '      ',
            '       ', '       ', '35554', '35554', ' 34', '354', '   ',
            ' 354 354   ', ' 34', '354', '  354', '354  ', '354    ',
            '   354  '
        ], 6
    ]]
    hitchars = list(
        'abcdefghijklmnopqrstuvwxyz0123456789!"$%()-=+[];:\'#,.<>/?')
    if ol:
        ot = [[] for _ in range(hitdata[font][-1])]
        for i in txt.lower():
            for j in range(hitdata[font][-1]):
                if i in hitchars:
                    ot[j].append(hitdata[font][j][hitchars.index(i)] +
                                 ' ' * cs)
                elif i == ' ':
                    ot[j].append(' ' * sa)
        return [[
            j.replace(' ',
                      bc).replace('0', rep[0]).replace('1', rep[1]).replace(
                          '2', rep[2]).replace('3', rep[3]).replace(
                              '4', rep[4]).replace('5', rep[5]).replace(
                                  '6', rep[6]).replace('7', rep[7]) for j in i
        ] for i in ot]
    ot = ['' for _ in range(hitdata[font][-1])]
    for i in txt.lower():
        for j in range(hitdata[font][-1]):
            if i in hitchars:
                ot[j] += hitdata[font][j][hitchars.index(i)] + ' ' * cs
            elif i == ' ':
                ot[j] += ' ' * sa
    return '\n'.join(ot).replace(' ', bc).replace('0', rep[0]).replace(
        '1', rep[1]).replace('2', rep[2]).replace('3', rep[3]).replace(
            '4', rep[4]).replace('5',
                                 rep[5]).replace('6',
                                                 rep[6]).replace('7', rep[7])


def gtxt(txt, ingclrs, gdir=0):
    gclrs, f, clrl = ingclrs.split(','), '', []
    if gdir == 1:
        gclrs = gclrs[:len(txt[0])]
        for i in gclrs:
            clrl.extend([i for _ in range(len(txt[0]) // len(gclrs))])
        clrl.extend([gclrs[-1] for _ in range(len(txt[0]) - len(clrl))])
        for i in txt:
            for n, j in enumerate(i):
                f += f"{clr(j, clrl[n])}"
            f += '\n'
        f = f[:-1]
    elif gdir == 2 or gdir == 3:
        gclrs = gclrs[:len(txt[0])]
        clrl.extend([gclrs[0] for _ in range(len(txt) // 2)])
        for i in gclrs:
            clrl.extend([i for _ in range(len(txt[0]) // len(gclrs))])
        clrl.extend([gclrs[-1] for _ in range(len(txt[0]) - len(clrl))])
        clrl.extend([gclrs[-1] for _ in range(len(txt))])
        for n, i in enumerate(txt):
            for m, j in enumerate(i):
                if gdir == 2:
                    f += f"{clr(j, clrl[m+n])}"
                else:
                    f += f"{clr(j, clrl[m+(len(txt)-n-1)])}"
            f += '\n'
        f = f[:-1]
    else:
        gclrs = gclrs[:len(txt)]
        for i in gclrs:
            clrl.extend([i for _ in range(len(txt) // len(gclrs))])
        clrl.extend([gclrs[-1] for _ in range(len(txt) - len(clrl))])
        for n, i in enumerate(txt):
            f += f"{clr(i, clrl[n])}\n"
        f = f[:-1]
    return f


def ghit(txt, ingclrs, gdir=0, bc=' ', sa=5, cs=0, font=0, rep=''):
    return gtxt([''.join(i) for i in hit(txt, bc, sa, cs, True, 0, '')],
                ingclrs, gdir)


app = flask.Flask('FLASK TEMPLATE')
app.secret_key = 'SECRET'

@app.route('/')
def index():
    return f"<body style='background:#080808;font-family:monospace;color:white'>{hit('CSCARD', '&nbsp;').replace(nl, '<br>')}</body>"

def run():
    app.run(host='0.0.0.0', port=5050)


def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
print(ghit('  FLASK  ', 'd,G,M,m,g', 2, sa=8))
print(ghit('TEMPLATE!', 'C,B,c,b', 2))
