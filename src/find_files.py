#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:43:10 2019

@author: rishu
"""
import os
import zipfile
import glob
from subprocess import call
import shutil
import pandas as pd
from osgeo import ogr
import datetime as dt
import numpy as np
from apya.raster import ReadRaster
def get_polygon_from_extents(extents):
	xmin,ymin,xmax,ymax = extents
	return 'POLYGON(('+str(xmin)+' '+str(ymin)+','+str(xmin)+' '+str(ymax)+','+str(xmax)+' '+str(ymax)+','+str(xmax)+' '+str(ymin)+','+str(xmin)+' '+str(ymin)+'))'

def get_good_wkt(polygon):
	good_wkt = []
	wkt1 = polygon
	poly1 = ogr.CreateGeometryFromWkt(wkt1)
	i=0
	for wkt in glob.glob('/home/rishu/Projects/1000/matchncz/inp/wkt/*.wkt'):
		wkt2 = open(wkt).read()
		if not wkt2 == '':
			poly2 = ogr.CreateGeometryFromWkt(wkt2)
			intersection = poly1.Intersection(poly2)
			if not str(intersection) == 'GEOMETRYCOLLECTION EMPTY':
				good_wkt.append(os.path.basename(wkt).split('.')[0])
	return good_wkt


xmin = 76
ymin = 11
xmax = 77
ymax = 12
extents = (xmin, ymin, xmax, ymax)

poly = get_polygon_from_extents(extents)
good_wkts = get_good_wkt(poly)
nc_files = glob.glob('/home/rishu/Projects/1000/matchncz/inp/nc/*.nc')
good_ncs = []
for fl in nc_files:
    b_name = os.path.basename(fl)
    req_name = b_name.split("_")
    req_name.pop()
    req_name = "_".join(req_name)
    if req_name in good_wkts:
        print fl
        good_ncs.append(fl)
        
great_ncs = []

for fl in good_ncs:
    b_name = os.path.basename(fl)
    req_name = b_name.split("_")
    nc_type = req_name.pop()
    if nc_type == 'IA.nc' or nc_type == 'VV.nc':
        great_ncs.append(fl)

des = '/media/rishu/My Passport/berambadi_files/'

sts = [shutil.copyfile(x,des+os.path.basename(x)) for x in great_ncs]