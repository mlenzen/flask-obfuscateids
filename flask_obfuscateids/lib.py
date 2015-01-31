
from random import Random

from collections_extended import setlist

# The version of seeding to use for random
SEED_VERSION = 2

# Common alphabets to use
ALPHANUM = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
BASE58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def shuffle(key, x):
	random = Random(key)
	random.shuffle(x)


def key_gen(key, base):
	'''Generate values from the key.
	This will indefinitely generate integers in [0, base).
	key is used to initialize random, so that the "random" number generated are
	the same each time for a given key. This turns a key of any length into an
	"infinitely" long key without simply cycling over the key.
	'''
	random = Random(key)
	while True:
		value = random.randint(0, base-1)
		yield value


def encode_base_n(num, base, min_length=0):
	'''Convert an integer into a list of integers storing the number in base base.
	If a minimum length is specified, the result will be 0-padded.
	'''
	out = []
	while num > 0 or len(out) < min_length:
		num, remainder = divmod(num, base)
		out.append(remainder)
	return out


def decode_base_n(int_list, base):
	'''Convert a list of numbers representing a number in base base to an integer.'''
	out = 0
	for index, num in enumerate(int_list):
		if num >= base or num < 0:
			raise ValueError
		out += (base ** index) * num
	return out


def calc_check_digits(int_list, base, num_check_chars):
	checksum_base = base ** num_check_chars
	checksum_value = sum(int_list) % checksum_base
	return encode_base_n(checksum_value, base, min_length=num_check_chars)


def add_check_digits(int_list, base, num_check_chars):
	'''Calculate a checksum for int_list and translate into a number of base base
	made up of num_check_chars digits.

	Args:
		int_list: A list of integers >= 0 and < base
		base: The number of characters in the alphabet
		num_check_chars: The number of check characters to return
	Returns:
		A list of integers that represent the checksum in base base.
	'''
	check_digits = calc_check_digits(int_list, base, num_check_chars)
	return int_list + check_digits


def eval_check_digits(decrypted_ints, base, num_check_chars):
	'''Evaluate the check digits in decrypted_ints.

	Args:
		decrypted_ints: A list of integers >=0 and < base (the result of add_check_digits)
	Returns:
		The decrypted_ints without the check digits
	Raises:
		ValueError: if the check digits don't match
	'''
	if num_check_chars == 0:
		return decrypted_ints
	int_list = decrypted_ints[:-num_check_chars]
	check_digits = decrypted_ints[-num_check_chars:]
	if calc_check_digits(int_list, base, num_check_chars) != check_digits:
		raise ValueError()
	return int_list


def encode(int_list, alphabet):
	'''Encode ints using alphabet.'''
	char_list = []
	for i in int_list:
		if i > len(alphabet) or i < 0:
			raise ValueError
		char_list.append(alphabet[i])
	return ''.join(char_list)


def decode(s, alphabet):
	'''Decode a string s using alphabet returning a list of ints.'''
	try:
		return [alphabet.index(c) for c in s]
	except (TypeError, IndexError):
		raise ValueError


def encrypt(int_list, key, base):
	encrypted_ints = []
	moving_value = 0
	for char_index, key_value in zip(int_list, key_gen(key, base)):
		encrypted_int = (char_index + key_value + moving_value) % base
		encrypted_ints.append(encrypted_int)
		moving_value += encrypted_int
	return encrypted_ints


def decrypt(int_list, key, base):
	decrypted_ints = []
	moving_value = 0
	for char_index, key_value in zip(int_list, key_gen(key, base)):
		decrypted_int = (char_index - key_value - moving_value) % base
		decrypted_ints.append(decrypted_int)
		moving_value += char_index
	return decrypted_ints


def obfuscate(num, key, alphabet, min_chars=0, num_check_chars=1):
	''' Obfuscate num using key.

	This does some minor encryption by adding values to a key and a moving value.
	The moving value is so that one small change makes all of the resulting
	characters change.

	Args:
		num: The integer to obfuscate
		key: An int, string or bytes to generate key values (anything that can be passed to random.seed)
		alphabet: A list of characters to use for the alphabet
		min_chars: A minimum number of chars for the resulting string
		num_check_chars: The number of chars to use as a check
	Returns:
		A string encoding the number in the passed alphabet and encrypted with key.
	Raises:
		ValueError: if num is not a number or < 0
	'''
	try:
		if num < 0:
			raise ValueError()
	except TypeError:
		raise ValueError()
	base = len(alphabet)
	num_as_ints = encode_base_n(num, base, min_chars)
	unencrypted_digits = add_check_digits(num_as_ints, base, num_check_chars)
	encrypted_digits = encrypt(unencrypted_digits, key, base)
	return encode(encrypted_digits, alphabet)


def deobfuscate(s, key, alphabet, num_check_chars=1):
	'''Deobfuscate a string using key and alphabet.

	key, alphabet and num_check_chars must be identical to the values used to obfuscate.

	Args:
		s: The string to deobfuscate
		key: The key used to obfuscate
		alphabet: The alphabet used to obfuscate
		num_check_chars: The number of chars to use as a check
	Returns:
		The deobfuscated integer.
	Raises:
		ValueError: if s isn't a string, s doesn't use alphabet or the checksum doesn't match
	'''
	base = len(alphabet)
	encrypted_ints = decode(s, alphabet)
	decrypted_ints = decrypt(encrypted_ints, key, base)
	num_as_ints = eval_check_digits(decrypted_ints, base, num_check_chars)
	return decode_base_n(num_as_ints, base)


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
		shuffle(key, alphabet)
		self.alphabet = setlist(alphabet)

	def obfuscate(self, num, salt=None, min_length=None):
		if salt:
			key = self.key + salt
		else:
			key = self.key
		if min_length is None:
			min_length = self.min_length
		return obfuscate(num, key, self.alphabet, min_length, self.num_check_chars)

	def deobfuscate(self, s, salt=None):
		if salt:
			key = self.key + salt
		else:
			key = self.key
		return deobfuscate(s, key, self.alphabet, self.num_check_chars)
