from math import sqrt
import sys

if len(sys.argv) < 4 :
	print( " ERROR!! : Require 3 arguments: E, v, rho, respectively")
	sys.exit()

E = (float)(sys.argv[1])
v = (float)(sys.argv[2])
rho = (float)(sys.argv[3])

print( "E   = " + str(E) +   " Pa    ")
print( "v   = " + str(v) +   "       ")
print( "rho = " + str(rho) + " kg/m^3")

G = E / 2. / (1 + v )
print( "G   = " + str(G)  +  " Pa    ")

Vs = sqrt(G / rho )
print( "Vs  = " + str(Vs) +  " m/s   ")

M = E * ( 1 - v ) / (1 + v ) / ( 1 - 2 * v )
print( "M   = " + str(M)  +  " Pa    ")
Vp = sqrt( M  / rho )
print( "Vp  = " + str(Vp) +  " m/s   ")






