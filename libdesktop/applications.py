# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju@keemail.me>

# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

import subprocess as sp
import tempfile
import os

from libdesktop import desktopfile
from libdesktop import system

def mac_app_exists(app):

	'''Check if 'app' is installed (OS X).

	Check if the given applications is installed on this OS X system.

	Args:
		app (str): The application name.

	Returns:
		bool: Is the app installed or not?
	'''

	APP_CHECK_APPLESCRIPT = '''try
	tell application "Finder"
		set appname to name of application file id "%s"
		return 0
	end tell
	on error err_msg number err_num
		return 1
	end try'''

	with open('/tmp/app_check.AppleScript', 'w') as f:
		f.write(APP_CHECK_APPLESCRIPT % app)

	app_check_proc = sp.Popen(['osascript', '-e', '/tmp/app_check.AppleScript'])

	if app_check_proc.wait() != 0:
		return False
	else:
		return True

def open_file_with_default_program(file, background=False, return_cmd=False):

	'''Opens a file with the default program for that type.

	Open the file with the user's preferred application.

	Args:
		file       (str) : Path to the file to be opened.
		background (bool): Run the program in the background, instead of waiting for completion. Defaults to ``False``.
		return_cmd (bool): Returns the command to run the program (str) instead of running it. Defaults to ``False``.

	Returns:
		str: Only if ``return_cmd``, the command to run the program is returned instead of running it. Else returns nothing.
	'''

	desktop_env = system.get_name()

	if desktop_env == 'windows':
		open_file_cmd = 'explorer.exe ' + "'%s'" % file

	elif desktop_env == 'mac':
		open_file_cmd = 'open ' + "'%s'" % file

	else:
		file_mime_type = system.get_cmd_out(['xdg-mime', 'query', 'filetype', file])
		desktop_file = system.get_cmd_out(['xdg-mime', 'query', 'default', file_mime_type])
		open_file_cmd = desktopfile.execute(desktopfile.locate(desktop_file)[0], files=[file], return_cmd=True)

	if return_cmd:
		return open_file_cmd

	else:
		def_program_proc = sp.Popen(open_file_cmd, shell=True)

		if not background:
			def_program_proc.wait()

def terminal(exec_='', background=False, shell_after_cmd_exec=False, keep_open_after_cmd_exec=False, return_cmd=False):

	'''Start the default terminal emulator.

	Start the user's preferred terminal emulator, optionally running a command in it.

	**Order of starting**
		Windows:
			Powershell

		Mac:
			- iTerm2
			- Terminal.app

		Linux/Unix:
			- ``$TERMINAL``
			- ``x-terminal-emulator``
			- Terminator
			- Desktop environment's terminal
			- gnome-terminal
			- urxvt
			- rxvt
			- xterm

	Args:
		exec\_               (str) : An optional command to run in the opened terminal emulator. Defaults to empty (no command).
		background           (bool): Run the terminal in the background, instead of waiting for completion. Defaults to ``False``.
		shell_after_cmd_exec (bool): Start the user's shell after running the command (see exec_). Defaults to `False`.
		return_cmd           (bool): Returns the command used to start the terminal (str) instead of running it. Defaults to ``False``.
	Returns:
		str: Only if ``return_cmd``, returns the command to run the terminal instead of running it. Else returns nothing.
	'''

	desktop_env = system.get_name()

	if not exec_:
		shell_after_cmd_exec = True

	if desktop_env == 'windows':
		terminal_cmd_str = 'start powershell.exe'

	if desktop_env == 'mac':
		# Try iTerm2 first, apparently most popular Mac Terminal
		if mac_app_exists('iTerm2'):
			terminal_cmd_str = 'open -a iTerm2'

		else:
			terminal_cmd_str = 'open -a Terminal'

	else:

		# sensible-terminal

		if os.getenv('TERMINAL'):
			# Not everywhere, but if user *really* has a preference, they will
			# set this

			terminal_cmd_str = os.getenv('TERMINAL')

		elif system.is_in_path('x-terminal-emulator'):
			# This is a convenience script that launches terminal based on
			# user preferences.
			# This is not available on some distros (but most have it)
			# so try this first
			terminal_cmd_str = 'x-terminal-emulator'

		elif system.is_in_path('terminator'):
			terminal_cmd_str = 'terminator'

		elif desktop_env in ['gnome', 'unity', 'cinnamon', 'gnome2']:
			terminal_cmd_str = 'gnome-terminal'

		elif desktop_env == 'xfce4':
			terminal_cmd_str = 'xfce4-terminal'

		elif desktop_env == 'kde' or desktop_env == 'trinity':
			terminal_cmd_str = 'konsole'

		elif desktop_env == 'mate':
			terminal_cmd_str = 'mate-terminal'

		elif desktop_env == 'i3':
			terminal_cmd_str = 'i3-sensible-terminal'

		elif desktop_env == 'pantheon':
			terminal_cmd_str = 'pantheon-terminal'

		elif desktop_env == 'enlightenment':
			terminal_cmd_str = 'terminology'

		elif desktop_env == 'lxde' or desktop_env == 'lxqt':
			terminal_cmd_str = 'lxterminal'

		else:
			if system.is_in_path('gnome-terminal'):
				terminal_cmd_str = 'gnome-terminal'

			elif system.is_in_path('urxvt'):
				terminal_cmd_str = 'urxvt'

			elif system.is_in_path('rxvt'):
				terminal_cmd_str = 'rxvt'

			elif system.is_in_path('xterm'):
				terminal_cmd_str = 'xterm'

	if exec_:
		if desktop_env == 'windows':
			if keep_open_after_cmd_exec and not shell_after_cmd_exec:
				exec_ += '; pause'

			if os.path.isfile(exec_):
				terminal_cmd_str += exec_

			else:
				terminal_cmd_str += ' -Command ' + '"' + exec_ + '"'

			if shell_after_cmd_exec:
				terminal_cmd_str += ' -NoExit'

		else:
			if keep_open_after_cmd_exec and not shell_after_cmd_exec:
				exec_ += '; read'

			if shell_after_cmd_exec:
				exec_ += ' ; ' + os.getenv('SHELL')

			if desktop_env == 'mac':
				terminal_cmd_str += ' ' + 'sh -c ' + '"' + exec_ + '"'

			else:
				terminal_cmd_str += ' -e \'sh -c ' + '"' + exec_ + '"\''

	if return_cmd:
		return terminal_cmd_str

	terminal_proc = sp.Popen([terminal_cmd_str], shell=True, stdout=sp.PIPE)

	if not background:
		# Wait for process to complete
		terminal_proc.wait()

def text_editor(files=None, background=False, return_cmd=False):

	'''Starts the default graphical text editor.

	Start the user's preferred graphical text editor, optionally with a file.

	Args:
		files      (list): A list of files to be opened with the editor. Defaults to an empty list.
		background (bool): Runs the editor in the background, instead of waiting for completion. Defaults to ``False``.
		return_cmd (bool): Returns the command (str) to run the editor instead of running it. Defaults to ``False``.

	Returns:
		str: Only if ``return_cmd``, the command to run the editor is returned. Else returns nothing.
	'''

	if files is None:
		files = []

	desktop_env = system.get_name()

	if desktop_env == 'windows':
		editor_cmd_str = system.get_cmd_out(['ftype', 'textfile']).split('=', 1)[1]

	elif desktop_env == 'mac':
		editor_cmd_str = 'open -a' + system.get_cmd_out(['def', 'read', 'com.apple.LaunchServices', 'LSHandlers' '-array' '{LSHandlerContentType=public.plain-text;}'])

	else:
		# Use def handler for MIME-type text/plain
		editor_cmd_str = system.get_cmd_out(['xdg-mime', 'query', 'default', 'text/plain'])

		if '\n' in editor_cmd_str:
			# Sometimes locate returns multiple results
			# use first one

			editor_cmd_str = editor_cmd_str.split('\n')[0]

	if editor_cmd_str.endswith('.desktop'):
		# We don't use desktopfile.execute() in order to have working return_cmd and background

		editor_cmd_str = desktopfile.parse(desktopfile.locate(editor_cmd_str)[0])['Exec']

		for i in editor_cmd_str.split():
			if i.startswith('%'):
				# %-style formatters
				editor_cmd_str = editor_cmd_str.replace(i, '')

			if i == '--new-document':
				# Gedit
				editor_cmd_str = editor_cmd_str.replace(i, '')

	final_cmd = editor_cmd_str + ' ' + ' '.join(files)

	if return_cmd:
		return final_cmd

	text_editor_proc = sp.Popen([final_cmd], shell=True)

	if not background:
		text_editor_proc.wait()
