# -*- coding: utf-8 -*-
#!/usr/bin/python3


def format_func(n):
    for i in range(1,1+n):
        for k in range(i, n):
            print(' '),
        for j in range(i, 0, -1):
            print(j),
        print("")


if __name__=='__main__':
    format_func(5)
