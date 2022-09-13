from Pde import PdeSlice, GridParameters
from fractions import Fraction
from collections import namedtuple

CallParameters = namedtuple('CallParameters', 'strike rf sigma dividend_yield')

class BlackScholesCall(PdeSlice):
    def __init__(self, gp, cp):
        self.call_parameters = cp        
        super().__init__(gp)

    def initialize_value(self, x):
        return max(x - self.call_parameters.strike, 0)

    def ddx_upper_bound(self):
        return 1
        
    def ddx_lower_bound(self):
        return 0
        
    def pde_dt(self, grid_point):
        s = grid_point.x
        v = grid_point.fx
        ix = grid_point.ix
        cp = self.call_parameters

        return (cp.rf  * v) - ((cp.rf - cp.dividend_yield) * s  * self.ddx(ix)) - (0.5 * cp.sigma**2 * s**2 * self.d2dx2(ix))
        
if __name__ == '__main__':
    gp = GridParameters(x_steps = 100, x_min = 1, x_max = 100, t = Fraction(1, 1), t_steps = 5000)
    cp = CallParameters(strike = 50, rf = 0.10, sigma = 0.3, dividend_yield = 0.05)
    pde = BlackScholesCall(gp, cp)
    pde.solve()
    for gp in pde.grid:
        print(gp)
    