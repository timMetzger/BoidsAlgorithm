# By: Timothy Metzger
from p5 import *
import numpy as np
from random import randint

COUNT = 25
boids = []

# Rule tuning factors
C_FACTOR = 100
COLLISION_THRESHOLD = 15
V_FACTOR = 5
MAX_VELOCITY = 15

class Boid:
    def __init__(self,x,y):
        self.position = np.array([x*1.0,y*1.0])
        self.velocity = np.array([1.0,-1.0])

    def display(self):
        x,y = self.position
        fill(255)
        triangle((x+5,y+5),(x+5,y-5),(x+10,y))
        #circle(x,y,10)


def setup():
    size(1000,1000)
    no_stroke()

    global COUNT,boids

    for _ in range(COUNT):
        boids.append(Boid(randint(0,width),randint(0,height)))

def draw():
    background(0)
    global COUNT,boids

    for boid in boids:
        v1 = rule1(boid)
        v2 = rule2(boid)
        v3 = rule3(boid)


        boid.velocity += v1 + v2 + v3
        boid.position += boid.velocity

        check_bounding(boid)
        check_velocity(boid)
        boid.display()

# Center of mass
def rule1(b):
    global COUNT,C_FACTOR,boids

    center = np.array([0.0,0.0])

    for boid in boids:
        if boid is not b:
            center += boid.position

    center = center / (COUNT - 1)
    print("Center: ",center,"Current boid:",b.position,"Correction: ",(center - b.position) / C_FACTOR)
    return (center - b.position) / C_FACTOR

# Collision aovidance
def rule2(b):
    global COUNT, COLLISION_THRESHOLD, boids

    heading = np.array([0.0,0.0])

    for boid in boids:
        if boid is not b:
            diff = abs(boid.position - b.position)
            if np.linalg.norm(diff) < COLLISION_THRESHOLD:
                heading -= (boid.position - b.position)

    return heading * 1.0

# Center of velocity
def rule3(b):
    global COUNT, V_FACTOR, boids

    center = np.array([0.0,0.0])

    for boid in boids:
        if boid is not b:
            center += boid.velocity

    center = center / (COUNT - 1)

    return (center - b.velocity) / V_FACTOR

# Keeps boids within the zone
def check_bounding(b):
    if b.position[0] < 0:
        b.position[0] = width + 10

    elif b.position[0] > width:
        b.position[0] = -10

    if b.position[1] < 0:
        b.position[1] = height + 10

    elif b.position[1] > height:
        b.position[1] = -10

# Limit the boids max velocity
def check_velocity(b):
    global MAX_VELOCITY

    norm = np.linalg.norm(b.velocity)
    if norm > MAX_VELOCITY:
        b.velocity = (b.velocity / norm) * MAX_VELOCITY

if __name__ == "__main__":
    run()