#!/usr/bin/python
# coding=utf-8
import importlib

# if len(sys.argv) == 1:
#     raise SyntaxError("Please provide a module to load.")
module = importlib.import_module('strategy')
module.main()
