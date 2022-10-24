from collections import namedtuple
from pde import PdeSlice, GridParameters

CallParameters = namedtuple('CallParameters', 'strike rf sigma dividend_yield')

class BlackScholesCall(PdeSlice):
    def __init__(self, grid_params, call_params):
        self.call_params = call_params
        super().__init__(grid_params)
        
    def dfdx_lower_bound(self):
        return 0
    
    def dfdx_upper_bound(self):
        return 1

    def pde_dt(self, grid_index):
        gp = self.values[grid_index]
        option_value = gp.fx
        stock_price = gp.x
    
        return self.call_params.rf * option_value - \
               self.dfdx(grid_index) * stock_price * (self.call_params.rf - self.call_params.dividend_yield) - \
               0.5 * self.d2fdx2(grid_index) * self.call_params.sigma ** 2 * stock_price ** 2

    def discrete_choice_value(self, grid_index):
        stock_price = self.values[grid_index].x
        return stock_price - self.call_params.strike        
        
    def terminal_value(self, stock):
        return max(stock - self.call_params.strike, 0)


# Main function
if __name__ == '__main__':
    grid_params = GridParameters(x_steps = 99, x_min = 1, x_max = 100, t = 1, t_steps = 5000)
    call_params = CallParameters(strike = 50, rf = 0.10, sigma = 0.3, dividend_yield = 0.50)
    pde_slice   = BlackScholesCall(grid_params, call_params)
    
    pde_slice.solve()
    print(pde_slice.values[50])
    
