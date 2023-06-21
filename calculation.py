# -*- coding: utf-8 -*-

import CoolProp.CoolProp as cp

from math import pi, log

#КОНСТАНТЫ
g = 9.80665 #ускорение свободного падения м/с**2


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
    
def get_pressure_loss():
    pass

def get_alpha_water(p_water, t_water, mass_flow, flow_area, hydr_d):
    density = cp.PropsSI('D', 'P', p_water, 'T', t_water)
    viscosity = cp.PropsSI('V', 'P', p_water, 'T', t_water)
    pr = cp.PropsSI('PRANDTL', 'P', p_water, 'T', t_water)
    therm_cond = cp.PropsSI('PRANDTL', 'L', p_water, 'T', t_water)
    velocity = mass_flow/(flow_area * density)
    re = get_re(p_water, t_water, mass_flow, flow_area, hydr_d)
    nu1 = (0.023 * (pr**0.33) * re ** 0.8)/(1 + 2.14 * (re ** (-0.1)) * (pr ** 0.7 - 1))
    nu2 = 0.023*(re**0.8) * (pr**0.4)
    nu = min(nu1, nu2)
    return nu * therm_cond / hydr_d

'''
def get velocity_steam(ps, q, length, tubes, d_out):
    hs = cp.PropsSI("H", "P", ps, "Q", 1, "H2O")
    density = cp.PropsSI("D", "P", ps, "Q", 1, "H2O")
    hs_c = cp.PropsSI("H", "P", ps, "Q", 0, "H2O")
    mass_flow_steam = q / (hs - hs_c)
    flow_area = ??? need to count from rows of tube bundle, undefined. 
'''


def get_alpha_steam(ps, q, heat_surface, length, velocity):
    hs = cp.PropsSI("H", "P", ps, "Q", 1, "H2O")
    density = cp.PropsSI("D", "P", ps, "Q", 1, "H2O")
    
    hs_c = cp.PropsSI("H", "P", ps, "Q", 0, "H2O")
    density_c = cp.PropsSI("D", "P", ps, "Q", 0, "H2O")
    viscosity_c = cp.PropsSI("V", "P", ps, "Q", 0, "H2O")
    therm_cond_c = cp.PropsSI("L", "P", ps, "Q", 0, "H2O")
    pr_c = cp.PropsSI("PRANDTL", "P", ps, "Q", 0, "H2O")
    kyn_viscosity_c = density_c / viscosity_c
    
    
    
    correction_density = (density / density_c) ** 0.5
    re_pl = (length * q / heat_surface) / ((hs - hs_c) * viscosity_c)
    
    if re_pl > 110:
        empiric_const = therm_cond_c * ((g / (kyn_viscosity_c ** 2)) ** 0.33)
        alpha_steam = empiric_const * 0.16 * (pr_c ** 0.33) * re_pl * \
            (1 + (0.013 * correction_density) * (velocity / 1.73) / ((g * kyn_viscosity_c) ** 0.33)) / (re_pl - 100 + 63 * (pr_c ** 0.33))
    
    pass