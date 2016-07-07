# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# All Rights Reserved.

# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

import os
import subprocess as sp
import shutil
from .get_desktop_environment import get_desktop_environment
from .get_config_dir import get_config_dir
from .linux_create_desktop_file import linux_create_desktop_file
from .start_terminal_emulator import start_terminal_emulator

def add_to_system_startup(command, name, all_users=False, run_in_terminal=False):

	desktop_env = get_desktop_environment()

	if os.path.isfile(command):

		command_is_file = True

		if not desktop_env == 'windows':

			# Will not exit program if insufficient permissions
			sp.Popen(['chmod +x %s' % command], shell=True)

	if desktop_env == 'windows':

		import winreg

		if all_users:

			startup_dir = os.path.join(winreg.ExpandEnvironmentStrings('%PROGRAMDATA%'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')

		else:

			startup_dir = os.path.join(get_config_dir(), 'Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')

		if not command_is_file:

			if run_in_terminal:

				command = start_terminal_emulator(exec_cmd=command, return_cmd=True)

			with open(os.path.join(startup_dir, name + '.bat'), 'w') as f:

				f.write(command)
		else:

			shutil.copy(command, startup_dir)

	elif desktop_env == 'mac':

		if run_in_terminal:

			command = start_terminal_emulator(exec_cmd=command, return_cmd=True)

		if all_users:

			sp.Popen(['sudo launchctl submit -l name_of_startup_item -- %s'] % command, shell=True)

		else:

			sp.Popen(['launchctl submit -l name_of_startup_item -- %s'] % command, shell=True)

	else:

		# Linux/Unix

		desktop_file_name = name + '.desktop'

		if all_users:

			startup_file = os.path.join('/etc/xdg/autostart', desktop_file_name)

		else:

			startup_file = os.path.join(get_config_dir('autostart'), desktop_file_name)

		# .desktop files' Terminal option uses an independent method to find terminal emulator

		linux_create_desktop_file(name=name, execute=command, terminal=run_in_terminal, filename=startup_file)
