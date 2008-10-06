import DST
import math
import numpy
import sns_timing
import SOM
import sys

EMPTY = ""

def __get_corner(point, transmat, orientmat, db):
    newpt = __point_transformation(point, transmat, orientmat)
    if db:
        print "New Point:", newpt
    pol = __calc_polar(newpt[0], newpt[1], newpt[2])
    azi = __calc_azi(newpt[0], newpt[1])
    return (pol, azi)

def __point_transformation(pt, trans, rot):
    rotpt = numpy.dot(rot, pt)
    return rotpt + trans

def __calc_polar(xi, yi, zi):
    xi2 = xi * xi
    yi2 = yi * yi
    zi2 = zi * zi

    return math.acos(zi / math.sqrt(xi2 + yi2 + zi2))

def __calc_azi(xi, yi):
    return math.atan2(yi, xi)

filename = sys.argv[1]
try:
    temp = sys.argv[2]
    debug = True
except IndexError:
    debug = False

# Setup output file
outtag = filename.split('/')[-1].split('_')[0]
outfilename = outtag + "_geom.txt"
outfile = open(outfilename, "w")

timer = sns_timing.DiffTime()

data_dst = DST.getInstance("application/x-NeXus", filename) 
timer.getTime(msg="After reading data ")

SOM_ids = data_dst.get_SOM_ids()

# Get the bank numbers sorted in proper order
bank_list = [SOM_id[0].split('/')[-1] for SOM_id in SOM_ids]
bank_nums = [int(id.replace('bank', '')) for id in bank_list
             if not id.startswith("monitor")]
bank_nums.sort()

signs = [-1.0, 1.0]

timer.getTime(False)

# Grabbing file handle
nexus = data_dst.getResource()

for bank_num in bank_nums:
    bank_id = "bank" + str(bank_num)
    main_path = "/entry/instrument/" + bank_id

    print bank_id

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

    if debug:
        print "Orientation:", orientm

    # Get the bank translation point
    trans_path = main_path + "/origin/translation/distance"
    nexus.openpath(trans_path)
    translation = nexus.getdata().toNumPy()

    if debug:
        print "Translation:", translation
    
    for i in xrange(nx):
        for j in xrange(ny):
            # Make the pixel ID
            nexus_id = SOM.NeXusId(bank_id, i, j)

            if debug:
                print nexus_id

            print >> outfile, nexus_id.toJoinedStr()
                
            # Get pixel center
            x = cur_geom.get_x_pix_offset(nexus_id.toTuple())
            y = cur_geom.get_y_pix_offset(nexus_id.toTuple())

            # Get indicies for nearest neighbors
            xindex = nexus_id.getXindex() + 1
            if xindex == nx:
                xindex -= 2

            yindex = nexus_id.getYindex() + 1
            if yindex == ny:
                yindex -= 2                

            # Make pixel ID for nearest x direction neighbor
            xneighbor_id = SOM.NeXusId(nexus_id.getDetId(), xindex,
                                       nexus_id.getYindex())

            yneighbor_id = SOM.NeXusId(nexus_id.getDetId(), 
                                       nexus_id.getXindex(),
                                       yindex)
            
            # Get x and y from x and y neighbors
            xp = cur_geom.get_x_pix_offset(xneighbor_id.toTuple())
            yp = cur_geom.get_y_pix_offset(yneighbor_id.toTuple())

            # Get half width and half height from pixel centers
            hdw = math.fabs(x - xp) * 0.5
            hdh = math.fabs(y - yp) * 0.5

            polar_angles = []
            azi_angles = []

            # Make each corner and calculate the polar and azimuthal angles
            for signx in signs:
                for signy in signs:
                    cpt = numpy.array([x+(signx*hdw), y+(signy*hdh), 0.0])
                    if debug:
                        print "Corner Pt:", cpt
                    values = __get_corner(cpt, translation, orientm, debug)
                    polar_angles.append(values[0])
                    azi_angles.append(values[1])

            if debug:
                print "Polar:", polar_angles
                print "Azi:", azi_angles

            for polar_angle in polar_angles:
                print >> outfile, polar_angle,

            print >> outfile, EMPTY

            for azi_angle in azi_angles:
                print >> outfile, azi_angle,

            print >> outfile, EMPTY            

timer.getTime(msg="After calculating and writing data ")
