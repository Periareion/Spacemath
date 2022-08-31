
from spacemath import *

def tests():
    assert orbits.mean_to_ecc(orbits.ecc_to_mean(1, 0.7), 0.7, 10) == 1
    
if __name__ == '__main__':
    tests()