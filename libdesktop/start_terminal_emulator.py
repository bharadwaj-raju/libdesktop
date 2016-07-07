# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# All Rights Reserved.

# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

import subprocess as sp
import tempfile
import os
from .get_desktop_environment import get_desktop_environment
from .is_in_path import is_in_path

def start_terminal_emulator(background=False, exec_cmd='', shell_after_cmd_exec=False, return_cmd=False):

	desktop_env = get_desktop_environment()

	if desktop_env == 'windows':

		terminal_cmd_str = 'start powershell.exe'

	if desktop_env == 'mac':

		# Try iTerm2 first, most popular Mac Terminal from what I've heard

		ITERM2_CHECK_SCRIPT = '''APPLESCRIPT=`cat <<EOF
			on run argv
			  try
			    tell application "Finder"
			      set appname to name of application file id "$1"
			      return 1
			    end tell
			  on error err_msg number err_num
			    return 0
			  end try
			end run
			EOF`

			retcode=`osascript -e "$APPLESCRIPT"`
			exit $retcode'''

		iterm2_check_proc = sp.Popen([ITERM2_CHECK_SCRIPT, 'iTerm2'], shell=True, stdout=sp.PIPE)

		iterm2_check_proc.communicate()

		if iterm2_check_proc.returncode == 0:

			terminal_cmd_str = 'open -a iTerm2'

		else:

			terminal_cmd_str = 'open -a Terminal'

	else:

		if is_in_path('x-terminal-emulator'):

			# This is a convenience script that launches terminal based on
			# user preferences.
			# This is not available on some distros (but most have it)
			# so try this first

			terminal_cmd_str = 'x-terminal-emulator'

		elif desktop_env in ['gnome', 'unity', 'cinnamon'] or desktop_env == 'gnome2':

			terminal_cmd_str = 'gnome-terminal'

		elif desktop_env == 'xfce4':

			terminal_cmd_str = 'xfce4-terminal'

		elif desktop_env == 'kde' or desktop_env == 'trinity':

			terminal_cmd_str = 'konsole'

		elif desktop_env == 'i3':

			terminal_cmd_str = 'i3-sensible-terminal'

		elif desktop_env == 'pantheon':

			terminal_cmd_str = 'pantheon-terminal'

		elif desktop_env == 'enlightenment':

			terminal_cmd_str = 'terminology'

		elif desktop_env == 'lxde' or desktop_env == 'lxqt':

			terminal_cmd_str = 'lxterminal'

		else:

			if is_in_path('gnome-terminal'):

				terminal_cmd_str = 'gnome-terminal'

			else:

				if is_in_path('xterm'):

					terminal_cmd_str = 'xterm'

	# Process the terminal_cmd_str

	# if exec_cmd:
	#
	# 	if shell_after_cmd_exec:
	#
	# 		exec_cmd += ' ; ' + os.getenv('SHELL')
	#
	# if desktop_env == 'windows':
	#
	# 	if background:
	#
	# 		terminal_cmd_str = terminal_cmd_str.replace('start', 'start /B', 1)
	#
	# else:
	#
	# 	if exec_cmd:
	#
	# 		if desktop_env == 'mac':
	#
	# 			terminal_cmd_str += ' ' + exec_cmd
	#
	# 		else:
	#
	# 			# Linux/Unix
	# 			# Most Terminals on Linux/Unix use -e 'command to execute'
	#
	# 			terminal_cmd_str += ' -e ' + '\'' + exec_cmd + '\''
	#
	# 	if background:
	#
	# 		terminal_cmd_str += ' &'
	#
	# if exec_cmd:
	#
	# 	if desktop_env == 'windows':
	#
	# 		exec_cmd_script_file += '.ps1'
	#
	# 	if shell_after_cmd_exec:
	#
	# 		if desktop_env == 'windows':
	#
	# 			terminal_cmd_str = terminal_cmd_str.replace('powershell.exe', 'powershell.exe -noexit')
	#
	# 	if not desktop_env == 'windows':
	#
	# 		sp.Popen(['chmod +x %s' % exec_cmd_script_file], shell=True)

	if exec_cmd:

		if desktop_env == 'windows':

			if os.path.isfile(exec_cmd):

				terminal_cmd_str += exec_cmd

			else:

				terminal_cmd_str += ' -Command ' + '"' + exec_cmd + '"'

			if shell_after_cmd_exec:

				terminal_cmd_str += ' -NoExit'

		else:

			if shell_after_cmd_exec:

				exec_cmd += ' ; ' + os.getenv('SHELL')

			if desktop_env == 'mac':

				terminal_cmd_str += ' ' + 'sh -c ' + '"' + exec_cmd + '"'

			else:

				terminal_cmd_str += ' -e ' + 'sh -c ' + '"' + exec_cmd + '"'

	if return_cmd:

		return terminal_cmd_str

	terminal_proc = sp.Popen([terminal_cmd_str], shell=True, stdout=sp.PIPE)

	if not background:

		# Wait for process to complete
		terminal_proc.wait()
