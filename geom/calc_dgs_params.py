import DST
import sns_timing
import sys

filename = sys.argv[1]

timer = sns_timing.DiffTime()

data_dst = DST.getInstance("application/x-NeXus", filename) 
timer.getTime(msg="After reading data ")

