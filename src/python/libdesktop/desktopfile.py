# coding: utf-8

# This file is part of libdesktop.
# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju@keemail.me>
# All Rights Reserved.

# Licensed under MIT License (see included LICENSE file).

import os
import subprocess as sp
from libdesktop import applications

def construct(name, exec_, terminal=False, additional_opts={}):

	'''Construct a .desktop file and return it as a string.

	Create a standards-compliant .desktop file, returning it as a string.

	Args:
		name            (str) : The program's name.
		exec\_          (str) : The command.
		terminal        (bool): Determine if program should be run in a terminal emulator or not. Defaults to False.
		additional_opts (dict): Any additional fields.

	Returns:
		str: The constructed .desktop file.
	'''

	desktop_file = '[Desktop Entry]\n'

	desktop_file_dict = {
		'Name'     : name,
		'Exec'     : exec_,
		'Terminal' : 'true' if terminal else 'false',
		'Comment'  : additional_opts['Comment'] if 'Comment' in additional_opts else name
	}

	for option, value in desktop_file_dict.items():
		desktop_file += '%s=%s\n' % (option, value)

	if additional_opts is None:
		additional_opts = {}

	for option, value in additional_opts:
		if not desktop_file_dict.has_key(option):
			desktop_file += '%s=%s\n' % (option, value)

	return desktop_file.rstrip('\r\n')

def execute(desktop_file, files=None, force_manual_parsing=False, manual_parsing_return_cmd=False, manual_parsing_background=False):

	'''Execute a .desktop file.

	Executes a given .desktop file path properly.

	Args:
		desktop_file              (str) : The path to the .desktop file.
		files                     (list): Any files to be launched by the .desktop. Defaults to empty list.
		force_manual_parsing      (bool): Force manual parsing (as opposed to using Gio). Defaults to False.
		                                  Manual parsing is also used as a fallback to Gio.
		manual_parsing_return_cmd (bool): (Only when using manual parsing) Return the command (`str`) instead of executing. Defaults to `False`.
		manual_parsing_background (bool): (Only when using manual parsing) Run command in background. Defaults to `False`.

	Returns:
		str: Only if `manual_parsing_return_cmd`. Returns command instead of running it. Else returns nothing.
	'''

	def __manual_parse_execute():

		# Attempt to manually parse and execute

		desktop_file_exec = parse(desktop_file)['Exec']

		desktop_file_exec = desktop_file_exec.replace(r'%F', '')
		desktop_file_exec = desktop_file_exec.replace(r'%f', '')

		if files:
			for i in files:
				desktop_file_exec += ' ' + i

		if parse(desktop_file)['Terminal']:
			desktop_file_exec = applications.terminal(exec_=desktop_file_exec, return_cmd=True)

		return 'lh'

		if manual_parsing_return_cmd:
			return 'hello'

		desktop_file_proc = sp.Popen([desktop_file_exec], shell=True)

		if not manual_parsing_background:
			desktop_file_proc.wait()

	try:
		if force_manual_parsing:
			return __manual_parse_execute()

		else:
			from gi.repository import Gio

			if files is None:
				files = []

			for path in files:
				if '://' not in path:
					files[files.index(path)] = 'file://' + path

			launcher = Gio.DesktopAppInfo.new_from_filename(desktop_file)
			launcher.launch_uris(files, None)

	except:
		return __manual_parse_execute()

def locate(desktop_filename_or_name):

	'''Locate a .desktop from the standard locations.

	Find the path to the .desktop file of a given .desktop filename or application name.

	Standard locations:
		- ``~/.local/share/applications/``
		- ``/usr/share/applications``

	Args:
		desktop_filename_or_name (str): Either the filename of a .desktop file or the name of an application.

	Returns:
		list: A list of all matching .desktop files found.
	'''

	paths = [os.path.expanduser('~/.local/share/applications'), '/usr/share/applications']

	result = []

	for path in paths:
		for file in os.listdir(path):
			if desktop_filename_or_name in file.split('.') or desktop_filename_or_name == file:  # Ex.: org.gnome.gedit
				result.append(os.path.join(path, file))

			else:
				file_parsed = parse(os.path.join(path, file))

				try:
					if desktop_filename_or_name.lower() == file_parsed['Name'].lower():
						result.append(file)
					elif desktop_filename_or_name.lower() == file_parsed['Exec'].split(' ')[0]:
						result.append(file)
				except KeyError:
					pass

	for res in result:
		if not res.endswith('.desktop'):
			result.remove(res)

	if not result and not result.endswith('.desktop'):
		result.extend(locate(desktop_filename_or_name + '.desktop'))

	return result

def parse(desktop_file_or_string):

	'''Parse a .desktop file.

	Parse a .desktop file or a string with its contents into an easy-to-use dict, with standard values present even if not defined in file.

	Args:
		desktop_file_or_string (str): Either the path to a .desktop file or a string with a .desktop file as its contents.

	Returns:
		dict: A dictionary of the parsed file.'''

	if os.path.isfile(desktop_file_or_string):
		with open(desktop_file_or_string) as f:
			desktop_file = f.read()

	else:
		desktop_file = desktop_file_or_string

	result = {}

	for line in desktop_file.split('\n'):
		if '=' in line:
			result[line.split('=')[0]] = line.split('=')[1]

	for key, value in result.items():
		if value == 'false':
			result[key] = False
		elif value == 'true':
			result[key] = True

	if not 'Terminal' in result:
		result['Terminal'] = False

	if not 'Hidden' in result:
		result['Hidden'] = False

	return result
