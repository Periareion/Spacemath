
import math

from .utils import newtons_method


def ecc_to_mean(E, e):
    return E - e * math.sin(E)

e_to_ecc_to_mean = lambda e: lambda E: ecc_to_mean(E, e)


def mean_to_ecc(M, e, n=2):
    """
    Inverse of Kepler's equation using Newton's method
    """
    return newtons_method(
        lambda E: E - e * math.sin(E),
        lambda E: 1 - e * math.cos(E),
        math.pi, (M % math.tau), n)
    

def ecc_to_true(E, e):
    """
    Convert the eccentric anomaly to the true anomaly
    """
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
