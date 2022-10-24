from collections import namedtuple

# Stock parameters
strike = 50
rf = 0.10
sigma = 0.3
# dividend_yield = 0.05
t_to_expiration = 1

# Grid parameters
s_min = 1
s_max = 100
s_steps = 99
t_steps = 5000

delta_t = t_to_expiration / t_steps

# Tuple to store grid data
GridPoint = namedtuple('GridPoint', 'ix x fx')
# ix: index point
# x:  stock price
# fx: call option price


def derivatives(values, i):
    gp = values[i]

    if i > 0 and i < s_steps:
        # We know grid point above and below i
        # First get numerical derivatives
        gp_up = values[i + 1]
        gp_down = values[i - 1]

        dfdx_up = (gp_up.fx - gp.fx)/(gp_up.x - gp.x)
        dfdx_down = (gp.fx - gp_down.fx)/(gp.x - gp_down.x)

        dfdx = 0.5  * (dfdx_up + dfdx_down)
        d2fdx2 = (dfdx_up - dfdx_down)/(gp_up.x - gp.x)

    elif i == 0:
        dfdx = 0
        d2fdx2 = 0
    else:
        dfdx = 1
        d2fdx2 = 0
    
    return (dfdx, d2fdx2)


def step(values):
    values_back = []
    for i in range(0, s_steps + 1):
        # C(S,t)
        gp_current = values[i]
        dfdx, d2fdx2 = derivatives(values, i)
    
        # Solve for dCdT in PDE
        dCdT = rf * gp_current.fx - \
               dfdx * gp_current.x * rf - \
               0.5 * d2fdx2 * sigma ** 2 * gp_current.x ** 2
        
        # Numerical derivatives to get C(S,t-delta t)
        c_back = gp_current.fx - delta_t * dCdT
        
        gp_back = GridPoint(ix = i, x = gp_current.x, fx = c_back)
        
        values_back.append(gp_back)
    
    return (values_back)

def initialize():
    values = []
    for i in range(0, s_steps + 1):
        stock = s_min + i * (s_max - s_min)/s_steps
        call = max(stock - strike, 0)
        gp = GridPoint(ix = i, x = stock, fx = call)
        values.append(gp)
    return (values)


# Set up a loop
if __name__ == '__main__':
    values = initialize()
    for _ in range(0, t_steps):
        values = step(values)

    print(values[50])
    
    
