import DST
import sns_timing
import sys

filename = sys.argv[1]

timer = sns_timing.DiffTime()

data_dst = DST.getInstance("application/x-NeXus", filename) 
timer.getTime(msg="After reading data ")

SOM_ids = data_dst.get_SOM_ids()

# Get the bank numbers sorted in proper order
#bank_list = [SOM_id[0].split('/')[-1] for SOM_id in SOM_ids]
#bank_nums = [int(id.replace('bank', '')) for id in bank_list
#             if not id.startswith("monitor")]
#bank_nums.sort()

bank_nums = [1]

# Grabbing file handle
nexus = data_dst.getResource()

for bank_num in bank_nums:
    bank_id = "bank" + str(bank_num)
    main_path = "/entry/instrument/" + bank_id

    # Get the bank geometry
    cur_geom = data_dst.getInstrument(main_path)

    # Get the number of pixels in each direction of the bank
    nx = cur_geom.get_num_x()
    ny = cur_geom.get_num_y()

