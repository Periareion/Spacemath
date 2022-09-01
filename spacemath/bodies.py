
import math

from aquaternion import *

from orbits import Orbit
from constants import AU
import constants


class Body:

    def __init__(self,
            name: str,
            mass: float):
        
        self.name = name
        self.mass = mass
        self.mu = constants.G * self.mass


class SphericalBody(Body):

    def __init__(self,
            name: str,
            mass: float,
            radius: float,
            color: tuple[int]):

        super().__init__(name, mass)

        self.radius = radius
        self.color = color

        self.shadow_area = math.pi * self.radius**2
        self.surface_area = 4 * self.shadow_area
        self.volume = 4 / 3 * math.pi * self.radius**3


class FixedBody(SphericalBody):

    def __init__(self,
            name: str,
            mass: float,
            radius: float,
            color: tuple[int],

            position: Quaternion = Q([0, 0, 0])):

        super().__init__(name, mass, radius, color)

        self.position = Q(position)


class OrbitingBody(SphericalBody):

    def __init__(self,
            name: str,
            mass: float,
            radius: float,
            color: tuple[int],
            
            orbit: Orbit):
        
        super().__init__(name, mass, radius, color)

        self.position = None
        self.orbit = orbit
    
    def update_position(self, t: float = 0):
        self.position = self.orbit.get_position(t)

stars = {
    'Sol': FixedBody(
        'Sol', 1.989*10**30, 6.9634*10**8, (0.8, 0.7, 0.2)),
}

planets = {
    'Mercury': OrbitingBody(
        'Mercury', 0.33010*10**24, 2.4397*10**6, (0.3, 0.3, 0.3),
        Orbit(
            stars['Sol'], 0.38709893*AU, 0.20563, 7.00487,
            48.33167, 77.45645, 252.25084,
            30*constants.seconds_in_year)),
    'Venus': OrbitingBody(
        'Venus', 4.8673*10**24, 6.0518*10**6, (0.8, 0.7, 0.3),
        Orbit(
            stars['Sol'], 0.723*AU, 0.00677323, 3.39471,
            76.68069, 131.53298, 181.97973,
            30*constants.seconds_in_year)),
    'Earth': OrbitingBody(
        'Earth', 5.972*10**24, 6.371*10**6, (0.1, 0.6, 0.9),
        Orbit(
            stars['Sol'], 1*AU, 0.01671, 0.00005,
            -11.26064, 102.94719, 100.46435,
            30*constants.seconds_in_year)),
    'Mars': OrbitingBody(
        'Mars', 1.524*AU, 3.3895*10**6, (0.721, 0.25, 0.13),
        Orbit(
            stars['Sol'], 2.27956*10**6, 0.09341233, 1.85061,
            49.57854, 336.04084, 355.45332,
            30*constants.seconds_in_year)),
}