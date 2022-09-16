import json

with open("shapes.json") as file:
    shapes_data = json.load(file)

from settings import *
from light import Laser
from mirror import MirrorLine, MirrorCircle

Shapes = {
    "laser": [],
    "mirror_line": [],
    "mirror_circle": []
}

for key in Shapes.keys():
    if shapes_data[key]["Number"] > 0:
        if shapes_data[key]["array"] is not None:
            array = shapes_data[key]["array"]
            for sub_array in array:
                if key == "laser":
                    Shapes[key].append( 
                        Laser(p1=sub_array[0], p2=sub_array[1]) 
                        )
                if key == "mirror_line":
                    Shapes[key].append(
                        MirrorLine(p1=sub_array[0], p2=sub_array[1])
                        )
                if key == "mirror_circle":
                    Shapes[key].append(
                        MirrorCircle(radius=sub_array[0], position=sub_array[1])
                        )
        else:
            # Set default only if both there is at least one object,
            # and it's array is not None
            if key == "laser":
                Shapes[key].append( Laser() )

if __name__ == "__main__":
    print(Shapes)