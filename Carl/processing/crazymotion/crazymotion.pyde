from collections import deque
from random import choice

class Rotator(object):
    """
    A spinning point.
    """
    def __init__(self, radius, angle=None, step=None):
        self.radius = radius
        self.angle = angle or 0
        self.step = step or radians(3)
    
    @property
    def x(self):
        return cos(self.angle) * self.radius
    
    @property
    def y(self):
        return sin(self.angle) * self.radius
    
    def update(self):
        self.angle += self.step


MINRADIUS = 10
MAXRADIUS = 250
MINSTEP = -9
MAXSTEP = 9

def randomrotator():
    """
    A randomly generated spinning point.
    """
    radius = random(MINRADIUS, MAXRADIUS)
    angle = radians(choice(range(0, 360, 30)))
    step = radians(choice(range(MINSTEP, MAXSTEP)))
    return Rotator(radius, angle, step)

def randomcolor(minc=25, maxc=255):
    """
    Return a 3-tuple, random RGB color.
    """
    return (random(minc, maxc), random(minc, maxc), random(minc, maxc))

# Min/max number of rotating points to create.
MINROTATORS = 2
MAXROTATORS = 10

# Length of worm body
WORMLENGTH = 25

# Worm ellipse size
MINSIZE = 5
MAXSIZE = 50

class Worm(object):
    """
    A collection of Rotator objects, whose x/y is summed to get a final point.
    The points generated every step are saved to provide a body for the worm.
    """
    def __init__(self, n=None, size=None, strokecolor=None, fillcolor=None):
        if n is None:
            n = int(random(MINROTATORS, MAXROTATORS))
        self.rotators = [randomrotator() for _ in range(n)]
        self.positions = deque([], WORMLENGTH)
        self.strokecolor = strokecolor or randomcolor()
        self.fillcolor = fillcolor or randomcolor()
        self.size = size or random(MINSIZE, MAXSIZE)
    
    @property
    def x(self):
        return width/2 + sum(d.x for d in self.rotators)
    
    @property
    def y(self):
        return height/2 + sum(d.y for d in self.rotators)
    
    def draw(self):
        a = 25
        astep = (255 - 25) / len(self.positions)
        for x, y in self.positions:
            fill(*(self.fillcolor + (a, )))
            stroke(*(self.strokecolor + (a, )))
            ellipse(x, y, self.size, self.size)
            a += astep
        
    def update(self):
        for Rotator in self.rotators:
            Rotator.update()
        self.positions.append((self.x, self.y))

NWORMS = 5
TEXTSIZE = 22

worms = []
drawing = {'worms': False, 'average': True, 'help': True}
drawingtogglekeys = {k[0]:k for k in drawing}

def setup():
    size(1024, 900)
    textSize(TEXTSIZE)
    randomize_worms()
    
def randomize_worms():
    """
    Fill the worms list with randomly generated worms.
    """
    while worms:
        worms.pop()
    for _ in range(NWORMS):
        worms.append(Worm())

def keyPressed():
    keystr = str(key).lower()
    if keystr == 'r':
        randomize_worms()
    else:
        for k,v in drawingtogglekeys.items():
            if keystr == k:
                drawing[v] = not drawing[v]

def average(values):
    return sum(values) / len(values)

def draw_worms():
    for worm in worms:
        worm.draw()
    
def draw_average_ellipse():
    avgx = average([rg.x for rg in worms])
    avgy = average([rg.y for rg in worms])
    fill(255)
    ellipse(avgx, avgy, 25, 25)

def draw_help():
    y = TEXTSIZE
    text('Help', 5, y)
    y += TEXTSIZE
    text('r: re-randomize', 5, y)    
    for k,v in drawingtogglekeys.items():
        y += TEXTSIZE
        text('%s: toggle %s' % (k, v), 5, y)

def draw():
    background(192,64,0)
    
    for worm in worms:
        worm.update()
    
    if drawing['help']:
        draw_help()
    
    if drawing['worms']:
        draw_worms()
        
    if drawing['average']:
        draw_average_ellipse()