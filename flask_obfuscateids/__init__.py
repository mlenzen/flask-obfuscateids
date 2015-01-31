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

from flask import current_app, abort

# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
	from flask import _app_ctx_stack as stack
except ImportError:
	from flask import _request_ctx_stack as stack

from . import lib

__version__ = '0.0.1'


class ObfuscateIDs():

	def __init__(self, app=None):
		self.app = app
		if app is not None:
			self.init_app(app)

	def init_app(self, app):
		app.config.setdefault('OBFUSCATE_IDS_KEY', app.config['SECRET_KEY'])
		app.config.setdefault('OBFUSCATE_IDS_MIN_LENGTH', 8)
		app.config.setdefault('OBFUSCATE_IDS_ALPHABET', lib.ALPHANUM)
		app.config.setdefault('OBFUSCATE_IDS_NUM_CHECK_CHARS', 1)
		app.config.setdefault('OBFUSCATE_IDS_ALG_VER', 1)
		# Use the newstyle teardown_appcontext if it's available,
		# otherwise fall back to the request context
		if hasattr(app, 'teardown_appcontext'):
			app.teardown_appcontext(self.teardown)
		else:
			app.teardown_request(self.teardown)

	def create_obfuscator(self):
		return lib.Obfuscator(
			key=current_app.config['OBFUSCATE_IDS_KEY'],
			alphabet=current_app.config['OBFUSCATE_IDS_ALPHABET'],
			min_length=current_app.config['OBFUSCATE_IDS_MIN_LENGTH'],
			num_check_chars=current_app.config['OBFUSCATE_IDS_NUM_CHECK_CHARS'],
			)

	def teardown(self, exception):
		pass

	@property
	def obfuscator(self):
		ctx = stack.top
		if ctx is not None:
			if not hasattr(ctx, '_obfuscator'):
				ctx._obfuscator = self.create_obfuscator()
			return ctx._obfuscator

	def obfuscate(self, id):
		pass


class ModelMixin():
	'''

	Two class variables are in place to handle refactoring:
	__obfuscate_ids_salt__ - by default, just use the class name
	__obfuscate_ids_attr__ - The attribute of instances of this class to
		use as the id. Defaults to 'id'
	If the class name changes, set __obfuscate_ids_salt__ to the old class name
	to preserve obfuscated ids for that class.
	'''

	@classmethod
	def _obfuscate_ids_class_salt(cls):
		return getattr(cls, '__obfuscate_ids_salt__', '__name__')

	@classmethod
	def _obfuscate_ids_attr_name(cls):
		'''Return the name of the attribute to use.'''
		return getattr(cls, '__obfuscate_ids_attr__', 'id')

	@classmethod
	def get_from_web_id(cls, web_id, or_abort=None):
		'''Return the object corresponding to web_id.

		If the web_id is malformed or there is no object with the deobfuscated id,
		the behavior depends on the or_abort parameter. If or_abort is None, then
		None is returned. If not, flask.abort is called with or_abort as it's
		argument (an HTTP status code).

		Args:
			web_id: The web_id of the object to get
			or_abort: None or an int status code
		'''
		try:
			ident = current_app.obfuscator.deobfuscate(web_id, salt=cls._obfuscate_ids_class_salt())
		except ValueError:
			obj = None
		else:
			obj = cls.query.get(ident)
		if obj is None and or_abort is not None:
			abort(or_abort)
		else:
			return obj

	@property
	def web_id(self):
		ident_attr = getattr(self, self._obfuscate_ids_attr_name())
		return current_app.obfuscator.obfuscate(ident_attr, salt=self._obfuscate_ids_class_salt())
