# python-fluid-flow-analysis
a script to analyse fluid flow based on user inputs.

this is a tool that, based on user inputs, calculates:
-flow velocity
-reynold's number
-flow type (based on reynold's number values cited from ward-smith's 'mechanics of fluids', 9th edition)
-friction factor (using Darcy's formula for laminar flow and S.E. Haaland's formula for turbulent flow as is said to be within 1.5% of the experimental value within 'mechanics of fluids')
-pressure loss from inlet to outlet, provided the area is the same
- power loss to friction during flow

it also calculates volumetric flow rates 0.1-2x the inputted value and models this against the ranged pressure and power losses to show the correlation between the two (excluding transitional flows in any plots)
