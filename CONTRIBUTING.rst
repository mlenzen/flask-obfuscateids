============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

This document is adapted from the cookiecutter cookie-contrib_.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at github-issue-tracker_.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

This could always use more documentation, whether as part of the
official docs, in docstrings, or even on the web in blog posts,
articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at github-issue-tracker_.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up `flask-obfuscateids` for local development.

1. Fork the `flask-obfuscateids` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/flask-obfuscateids.git

3. Install your local copy into a virtualenv.

    $ cd flask-obfuscateids
    $ pyvenv env
    $ . env/bin/activate
    $ pip install -r requirements/dev.txt
    $ pip install --editable .

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass flake8 and the tests, including testing other Python versions with tox::

    $ flake8 collections_extended tests
    $ python setup.py test
    $ tox

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 2.7, 3.3, and 3.4, and for PyPy. Check _travis-ci-pull-requests_ and make sure that the tests pass for all supported Python versions.

Tips
----

To run a subset of tests::

    $ py.test tests/test_example.py

.. _cookie-contrib: https://github.com/audreyr/cookiecutter/blob/master/CONTRIBUTING.rst
.. _github-issue-tracker: https://github.com/mlenzen/flask-obfuscateids/issues
.. _travis-ci-pull-requests: https://travis-ci.org/mlenzen/flask-obfuscateids/pull_requests