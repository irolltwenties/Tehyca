# -*- coding: utf-8 -*-

import CoolProp.CoolProp as cp

from math import pi, log

def get_intube_flow_area(number_of_tubes, din):
    return (0.25* pi * din**2) * number_of_tubes

def get_re(p_water, t_water, mass_flow, flow_area, hydr_d):
    density = cp.PropsSI('D', 'P', p_water, 'T', t_water)
    viscosity = cp.PropsSI('V', 'P', p_water, 'T', t_water)
    velocity = mass_flow/(flow_area * density)
    return (velocity * hydr_d / (density / viscosity))

def check_thrust(velocity, density, max_thrust = 2250, min_thrust = 500):
    thrust = 0.5 * density * velocity**2
    if min_thrust < thrust < max_thrust:
        return True
    else: return False

def get_alpha_water(p_water, t_water, mass_flow, flow_area, hydr_d):
    density = cp.PropsSI('D', 'P', p_water, 'T', t_water)
    viscosity = cp.PropsSI('V', 'P', p_water, 'T', t_water)
    velocity = mass_flow/(flow_area * density)
    
    pass