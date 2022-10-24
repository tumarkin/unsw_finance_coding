import abc
from collections import namedtuple

################################################################################
# General functions for finite differences
################################################################################

# Tuple to store grid data
#   ix: index point
#   x:  stock price
#   fx: call option price
GridPoint = namedtuple('GridPoint', 'ix x fx')
GridParameters = namedtuple('GridParameters', 'x_steps x_min x_max t t_steps')
CallParameters = namedtuple('CallParameters', 'strike rf sigma')


class PdeSlice:

    def __init__(self, grid_params):
        delta_t = grid_params.t / grid_params.t_steps
        delta_x = (grid_params.x_max - grid_params.x_min)/grid_params.x_steps
        
        self.grid_params = grid_params

        values = []
        for i in range(0, grid_params.x_steps + 1):
            x = grid_params.x_min + i * (grid_params.x_max - grid_params.x_min)/grid_params.x_steps
            fx = self.terminal_value(x)
            gp = GridPoint(ix = i, x = x, fx = fx)
            values.append(gp)
        
        self.delta_t = delta_t
        self.delta_x = delta_x
        self.values  = values
        self.t       = grid_params.t


    def dfdx_left(self, grid_index):
        values = self.values
        if grid_index > 0:
           return (values[grid_index].fx -values[grid_index-1].fx) / self.delta_x
        else:
           return self.dfdx_lower_bound()

    def dfdx_right(self, grid_index):
        values = self.values
        if grid_index < self.grid_params.x_steps:
           return (values[grid_index+1].fx -values[grid_index].fx) / self.delta_x
        else:
           return self.dfdx_upper_bound()

    def dfdx(self, grid_index):
        values = self.values
        return 0.5  * (self.dfdx_left(grid_index)+ self.dfdx_right(grid_index))

    def d2fdx2(self, grid_index):
        values = self.values
        return (self.dfdx_right(grid_index) - self.dfdx_left(grid_index)) / self.delta_x

    def step_backwards(self):
        values_back = []
        for i in range(0, self.grid_params.x_steps + 1):

            # Numerical derivatives to get C(S,t-delta t)
            gp_current = self.values[i]
            fx_back = gp_current.fx - self.delta_t * self.pde_dt(i)
            gp_back = GridPoint(ix = i, x = gp_current.x, fx = fx_back)
            values_back.append(gp_back)
    
        self.values = values_back
        self.t = self.t - self.delta_t
        
    def solve(self):
        while self.t > 0:
            self.step_backwards()
   
    # Functions that subclass needs to define for its specific PDE
    @abc.abstractmethod
    def dfdx_lower_bound(self):
        pass
    
    @abc.abstractmethod
    def dfdx_upper_bound(self):
        pass

    @abc.abstractmethod
    def pde_dt(self, grid_index):
        pass

    @abc.abstractmethod
    def terminal_value(self, stock):
        pass




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
    
        # Solve for dCdT in PDE
        return self.call_params.rf * option_value - \
               self.dfdx(grid_index) * stock_price * self.call_params.rf - \
               0.5 * self.d2fdx2(grid_index) * self.call_params.sigma ** 2 * stock_price ** 2

    def terminal_value(self, stock):
        return max(stock - self.call_params.strike, 0)



# Main function
if __name__ == '__main__':
    grid_params = GridParameters(x_steps = 99, x_min = 1, x_max = 100, t = 1, t_steps = 5000)
    call_params = CallParameters(strike = 50, rf = 0.10, sigma = 0.3)
    pde_slice   = BlackScholesCall(grid_params, call_params)
    
    pde_slice.solve()
    print(pde_slice.values[50])
    
