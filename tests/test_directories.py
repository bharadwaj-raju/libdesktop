import os
from context import libdesktop

def test_directories_get():

	print('\n')

	for i in ['videos', 'documents', 'pictures', 'music', 'downloads', 'desktop']:
		print(i.capitalize() + ':', getattr(libdesktop.directories, 'get_%s_dir' % i)())

	print('-' * 50)

def test_directories_get_windows():

	if os.name != 'nt':
		print('OS is not Windows, skipping')
		print('-' * 50)
		return

	for i in dir(libdesktop.directories):
		if 'windows_get' in i:
			print(getattr(libdesktop, i)())

	print('-' * 50)


def test_directories_get_config_dir():

	print('Config dirs:', libdesktop.directories.get_config_dir())

	if os.name == 'nt':
		print('Config dir for Microsoft:', libdesktop.directories.get_config_dir('Microsoft'))

	elif os.name == 'darwin':
		print('Config dir for Finder:', libdesktop.directories.get_config_dir('Finder'))

	else:
		print('Config dir for autostart:', libdesktop.directories.get_config_dir('autostart'))

	print('-' * 50)

def test_directories_get_config_file():

	with open(os.path.join(libdesktop.directories.get_config_dir()[0], 'test.conf'), 'w'):
		pass

	expected = os.path.join(libdesktop.directories.get_config_dir()[0], 'test.conf')
	actual = libdesktop.directories.get_config_file('test.conf')[0]

	assert expected == actual

	os.remove(expected)


