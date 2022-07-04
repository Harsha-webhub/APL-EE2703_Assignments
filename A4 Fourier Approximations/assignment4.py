# -*- coding: utf-8 -*-
"""Assignment4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kDlUWjtcjdhlSlsAUiZSIwhTXbhCvBfK
"""

import pylab as py
import numpy as np
import scipy.integrate
from scipy.linalg import lstsq

#Q1
def exponential(x):
  return py.exp(x)

def cos_cos(x):
  return py.cos(py.cos(x))

x = np.linspace(-2*py.pi,4*py.pi,100,endpoint = False)
y1 = exponential(x)
y2 = cos_cos(x)

py.figure()
Figure1 = py.plot(x,py.log10(y1))
py.xlabel('$x$')
py.ylabel('$\exp(x)$')
py.title('Figure 1')
py.grid(True)
py.savefig('exponential_x.png')

py.figure()
Figure2 = py.plot(x,y2)
py.xlabel('$x$')
py.ylabel('$cos(cos(x))$')
py.title('Figure 2')
py.grid(True)
py.savefig('cos_cos_x.png')

py.show()

#Q2
def u(x,k,f):
  return f(x)*py.cos(k*x)/(py.pi)

def v(x,k,f):
  return f(x)*py.sin(k*x)/(py.pi)

exp_ab = np.zeros(51)
cos_cos_ab = np.zeros(51)

f1 = exponential 
exp_ab[0] = scipy.integrate.quad(u,0,2*py.pi,args=(0,f1))[0]/2
for n in range(1,26):
  exp_ab[2*n-1] = scipy.integrate.quad(u,0,2*py.pi,args=(n,f1))[0]
  exp_ab[2*n] = scipy.integrate.quad(v,0,2*py.pi,args=(n,f1))[0]

f2 = cos_cos
cos_cos_ab[0] = scipy.integrate.quad(u,0,2*py.pi,args=(0,f2))[0]/2
for n in range(1,26):
  cos_cos_ab[2*n-1] = scipy.integrate.quad(u,0,2*py.pi,args=(n,f2))[0]
  cos_cos_ab[2*n] = scipy.integrate.quad(v,0,2*py.pi,args=(n,f2))[0]

#Q3
n = np.linspace(0,50,51)

py.figure()
py.plot(n,py.log10(abs(exp_ab)),"ro")
py.xlabel('$n$')
py.ylabel('coefficients of exp(x)')
py.title('semilog plot, Figure 3')
py.grid(True)
py.savefig('semilog_exp_ab_n.png')

py.figure()
py.plot(py.log10(n[1:]),py.log10(abs(exp_ab[1:])),"ro")
py.xlabel('$n$')
py.ylabel('coefficients of exp()')
py.title('loglog plot, Figure 4')
py.grid(True)
py.savefig('loglog_exp_ab_n.png')

py.figure()
py.plot(n,py.log10(abs(cos_cos_ab)),"ro")
py.xlabel('$n$')
py.ylabel('coefficients of cos(cos(x))')
py.title('semilog plot, Figure 5')
py.grid(True)
py.savefig('semilog_cos_cos_ab_n.png')

py.figure()
py.plot(py.log10(n[1:]),py.log10(abs(cos_cos_ab[1:])),"ro")
py.xlabel('$n$')
py.ylabel('coefficients of cos(cos(x))')
py.title('loglog plot, Figure 6')
py.grid(True)
py.savefig('loglog_cos_cos_ab_n.png')

py.show()

#Q4
A = np.ones((400,51))
x0 = np.linspace(0,2*py.pi,401)
x0=x0[:-1]

for i in range(1,26):
  A[:,2*i-1] = np.cos(i*x0)
  A[:,2*i] = np.sin(i*x0)

B1 = f1(x0)
B2 = f2(x0)

C1 = lstsq(A,B1)[0]
C2 = lstsq(A,B2)[0]

#Q5
py.figure()
py.plot(n,py.log10(abs(C1)),'go',label = "Least Squares")
py.plot(n,py.log10(abs(exp_ab)),"ro", label = "Direct Integration")
py.xlabel('$n$')
py.ylabel('coefficients of $\exp(x)$')
py.title('Semilogy plot ofLeast Squares method and Integration method')
py.grid(True)
py.legend()
py.savefig('Best_fit_exp_ab_n.png')

py.figure()
py.plot(n,py.log10(abs(C2)),'go',label = "Least Squares")
py.plot(n,py.log10(abs(cos_cos_ab)),"ro", label = "Direct Integration")
py.xlabel('$n$')
py.ylabel('coefficients of cos(cos(x))')
py.title('Semilogy plot of Least Squares method and Integration method')
py.grid(True)
py.legend()
py.savefig('Best_fit_cos_cos_ab_n.png')

py.show()

#Q6
D1 = abs(C1-exp_ab)
D2 = abs(C2-cos_cos_ab)
Large_D1 = max(D1)
Large_D2 = max(D2)
print("Largest Deviation for exp(x) is ", Large_D1)
print("Largest Deviation for cos(cos(x)) is ", Large_D2)

#Q7
AC1 = py.dot(A,C1)
AC2 = py.dot(A,C2)

py.figure()
py.plot(x,py.log10(y1),label = "True Function")
py.plot(x0,py.log10(abs(AC1)),"go",label = "Estimated Function",markersize = 2)
py.xlabel('$x$')
py.ylabel('$\exp(x)$')
py.title('plot of exp(x) from Estimated values C1 and True function')
py.grid(True)
py.savefig('Deviation_estimated_true_exp_x.png')

py.figure()
py.plot(x,y2,label = "True Function")
py.plot(x0,AC2,"go",label = "Estimated Function",markersize = 2)
py.xlabel('$x$')
py.ylabel('$cos(cos(x))$')
py.title('plot of cos(cos(x)) from Estimated values C2 and True function')
py.grid(True)
py.savefig('Deviation_estimated_true_cos_cos_x.png')

py.show()