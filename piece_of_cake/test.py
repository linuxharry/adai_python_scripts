# -*- coding: utf-8 -*-


class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age


laowang = Person("laowang", 10000)
print(laowang.name)
print(laowang.age)


