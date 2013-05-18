#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import with_statement, print_function
from itertools import imap
from lxml import etree
import re, pickle, requests

NS = 'http://www.mediawiki.org/xml/export-0.8/'
TEXT_XPATH = etree.XPath('w:page/w:revision/w:text/text()', namespaces={'w': NS})
CITY_RE = re.compile(r'^\|\[\[(?:[^\|\]]+\|)?([^\]]+)\]\]\|\|[^\|]+\|\|([^\|]+)\|\|', re.MULTILINE)

def generate_pickled(filename):
	output = generate_dict()
	with file(filename, 'wb') as jar:
		pickle.dump(output, jar, protocol=pickle.HIGHEST_PROTOCOL)

def generate_dict():
	return dict(generate_items())

def generate_items():
	resp = requests.get('https://hu.wikipedia.org/w/api.php?format=json&action=query&titles=Magyarorsz%C3%A1g_v%C3%A1rosainak_list%C3%A1ja&export')
	json = resp.json()
	xml = json['query']['export']['*']
	root = etree.fromstring(xml)
	(text,) = TEXT_XPATH(root)
	for match in CITY_RE.finditer(text):
		yield match.groups()


def main():
	import sys
	try:
		output_file = sys.argv[1]
	except IndexError:
		print('Usage: {0} output.pickle'.format(sys.argv[0]), file=sys.stderr)
		raise SystemExit(1)
	else:
		generate_pickled(output_file)


if __name__ == '__main__':
	main()
