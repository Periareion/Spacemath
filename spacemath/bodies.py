
import math

from aquaternion import *

from .orbits import Orbit
from .constants import AU
from . import constants


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
        'Sol', 1.989e30, 6.9634e8, (0.8, 0.7, 0.2)),
}

planets = {
    'Mercury': OrbitingBody(
        'Mercury', 0.33010e24, 2.4397e6, (0.3, 0.3, 0.3),
        Orbit(
            stars['Sol'], 0.38709893*AU, 0.20563, 7.00487,
            48.33167, 77.45645, 252.25084,
            30*constants.seconds_in_year)),
    'Venus': OrbitingBody(
        'Venus', 4.8673e24, 6.0518e6, (0.8, 0.7, 0.3),
        Orbit(
            stars['Sol'], 0.723*AU, 0.00677323, 3.39471,
            76.68069, 131.53298, 181.97973,
            30*constants.seconds_in_year)),
    'Earth': OrbitingBody(
        'Earth', 5.972e24, 6.371e6, (0.1, 0.6, 0.9),
        Orbit(
            stars['Sol'], 1*AU, 0.01671, 0.00005,
            -11.26064, 102.94719, 100.46435,
            30*constants.seconds_in_year)),
    'Mars': OrbitingBody(
        'Mars', 0.64169e24, 3.3895e6, (0.721, 0.25, 0.13),
        Orbit(
            stars['Sol'], 1.52366231*AU, 0.09341233, 1.85061,
            49.57854, 336.04084, 355.45332,
            30*constants.seconds_in_year)),
    'Jupiter': OrbitingBody(
        'Jupiter', 1898.13e24, 69.911e6, (0.8, 0.7, 0.5),
        Orbit(
            stars['Sol'], 5.20336301*AU, 0.04839266, 1.30530,
            100.55615, 14.75385, 34.40438,
            30*constants.seconds_in_year)),
    'Saturn': OrbitingBody(
        'Saturn', 568.32e24, 58.232e6, (0.95, 0.8, 0.5),
        Orbit(
            stars['Sol'], 9.5370732*AU, 0.05415060, 2.48446,
            113.71504, 92.43194, 49.94432,
            30*constants.seconds_in_year)),
    'Uranus': OrbitingBody(
        'Uranus', 86.811e24, 25.362e6, (0.8, 0.9, 0.95),
        Orbit(
            stars['Sol'], 19.19126393*AU, 0.04716771, 0.76986,
            74.22988, 170.96424, 313.23218,
            30*constants.seconds_in_year)),
    'Neptune': OrbitingBody(
        'Neptune', 102.409e24, 24.622e6, (0.3, 0.5, 0.95),
        Orbit(
            stars['Sol'], 30.06896348*AU, 0.00858586, 1.76917,
            131.72169, 44.97135, 304.88003,
            30*constants.seconds_in_year)),
}