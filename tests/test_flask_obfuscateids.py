# -*- coding: utf-8 -*-
"""
test_flask_obfuscateids
----------------------------------

Tests for `flask_obfuscateids` module.
"""
import random

import pytest

from flask_obfuscateids.lib import encode_base_n, decode_base_n, shuffle, key_gen, Obfuscator, ALPHANUM


def test_reflexivity():
	o = Obfuscator(0)
	for i in range(1000):
		assert i == o.deobfuscate(o.obfuscate(i))


def test_key_types():
	o = Obfuscator('abspoudhsfg')
	for i in range(1000):
		assert i == o.deobfuscate(o.obfuscate(i))
	o = Obfuscator(b'sldkhjfgl')
	for i in range(1000):
		assert i == o.deobfuscate(o.obfuscate(i))
	o = Obfuscator(42)
	for i in range(1000):
		assert i == o.deobfuscate(o.obfuscate(i))


def test_separate_objects():
	o1 = Obfuscator(0)
	o2 = Obfuscator(0)
	for i in range(1000):
		assert o1.obfuscate(i) == o2.obfuscate(i)
		assert i == o2.deobfuscate(o1.obfuscate(i))


def test_obfuscate_invalid_types():
	o = Obfuscator(0)
	with pytest.raises(ValueError):
		o.obfuscate('a')
	with pytest.raises(ValueError):
		o.obfuscate('1')
	with pytest.raises(ValueError):
		o.obfuscate(-1)


def test_deobfuscate_bad_checksums():
	o = Obfuscator(0)
	with pytest.raises(ValueError):
		o.deobfuscate('gbm')
	with pytest.raises(ValueError):
		o.deobfuscate('bgM')


def test_deobfuscate_outside_alphabet():
	o = Obfuscator(0)
	with pytest.raises(ValueError):
		o.deobfuscate('s&M')


def test_deobfuscate_wrong_type():
	o = Obfuscator(0)
	with pytest.raises(ValueError):
		o.deobfuscate(1)
	with pytest.raises(ValueError):
		o.deobfuscate(0)


def test_encode_base_n():
	assert encode_base_n(5, 2) == [1, 0, 1]
	assert encode_base_n(5, 2, 4) == [1, 0, 1, 0]


def test_decode_base_n():
	assert decode_base_n([1, 0, 1], 2) == 5
	assert decode_base_n([1, 0, 1, 0], 2) == 5
	assert decode_base_n([1, 0, 1], 3) == 10
	with pytest.raises(ValueError):
		decode_base_n([2, 1], 2)


def test_shuffle():
	a1 = list(ALPHANUM)
	a2 = a1[:]
	a3 = a1[:]
	shuffle(0, a1)
	shuffle(0, a2)
	shuffle(1, a3)
	assert a1 == a2
	assert a1 != a3


def test_update_middle():
	uninterupted = [digit for i, digit in zip(range(10), key_gen('key', 10))]
	interupted = []
	for i, digit in zip(range(10), key_gen('key', 10)):
		random.random()
		interupted.append(digit)
	assert uninterupted == interupted


def test_preserve_state():
	'''Generating a key shouldn't affect the state of random.'''
	random.random()
	init_state = random.getstate()
	shuffle(0, [1, 2, 3])
	assert random.getstate() == init_state
	for _ in zip(range(10), key_gen('key', 10)):
		assert random.getstate() == init_state
	assert random.getstate() == init_state
