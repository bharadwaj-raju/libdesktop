# coding: utf-8

# This file is part of libdesktop

# The MIT License (MIT)
#
# Copyright (c) 2016 Bharadwaj Raju
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import subprocess as sp
import subprocess
import os
import sys


def get_cmd_out(command):
	'''Get the output of a command.

	Gets a nice Unicode no-extra-whitespace string of the ``stdout`` of a given command.

	Args:
			command (str or list): A string of the command, or a list of the arguments (as would be used in :class:`subprocess.Popen`).

	Note:
			If ``command`` is a ``str``, it will be evaluated with ``shell=True`` i.e. in the default shell (for example, bash).

	Returns:
			str: The ``stdout`` of the command.'''

	if isinstance(command, list):
		result = sp.check_output(command)
	else:
		result = sp.check_output(command, shell=True)

	return result.decode('utf-8').rstrip()


def get_name():
	'''Get desktop environment or OS.

	Get the OS name or desktop environment.

	**List of Possible Values**

	+-------------------------+---------------+
	| Windows				 | windows	   |
	+-------------------------+---------------+
	| Mac OS X				| mac		   |
	+-------------------------+---------------+
	| GNOME 3+				| gnome		 |
	+-------------------------+---------------+
	| GNOME 2				 | gnome2		|
	+-------------------------+---------------+
	| XFCE					| xfce4		 |
	+-------------------------+---------------+
	| KDE					 | kde		   |
	+-------------------------+---------------+
	| Unity				   | unity		 |
	+-------------------------+---------------+
	| LXDE					| lxde		  |
	+-------------------------+---------------+
	| i3wm					| i3			|
	+-------------------------+---------------+
	| \*box				   | \*box		 |
	+-------------------------+---------------+
	| Trinity (KDE 3 fork)	| trinity	   |
	+-------------------------+---------------+
	| MATE					| mate		  |
	+-------------------------+---------------+
	| IceWM				   | icewm		 |
	+-------------------------+---------------+
	| Pantheon (elementaryOS) | pantheon	  |
	+-------------------------+---------------+
	| LXQt					| lxqt		  |
	+-------------------------+---------------+
	| Awesome WM			  | awesome	   |
	+-------------------------+---------------+
	| Enlightenment		   | enlightenment |
	+-------------------------+---------------+
	| AfterStep			   | afterstep	 |
	+-------------------------+---------------+
	| WindowMaker			 | windowmaker   |
	+-------------------------+---------------+
	| [Other]				 | unknown	   |
	+-------------------------+---------------+

	Returns:
			str: The name of the desktop environment or OS.
	'''

	if sys.platform in ['win32', 'cygwin']:
		return 'windows'

	elif sys.platform == 'darwin':
		return 'mac'

	else:
		desktop_session = os.environ.get(
			'XDG_CURRENT_DESKTOP') or os.environ.get('DESKTOP_SESSION')

		if desktop_session is not None:
			desktop_session = desktop_session.lower()

			# Fix for X-Cinnamon etc
			if desktop_session.startswith('x-'):
				desktop_session = desktop_session.replace('x-', '')

			if desktop_session in ['gnome', 'unity', 'cinnamon', 'mate',
								   'xfce4', 'lxde', 'fluxbox',
								   'blackbox', 'openbox', 'icewm', 'jwm',
								   'afterstep', 'trinity', 'kde', 'pantheon',
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
	Check if a program is in the system ``PATH``.

	Checks if a given program is in the user's ``PATH`` or not.

	Args:
			program (str): The program to try to find in ``PATH``.

	Returns:
			bool: Is the program in ``PATH``?
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
			On a Linux system, kernel threads (like	``kthreadd`` etc.)
			are excluded.

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
