import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import bisect
from tqdm import tqdm
#Energy           s          py          pz          px         dxy         dyz         dz2         dxz         dx2       tot


def band_num_reader(file_open):
# Open the file and iterate through lines
    with open(file_open, 'r') as file:
        for line in file:
            if line.startswith("# NKPTS & NBANDS:"):
                # Extract NKPTS and NBANDS values
               # print(line)
                val = line.split()
                
                nkpts = int(val[4])
                nbands = int(val[5])
                #print(nkpts,nbands)
                return(nkpts,nbands)  # Exit the loop after finding the relevant line

def single_band_reader(file_name,start_index,number_of_lines):
    column_names = ["K-Path", "Energy", "s", "py", "pz", "px", "dxy", "dyz", "dz2", "dxz", "x2-y2", "tot"]

# Read the data using read_csv with specific parameters
    #print("THIS MANY ROWS SKIPPED -->", start_index)
    df = pd.read_csv(file_name, skiprows=start_index, nrows=number_of_lines, delim_whitespace=True, names=column_names)

    return(df)


def full_file_plotter(file_name,name_of_band,orbital_list,number_of_kpoints,number_of_bands,rang,diameter):

    #orbital_list=("dxy", "dyz", "dz2", "dxz", "x2-y2")
    start=3
    for band_num in tqdm(range(48), desc=f"{name_of_band} system", unit="BANDS"):
        data_this_band=single_band_reader(file_name,start,number_of_kpoints)
        start=start+number_of_kpoints+2
        #print("THIS IS START INDEX --> ",start)
        orbital_sum=0
        for orbital in orbital_list:
            orbital_sum=orbital_sum+data_this_band[orbital]
        y_values_plot=data_this_band["Energy"]
        x_values_plot=data_this_band["K-Path"]
#        if max(y_values_plot)<-2+fermi-1:continue

        

        #print("THIS IS BAND_NUMBER", band_num)
        #print(x_values_plot,y_values_plot,orbital_sum)
        skip=1
        ax.scatter(
x_values_plot[::skip], 
y_values_plot[::skip]-fermi+1,
s=10,#orbital_sum[::skip]*1000,
color=rang,
marker="o",
alpha=orbital_sum[::skip], 
edgecolors='none')
    ax.plot([], [],color=rang,marker="o",label=name_of_band)
        #ax.scatter(x_values_plot, y_values_plot,s=orbital_sum,color=rang,marker="o")
    

##Energy        TDOS
fig, ax = plt.subplots(figsize=(10, 6))
# Extract relevant columns
fermi=-4.1720

nkpts = None
nbands = None
academic_colors = ['cyan', 'blue', 'purple', 'orange', 'green', 'red',  'brown', 'pink', 'gray', 'olive', 'teal', 'lightblue', 'darkgreen', 'salmon', 'indigo']


nkpts,nbands=band_num_reader("PBAND_Bi_SOC.dat")

class atom_orbital:
    def __init__(self, name, filename, orbitals,colour):
        self.name=name
        self.filename=filename
        self.orbitals=orbitals
        self.colour=colour



with open("POSCAR", 'r') as file:
    # Read all lines from the file
    lines = file.readlines()
    atoms= lines[5].split()


atom_orbital_list=[]
i=0
for atom in atoms:
    atom_orbital_list.append(atom_orbital(name=f"{atom}_p",colour=academic_colors[i],filename=f"PBAND_{atom}_SOC.dat",orbitals=("px", "py", "pz")))
    atom_orbital_list.append(atom_orbital(name=f"{atom}_d",colour=academic_colors[i+1],filename=f"PBAND_{atom}_SOC.dat",orbitals=("dxy", "dyz", "dz2", "dxz", "x2-y2")))
    atom_orbital_list.append(atom_orbital(name=f"{atom}_s",colour=academic_colors[i+2],filename=f"PBAND_{atom}_SOC.dat",orbitals=("s")))
    i+=3



dia=0
for single_atom_orbit in atom_orbital_list:
    dia+=1	
    full_file_plotter(single_atom_orbit.filename,single_atom_orbit.name,single_atom_orbit.orbitals,nkpts,nbands,single_atom_orbit.colour,dia)






#print(x_values)
#print(y_values)
# Plot each y-value separately


#plt.axvline(x=0, color='black', linestyle='--')

# Set labels and title
ax.set_xlabel('k path')
ax.set_ylabel('Energy(eV)')
ax.set_title('BAND_STRUCTURE')

important_points=[[0.0,"M"],[0.55921,"K"],[1.67782 ,"Γ"], [2.64608,"M"]]

values_list, names_list = zip(*important_points)
plt.xticks(values_list, names_list)
for x_val in values_list:
    plt.axvline(x=x_val,color="black")

plt.axhline(y=0,color="black")
# Add legend
ax.legend()
ax.set_ylim([-4, 6])
ax.set_xlim(values_list[0],values_list[-1])
#grid
#ax.grid(True)
# Show the plot
plt.savefig("band_plot5.png")
plt.show()
