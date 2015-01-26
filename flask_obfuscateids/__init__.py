# -*- coding: utf-8 -*-
'''
flask_obfuscateids
~~~~~~~~~~~~~~~~~~~

Obfuscate objects primary keys for URLs

:copyright: (c) 2015 by Michael Lenzen
:licence: BSD, see LICENCE for more details
This module is used to obfuscate integer ids (primary keys exposed in a web app).

Usage:
.. code:: python

	>>> o = Obfuscator('my secret key')
	>>> o.obfuscate(10001)
	'sUXU'
	>>> o.deobfuscate('sUXU')
	10001
	>>> o.obfuscate(1)
	'Di'
	>>> o = Obfuscator('my secret key', min_length=4)
	>>> o.obfuscate(1)
	'DxzB'


Goals:
* Ids are encoded using any alphabet of any length
* Output is succinct and "pretty"
* Specify minumum output length
* Sequential ids don't appear to have anything in common
* There's some sort of checking so that random inputs won't work
* Fast
* Different objects returns different obfuscations for the same id

Alternatives:
# http://hashids.org/
  * Can encode multiple numbers at a time which I consider a bug (someone can
    alter an ID then the decode function returns an object of a different type)
  * Doesn't check for valid input

# Real encryption
  * Generally can't specify nice short output

# Use primary key
  * Exposes unwanted information, eg. how many users you have
  * Makes it easy to sequentially access items

# GUIDs
  * Another column seems unnecessary
  * A second index would be required and would require inserting records in
    the middle instead of on the end of the table

Discussions:
http://programmers.stackexchange.com/questions/139450/is-obscuring-obfuscating-public-facing-database-ids-really-a-best-practice
http://joshua.schachter.org/2007/01/autoincrement
http://stackoverflow.com/questions/1895685/should-i-obscure-primary-key-values
'''
from __future__ import absolute_import, unicode_literals

__version__ = '0.0.1'

from collections_extended import setlist

from . import lib

# Common alphabets to use
ALPHANUM = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
BASE58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


class Obfuscator():

	def __init__(self, key, alphabet=None, min_length=0, num_check_chars=1):
		'''
		Args:
			key: The key.
			alphabet: Optionally, specify an alternative alphabet to use.
			min_length: An encoded value will always be at least min_length characters (including the check characters)
			num_check_chars: The number of chars used for the check
		'''
		if isinstance(num_check_chars, int) and num_check_chars >= 0:
			self.num_check_chars = num_check_chars
		else:
			raise ValueError('num_check_chars must be an int >= 0')
		if isinstance(min_length, int) and min_length >= 0:
			self.min_length = min_length - num_check_chars
		else:
			raise ValueError('min_length must be an int >= 0')
		self.key = key
		alphabet = list(alphabet or ALPHANUM)
		lib.shuffle(key, alphabet)
		self.alphabet = setlist(alphabet)

	def obfuscate(self, num):
		return lib.obfuscate(num, self.key, self.alphabet, self.min_length, self.num_check_chars)

	def deobfuscate(self, s):
		return lib.deobfuscate(s, self.key, self.alphabet, self.num_check_chars)
