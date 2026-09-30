import numpy as np

#FUNCTIONS      
def positive_flt_input(prompt):
     while True:
         try: 
             print(prompt)
             value = float(input())
             if value<=0:
                 print("Requires a positive number.")
             else:
                 return value
         except ValueError:
             print("Input must be a valid number.")
             
def reynolds_number(rho,mu,D,v):
    Re = (rho*v*D)/mu
    return Re
         
def laminar_friction_factor(Re):
    lff = 64/Re
    return lff

def turbulent_friction_factor(Re,epsilon,D):
    tff = (1/(-3.6*np.log10(((6.9/Re)+(epsilon/(3.71*D))**1.11))))**2
    return tff

def pressure_loss(f,L,D,rho,v):
    dp = f*(L/D)*(rho*(v**2/2))
    return dp

def power_loss(deltap,Q):
    pl = deltap*Q
    return pl

#USER INPUTS

D = positive_flt_input("Enter pipe diameter (m):")
L = positive_flt_input("Enter pipe length (m):")        
Q = positive_flt_input("Enter volumetric flow rate (m^3/s):")
rho = positive_flt_input("Enter density of the fluid (kg/m^3):")
mu = positive_flt_input("Enter viscosity of the fluid (Pa*s)")
epsilon = positive_flt_input("Enter the surface roughness of the pipe (m):")

#calculating area of pipe and flow velocity
#also rounded all printed values for v2
A = np.pi*(D/2)**2
v = Q / A
print(f"Flow velocity: {v:.3f} m/s")

#calculating Reynolds' number and printing
Re = reynolds_number(rho, mu, D, v)
print(f"Reynolds' value: {Re:.0f}")

#evaluating type of flow and printing a response and calculating friction factor based on Reynolds' number
#note:these reference numbers were decided by Ward-Smith's 'mechanics of fluids'
#note:using the darcy friction factor equation here for laminar flow
if Re<2000:
    print("Flow type: Laminar")
    f = laminar_friction_factor(Re)
    print(f"Friction factor: {f:.5f}.")
elif 2000<=Re<=4000:
    print("Flow type: Transitional")
    f = np.nan
    print("Friction factor: indeterminate with model as flow is transitional.")
else:
    print("Flow type: Turbulent")
#note:S.E. Haaland's equation is being used as is said to be within 1.5% of correct value in 'mechanics of fluids'
    f = turbulent_friction_factor(Re, epsilon, D)
    print(f"Friction factor: {f:.5f}")

#calculating pressure loss and power dissipated by pipe friction
if not np.isnan(f):
    deltap = pressure_loss(f, L, D, rho, v)
    print(f"Pressure loss: {deltap:.3f} Pa")
    powerloss = power_loss(deltap, Q)
    print(f"Power dissipated by pipe friction: {powerloss:.3f} W")
else:
    print("Pressure loss and power loss not calculated.")       

#producing a graph of Q against delta p, using a range of 0.1Q-2Q
Q_range = np.linspace(0.1*Q, 2*Q,100)
v_range = Q_range/A
Re_range = reynolds_number(rho,mu,D,v_range)

#creating an empty friction factor array to fill with non-transitional values
f_range = np.full(Re_range.shape, np.nan)
laminar_mask = Re_range<2000
turbulent_mask = Re_range>4000

#calculating f_range for all laminar and turbulent values using Boolean masks to separate data into flow types
f_range[laminar_mask] = laminar_friction_factor(Re_range[laminar_mask])
f_range[turbulent_mask] = turbulent_friction_factor(Re_range[turbulent_mask],epsilon,D)

#calculating delta_range and powerloss_range
deltap_range = pressure_loss(f_range,L,D,rho,v_range)
powerloss_range = power_loss(deltap_range, Q_range)