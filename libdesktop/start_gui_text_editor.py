# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# All Rights Reserved.

# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

from .is_in_path import is_in_path
from .get_desktop_environment import get_desktop_environment
from .linux_exec_desktop_file import linux_exec_desktop_file
import subprocess as sp

def start_gui_text_editor(file=''):

	desktop_env = get_desktop_environment()

	if desktop_env == 'windows':

		win_default_editor_proc = sp.Popen(['ftype txtfile'], shell=True, stdout=sp.PIPE)

		editor_cmd_str = win_default_editor_proc.communicate()[0]

		editor_cmd_str = editor_cmd_str.decode('utf-8').rstrip().split('=', 1)

		editor_cmd_str = editor_cmd_str[1]

	elif desktop_env == 'mac':

		if file:

			editor_cmd_str = 'open ' + file

		else:

			mac_default_editor_proc = sp.Popen(['defaults read com.apple.LaunchServices LSHandlers -array "{LSHandlerContentType=public.plain-text;}"'], shell=True, stdin=sp.PIPE)

			editor_cmd_str = mac_default_editor_proc.communicate()[0]

			editor_cmd_str = editor_cmd_str.decode('utf-8').rstrip()

			editor_cmd_str = 'open -a ' + editor_cmd_str

	else:

		# Use default handler for text/plain

		unix_default_editor_proc = sp.Popen(['locate $(xdg-mime query default "text/plain")'], shell=True, stdout=sp.PIPE)

		editor_cmd_str = unix_default_editor_proc.communicate()[0]

		editor_cmd_str = editor_cmd_str.decode('utf-8').rstrip()

		if '\n' in editor_cmd_str:

			# Sometimes locate returns multiple results
			# use first one

			editor_cmd_str = editor_cmd_str.split('\n')[0]

		if '.desktop' in editor_cmd_str:

			if file:

				file = 'file://' + file

				linux_exec_desktop_file(editor_cmd_str, file)

			else:

				linux_exec_desktop_file(editor_cmd_str)

		else:

			if file:

				sp.Popen([editor_cmd_str, file], shell=True)

			else:

				sp.Popen([editor_cmd_str], shell=True)
