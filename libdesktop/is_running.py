# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# All Rights Reserved.

# Licensed under MIT License (see included LICENSE file).

# This file is part of libdesktop.

import subprocess

def is_running(process):

	try:  # Linux/Unix

		s = subprocess.Popen(['ps', 'axw'], stdout=subprocess.PIPE)

	except:  # Windows

		s = subprocess.Popen(['tasklist', '/v'], stdout=subprocess.PIPE)

	process_list, err = s.communicate()

	return process in str(process_list)
