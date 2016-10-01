# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju@keemail.me>


# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

import subprocess as sp
import subprocess
import os
import sys

def get_cmd_out(command):

	'''Get the output of a command.

	Gets a nice Unicode no-extra-whitespace string of the `stdout` of a given command.

	Args:
		command (str or list): A string of the command, or a list of the arguments (as would be used in :class:`subprocess.Popen`).

	Note:
		If `command` is a `str`, it will be evaluated with `shell=True` i.e. in the default shell (for example, bash).

	Returns:
		str: The `stdout` of the command.'''

	if type(command) == list:
		result = sp.check_output(command)
	else:
		result = sp.check_output(command, shell=True)

	return result.decode('utf-8').rstrip()

def get_config_dir(app_name='', system_wide=False):

	'''Get the configuration directory.

	Get the configuration directories, optionally for a specific program.

	Args:
		app_name    (str) : The name of the program whose configuration directories have to be found.
		system_wide (bool): Gets the system-wide configuration directories.

	Returns:
		list: A list of all matching configuration directories found.
	'''

	config_homes = []

	if system_wide:
		if os.name == 'nt':
			config_homes.append(winreg.ExpandEnvironmentStrings('%PROGRAMDATA%'))

		else:
			config_homes.append('/etc')
			config_homes.append('/etc/xdg')
			config_homes.append('/usr/')
			config_homes.append('/usr/share')
			config_homes.append('/usr/local/share')

			if os.name == 'darwin':
				config_homes.append('/Library')

	else:
		if os.name == 'nt':
			import winreg
			config_homes.append(winreg.ExpandEnvironmentStrings('%LOCALAPPDATA%'))
			config_homes.append(os.path.join(winreg.ExpandEnvironmentStrings('%APPDATA%'), 'Roaming'))
		else:
			if os.getenv('XDG_CONFIG_HOME'):
				config_homes.append(os.getenv('XDG_CONFIG_HOME'))
			else:
				try:
					from xdg import BaseDirectory
					config_homes.append(BaseDirectory.xdg_config_home)
				except ImportError:
					config_homes.append(os.path.expanduser('~/.config'))

				config_homes.append(os.path.expanduser('~/.local/share'))
				config_homes.append(os.path.expanduser('~'))

				if os.name == 'darwin':
					config_homes.append(os.path.expanduser('~/Library'))

	if app_name:
		def __find_homes(app, dirs):

			homes = []

			for home in dirs:
				if os.path.isdir(os.path.join(home, app)):
					homes.append(os.path.join(home, app))

				if os.path.isdir(os.path.join(home, '.' + app)):
					homes.append(os.path.join(home, '.' + app))

				if os.path.isdir(os.path.join(home, app + '.d')):
					homes.append(os.path.join(home, app + '.d'))

			return homes

		app_homes = __find_homes(app_name, config_homes)

		# Special Cases

		if app_name == 'vim':
			app_homes.extend(__find_homes('vimfiles', config_homes))

		elif app_name == 'chrome':
			app_homes.extend(__find_homes('google-chrome', config_homes))

		elif app_name in ['firefox', 'thunderbird']:
			app_homes.extend(__find_homes(app_name, [os.path.expanduser('~/.mozilla')]))

		return app_homes

	return config_homes

def get_name():

	'''Get desktop environment or OS.

	Get the OS name or desktop environment.

	List of Possible Values:

	+-------------------------+---------------+
	| Windows                 | windows       |
	+-------------------------+---------------+
	| Mac OS X                | mac           |
	+-------------------------+---------------+
	| GNOME 3+                | gnome         |
	+-------------------------+---------------+
	| GNOME 2                 | gnome2        |
	+-------------------------+---------------+
	| XFCE                    | xfce4         |
	+-------------------------+---------------+
	| KDE                     | kde           |
	+-------------------------+---------------+
	| Unity                   | unity         |
	+-------------------------+---------------+
	| LXDE                    | lxde          |
	+-------------------------+---------------+
	| i3wm                    | i3            |
	+-------------------------+---------------+
	| \*box                   | \*box         |
	+-------------------------+---------------+
	| Trinity (KDE 3 fork)    | trinity       |
	+-------------------------+---------------+
	| MATE                    | mate          |
	+-------------------------+---------------+
	| IceWM                   | icewm         |
	+-------------------------+---------------+
	| Pantheon (elementaryOS) | pantheon      |
	+-------------------------+---------------+
	| LXQt                    | lxqt          |
	+-------------------------+---------------+
	| Awesome WM              | awesome       |
	+-------------------------+---------------+
	| Enlightenment           | enlightenment |
	+-------------------------+---------------+
	| AfterStep               | afterstep     |
	+-------------------------+---------------+
	| WindowMaker             | windowmaker   |
	+-------------------------+---------------+
	| [Other]                 | unknown       |
	+-------------------------+---------------+

	Returns:
		str: The name of the desktop environment or OS.
	'''

	if sys.platform in ['win32', 'cygwin']:
		return 'windows'

	elif sys.platform == 'darwin':
		return 'mac'

	else:
		desktop_session = os.environ.get('XDG_CURRENT_DESKTOP') or os.environ.get('DESKTOP_SESSION')

		if desktop_session is not None:
			desktop_session = desktop_session.lower()

			# Fix for X-Cinnamon etc
			if desktop_session.startswith('x-'):
				desktop_session = desktop_session.replace('x-', '')

			if desktop_session in ['gnome','unity', 'cinnamon', 'mate',
									'xfce4', 'lxde', 'fluxbox',
								   'blackbox', 'openbox', 'icewm', 'jwm',
								   'afterstep','trinity', 'kde', 'pantheon',
								   'i3', 'lxqt', 'awesome', 'enlightenment']:

				return desktop_session

			#-- Special cases --#

			# Canonical sets environment var to Lubuntu rather than
			# LXDE if using LXDE.
			# There is no guarantee that they will not do the same
			# with the other desktop environments.

			elif 'xfce' in desktop_session:
				return 'xfce4'

			elif desktop_session.startswith('ubuntu'):
				return 'unity'

			elif desktop_session.startswith('xubuntu'):
				return 'xfce4'

			elif desktop_session.startswith('lubuntu'):
				return 'lxde'

			elif desktop_session.startswith('kubuntu'):
				return 'kde'

			elif desktop_session.startswith('razor'):
				return 'razor-qt'

			elif desktop_session.startswith('wmaker'):
				return 'windowmaker'

		if os.environ.get('KDE_FULL_SESSION') == 'true':
			return 'kde'

		elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
			if not 'deprecated' in os.environ.get('GNOME_DESKTOP_SESSION_ID'):
				return 'gnome2'

		elif is_running('xfce-mcs-manage'):
			return 'xfce4'
		elif is_running('ksmserver'):
			return 'kde'

		return 'unknown'

def is_in_path(program):

	'''
	Check if a program is in the system `PATH`.

	Checks if a given program is in the user's `PATH` or not.

	Args:
		program (str): The program to try to find in `PATH`.

	Returns:
		bool: Is the program in `PATH`?
	'''

	if sys.version_info.major == 2:
		path = os.getenv('PATH')
		if os.name == 'nt':
			path = path.split(';')
		else:
			path = path.split(':')
	else:
		path = os.get_exec_path()

	for i in path:
		if os.path.isdir(i):
			if program in os.listdir(i):
				return True
def is_running(process):

	'''
	Check if process is running.

	Check if the given process name is running or not.

	Note:
		On a Linux system, kernel threads (like	`kthreadd` etc.) are excluded.

	Args:
		process (str): The name of the process.

	Returns:
		bool: Is the process running?
	'''

	if os.name == 'nt':
		process_list = get_cmd_out(['tasklist', '/v'])
		return process in process_list

	else:
		process_list = get_cmd_out('ps axw | awk \'{print $5}\'')

		for i in process_list.split('\n'):
			# 'COMMAND' is the column heading
			# [*] indicates kernel-level processes like \
			# kthreadd, which manages threads in the Linux kernel
			if not i == 'COMMAND' or i.startswith('['):
				if i == process:
					return True

				elif os.path.basename(i) == process:
					# check i without executable path
					# for example, if 'process' arguments is 'sshd'
					# and '/usr/bin/sshd' is listed in ps, return True
					return True

	return False  # finally
