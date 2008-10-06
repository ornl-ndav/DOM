import DST
import math
import sns_timing
import SOM
import sys

def __calc_polar(xi, yi, zi):
    xi2 = xi * xi
    yi2 = yi * yi
    zi2 = zi * zi

    return 0.5 * math.acos(zi / math.sqrt(xi2 + yi2 + zi2))

def __calc_azi(xi, yi):
    return math.atan2(yi, xi)

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

    # Get the bank orienatation matrix
    orient_path = main_path + "/origin/orientation/value"
    nexus.openpath(orient_path)
    orient = nexus.getdata()

    # Get the bank translation point
    trans_path = main_path + "/origin/translation/distance"
    nexus.openpath(trans_path)
    translation = nexus.getdata()

    for i in xrange(nx):
        for j in xrange(ny):
            # Make the pixel ID
            nexus_id = SOM.NeXusId(bank_id, i, j).toTuple()

            # Get pixel center
            x = cur_geom.get_x_pixel_offset(nexus_id)
            y = cur_geom.get_y_pixel_offset(nexus_id)

            # Get indicies for nearest neighbors
            xindex = nexus_id.getXindex() + 1
            if xindex == nx:
                xindex -= 2

            yindex = nexus_id.getYindex() + 1
            if yindex == ny:
                yindex -= 2                

            # Make pixel ID for nearest x direction neighbor
            xneighbor_id = SOM.NeXusID(nexus_id.getDetId(), xindex,
                                       nexus_id.getYindex()).toTuple()

            yneighbor_id = SOM.NeXusID(nexus_id.getDetId(), 
                                       nexus_id.getXindex(),
                                       yindex).toTuple()
            
            # Get x and y from x and y neighbors
            xp = cur_geom.get_x_pixel_offset(xneighbor_id)
            yp = cur_geom.get_y_pixel_offset(yneighbor_id)

            # Get width and height from pixel centers
            dw = math.fabs(x - xp)
            dh = math.fabs(y - yp)
