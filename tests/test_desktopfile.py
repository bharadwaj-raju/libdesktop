from context import libdesktop
import sys
import os
import json

def test_desktopfile_construct():

	expected = '''[Desktop Entry]
	Name=Libdesktop Test
	Exec=ls
	Terminal=true
	Comment=Something
	Name[somelang]=Libdesktop TEST →
	Description=A test module for libdesktop
	'''.replace('\t', '')

	also_expected = expected.splitlines()

	# NOTE: also_expected is to account for the fact that the last two lines may not be in that order
	#		since Python default dictionaries are unordered

	also_expected[5], also_expected[6] = also_expected[6], also_expected[5]

	also_expected = '\n'.join(also_expected)

	also_expected += '\n'

	actual = libdesktop.desktopfile.construct(name='Libdesktop Test', exec_='ls', terminal=True,
			additional_opts={'Description': 'A test module for libdesktop', 'Comment': 'Something', 'Name[somelang]': 'Libdesktop TEST →'})

	print(expected)

	print('\n')

	print(also_expected)

	print('\n')

	print(actual)

	try:
		assert expected == actual

	except AssertionError:
		assert also_expected == actual

def test_desktopfile_parse():

	print('\n')

	desktop_file_for_test = '''[Desktop Entry]
	Terminal=true
	Name=Libdesktop Test
	Exec=ls -l
	Comment=A test desktop file
	Description=Hello
	'''.replace('\t', '')

	print(desktop_file_for_test)

	print('\n')

	expected = {
				'Name': 'Libdesktop Test',
				'Terminal': True,
				'Exec': 'ls -l',
				'Comment': 'A test desktop file',
				'Hidden': False,
				'Description': 'Hello'
				}

	actual = libdesktop.desktopfile.parse(desktop_file_for_test)

	print(json.dumps(expected, indent=4))

	print('\n')

	print(json.dumps(actual, indent=4))

	assert expected == actual

def test_desktopfile_execute():

	if os.name in ['darwin', 'nt']:
		print('Not a Linux/Unix (Mac OS X is one, but not suitable for this) system, skipping')

		return

	desktop_file_for_test = '''[Desktop Entry]
	Name=Libdesktop test
	Exec=ls -l
	Terminal=true
	Comment=Something
	Description=Something else
	'''.replace('\t', '')


	if not os.getenv('LIBDESKTOP_TESTS_RUN_GUI'):
		print('LIBDESKTOP_TESTS_RUN_GUI is not set, won\'t actually run programs')
		no_gui = True

	else:
		no_gui = False

	print(libdesktop.desktopfile.execute(desktop_file_for_test, return_cmd=True))

	if no_gui:
		return

	libdesktop.desktopfile.execute(desktop_file_for_test)

