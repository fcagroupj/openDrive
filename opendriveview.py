#!/usr/bin/env python
# -*- coding: utf8 -*-
# 			opendriveview.py
#
#	input o or long click middle button of mouse 
#	    to open a file for handling, select type of .xodr
# 	the default path is in ~/data
#
# 	in GUI of opendriver, 
# 	    input a to center the show, use mouse to select zoomed region 
# 	    can click left, right button of mouse
# 	    can double click left, middle, right button of mouse
# 	    
#

from __future__ import print_function
# class for opendriveview
class runOpendriveView(object):
    ## the start entry of this class
    def __init__(self):
        pass
    ## xml to opendrive
    def conv_xml2opendrive(self, xml_fname):
        # 1. get data from file
        with open(xml_fname) as fi:
        	xml_root = etree.parse(fi).getroot()
        # 2. get reference data
        self.od_refer_all = []
        self.od_lanes_all = []
        self.od_junct_all = []
        x_max, x_min, y_max, y_min = -9999, 9999, -9999, 9999
        for x_child in xml_root:
            if(x_child.tag == "road"): 
                d_hdg, d_length = 0.0, 0.0                
                road_id = int(x_child.get("id"))
                d_refer_b = []
                d_lanes_b = []
                for y_child in x_child:
                    if(y_child.tag == "planView"): 
                        for z_child in y_child:
                            if(z_child.tag == "geometry"): 
                                curv = None
                                spiral_c = 9999
                                for a_child in z_child:
                                    if(a_child.tag == "arc"): 
                                        curv = a_child.get("curvature")
                                    if(a_child.tag == "spiral"): 
                                        curvS = float(a_child.get("curvStart"))
                                        curvE = float(a_child.get("curvEnd"))
                                        spiral_c = (curvE - curvS)
                                posy =  float(z_child.get("y"))
                                posx =  float(z_child.get("x"))
                                d_hdg =  float(z_child.get("hdg"))
                                d_length =  float(z_child.get("length"))
                                if(True):
                                    if(posy > y_max): y_max = posy
                                    if(posy < y_min): y_min = posy
                                    if(posx > x_max): x_max = posx
                                    if(posx < x_min): x_min = posx
                                    d_refer_b.append( (posx, posy, road_id) )
                                if( curv is not None): 
                                    rr = 1.0 / float( curv )
                                    c_x = posx - rr * math.sin(d_hdg)
                                    c_y = posy + rr * math.cos(d_hdg)
                                    theta = d_length/rr
                                    if(theta > math.pi*2): theta = math.pi*2
                                    n_angle = int(theta / (math.pi/12))
                                    
                                    #print("curv", rr, posx, posy, c_x, c_y, theta, n_angle)
                                    for ii in range(1, n_angle): 
                                        t_angle = -(math.pi/2 - d_hdg) + ii * math.pi/12
                                        posy =  c_y + rr * math.sin(t_angle) 
                                        posx =  c_x + rr * math.cos(t_angle)
                                        if(posy > y_max): y_max = posy
                                        if(posy < y_min): y_min = posy
                                        if(posx > x_max): x_max = posx
                                        if(posx < x_min): x_min = posx
                                        d_refer_b.append( (posx, posy, road_id) )
                                    # end position
                                    if(theta <= math.pi*2):
                                        t_angle = -(math.pi/2 - d_hdg) + theta
                                        posy =  c_y + rr * math.sin(t_angle) 
                                        posx =  c_x + rr * math.cos(t_angle)
                                        if(posy > y_max): y_max = posy
                                        if(posy < y_min): y_min = posy
                                        if(posx > x_max): x_max = posx
                                        if(posx < x_min): x_min = posx
                                        d_refer_b.append( (posx, posy, road_id) )
                                elif( spiral_c < 9999): 
                                    spiral_c = spiral_c / d_length
                                    for ss in range(10, int(d_length), 10): 
                                        (posx2, posy2, t2) = self.od_spirial.odrSpiral(ss, spiral_c)
                                        posy3 =  posy2 + posy 
                                        posx3 =  posx2 + posx 
                                        if(posy3 > y_max): y_max = posy3
                                        if(posy3 < y_min): y_min = posy3
                                        if(posx3 > x_max): x_max = posx3
                                        if(posx3 < x_min): x_min = posx3
                                        d_refer_b.append( (posx3, posy3, road_id) )
                                    # end position
                                    if(int(d_length) < d_length):
                                        (posx2, posy2, t2) = self.od_spirial.odrSpiral(d_length, spiral_c)
                                        posy3 =  posy2 + posy 
                                        posx3 =  posx2 + posx 
                                        if(posy3 > y_max): y_max = posy3
                                        if(posy3 < y_min): y_min = posy3
                                        if(posx3 > x_max): x_max = posx3
                                        if(posx3 < x_min): x_min = posx3
                                        d_refer_b.append( (posx3, posy3, road_id) )
                    if(y_child.tag == "lanes"): 
                        for z_child in y_child:
                            if(z_child.tag == "laneSection"): 
                                for a_child in z_child:
                                    if(a_child.tag == "center"): 
                                        pass
                                    if(a_child.tag == "right" or a_child.tag == "left" ): 
                                        for b_child in a_child:
                                            if(b_child.tag == "lane"): 
                                                tt = ""
                                                (ii,ss,aa,bb,cc) = (0,0,0,0,0)
                                                for c_child in b_child:
                                                    if(c_child.tag == "width"): 
                                                        (ii,ss,aa,bb,cc) = (int(b_child.get("id")), float(c_child.get("sOffset")), 
                                                            float(c_child.get("a")), float(c_child.get("b")), float(c_child.get("c")))
                                                    if(c_child.tag == "roadMark"): 
                                                        tt = c_child.get("type")
                                                d_lanes_b.append( (ii,ss,aa,bb,cc,tt) )
                # if there is one point, add the 2nd
                if( 1 == len(d_refer_b)):
                    (posx0, posy0, road_id0) = d_refer_b[0]
                    posx = posx0 + d_length*math.cos(d_hdg)
                    posy = posy0 + d_length*math.sin(d_hdg)
                    if(posy > y_max): y_max = posy
                    if(posy < y_min): y_min = posy
                    if(posx > x_max): x_max = posx
                    if(posx < x_min): x_min = posx
                    d_refer_b.append( (posx, posy, road_id0) )
                    #print(posx0, posy0, road_id0, d_hdg, d_length) 
                    #print(posx, posy, road_id0) 
                self.od_refer_all.append(d_refer_b)
                self.od_lanes_all.append(d_lanes_b)
            elif(x_child.tag == "junction"): 
                jt_id =  int(x_child.get("id"))
                for y_child in x_child:
                    if(y_child.tag == "connection"): 
                        road_in =  int(y_child.get("incomingRoad"))
                        road_o =  int(y_child.get("connectingRoad"))
                        for z_child in y_child:
                            if(z_child.tag == "laneLink"): 
                                lane_in =  int(z_child.get("from"))
                                lane_o =  int(z_child.get("to"))
                                self.od_junct_all.append( (road_in, lane_in, road_o, lane_o, jt_id) )
                                lane_i_n =  lane_in-lane_in/abs(lane_in)
                                lane_o_n =  lane_o-lane_o/abs(lane_o)
                                if(self.od_is_new_jct(road_in, lane_i_n, road_o, lane_o_n)):
                                    self.od_junct_all.append( (road_in, lane_i_n, road_o, lane_o_n, jt_id) )

                pass
        # 3. draw reference data
        if((x_max - x_min) == 0): refer_z = 10.0
        else: refer_z = VIZ_W / (x_max - x_min) - 0.01
        if((y_max - y_min) == 0): refer_z_y = 10.0
        else: refer_z_y  = VIZ_H / (y_max - y_min) - 0.01
        if(refer_z_y < refer_z): refer_z = refer_z_y
        self.od_refer = [(y_min+y_max)/2, (x_min+x_max)/2, refer_z]
        print("refer_zoom ", refer_z)
        self.od_ref00 = self.od_refer[:]
        #
        self.update_road_data()
