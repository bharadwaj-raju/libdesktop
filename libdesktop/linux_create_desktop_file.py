# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# All Rights Reserved.

# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

def linux_create_desktop_file(name, execute, terminal=False, additional_opts=None, filename='', return_str=False):

	DESKTOP_FILE_BASE = '''[Desktop Entry]
Name=%s
Exec=%s
Terminal=%s
'''

	# Desktop files use lower case true/false

	if terminal:

		terminal = 'true'

	else:

		terminal = 'false'

	desktop_file = DESKTOP_FILE_BASE % (name, execute, terminal)

	if not additional_opts:

		additional_opts = []

	for i in additional_opts:

		desktop_file += '\n' + i

	if return_str:

		return desktop_file

	else:

		with open(filename, 'w') as f:

			f.write(desktop_file)
