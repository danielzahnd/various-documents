#Import packages
import math as m
import numpy as np 

def monteCarloInt(a_0, b_0, a_1, b_1, a_2, b_2, a_3, b_3, n, dim):
	'''
	Parameters
	----------
	a_0 : TYPE: Floating point number.
		DESCRIPTION: Lower boundary of integration in zeroth component.
	b_0 : TYPE: Floating point number.
		DESCRIPTION: Upper boundary of integration in zeroth component.
	a_1 : TYPE: Floating point number.
		DESCRIPTION: Lower boundary of integration in first component.
	b_1 : TYPE: Floating point number.
		DESCRIPTION: Upper boundary of integration in first component.
	a_2 : TYPE: Floating point number.
		DESCRIPTION: Lower boundary of integration in second component.
	b_2 : TYPE: Floating point number.
		DESCRIPTION: Upper boundary of integration in second component.
	a_3 : TYPE: Floating point number.
		DESCRIPTION: Lower boundary of integration in third component.
	b_3 : TYPE: Floating point number.
		DESCRIPTION: Upper boundary of integration in third component.
	n : TYPE: Integer, natural number.
		DESCRIPTION: Number of random vectors to be generated for sampling the
		function.
	dim : TYPE: Integer, natural number.
		DESCRIPTION: Number of dimensions of implemented function.

		
	Important
	---------
	The function to be integrated using this Monte-Carlo integration method
	needs to be implemented directly in the code. That means, it must be hard
	coded in line xxx.\n\n
	If there is not a 4-dimensional integration to be carried out, it shall be
	begun with a_0, b_0 and so on to fill moneCarloInt(). The corresponding
	number of dimensions for the integration is to be assigned to dim.

	Returns
	-------
	Value of the desired integral.

	'''
	if (dim == 1):
		# print('1-dimensional integration chosen.') 
		# Generate n random vectors of dimension 1
		x = np.random.rand(1, n)
		x[0][:] = x[0][:]*abs(b_0-a_0)-(0-a_0)
		
		# Define integral value
		I = float(0)
		
		# Calculate integral
		for i in range(len(x[0])):
			I = I + m.exp(-2*(x[0][i]**2)) # Function implementation
		I = I*abs(b_0-a_0)*n**(-1)
		
		# Return integral value
		return I
	
	if (dim == 2):
		# print('2-dimensional integration chosen.')
		# Generate n random vectors of dimension 2
		x = np.random.rand(2, n)
		x[0][:] = x[0][:]*abs(b_0-a_0)-(0-a_0)
		x[1][:] = x[1][:]*abs(b_1-a_1)-(0-a_1)
		
		# Define integral value
		I = float(0)
		
		# Calculate integral
		for i in range(len(x[0])):
			I = I + m.exp(-2*(x[0][i]**2+x[1][i]**2)) # Function implementation
		I = I*abs(b_0-a_0)*abs(b_1-a_1)*n**(-1)
		
		# Return integral value
		return I
	
	if (dim == 3):
		# print('3-dimensional integration chosen.')
		# Generate n random vectors of dimension 3
		x = np.random.rand(3, n)
		x[0][:] = x[0][:]*abs(b_0-a_0)-(0-a_0)
		x[1][:] = x[1][:]*abs(b_1-a_1)-(0-a_1)
		x[2][:] = x[2][:]*abs(b_2-a_2)-(0-a_2)

		# Define integral value
		I = float(0)
		
		# Calculate integral
		for i in range(len(x[0])):
			I = I + m.exp(-2*(x[0][i]**2+x[1][i]**2+x[2][i]**2)) # Function implementation
		I = I*abs(b_0-a_0)*abs(b_1-a_1)*abs(b_2-a_2)*n**(-1)
		
		# Return integral value
		return I
	
	if (dim == 4):
		# print('4-dimensional integration chosen.')
		# Generate n random vectors of dimension 3
		x = np.random.rand(4, n)
		x[0][:] = x[0][:]*abs(b_0-a_0)-(0-a_0)
		x[1][:] = x[1][:]*abs(b_1-a_1)-(0-a_1)
		x[2][:] = x[2][:]*abs(b_2-a_2)-(0-a_2)
		x[3][:] = x[3][:]*abs(b_3-a_3)-(0-a_3)

		# Define integral value
		I = float(0)
		
		# Calculate integral
		for i in range(len(x[0])):
			I = I + m.exp(-2*(x[0][i]**2+x[1][i]**2+x[2][i]**2+x[3][i]**2)) # Function implementation
		I = I*abs(b_0-a_0)*abs(b_1-a_1)*abs(b_2-a_2)*abs(b_3-a_3)*n**(-1)
		
		# Return integral value
		return I
	
	else:
		I = 0
		print('Something with the input was wrong, please check input and compare with function description of monteCarloInt!')
		return I

# Execute program
Integral_1 = monteCarloInt(-1, 3, 0, 0, 0, 0, 0, 0, 1000000, 1)
Integral_2 = monteCarloInt(-1, 3, 1, 5, 0, 0, 0, 0, 1000000, 2)
Integral_3 = monteCarloInt(-1, 3, 1, 5, -1, 1, 0, 0, 1000000, 3)
Integral_4 = monteCarloInt(-1, 3, 1, 5, -1, 1, -18, 7, 1000000, 4)

# Print results
print('Integral_1 is I = ',Integral_1)
print('Integral_2 is I = ',Integral_2)
print('Integral_3 is I = ',Integral_3)
print('Integral_4 is I = ',Integral_4)