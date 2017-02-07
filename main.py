#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import codecs
import pprint
from time import sleep

kindleDb = 'vocab.db'
dicDb = 'dic.db'
outputFile = 'Kindle.txt'

connK = sqlite3.connect(kindleDb)
cK = connK.cursor()

connD = sqlite3.connect(dicDb)
cD = connD.cursor()

output = open(outputFile, "w+")

words = cK.execute('SELECT words.word, \
       words.stem, \
       lookups.usage, \
       words.lang, \
       Trim(book_info.title), \
       book_info.authors, \
       book_info.lang, \
       lookups.timestamp \
FROM   lookups, \
       words, \
       book_info \
WHERE  words.id = lookups.word_key \
       AND book_info.id = lookups.book_key \
       AND words.lang = "en"')
for word in words:
	temp = []
	tag = '['+word[6]+']_'+word[5]+'_-_'+word[4]
	tag = tag.replace (" ", "_")
	print word[1]
	print word[2]
	
	translated = cD.execute('SELECT pl FROM dic WHERE en = "'+word[1]+'"')
	for ind, option in enumerate(translated):
		print '['+str(ind +1)+'] '+option[0]
		temp.append(option)
	if not temp:
		continue
	
	
	if ind == 0:
		inp = 0
	else:
		inp = raw_input('\nNumer tłumaczenia: \n')
		while not inp == '' and not int(inp) < ind+2 : 
			inp = raw_input('\nZły numer: \n')
		
		if inp == '':
			continue
		else:
			inp = int(inp)-1
	
	
	row = temp[inp][0][:-1] + '	'+word[1]+'	'+word[2].replace(word[0], '{{c1::'+word[0]+'}}', 1)+'	'+word[3]+'	'+str(word[7])+'	'+tag + '\n'
	output.write(row.encode('utf-8'))
	print 
	print 
	

connK.close()
connD.close()
