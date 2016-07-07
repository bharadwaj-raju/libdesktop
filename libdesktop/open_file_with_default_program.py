# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# All Rights Reserved.

# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

from .get_desktop_environment import get_desktop_environment
import subprocess as sp

def open_file_with_default_program(file, background=False, return_cmd=False):

	desktop_env = get_desktop_environment()

	if desktop_env == 'windows':

		open_file_cmd_str = 'explorer.exe ' + file

	elif desktop_env == 'mac':

		open_file_cmd_str = 'open ' + file

	else:

		open_file_cmd_str = 'xdg-open ' + file

	if background:

		if desktop_env == 'windows':

			open_file_cmd_str = 'start /B ' + open_file_cmd_str

		else:

			open_file_cmd_str += ' &'

	if return_cmd:

		return open_file_cmd_str

	else:

		sp.Popen([open_file_cmd_str], shell=True)
