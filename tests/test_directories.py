import os
from context import libdesktop

def test_get():

	print('\n')

	for i in ['videos', 'documents', 'pictures', 'music', 'downloads', 'desktop']:
		print(i.capitalize() + ':', getattr(libdesktop.directories, 'get_%s_dir' % i)())

def test_get_windows():

	if os.name != 'nt':
		print('OS is not Windows, skipping')
		print('-' * 50)
		return

	for i in dir(libdesktop.directories):
		if 'windows_get' in i:
			print(getattr(libdesktop, i)())
