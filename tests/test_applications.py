from context import libdesktop
import sys
import os

def test_applications_mac_app_exists():

	if os.name != 'darwin':
		print('Not a Mac OS X system, skipping')

		return

	assert libdesktop.applications.mac_app_exists('Finder') is True

def test_applications_terminal():

	if not os.getenv('LIBDESKTOP_TESTS_RUN_GUI'):
		print('LIBDESKTOP_TESTS_RUN_GUI is not set, won\'t actually execute programs')
		no_gui = True

	else:
		no_gui = False

	print(libdesktop.applications.terminal(return_cmd=True))
	print(libdesktop.applications.terminal(exec_='ls', return_cmd=True))
	print(libdesktop.applications.terminal(exec_='ls', shell_after_cmd_exec=True, return_cmd=True))

	if no_gui:
		return

	print('Starting terminal program. Verify that correct program is opened.')

	libdesktop.applications.terminal()

	print('Starting terminal program and running "ls". Verify that correct program is opened.')
	libdesktop.applications.terminal(exec_='ls', keep_open_after_cmd_exec=True)

	print('Starting terminal program and running "ls" and then the system shell. Verify that correct program is opened.')
	libdesktop.applications.terminal(exec_='ls', shell_after_cmd_exec=True)

def test_applications_text_editor():

	print('\nTesting applications.text_editor()')

	if not os.getenv('LIBDESKTOP_TESTS_RUN_GUI'):
		print('LIBDESKTOP_TESTS_RUN_GUI is not set, won\'t actually execute programs')
		no_gui = True

	else:
		no_gui = False

	print(libdesktop.applications.text_editor(return_cmd=True))
	print(libdesktop.applications.text_editor(files=['test_plaintext.txt'], return_cmd=True))

	if no_gui:
		return

	print('Opening the system text editor. Verify that correct program is opened.')
	libdesktop.applications.text_editor()

	print('Opening "test_plaintext.txt" text file in the system text editor. Verify that correct program is opened.')
	libdesktop.applications.text_editor(files=['test_plaintext.txt'])

def test_applications_open_with_default_program():

	print('\nTesting applications.open_file_with_default_program()')

	if not os.getenv('LIBDESKTOP_TESTS_RUN_GUI'):
		print('LIBDESKTOP_TESTS_RUN_GUI is not set, won\'t actually execute programs')

		no_gui = True

	else:
		no_gui = False

	print(libdesktop.applications.open_file_with_default_program('test_image.png', return_cmd=True))

	if no_gui:
		print('-' * 60)
		return

	print('Opening "test_image.png" image. Verify that correct program is opened.')
	libdesktop.applications.open_file_with_default_program('test_image.png')

	print('-' * 60)
