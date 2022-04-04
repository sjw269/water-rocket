from math import *
import numpy as np
import matplotlib.pyplot as plt

def press(volume, temperature, pressure_initial, temp_initial, volume_initial):
    return (((pressure_initial * volume_initial) / temp_initial) * temperature) / volume

def exit_velocity(pressure, pressure_atm):
    return sqrt((pressure - pressure_atm) / 500)

def vol(volume_previous, pressure, pressure_atm, dt, area):
    return volume_previous + area * exit_velocity(pressure, pressure_atm) * dt

def temp(temp_previous, pressure, pressure_atm, dt, area, c_v):
    return temp_previous - ((pressure * area * exit_velocity(pressure, pressure_atm) * dt) / c_v)

def thrust(pressure, pressure_atm, area):
    return area * 1000 * exit_velocity(pressure, pressure_atm)**2

def mass_func(mass_initial, area, pressure, pressure_atm):
    return (mass_initial - 0.5 * area * 1000 * exit_velocity(pressure, pressure_atm) * dt, mass_initial - area * 1000 * exit_velocity(pressure, pressure_atm) * dt)

def accel(mass, g, k, velocity, pressure, pressure_atm, area):
    return (thrust(pressure, pressure_atm, area) - mass * g - k * velocity**2) / mass

def speed(velocity_initial, accel, dt):
    return velocity_initial + accel * dt

def dis(height_initial, velocity, dt, accel):
    return height_initial + velocity * dt - 0.5 * accel * dt**2

pressure_initial = 250000
pressure_atm = 100000
temp_initial = 300
volume_final = 0.002
area = 0.000314
c_v = 700
mass_rocket = 1.4
g = 9.81
k = 0.004

dt = 0.0001

volume_initial = np.arange(0.3* volume_final, 0.9*volume_final, (0.01 * volume_final))

values_list = []

for v in volume_initial:
    time = 0
    volume = v
    pressure = pressure_initial
    temperature = temp_initial
    height = 0
    velocity = 0
    peak_accel = 0
    mass_initial = mass_rocket + 1000 * (volume_final - volume)
    mass = (mass_initial, mass_initial)

    while volume < volume_final:

        if volume == volume_final or pressure <= pressure_atm:
            break

        volume = vol(volume, pressure, pressure_atm, dt, area)
        temperature = temp(temperature, pressure, pressure_atm, dt, area, c_v)
        pressure = press(volume, temperature, pressure_initial, temp_initial, v)

        if pressure <= pressure_atm:
            print("Pressure dropped too low")
            break

        mass = mass_func(mass[1], area, pressure, pressure_atm)
        acceleration = accel(mass[0], g, k, velocity, pressure, pressure_atm, area)

        if acceleration > peak_accel:
            peak_accel = acceleration

        velocity = speed(velocity, acceleration, dt)
        height = dis(height, velocity, dt, acceleration)
        time += dt

    values_list.append((height, velocity, peak_accel / g))

velocity_list = []
height_list = []

for i in values_list:
    velocity_list.append(i[1])
    height_list.append(i[0])

comparator_list = []

for i in values_list:
    comparator_list.append(round(i[0] + ((i[1]**2) / 2 * g), 6))

print(volume_initial[comparator_list.index(max(comparator_list))], values_list[comparator_list.index(max(comparator_list))][0], values_list[comparator_list.index(max(comparator_list))][1])

water_volume = []

for i in volume_initial:
    water_volume.append(volume_final - i)

plt.figure(1)
plt.plot(volume_initial, velocity_list, label="Launch Velocity Max.")
plt.plot(volume_initial, height_list, label="Launch Altitude Max.")
plt.xlabel("Air Volume At Launch")
plt.ylim(0, 1.1 * values_list[comparator_list.index(max(comparator_list))][1])
plt.plot(volume_initial[comparator_list.index(max(comparator_list))],values_list[comparator_list.index(max(comparator_list))][1],'ro')
plt.text(0.98 * volume_initial[comparator_list.index(max(comparator_list))], values_list[comparator_list.index(max(comparator_list))][1], "Optimal Solution: {}".format(round(volume_initial[comparator_list.index(max(comparator_list))], 5)), horizontalalignment='right')
plt.legend()

plt.figure(2)
plt.plot(water_volume, velocity_list, label="Launch Velocity Max.")
plt.plot(water_volume, height_list, label="Launch Altitude Max.")
plt.xlabel("Water Volume At Launch")
plt.ylim(0, 1.1 * values_list[comparator_list.index(max(comparator_list))][1])
plt.plot(volume_final - volume_initial[comparator_list.index(max(comparator_list))],values_list[comparator_list.index(max(comparator_list))][1],'ro')
plt.text(1.03 * (volume_final - volume_initial[comparator_list.index(max(comparator_list))]), values_list[comparator_list.index(max(comparator_list))][1], "Optimal Solution: {}".format(round(volume_final - volume_initial[comparator_list.index(max(comparator_list))], 5)), horizontalalignment='left')
plt.legend()

plt.show()