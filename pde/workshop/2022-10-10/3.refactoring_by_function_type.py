from collections import namedtuple

# Stock parameters
strike = 50
rf = 0.10
sigma = 0.3
# dividend_yield = 0.05
t_to_expiration = 1

# Grid parameters
x_min = 1
x_max = 100
x_steps = 99
t_steps = 5000

delta_t = t_to_expiration / t_steps
delta_x = (x_max - x_min)/x_steps

################################################################################
# General functions for finite differences
################################################################################

# Tuple to store grid data
#   ix: index point
#   x:  stock price
#   fx: call option price
GridPoint = namedtuple('GridPoint', 'ix x fx')

def dfdx_left(values, grid_index):
    if grid_index > 0:
       return (values[grid_index].fx -values[grid_index-1].fx) / delta_x
    else:
       return dfdx_lower_bound()

def dfdx_right(values, grid_index):
    if grid_index < x_steps:
       return (values[grid_index+1].fx -values[grid_index].fx) / delta_x
    else:
       return dfdx_upper_bound()

def dfdx(values, grid_index):
    return 0.5  * (dfdx_left(values, grid_index)+ dfdx_right(values, grid_index))

def d2fdx2(values, grid_index):
    return (dfdx_right(values, grid_index) - dfdx_left(values, grid_index)) / delta_x

def step(values):
    values_back = []
    for i in range(0, x_steps + 1):

        # Numerical derivatives to get C(S,t-delta t)
        gp_current = values[i]
        fx_back = gp_current.fx - delta_t * pde_dt(values, i)
        
        gp_back = GridPoint(ix = i, x = gp_current.x, fx = fx_back)
        
        values_back.append(gp_back)
    
    return (values_back)
    
def initialize():
    values = []
    for i in range(0, x_steps + 1):
        x = x_min + i * (x_max - x_min)/x_steps
        fx = terminal_value(x)
        gp = GridPoint(ix = i, x = x, fx = fx)
        values.append(gp)
    return (values)
    
################################################################################
# Specific to the black scholes pde
################################################################################
def dfdx_lower_bound():
    return 0
    
def dfdx_upper_bound():
    return 1

def pde_dt(values, grid_index):
    gp = values[grid_index]
    option_value = gp.fx
    stock_price = gp.x
    
    # Solve for dCdT in PDE
    return rf * option_value - \
           dfdx(values, grid_index) * stock_price * rf - \
           0.5 * d2fdx2(values, grid_index) * sigma ** 2 * stock_price ** 2

def terminal_value(stock):
    return max(stock - strike, 0)



# Main function
if __name__ == '__main__':
    values = initialize()
    for _ in range(0, t_steps):
        values = step(values)

    print(values[50])
