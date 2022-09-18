import numpy as np
from numpy.linalg import norm

class HitManager(object):
    def __init__(self):
        pass

    def arangeHits(self, line, shapes):
        '''
        this function both set cross points of given line and shapes,
        and returns the objects the line hit, by order of closest to farthest
        '''
        
        # first clear previous calculated lists
        line_crossPoints = []
        hit_objects = np.array([])
        distances_to_objects = np.array([])

        # check cross point of the given line 
        # with all given shapes
        for shape in shapes:
            crossPoint = shape.getCrossPoint(line)

            if crossPoint is not None:

                # only if the cross point is on the line and the shape, keep it.
                if line.checkPointOn(crossPoint) and shape.checkPointOn(crossPoint):
                    line_crossPoints.append(crossPoint)
                    
                    distance = norm( np.array(line.p1) - np.array(crossPoint) )
                    distances_to_objects = np.append(distances_to_objects, distance)
                    hit_objects = np.append(hit_objects, shape)
        
        # sort hit objects by their order of distance 
        # to the start point of the line
        dist_sorted_indices = distances_to_objects.argsort()
        hit_objects = hit_objects[dist_sorted_indices[::1]]
        line_crossPoints = np.array(line_crossPoints)

        # set cross point of line by the first it meets
        if len(line_crossPoints) > 0:
            line.cross_point = line_crossPoints[ dist_sorted_indices[::1] ][0, :]
            hit_objects[0].cross_point = list(line_crossPoints[dist_sorted_indices[::1]][0, :])
            for hit_object in hit_objects[1:]:
                hit_object.cross_point = None
        else:
            line.cross_point = None
            for hit_object in hit_objects:
                hit_object.cross_point = None
        
        return hit_objects

    def calculateReflected(self, shapes, reflected_num):
        # Clear previous reflected laser rays
        del shapes["laser"][:-reflected_num-1:-1]
        reflected_num = 0
        
        # Find all reflected lasers
        mirrors = shapes["mirror_line"] + shapes["mirror_circle"]
        for laser in shapes["laser"]:
            laser.findEndpoint()
            
            hit_objects = self.arangeHits(laser, mirrors)
            
            for hit_object in hit_objects:
                reflected = hit_object.reflect(laser)
                if reflected is not None:
                    reflected_num += 1
                    shapes["laser"].append( reflected )
            
            # Currently the program can't handle too much rays.
            # This is temporary solution.
            if len(shapes["laser"]) > 20:
                break

        return reflected_num