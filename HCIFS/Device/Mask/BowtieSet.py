from HCIFS.Device.Mask.Mask import Mask
import astropy.units as u

class BowtieSet(Mask):
    """Focal Plane mask (set of 9 masks)
    """
    
    def __init__(self, numON=9, numOFF=8, **specs):
        
        # call the Mask constructor
        super().__init__(**specs)
        
        # Those are the x,y positions of each mask in the set (in mm)
        self.allPos = {1:[0,0], 2:[0,0], 3:[0,0], 
                       4:[0,0], 5:[0,0], 6:[0,0], 
                       7:[0,0], 8:[0,0], 9:[0,0]}
        self.allPos = dict((int(num), pos*u.mm) for (num, pos) in self.allPos.items())
        
        # load specific BowtieSet attributes
        self.numON = int(specs.get('numON', numON))     # mask ON number
        self.numOFF = int(specs.get('numOFF', numOFF))  # mask OFF number
        self.posON = self.allPos[self.numON]
        self.posOFF = self.allPos[self.numOFF]
