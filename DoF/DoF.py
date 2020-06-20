#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 22:17:11 2020

@author: inderpreet
"""

import numpy as np
import os
from TB_aws import TB_AWS

channels = ['C21','C31', 'C32', 'C33', 'C34', 'C35', 'C36', 'C41', 'C42', 'C43']
Y = TB_AWS(os.path.expanduser('~/Dendrite/Projects/AWS-325GHz/TB_AWS/TB_AWS_m60_p60.nc'),
           inChannels = channels, option = "3a", T_rec = None)

Y.get_cloudy()
noise = Y.add_noise(Y)
U, S, V = Y.svd()
S_l = Y.get_S_lambda( U, noise)

S_y = Y.cov_mat()

print(S_y.diagonal())
print(S_l)