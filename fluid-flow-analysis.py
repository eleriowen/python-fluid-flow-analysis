import numpy as np

#hard coded values - will eventually become user inputs
#note:the values for rho and mu are given for a temp of 20 degrees celcius
D = 0.05
L = 10
Q = 0.0002
rho = 998
mu = 0.001002
epsilon = 0.000045

#calculating area of pipe and flow velocity
A = np.pi*(D/2)**2
v = Q / A
print(f"Flow velocity: {v}m/s")

#calculating Reynolds' number
Re = (rho*v*D)/mu
print(f"Reynolds' value: {Re}")

#evaluating type of flow and printing a response and calculating friction factor based on Reynolds' number
#note:these reference numbers were decided by Ward-Smith's 'mechanics of fluids'
if Re<2000:
    print("Flow type: Laminar")
    f = 16/Re
    print(f"Friction factor: {f}.")
    deltap = f*(L/D)*(rho*(v**2/2))
    print(f"Pressure loss: {deltap}Pa")
    powerloss = deltap*Q
    print(f"Power dissipated by pipe friction: {powerloss}W") 
#determining pressure loss
elif 2000<=Re<=4000:
    print("Flow type: Transitional")
    print("Friction factor: indeterminate with model as flow is transitional.")
    print("Cannot determine pressure or head loss. Ending script.")
    exit()
else:
    print("Flow type: Turbulent")
#note:S.E. Haaland's equation is being used as is said to be within 1.5% of correct value in 'mechanics of fluids'
    f = (1/(-3.6*np.log10(((6.9/Re)+(epsilon/(3.71*D))**1.11))))**2
    print(f"Friction factor: {f}")
    deltap = f*(L/D)*(rho*(v**2/2))
    print(f"Pressure loss: {deltap}Pa")
    powerloss = deltap*Q
    print(f"Power dissipated by pipe friction: {powerloss}W") 
