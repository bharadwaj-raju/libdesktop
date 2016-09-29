# coding: utf-8

# Copyright © Bharadwaj Raju <bharadwaj.raju@keemail.me>

# Licensed under the MIT License (see included LICENSE file).

# This file is part of libdesktop.

import os

# This file is not exported in the libdesktop module.
# This is just a copy of desktopfile.parse() and desktopfile.locate()
# in order to remove a circular dependency between applications and desktopfile

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

