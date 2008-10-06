import DST
import math
import numpy
import sns_timing
import SOM
import sys

def __get_corner(point, transmat, orientmat):
    newpt = __point_transformation(point, transmat, orientmat)
    pol = __calc_polar(newpt[0,0], newpt[0,1], newpt[0,2])
    azi = __calc_azi(newpt[0,1], newpt[0,0])
    return (pol, azi)

def __point_transformation(pt, trans, rot):
    rotpt = numpy.dot(rot, pt)
    return rotpt + trans


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

signs = [-1.0, 1.0]

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

    # Fill out rest of 3x3 matrix
    orient.append(orient[1]*orient[5] - orient[2]*orient[4])
    orient.append(orient[2]*orient[3] - orient[0]*orient[5])
    orient.append(orient[0]*orient[4] - orient[1]*orient[3])

    # Put orientation matrix in correct order
    orientm = orient.toNumPy().reshape(3, 3).T

    # Get the bank translation point
    trans_path = main_path + "/origin/translation/distance"
    nexus.openpath(trans_path)
    translation = nexus.getdata().toNumPy()

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

            # Get half width and half height from pixel centers
            hdw = math.fabs(x - xp) * 0.5
            hdh = math.fabs(y - yp) * 0.5

            polar_angles = []
            azi_angles = []

            # Make each corner and calculate the polar and azimuthal angles
            for signx in signs:
                for signy in signs:
                    cpt = numpy.array([x+(signx*hdw), y+(signy*hdh), 0.0])
                    values = __get_corner(cpt, translation, orientm)
                    polar_angles.append(values[0])
                    azi_angle.append(values[1])
            
