import os
import sys
import numpy as np

# Inputs to be given, 1. type of sim, File name

band_type=sys.argv[1] ## possible options - "vbm" "cbm"
file_input=sys.argv[2] ## any file with array type dataset, with first column with k path (angstrom inverse) and second column in energy (eV)
file_output="eff.dat"
if len(sys.argv)>3: file_output=sys.argv[3]

with open(file_input, 'r') as file:
    lines = file.readlines()

# Initialize lists to store the data
x_values = []
y_values = []
checker=[]
# Skip the first line starting with '#'
for line in lines[1:]:
    # Split the line by whitespace and convert the values to float
    values = line.split()
    if values==[]:break
    if values==checker:continue
    checker=values
    x_values.append(float(values[0]))
    y_values.append(float(values[1]))

## Check the simulation type
if band_type=="cbm":min_index = y_values.index(min(y_values))
elif band_type=="vbm":min_index = y_values.index(max(y_values))
else:
    print("ERROR : Wrong input")
    
def effective(index_1, index_2,direction):

    subset_x=x_values[index_1:index_2:direction]
    subset_y=y_values[index_1:index_2:direction]
  #  print(subset_y)
    #print(subset_y.sort())
    sorted_list=sorted(subset_y)
    reverse_sort=sorted_list[-1::-1]
 #   print(sorted_list)
#    print(reverse_sort)
    if subset_y!=sorted_list and subset_y!=reverse_sort:
        print("BAD DATA")
        return(0)
    symm_y=subset_y[:]+subset_y[-2::-1]
#    print("THIS IS Y --> ", symm_y)
    tmp2=[(2*subset_x[-1]-val) for val in subset_x]
    symm_x = subset_x+tmp2[-2::-1]
 #   print("THIS IS X --> ", symm_x)
    a,b,c = coefficients = np.polyfit(symm_x, symm_y, 2)
    diff=2*a  ## double derivative of Energy by k ## unit eV Angstrom
    hbar= 6.5821  # 6.5821 × 10-16 eV s ; note -32 has to be taken 
    mass= 0.510998950 #MeV/c2 - M = 10^6, 
    c = 2.99792458 #10^8 m/sec =  10^18 angstrom/sec

    #effective mass formuala -> mass^-1 * hbar^2 * diff^-1 * c^2
    ## exponential --> mass^-1 = -6, hbar^2 = -32, diff^-1 = 0, c^2 = 36
    ## Final exponential = -2
    return(hbar*hbar*c*c/mass/diff/100)


points=3  ## How many points used for interpolation



eff_mass_1=effective(min_index-points+1,min_index+1,1) ##
eff_mass_2=effective(min_index+points-1,min_index-1,-1)

if x_values[min_index]<x_values[min_index-1]:
    eff_mass_1,eff_mass_2=eff_mass_2,eff_mass_1

output_str=f"{min_index}\t{eff_mass_1}\t{eff_mass_2}" + "\n"

with open(file_output, "w") as file:
    file.write(output_str)
   
#print(output_str)
