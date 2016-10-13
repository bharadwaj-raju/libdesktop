from distutils.core import setup

_version = 0.5  # Changed in make upload

setup(
  name = 'libdesktop',
  packages = ['libdesktop', 'libdesktop.dialog'],
  version = str(_version),
  description = 'A cross-platform library for miscellaneous OS functions and conveniences.',
  author = 'Bharadwaj Raju',
  author_email = 'bharadwaj.raju@keemail.me',
  url = 'https://github.com/bharadwaj-raju/libdesktop',
  download_url = 'https://github.com/bharadwaj-raju/libdesktop/archive/master.tar.gz',
  keywords = ['desktop', 'library', 'os', 'operating', 'system'],
  classifiers = ['Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
	'Programming Language :: Python :: 2',
	'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Software Development :: Libraries :: Python Modules',
	'Topic :: Utilities',
	'Topic :: System',
	'Topic :: Desktop Environment'],
)
