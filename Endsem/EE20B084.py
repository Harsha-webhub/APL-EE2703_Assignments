# -*- coding: utf-8 -*-
"""EE20B084.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15uJXqnsgF5iXJJqv7YGpZ3dMaNaMI3bX
"""

#             Final Exam for EE2703  
#             Finding the Antenna currents in a half-wave dipole antenna
#             Name: Harshavardhan Mudadla
#             Roll No.: EE20B084


#Q1
from pylab import *
import numpy as np

N = 100 #Number of sections in each half section of the antenna
l = 0.5 #quarter wavelength
Im = 1.0 # current injected into the antenna
k = pi #wave number
dz = l/N #spacing of current samples
I = np.zeros(2*N+1) # current vector at points corresponding to vector z
z = linspace(-l,l,2*N+1) #points at which we compute the currents.
u = delete(z,[0,N,2*N]) #2N −2 locations of unknown currents
J = np.zeros(2*N-2) # current vector at points corresponding to vector u

print("z")
print((z).round(2))
print("u")
print((u).round(2))

#Q2
a = 0.01 #radius of wire
def compM(): # function to compute and return the matrix M.
  M = (np.identity(2*N-2))*(1/(2*pi*a))
  return M
#H_phi = M*J
M = compM()
print("M")
print(M)

#Q3
Z = meshgrid(z,z)
zi = Z[0]
zj = Z[1]
#Rz computes distances including distances to known current
Rz = sqrt((zi-zj)**2 + ones([2*N+1,2*N+1],dtype=complex)*(a**2))

U = meshgrid(u, u)
ui = U[0]
uj = U[1]
# Ru is a vector of distances to unknown currents.
Ru = sqrt((ui-uj)**2 + ones([2*N-2,2*N-2],dtype=complex)*(a**2))

#distances with respect to z = 0
RiN = delete(Rz[:][N],[0,N,2*N])
mu0 = 4e-7*pi #permeability of free space

# P is the contribution to the vector potential due to unknown currents
P = (mu0/(4*pi))*(cos(k*Ru)-(sin(k*Ru))*1j)*(dz/Ru)
#Pb is the contribution to the vector potential due to current IN
Pb = (mu0/(4*pi))*(cos(k*RiN)-(sin(k*RiN))*1j)*(dz/RiN)

print("Rz")
print((Rz).round(2))
print("Ru")
print((Ru).round(2))
print("RiN")
print((RiN).round(2))

print("P*1e8")
print((P*1e8).round(2))
print("Pb*1e8")
print((Pb*1e8).round(2))

#Q4
#matrix corresponding to unknown currents
Q = (a/mu0)*(P)*((1j)*(k/Ru)+(1/Ru**2))
#matrix corresponding to the boundary current
Qb = (a/mu0)*(Pb)*((1j)*(k/RiN)+(1/RiN**2))

print("Q")
print((Q).round(2))
print("Qb")
print((Qb).round(2))

#Q5
J = inv(M-Q)@Qb*Im
#calculated currents
Ical = concatenate(([0],J[:N-1],[Im],J[N-1:],[0]))
#assumed currents
Iasm = Im*sin(k*(l-abs(z)))

print("Icalculated")
print((abs(Ical)).round(2))
print("Iassumed")
print((Iasm).round(2))

figure()
plot(z,abs(Ical),label = "Calculated Current")
plot(z,Iasm,label = "Assumed Current")
xlabel(r"$z$")
ylabel(r"$I$")
legend(loc = 'upper right')
title("Antenna currents in a half-wave dipole antenna at N=100")
grid()
savefig('fig1.png')
show()