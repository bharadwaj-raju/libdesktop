# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# All Rights Reserved.

# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

import subprocess as sp
from .start_terminal_emulator import start_terminal_emulator

try:

	from gi.repository import Gio

	def linux_exec_desktop_file(desktop_file, *uris):

		launcher = Gio.DesktopAppInfo.new_from_filename(desktop_file)
		launcher.launch_uris(uris, None)

except:

	from xdg import DesktopEntry

	def linux_exec_desktop_file(desktop_file, *uris):

		desktop_file_obj = DesktopEntry.DesktopEntry(filename=desktop_file)

		desktop_file_exec = desktop_file_obj.getExec()

		desktop_file_exec = desktop_file_exec.replace(r'%F', '')
		desktop_file_exec = desktop_file_exec.replace(r'%f', '')

		if uris:

			for i in uris:

				desktop_file_exec += ' ' + i

		if desktop_file_obj.getTerminal():

			start_terminal_emulator(background=True, exec_cmd=desktop_file_exec)

		else:

			sp.Popen([desktop_file_exec], shell=True)
