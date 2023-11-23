import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import bisect
import sys
#Energy           s          py          pz          px         dxy         dyz         dz2         dxz         dx2       tot

# Read the data from the text file into a Pandas DataFrame
filename = 'TDOS_SOC.dat'  # Replace with the actual file name
data = pd.read_table(filename, delim_whitespace=True)
# Extract relevant columns
fermi=float(sys.argv[1])
energy = data['#Energy']-fermi+1
min_index = bisect.bisect_right(energy,-4.2)
max_index = bisect.bisect_right(energy,4.2)
dos = data['TDOS']# Extract numeric part after 'biaxial_'

x_values=energy

maxvalue=max(energy[min_index:max_index])

# BrSSbSe 
#
fig, ax = plt.subplots(figsize=(10, 6))

with open("POSCAR", 'r') as file:
    # Read all lines from the file
    lines = file.readlines()

    atoms=lines[5].split()

for atom in atoms:
    data=pd.read_table(f"PDOS_{atom}_SOC.dat",delim_whitespace=True)
    S=data['s']
    Px=data['px']
    Py=data['py']
    Pz=data['pz']
    #Bi_D=data['dxy']+data['dyz']+data['dz2']+data['dxz']+data['dx2']


    alpha_val=0.3
    ax.plot(x_values, Px, label=f"{atom}_px")
    ax.plot(x_values, Py, label=f"{atom}_py")
    ax.plot(x_values, Pz, label=f"{atom}_pz")
    ax.plot(x_values, S, label=f"{atom}_s")


#######


plt.axvline(x=0, color='black', linestyle='--')

# Set labels and title
ax.set_xlabel('Energy (eV)')
ax.set_ylabel('Arb. Unit')
ax.set_title('Density of State')


# Add legend
ax.legend()

ax.set_xlim([-4, 4])
ax.set_ylim([-0.2, maxvalue*0.6])
#grid
ax.grid(True)
# Show the plot
plt.savefig("pdos.png")
plt.show()
