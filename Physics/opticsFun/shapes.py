import json

with open("shapes.json") as file:
    shapes_data = json.load(file)

from settings import *
from line import Line
from light import Laser
from mirror import Mirror

Shapes = {
    "laser": [],
    "mirror": []
}

for key in Shapes.keys():
    if shapes_data[key]["Number"] > 0:
        if shapes_data[key]["array"] is not None:
            array = shapes_data[key]["array"]
            for sub_array in array:
                start_point = sub_array[0]
                end_point = sub_array[1]
                if key == "laser":
                    Shapes[key].append( Laser(start_point, end_point) )
                if key == "mirror":
                    Shapes[key].append( Mirror(start_point, end_point) )
        else:
            if key == "laser":
                Shapes[key].append( Laser() )
            if key == "mirror":
                Shapes[key].append( Mirror() )

if __name__ == "__main__":
    print(Shapes)