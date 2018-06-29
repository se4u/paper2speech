#!/usr/bin/env python
from lxml import etree
from collections import defaultdict

def spans(fns):
  for fn in fns:
    for s in etree.HTML(open(fn).read()).xpath('//body/div/span'):
      font=[int(e[10:-2]) for e in s.attrib['style'].split(';') if e.startswith('font-size:')][0]
      text = s.text
      yield [font, s.text]

def merge(pt, t):
  if pt.endswith('-'):
    return pt[:-1]+t
  else:
    return pt.strip() + ' ' + t

INTRO = defaultdict(lambda: '')
INTRO[17] = 'TITLE'
INTRO[11] = 'SECTION'

def nips(args):
  pf, text = -1, []
  for cf,t in spans(args.fns):
    if cf in [5]:
      continue
    if pf == cf:
      text[-1] = merge(text[-1], t)
    else:
      text.append(INTRO[cf])
      text.append(t)
    pf = cf
  return text

def main(args):
  text = globals()[args.conf](args)
  with open(args.o, 'wb') as f:
    f.write(' '.join(text).encode('utf-8'))
  return

if __name__ == '__main__':
  import glob
  import argparse
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument('-o', type=str)
  arg_parser.add_argument('-conf', default='nips',
                          choices='nips naacl aaai'.split())
  arg_parser.add_argument('fns', nargs='+')
  args=arg_parser.parse_args()
  main(args)
