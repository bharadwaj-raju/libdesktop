Testing libdesktop
==================

Libdesktop has tests in the ``tests/`` directory.

Running the tests
-----------------

1. Install pytest: ``pip install pytest``.
2. Run ``make test``.

Customization of the tests
--------------------------

By default, the tests do not run GUI applications (like in the ``applications`` module functions).

To run them, set the environment variable ``LIBDESKTOP_TESTS_RUN_GUI`` to ``true``.
