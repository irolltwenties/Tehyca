# -*- coding: utf-8 -*-

import CoolProp.CoolProp as cp
import numpy as np

from math import pi, log

#Constants
g = 9.80665 # m/s**2
#functions
def get_htc(alpha_water, alpha_steam, d_in, d_out, dtlog, therm_cond_material, thermal_pollution = 10**(-6)):
    htc = 1 / (d_out/(alpha_steam*d_in) + 1/alpha_water + \
               d_in * (log(d_out/d_in))/(2* therm_cond_material) + thermal_pollution)
    return htc

def get_intube_flow_area(number_of_tubes, d_in):
    return (0.25* pi * d_in**2) * number_of_tubes

def f_factor(Re, hydr_d, roughness):
		return round((((8/Re)**12 + (2.457 * log(1 / (((7/Re)**0.9) + 0.27 * roughness / hydr_d)))**16 + \
                 (37530/Re) ** 16)**(-1.5))**(1/12), 4)

def get_re(p_water, t_water, mass_flow, flow_area, hydr_d):
    density = cp.PropsSI('D', 'P', p_water, 'T', t_water, 'H2O')
    viscosity = cp.PropsSI('V', 'P', p_water, 'T', t_water, 'H2O')
    velocity = mass_flow/(flow_area * density)
    return (velocity * hydr_d / (viscosity / density))

def check_thrust(velocity, density, max_thrust = 2250, min_thrust = 500):
    thrust = 0.5 * density * velocity**2
    if min_thrust < thrust < max_thrust:
        return True
    else: return False
    
def get_pressure_loss(p_water, t_water, mass_flow, flow_area, d_in, roughness, length):
    density = cp.PropsSI('D', 'P', p_water, 'T', t_water, 'H2O')
    pr = cp.PropsSI('PRANDTL', 'P', p_water, 'T', t_water, 'H2O')
    velocity = mass_flow / (density * flow_area)
    re = get_re(p_water, t_water, mass_flow, flow_area, d_in)
    f_by_Churchill = f_factor(re, d_in, roughness)
    return ((0.5 * length * density * f_by_Churchill * velocity**2) / d_in)

def get_const(t): #interpolation of empiric constant
    function_results = [7001, 8446, 9680, 10710, 11590, 12320, 12780, 13110, 13290, 13310, 13170]
    function_args = [273.15, 293.15, 313.15, 333.15, 353.15, 373.15, 393.15, 413.15, 433.15, 453.15, 473.15]  
    return np.interp(t, function_args, function_results)  

def get_alpha_water(p_water, t_water, mass_flow, flow_area, hydr_d):
    density = cp.PropsSI('D', 'P', p_water, 'T', t_water, 'H2O')
    viscosity = cp.PropsSI('V', 'P', p_water, 'T', t_water, 'H2O')
    pr = cp.PropsSI('PRANDTL', 'P', p_water, 'T', t_water, 'H2O')
    therm_cond = cp.PropsSI('L', 'P', p_water, 'T', t_water, 'H2O')
    velocity = mass_flow/(flow_area * density)
    re = get_re(p_water, t_water, mass_flow, flow_area, hydr_d)
    nu = 0.023*(re**0.8) * (pr**0.4)
    return nu * therm_cond / hydr_d

'''
def get velocity_steam(ps, q, length, tubes, d_out):
    hs = cp.PropsSI('H', 'P', ps, 'Q', 1, 'H2O')
    density = cp.PropsSI('D', 'P', ps, 'Q', 1, 'H2O')
    hs_c = cp.PropsSI('H', 'P', ps, 'Q', 0, 'H2O')
    mass_flow_steam = q / (hs - hs_c)
    flow_area = ??? need to count from rows of tube bundle, undefined. 
'''

def get_t_log(ts, tw_in, tw_out):
    t_min = ts - tw_out
    t_max = ts - tw_in
    return (t_max - t_min) / log(t_max/t_min)

def get_alpha_steam(ps, q, heat_surface, length, velocity, t_wall):
    hs = cp.PropsSI('H', 'P', ps, 'Q', 1, 'H2O')
    ts = cp.PropsSI('T', 'P', ps, 'Q', 1, 'H2O')
    density = cp.PropsSI('D', 'P', ps, 'Q', 1, 'H2O')
    viscosity = cp.PropsSI('V', 'P', ps, 'Q', 1, 'H2O')
    kyn_viscosity = viscosity / density
    
    hs_c = cp.PropsSI('H', 'P', ps, 'Q', 0, 'H2O')
    density_c = cp.PropsSI('D', 'P', ps, 'Q', 0, 'H2O')
    viscosity_c = cp.PropsSI('V', 'P', ps, 'Q', 0, 'H2O')
    therm_cond_c = cp.PropsSI('L', 'P', ps, 'Q', 0, 'H2O')
    pr_c = cp.PropsSI('PRANDTL', 'P', ps, 'Q', 0, 'H2O')
    kyn_viscosity_c = viscosity_c / density_c
    
    therm_cond_w = cp.PropsSI("L", "P", ps, "T", t_wall, "H2O")
    viscosity_w = cp.PropsSI("V", "P", ps, "T", t_wall, "H2O")
    
    correction_density = (density / density_c) ** 0.5
    re_pl = (length * q / heat_surface) / ((hs - hs_c) * viscosity_c)
    
    if re_pl > 110:
        empiric_const = therm_cond_c * ((g / (kyn_viscosity_c ** 2)) ** 0.33)
        alpha_steam = empiric_const * 0.16 * (pr_c ** 0.33) * re_pl * \
            (1 + (0.013 * correction_density) * (velocity / 1.73) / \
             ((g * kyn_viscosity_c) ** 0.33)) / (re_pl - 100 + 63 * (pr_c ** 0.33))
    elif 0 < re_pl <= 110:
        empiric_const = get_const(ts)
        wave_correlation = re_pl ** 0.04
        wall_correlation = ((therm_cond_w / therm_cond_c) ** 3) * (viscosity_c / viscosity_w) ** (0.125)
        alpha_steam = 1.13 *  ((1 / (length * (ts - t_wall)))**0.25) * wave_correlation * wall_correlation * empiric_const
    else:
        return 'ERROR, RE < 0'
    empiric_const = (velocity/((g * kyn_viscosity_c)**(1/3)))*((density/density_c)**(2/3)) * ((viscosity/viscosity_c)**0.1)* (pr_c**0.5)
    alpha_another = 0.925 * therm_cond_c * ((g / (kyn_viscosity_c**2))**(1/3)) * (re_pl**(-0.28)) * (1 + (0.075 * empiric_const)**3)**0.33
    
    return min(alpha_steam, alpha_another)

def calculation_step(tw_in, pw_in, mass_flow, ps, length, tubes, d_in, d_out, velocity_steam, roughness):
    ts = cp.PropsSI('T', 'P', ps, 'Q', 1, 'H2O')
    hw_in = cp.PropsSI('H', 'P', pw_in, 'T', tw_in, 'H2O')
    intube_flow_area = get_intube_flow_area(tubes, d_in)
    
    tw_out = 0.45*(ts + tw_in)
    searching_area = np.arange(tw_in, tw_out, 0.001)
    heatsurface = length * tubes * pi * d_out
    heatsurface_check = 0
    
    while round(heatsurface, 2) != round(heatsurface_check, 2):
        
        tw_out = searching_area[len(searching_area) // 2]
        hw_out = cp.PropsSI('H', 'P', pw_in, 'T', tw_out, 'H2O')
        tw_mid = 0.5 * (tw_in + tw_out)
        pressure_lost = get_pressure_loss(pw_in, tw_mid, mass_flow, intube_flow_area, d_in, roughness, length)
        alpha_water = get_alpha_water(pw_in, tw_mid, mass_flow, intube_flow_area, d_in)
        t_wall_check = 0.5 * (tw_mid + ts)
        t_wall = t_wall_check - 1
        q = mass_flow * (hw_out - hw_in)
        
        while round(t_wall, 2) != round(t_wall_check, 2):
            t_wall = t_wall_check
            alpha_steam = get_alpha_steam(ps, q, heatsurface, length, velocity_steam, t_wall_check)
            t_wall_check = ts - q / (alpha_steam * heatsurface)
            
        dtlog = get_t_log(ts, tw_in, tw_out)    
        htc = get_htc(alpha_water, alpha_steam, d_in, d_out, dtlog, 16)
        heatsurface_check = q / (htc * dtlog)
        if round(heatsurface*1000) > round(heatsurface_check*1000): 
            pivot = list(searching_area).index(tw_out)
            searching_area = np.delete(searching_area, np.arange(0, pivot))
        elif round(heatsurface*1000) < round(heatsurface_check*1000): 
            pivot = list(searching_area).index(tw_out)
            searching_area = np.delete(searching_area, np.arange(pivot, len(searching_area) - 1))
    return [tw_in, tw_out, htc, t_wall, pw_in - pressure_lost, pressure_lost / pw_in, alpha_water, alpha_steam]

def calculation_sequence(tw_in, pw_in, mass_flow, ps, length_list, tubes, d_in, d_out, velocity_steam, roughness):
    try:
        tw_in, pw_in, mass_flow, ps, length_list, \
            tubes, d_in, d_out, velocity_steam, roughness = np.float64(tw_in), \
                np.float64(pw_in), np.float64(mass_flow), np.float64(ps), \
                    np.float64(length_list), np.float64(tubes), np.float64(d_in), \
                        np.float64(d_out), np.float64(velocity_steam), \
                            np.float64(roughness)
    except ValueError:
        print('ValueError at the start of calculation sequence')
        pass
    
    calculated_data = np.zeros((len(length_list), 8))
    for counter in range(0, len(length_list)):
        if counter == 0:
            calculated_data[counter, 0] = tw_in
            calculated_data[counter] = calculation_step(tw_in, pw_in, mass_flow, ps, length_list[counter], tubes, d_in, d_out, velocity_steam, roughness)
        else:
            calculated_data[counter] = calculation_step(calculated_data[counter - 1, 1], pw_in, mass_flow, ps, length_list[counter], tubes, d_in, d_out, velocity_steam, roughness)           
    return calculated_data

length_list = ['0.375', '0.5', '0.5', '0.375']

print(calculation_sequence('300', '1000000', '50', '340000', length_list, '150', '0.014', '0.016', '17', '0.0001'))











