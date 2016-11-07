import sys
import os
from context import libdesktop

def test_system_get_cmd_out():

	if os.name == 'nt':
		poor_shell_ls_substitute = libdesktop.system.get_cmd_out('dir')
		expected_ls = os.listdir('.')

	else:
		poor_shell_ls_substitute = libdesktop.system.get_cmd_out('echo *')
		expected_ls = os.listdir('.')

	print(poor_shell_ls_substitute, '\n', expected_ls, '\n')

	assert sorted(poor_shell_ls_substitute.split()) == sorted(expected_ls)

	assert libdesktop.system.get_cmd_out([sys.executable, '-c', 'print("test")']) == 'test'

def test_system_get_name():

	# Difficult to test

	if os.name == 'darwin':
		assert libdesktop.system.get_name() == 'mac'

	if os.name == 'nt':
		assert libdesktop.system.get_name() == 'windows'

	else:
		# Errr...
		# Just call it
		libdesktop.system.get_name()

def test_system_is_in_path():

	if os.name == 'nt':
		assert libdesktop.system.is_in_path('explorer.exe') is True

	else:
		assert libdesktop.system.is_in_path('ls') is True

def test_system_is_running():

	if os.name == 'nt':
		assert libdesktop.system.is_running('ntoskrnl.exe') is True

	else:
		assert libdesktop.system.is_running(sys.executable) is True

def test_system_get_config_dir():

	print('Config dirs:', libdesktop.system.get_config_dir())

	if os.name == 'nt':
		print('Config dir for Microsoft:', libdesktop.system.get_config_dir('Microsoft'))

	elif os.name == 'darwin':
		print('Config dir for Finder:', libdesktop.system.get_config_dir('Finder'))

	else:
		print('Config dir for autostart:', libdesktop.system.get_config_dir('autostart'))

