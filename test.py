from foram import Foram

#foram = Foram(20, 1.1, 0.7, 235)
#foram = Foram(20, 1.1, 0.05, 180)
foram = Foram(20, 1.02, 0.1, 0)     # J
#foram = Foram(50, 1.01, 0.05, 177)  # D
#foram = Foram(50, 1.2, 0.3, -5)     # I
foram.make_foram()
foram.make_svg()
foram.save_svg('foram1.svg')

