# -*- coding: utf-8 -*-
import rrdtool
import time

cur_time = str(int(time.time()))
print(cur_time)

# 数据写频率--step为60秒（即每分钟一个数据点）
rrd = rrdtool.create('Flow.rrd', '--step', '60', '--start', cur_time,
                     'DS:en0_in:COUNTER:60:0:U',
                     'DS:en0_out:COUNTER:60:0:U',
                     'RRA:AVERAGE:0.5:1:600',
                     'RRA:AVERAGE:0.5:6:700',
                     'RRA:AVERAGE:0.5:24:775',
                     'RRA:AVERAGE:0.5:288:797',
                     'RRA:AVERAGE:0.5:1:600',
                     'RRA:AVERAGE:0.5:7:700',
                     'RRA:AVERAGE:0.5:24:775',
                     'RRA:AVERAGE:0.5:288:797',
                     'RRA:AVERAGE:0.5:1:600',
                     'RRA:AVERAGE:0.5:7:700',
                     'RRA:AVERAGE:0.5:24:775',
                     'RRA:AVERAGE:0.5:288:797')

if rrd:
    print(rddtool.error())
