# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju@keemail.me>


# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

import os
import sys
import plistlib
import subprocess as sp
import shutil
from libdesktop import system
from libdesktop import desktopfile
from libdesktop import applications

def add_item(name, command, system_wide=False):

	'''Adds a program to startup.

	Adds a program to user startup.

	Args:
		name        (str) : The name of the startup entry.
		command     (str) : The command to run.
		system_wide (bool): Add to system-wide startup.

	Note:
		``system_wide`` requires superuser/admin privileges.

	'''

	desktop_env = system.get_name()

	if os.path.isfile(command):
		command_is_file = True

		if not desktop_env == 'windows':
			# Will not exit program if insufficient permissions
			sp.Popen(['chmod +x %s' % command], shell=True)

	if desktop_env == 'windows':
		import winreg
		if system_wide:
			startup_dir = os.path.join(winreg.ExpandEnvironmentStrings('%PROGRAMDATA%'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')

		else:
			startup_dir = os.path.join(get_config_dir()[0], 'Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')

		if not command_is_file:
			with open(os.path.join(startup_dir, name + '.bat'), 'w') as f:
				f.write(command)
		else:
			shutil.copy(command, startup_dir)

	elif desktop_env == 'mac':
		sp.Popen(['launchctl submit -l %s -- %s'] % (name, command), shell=True)
		# system-wide will be handled by running the above as root
		# which will auto-happen if current process is root.

	else:
		# Linux/Unix

		if desktop_env == 'unknown':
			# CLI
			if system_wide:
				login_file = '/etc/profile'
			else:
				login_file = os.path.expanduser('~/.profile')

			with open(login_file, 'a') as f:
				f.write(command)

		else:
			try:
				desktop_file_name = name + '.desktop'

				startup_file = os.path.join(get_config_dir('autostart', system_wide=system_wide)[0], desktop_file_name)

				# .desktop files' Terminal option uses an independent method to find terminal emulator
				desktop_str = desktopfile.construct(name=name, exec_=command, additional_opts={'X-GNOME-Autostart-enabled': 'true'})

				with open(startup_file, 'w') as f:
					f.write(desktop_str)
			except:
				pass

def list_items(system_wide=False):

	'''List startup programs.

	List the programs set to run at startup.

	Args:
		system_wide (bool): Gets the programs that run at system-wide startup.

	Returns:
		list: A list of dictionaries in this format:

			.. code-block:: python

				{
				  'name': 'The name of the entry.',
				  'command': 'The command used to run it.'
				}
	'''

	desktop_env = system.get_name()

	result = []

	if desktop_env == 'windows':
		sys_startup_dir = os.path.join(winreg.ExpandEnvironmentStrings('%PROGRAMDATA%'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
		user_startup_dir = os.path.join(get_config_dir()[0], 'Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')

		startup_dir = sys_startup_dir if system_wide else user_startup_dir

		for file in os.listdir(startup_dir):
			file_path = os.path.join(startup_dir, file)

			result.append({ 'name': file, 'command': os.path.join(startup_dir, file) })

	elif desktop_env == 'mac':
		items_list = system.get_cmd_out('launchtl list | awk \'{print $3}\'')
		for item in items_list.split('\n'):
			# launchd stores each job as a .plist file (pseudo-xml)
			launchd_plist_paths = ['~/Library/LaunchAgents',
									'/Library/LaunchAgents',
									'/Library/LaunchDaemons',
									'/System/Library/LaunchAgents',
									'/System/Library/LaunchDaemons']

			for path in launchd_plist_paths:
				if item + '.plist' in os.listdir(path):
					plist_file = os.path.join(path, item + '.plist')

			# Parse the plist
			if sys.version_info.major == 2:
				plist_parsed = plistlib.readPlist(plist_file)
			else:
				with open(plist_file) as f:
					plist_parsed = plistlib.load(f)

			if 'Program' in plist_parsed:
				cmd = plist_parsed['Program']

				if 'ProgramArguments' in plist_parsed:
					cmd += ' '.join(plist_parsed['ProgramArguments'])

			elif 'ProgramArguments' in plist_parsed:
				cmd = ' '.join(plist_parsed['ProgramArguments'])

			else:
				cmd = ''

			result.append({ 'name': item, 'command': cmd })

		# system-wide will be handled by running the above as root
		# which will auto-happen if current process is root.

	else:
		# Linux/Unix

		# CLI
		profile = os.path.expanduser('~/.profile')

		if os.path.isfile(profile):
			with open(profile) as f:
				for line in f:
					if system.is_in_path(line.lstrip().split(' ')[0]):
						cmd_name = line.lstrip().split(' ')[0]

						result.append({ 'name': cmd_name, 'command': line.strip() })

		# /etc/profile.d
		if system_wide:
			if os.path.isdir('/etc/profile.d'):
				for file in os.listdir('/etc/profile.d'):
					file_path = os.path.join('/etc/profile.d', file)
					result.append({ 'name': file, 'command': 'sh %s' % file_path })

		# GUI

		try:
			startup_dir = system.get_config_dir('autostart', system_wide=system_wide)[0]

			for file in os.listdir(startup_dir):
				file_parsed = desktopfile.parse(os.path.join(startup_dir, file))

				if 'Name' in file_parsed:
					name = file_parsed['Name']

				else:
					name = file.replace('.desktop', '')

				if 'Exec' in file_parsed:
					if file_parsed['Terminal']:
						cmd = applications.terminal(exec_=file_parsed['Exec'],
														return_cmd=True)
					else:
						cmd = file_parsed['Exec']

				else:
					cmd = ''

				if not file_parsed.get('Hidden', False):
					result.append({ 'name': name, 'command': cmd })

		except IndexError:
			pass

	return result

def remove_item(name, system_wide=False):

	'''Removes a program from startup.

	Removes a program from startup.

	Args:
		name        (str) : The name of the program (as known to the system) to remove. See :func:``list_items``.
		system_wide (bool): Remove it from system-wide startup.

	Note:
		``system_wide`` requires superuser/admin privileges.
	'''

	desktop_env = system.get_name()

	if desktop_env == 'windows':
		import winreg
		if system_wide:
			startup_dir = os.path.join(winreg.ExpandEnvironmentStrings('%PROGRAMDATA%'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')

		else:
			startup_dir = os.path.join(system.get_config_dir()[0], 'Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup')

		for startup_file in os.path.listdir(start_dir):
			if startup_file == name or startup_file.split('.')[0] == name:
				os.remove(os.path.join(startup_dir, startup_file))

	elif desktop_env == 'mac':
		sp.Popen(['launchctl', 'remove', name])
		# system-wide will be handled by running the above as root
		# which will auto-happen if current process is root.

	else:
		# Linux/Unix

		if desktop_env == 'unknown':
			# CLI
			if system_wide:
				login_file = '/etc/profile'
			else:
				login_file = os.path.expanduser('~/.profile')

			with open(login_file) as f:
				login_file_contents = f.read()

			final_login_file_contents = ''

			for line in login_file_contents.split('\n'):
				if line.split(' ')[0] != name:
					final_login_file_contents += line

			with open(login_file, 'w') as f:
				f.write(final_login_file_contents)

		else:
			try:
				desktop_file_name = name + '.desktop'

				startup_file = os.path.join(system.get_config_dir('autostart', system_wide=system_wide)[0], desktop_file_name)

				if not os.path.isfile(startup_file):
					for possible_startup_file in os.listdir(system.get_config_dir('autostart', system_wide=system_wide)[0]):
						possible_startup_file_parsed = desktopfile.parse(possible_startup_file)

						if possible_startup_file_parsed['Name'] == name:
							startup_file = possible_startup_file

				os.remove(startup_file)

			except IndexError:
				pass
