# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# All Rights Reserved.

# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

from .get_desktop_environment import get_desktop_environment
import subprocess as sp

def is_in_path(program):

	desktop_env = get_desktop_environment()

	if desktop_env == 'windows':

		path_test_cmd_str = 'where %s' % program

	else:

		path_test_cmd_str = 'hash %s 2>/dev/null' % program

	path_test_proc = sp.Popen(path_test_cmd_str, shell=True, stdout=sp.PIPE)

	path_test_proc.communicate()

	if path_test_proc.returncode == 0:

		return True

	else:

		return False
