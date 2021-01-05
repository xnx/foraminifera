import numpy as np

def Vec(x,y):
    """Creates a 2-D vector as a NumPy array."""
    return np.array((x,y), dtype=float)

class Chamber:
    """A single chamber of a foraminifera."""

    def __init__(self, radius, centre, aperture_in):
        """Initialize the chamber.

        The following attributes are initialized: the (scalar) chamber radius,
        the vector position of the chamber centre and the vector position of
        the "in" aperture.

        """

        self.radius = radius
        self.centre = centre
        self.aperture_in = aperture_in

    def set_aperture_out(self, aperture_out):
        """Set the position of the "out" aperture.

        Set the absolute vector position of the "out" aperture, aperture_out,
        and its vector position relative to the chamber centre, r.

        """

        self.aperture_out = aperture_out
        self.r = self.aperture_out - self.centre

    def intersection(self, other):
        """Find any points of intersection between this circle and other.

        Return the two vector positions of the intersections between this
        circular chamber and another chamber. If the circles don't intersect
        because they don't overlap, return None. If one is inside the other,
        raise a ValueError: this is the signal to stop adding chambers.

        """

        # Some convenient relabelling of the vector centre positions, P0 and P1
        # and scalar radii, r0 and r1.
        P0, P1 = self.centre, other.centre
        r0, r1 = self.radius, other.radius
        # The distance between the circle centres.
        d = np.linalg.norm(P1 - P0)
        if d > r0 + r1:
            # The circles don't intersect
            return None
        if d < abs(r0 - r1):
            # One circle is inside the other: we can't add this chamber
            raise ValueError
        # NB we ignore the case of two identical circles which are not
        # physically realizable in our model.
        a = (d**2 + r0**2 - r1**2) / 2 / d
        h = np.sqrt(r0**2 - a**2)
        P2 = P0 + a / d * (P1  - P0)
        x0, y0 = P0
        x1, y1 = P1
        W = h / d * Vec(y0-y1, x1-x0)
        return P2 + W, P2 - W

    def svg(self, scale, displ, fill_colour='white', edge_colour='black'):
        """Return an SVG representation of the chamber.

        scale is a scaling factor and displ is the (x, y) position in image
        coordinates to displace by.

        """

        cx, cy = scale * self.centre + displ
        r = scale * self.radius
        svg = ('<circle cx="{}" cy="{}" r="{}" style="stroke: {}; '
              'stroke-width: 2px; fill: {};"/>'.format(cx, cy, r, edge_colour,
                                                       fill_colour))
        return svg

class Foram:
    """A class representing a foraminifera as a sequence of chambers."""

    def __init__(self, nchambers, GF, TF, DeltaPhi, fill_colour='white',
                 edge_colour='black'):
        """Initialize the foraminifera.

        The first chamber of the foraminifera is called the proloculus and
        it is defined to have unit radius and an "out" aperture at (1,0).

        Also initialize the chamber expansion ratio, GF, the chamber
        translation ratio, TF, and the angular deviation in the growth vector
        for each chamber, DeltaPhi.

        """
        
        self.fill_colour = fill_colour
        self.edge_colour = edge_colour
        proloculus = Chamber(1, Vec(0,0), None)
        proloculus.set_aperture_out(Vec(1,0))
        self.chambers = [proloculus]
        self.nchambers = nchambers
        self.GF, self.TF, self.DeltaPhi = GF, TF, np.radians(DeltaPhi)
        # self.rot is the rotation matrix corresponding to DeltaPhi
        self.rot = np.array(((np.cos(DeltaPhi), -np.sin(DeltaPhi)),
                            (np.sin(DeltaPhi),  np.cos(DeltaPhi))))

    def make_foram(self):
        """Make a foraminifera."""

        for i in range(1, self.nchambers):
            last_chamber = self.chambers[i-1]
            radius = self.GF * last_chamber.radius
            # The next line can use the '@' infix operator in Python 3.5+:
            # v = self.TF * self.rot @ last_chamber.r
            v = self.TF * self.rot.dot(last_chamber.r)
            centre = last_chamber.aperture_out + v
            chamber = Chamber(radius, centre, last_chamber.aperture_out)
            try:
                aperture_out = self.find_aperture_out(chamber)
            except ValueError:
                # This chamber would contain a previous one: the foraminifera
                # cannont grow any further.
                break
            chamber.set_aperture_out(aperture_out)
            self.chambers.append(chamber)

    def find_aperture_out(self, new_chamber):
        """Find the position of the "out" aperture.

        This is a point on the circle new_chamber which is as close as possible
        to the "in" aperture but not within any other chamber.

        """

        intersections = []
        for chamber in self.chambers:
            ret = chamber.intersection(new_chamber)
            if ret is None:
                # This chamber does not intersect new_chamber.
                continue
            # Check both intersections to ensure that they do not lie within
            # another chamber.
            for P in ret:
                if not self.in_chamber(P):
                    intersections.append(P)

        # Sort the intersections by distance from the "in" aperture...
        intersections.sort(key = lambda e: np.linalg.norm(
                                        new_chamber.aperture_in - e))
        # ... and return the closest.
        return intersections[0]

    def in_chamber(self, P):
        """Return True if P is inside any of the chambers, otherwise False."""

        for chamber in self.chambers:
            # NB because of finite floating point arithmetic, compare with
            # a radius ever so slightly smaller than the actual chamber radius.
            if np.linalg.norm(P - chamber.centre) < chamber.radius*0.999:
                return True
        return False
        
    def make_svg(self, scale=10, width=500, height=500):
        """Make an SVG representation of the foraminifera.

        The chamber coordinates are scaled up by a factor scale and the whole
        image has dimensions width x height.

        """

        svg_chunks = ["""<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{}" height="{}" style="background: #ffffff">
""".format(width, height)]

        for chamber in self.chambers:
            svg_chunks.append(chamber.svg(scale, (width/2, height/2),
                                          self.fill_colour, self.edge_colour))

        svg_chunks.append('</svg>')
        self.svg = '\n'.join(svg_chunks)

    def save_svg(self, filename):
        """Save the SVG image to filename."""
        if self.svg is None:
            self.make_svg()
        with open(filename, 'w') as fo:
            print(self.svg, file=fo)
