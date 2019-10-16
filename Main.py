from opensimplex import OpenSimplex
import numpy as np
from PIL import Image
import math
import random


seed = OpenSimplex(random.randint(0, 1000))     # object used to generate noise
w, h = 400, 300                                 # dimensions of the map
f = 0.03                                        # base frequency. scales frequency of all octaves
hvar = 5.0                                      # height variance. used to alter height values to a more desirable level
elevation = [[0 for x in range(w)] for y in range(h)]
max, maxA, maxB, maxC = -999.0, -999.0, -999.0, -999.0
min, minA, minB, minC = 999.0, 999.0, 999.0, 999.0


def simplex(x, y):                          # simplex algorithm used to create noise for height map
    return (seed.noise2d(x, y) + 1)/2


def adjustment_function(num, pow):          # adjusts heights of elevation map to make stronger contrasts
    return math.pow(num, pow)               # currently just original raised to a power


class Octave:

    def __init__(self, weight, frequency, array):
        self.weight = weight
        self.frequency = frequency
        self.array = array
        print("\ncreated octave with weight: " + str(self.weight) + " and frequency: " + str(self.frequency))

    def fill_array(self):
        for y in range(h):
            for x in range(w):
                self.array[y][x] = self.weight * simplex(x * f * self.frequency, y * f * self.frequency)

    def get_array(self):
        return self.array


oct_A = Octave(1.0, 1.0, [[0 for x in range(w)] for y in range(h)])         # init octaves
oct_B = Octave(0.25, 2.0, [[0 for x in range(w)] for y in range(h)])
oct_C = Octave(0.125, 3, [[0 for x in range(w)] for y in range(h)])

oct_A.fill_array()                                                          # populate arrays
oct_B.fill_array()
oct_C.fill_array()

arr_1 = oct_A.get_array()                                                   # get arrays
arr_2 = oct_B.get_array()
arr_3 = oct_C.get_array()

for y in range(h):                                                          # calculate min/max for testing purposes
    for x in range(w):
        numA = arr_1[y][x]
        numB = arr_2[y][x]
        numC = arr_3[y][x]
        if numA > maxA:
            maxA = numA
        if numA < minA:
            minA = numA
        if numB > maxB:
            maxB = numB
        if numB < minB:
            minB = numB
        if numC > maxC:
            maxC = numC
        if numC < minC:
            minC = numC

for y in range(h):                                                          # add octaves together to get composite img
    for x in range(w):
        num = adjustment_function((arr_1[y][x] + arr_2[y][x] + arr_3[y][x]), hvar)
        num = (int)(num * 255)
        if num > max:
            max = num
        if num < min:
            min = num
        elevation[y][x] = num

print("\nmax elevation A: " + str(maxA) + "\nmin elevation A: " + str(minA))
print("\nmax elevation B: " + str(maxB) + "\nmin elevation B: " + str(minB))
print("\nmax elevation C: " + str(maxC) + "\nmin elevation C: " + str(minC))
print("\nmax elevation: " + str(max) + "\nmin elevation: " + str(min))


water_level = 10                                                          # height map color key
beach_max = 20
plain_max = 200
mtn_max = 253

water = (0, 0, 153)
beach = (255, 255, 102)
plain = (0, 153, 0)
mountain = (128, 128, 128)
snow = (255, 255, 255)

for y in range(h):                  # assign color values
    for x in range(w):
        num = elevation[y][x]
        if num > 255:               # currently cuts off at max value. consider scaling values to fit range 0-255
            num = 255
        if num < water_level:
            elevation[y][x] = water
        elif num < beach_max:
            elevation[y][x] = beach
        elif num < plain_max:
            elevation[y][x] = plain
        elif num < mtn_max:
            elevation[y][x] = mountain
        else:
            elevation[y][x] = snow

array = np.array(elevation, dtype=np.uint8)
img = Image.fromarray(array)
img.save('test.png')
print("\nimg width: " + str(img.size[0]) + "\nimg height: " + str(img.size[1]))