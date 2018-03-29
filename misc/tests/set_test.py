#!/usr/bin/python
# coding=utf-8

element1 = ("0001", "aaaa")
element2 = ("0001", "aaaa")
element3 = ("0001", "aaab")
element4 = ("0002", "aaaa")

my_set = set()
my_set.add(element1)
my_set.add(element2)
my_set.add(element3)
my_set.add(element4)

print len(my_set)
print my_set
