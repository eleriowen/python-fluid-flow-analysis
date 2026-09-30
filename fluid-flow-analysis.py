import numpy as np
import matplotlib.pyplot as plt

#functions     
def positive_flt_input(prompt):
     while True:
         try: 
             print(prompt)
             user_input = float(input())
             if user_input<=0:
                 print("This number is below 0. Please retry!")
             else:
                 return user_input
         except ValueError:
             print("This input is not entirely numerical. Please retry!")
             
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

#variables
D = positive_flt_input("Enter pipe diameter (m):")
L = positive_flt_input("Enter pipe length (m):")        
Q = positive_flt_input("Enter volumetric flow rate (m\u00b3/s):")
rho = positive_flt_input("Enter density of the fluid (kg/m\u00b3):")
mu = positive_flt_input("Enter viscosity of the fluid (Pas)")
epsilon = positive_flt_input("Enter the surface roughness of the pipe (m):")

#area and flow velocity
A = np.pi*(D/2)**2
v = Q / A
print(f"Flow velocity: {v:.3f} m/s")

#calculating Reynolds' number and printing
Re = reynolds_number(rho, mu, D, v)
print(f"Reynolds' number: {Re:.0f}")

#type of flow, friction factor
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
    f = turbulent_friction_factor(Re,epsilon,D)
    print(f"Friction factor: {f:.5f}")

#pressure & power loss
if not np.isnan(f):
    deltap = pressure_loss(f,L,D,rho,v)
    print(f"Pressure loss: {deltap:.3f} Pa")
    powerloss = power_loss(deltap,Q)
    print(f"Power dissipated by pipe friction: {powerloss:.3f} W")
else:
    print("Pressure loss and power loss not calculated.")       

#ranged analysis (0.1-2 of inputted Q value)
Q_range = np.linspace(0.1*Q,2*Q,100)
v_range = Q_range/A
Re_range = reynolds_number(rho,mu,D,v_range)

#removing transitional Re values using Boolean masks
f_range = np.full(Re_range.shape, np.nan)
laminar_mask = Re_range<2000
turbulent_mask = Re_range>4000
f_range[laminar_mask] = laminar_friction_factor(Re_range[laminar_mask])
f_range[turbulent_mask] = turbulent_friction_factor(Re_range[turbulent_mask],epsilon,D)

#ranged pressure & power loss
deltap_range = pressure_loss(f_range,L,D,rho,v_range)
powerloss_range = power_loss(deltap_range, Q_range)

#plot of Q vs pressure loss
plt.plot(Q_range,deltap_range)
plt.xlabel("Volumetric flow rate, Q (m\u00b3/s)")
plt.ylabel("Pressure loss, Δp (Pa)")
plt.title("Pressure Loss vs Volumetric Flow Rates")
plt.grid()
plt.show()

#plot of Q vs power loss
plt.plot(Q_range,powerloss_range)
plt.xlabel("Volumetric flow rate, Q (m\u00b3/s)")
plt.ylabel("Power loss, P (W)")
plt.title("Power Loss vs Volumetric Flow Rates")
plt.grid()
plt.show()