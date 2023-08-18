#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 12:06:19 2023

@author: robertsoncl
"""
from guiScript import guiScript


class additionScript(guiScript):
    def __init__(self,
                 home_directory="/home/robertsoncl/",
                 input_filename="partrec_test"):
        def openFile():
            file = open(home_directory + "topas/" + input_filename, "a")
            return file
        self.openFile = openFile
