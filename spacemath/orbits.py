
import math

from aquaternion import *

from .utils import newtons_method


class Orbit:

    def __init__(self,
            parent,
            semi_major_axis: float,
            eccentricity: float,
            inclination: float,
            longitude_ascending_node: float,
            longitude_periapsis: float,
            mean_longitude: float = 0,
            epoch: float = 0,):
        
        self.parent = parent
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.inclination = inclination
        self.longitude_ascending_node = longitude_ascending_node
        self.longitude_periapsis = longitude_periapsis
        self.mean_longitude = mean_longitude
        self.epoch = epoch

        self.mu = parent.mu
        self.argument_periapsis = self.longitude_periapsis - self.longitude_ascending_node
        self.mean_motion = math.sqrt(self.mu/(self.semi_major_axis**3))
        self.semi_latus_rectum = self.semi_major_axis*(1 - self.eccentricity**2)

    def get_position(self, t: float = 0):
        
        mean_anomaly = self.mean_longitude - self.longitude_periapsis + self.mean_motion * (t - self.epoch)
        eccentric_anomaly = mean_to_ecc(mean_anomaly, self.eccentricity)
        true_anomaly = ecc_to_true(eccentric_anomaly, self.eccentricity)
        radius = self.semi_major_axis*(1 - self.eccentricity*math.cos(eccentric_anomaly))

        lon_AN = self.longitude_ascending_node
        arg_Pe =  self.argument_periapsis
        i = self.inclination

        x = radius * (math.cos(lon_AN)*math.cos(arg_Pe+true_anomaly) - math.sin(lon_AN)*math.sin(arg_Pe+true_anomaly)*math.cos(i))
        y = radius * (math.sin(lon_AN)*math.cos(arg_Pe+true_anomaly) + math.cos(lon_AN)*math.sin(arg_Pe+true_anomaly)*math.cos(i))
        z = radius * (math.sin(i)*math.sin(arg_Pe+true_anomaly))

        return Q((x, y, z)) + self.parent.position


def ecc_to_mean(E, e):
    return E - e * math.sin(E)

e_to_ecc_to_mean = lambda e: lambda E: ecc_to_mean(E, e)


def mean_to_ecc(M, e, n=2):
    "Inverse of Kepler's equation using Newton's method"
    return newtons_method(
        lambda E: E - e * math.sin(E),
        lambda E: 1 - e * math.cos(E),
        math.pi, (M % math.tau), n)
    

def ecc_to_true(E, e):
    "Convert the eccentric anomaly to the true anomaly"
    if E > math.pi:
        return math.tau - math.acos((math.cos(E) - e)/(1 - e*math.cos(E)))
    return math.acos((math.cos(E) - e)/(1 - e*math.cos(E)))


def kepler_to_cartesian(
        mu, # G * M
        a, # Semi-major axis
        e, # Eccentricity
        i, # Inclination
        lon_AN, # Longitude of the ascending node
        lon_PE, # Longitude of the periapsis
        lon_MEAN, # Mean longitude
        t, # time
        epoch=60*60*24*365.25*30):
    
    arg_Pe = lon_PE - lon_AN
    
    # Mean motion
    n = math.sqrt(mu/(a**3))

    # Mean anomaly
    M = lon_MEAN - lon_PE + n * (t - epoch)
    
    # Eccentric anomaly
    E = mean_to_ecc(M, e)
    
    # True anomaly
    nu = ecc_to_true(E, e)
    
    # Radius (distance from parent)
    r = a*(1 - e*math.cos(E))
    
    # Semi-latus rectum
    p = a*(1 - e**2)
    
    # Specific angular momentum
    h = math.sqrt(mu*p)

    # Uppercase and lowercase omega idk
    Om = lon_AN
    w =  arg_Pe

    # Position vector
    x = r*(math.cos(Om)*math.cos(w+nu) - math.sin(Om)*math.sin(w+nu)*math.cos(i))
    y = r*(math.sin(Om)*math.cos(w+nu) + math.cos(Om)*math.sin(w+nu)*math.cos(i))
    z = r*(math.sin(i)*math.sin(w+nu))

    # Velocity vector
    v_x = (x*h*e/(r*p))*math.sin(nu) - (h/r)*(math.cos(Om)*math.sin(w+nu) + math.sin(Om)*math.cos(w+nu)*math.cos(i))
    v_y = (y*h*e/(r*p))*math.sin(nu) - (h/r)*(math.sin(Om)*math.sin(w+nu) - math.cos(Om)*math.cos(w+nu)*math.cos(i))
    v_z = (z*h*e/(r*p))*math.sin(nu) + (h/r)*(math.cos(w+nu)*math.sin(i))

    return [x, y, z], [v_x, v_y, v_z]
