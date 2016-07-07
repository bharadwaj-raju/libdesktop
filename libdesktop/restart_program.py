# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# All Rights Reserved.

# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

import subprocess as sp
import sys
import time

def restart_program(additional_args=None, remove_args=None):

	# Restart
	# preserving all original arguments and optionally adding more
	# or removing more

	# Why these two ifs?
	# Because: http://stackoverflow.com/a/2004272/5413945

	if additional_args is None:

		additional_args = []

	if remove_args is None:

		remove_args = []

	new_cmd = ''

	for i in sys.argv:

		new_cmd += ' ' + i

	if not remove_args == []:

		for arg in remove_args:

			if arg in new_cmd:

				new_cmd = new_cmd.replace(arg, '')

	if not additional_args == []:

		for arg in additional_args:

			new_cmd += ' ' + arg

	with open('/tmp/restart.sh', 'w') as f:

		f.write('python3 %s &' % new_cmd)

	sp.Popen(['sh /tmp/restart.sh'], shell=True)

	time.sleep(1.5)  # Allow restart.sh to fully execute

	sys.exit(0)
