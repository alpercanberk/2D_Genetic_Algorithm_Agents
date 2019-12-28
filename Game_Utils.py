
import random

def generate_food_coordinates_with_margin(screen_width, screen_height, wall_thickness, density):

    coordinates = []

    for x in range(1, density-1):
        for y in range(1, density-1):
            randx = random.randrange(int(wall_thickness + (x/density)*screen_width), int(wall_thickness + ((x+1)/density)*screen_width))
            randy = random.randrange(int(wall_thickness + (y/density)*screen_height), int(wall_thickness + ((y+1)/density)*screen_height))
            coordinates.append([randx, randy])

    #a few more random food sprinkled in there
    for _ in range(10):
        randx = random.randrange(wall_thickness, wall_thickness + screen_width)
        randy = random.randrange(wall_thickness, wall_thickness + screen_height)
        coordinates.append([randx, randy])

    return coordinates
