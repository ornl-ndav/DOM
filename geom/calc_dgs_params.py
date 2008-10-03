import DST
import sns_timing
import sys

filename = sys.argv[1]

timer = sns_timing.DiffTime()

data_dst = DST.getInstance("application/x-NeXus", filename) 
timer.getTime(msg="After reading data ")

SOM_ids = data_dst.get_SOM_ids()

# Get the bank numbers sorted in proper order
bank_list = [SOM_id[0].split('/')[-1] for SOM_id in SOM_ids]
bank_nums = [int(id.replace('bank', '')) for id in bank_list
             if not id.startswith("monitor")]
bank_nums.sort()

# Grabbing file handle
nexus = data_dst.getResource()

