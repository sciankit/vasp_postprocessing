import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the data from the text file into a Pandas DataFrame
filename = 'STATS.out'  # Replace with the actual file name
data = pd.read_table(filename, delim_whitespace=True)
#print(data)
# Extract relevant columns
conf = data['System']
#System	Alpha1	Alpha2	delE1	delE2

Alpha1 = data['Alpha1'].astype(float)
Alpha2 = data['Alpha2'].astype(float)
delE1 = data['delE1'].astype(float)
delE2 = data['delE2'].astype(float)


strain_values = data['System'].str.replace('BiSF-T-biaxial_', '').str.replace(',','.').astype(float)     -1 # Extract numeric part after 'biaxial_'



atom_energy={
"F":-1.77796913,
"Cl":-1.789586605,
"Br":-1.53516465,
"I":-1.484483065,
"Bi":-3.88517589666667,
"Se":-3.71267639666667,
"Te":-3.50929706,
"S":-4.13779644875,
"As":-4.90480287833333,
"Sb":-4.45893412,
}


#print(y_values)
#  Energy(eV)      ElapsedTime(sec)        DOSElapsedTime(sec)    
# Volume(Ang^3)   Pressure(kBar) 
# fermi-level(eV) 
#Charge@A        Charge@B        Charge@C     
#   VBM(eV) CBM(eV)
# a_Unit(Å)       b_unit(Å)       c_Unit(Å)     
#   AATOM  BATOM   CATOM   ANumber BNumber CNumber
# VaccLevel(eV)  

# Create a plot
fig, ax = plt.subplots(figsize=(10, 6))

colo=['blue','orange','green']
markers = ['o', 's', '^']
charge_Label=['Charge@S','Charge@F']
charge_amount=[6,7]


charge_Label2=['Charge@Bi']
charge_amount2=[14]
#print(y_values)
#print(data["ANumber"]*2)

x_values=strain_values
y_values=Alpha1
y_values2=abs(Alpha2)


# Plot each y-value separately
ax.plot(x_values, y_values, label=f"Alpha $eV.\AA [K ⟶ \Gamma$]", marker=markers[0],color=colo[0])
ax.plot(x_values,y_values2, label=f"Alpha $eV.\AA [\Gamma ⟶ M$]", marker=markers[1],color=colo[1])

#ax.plot(x_values, y_values2,  marker=markers[1],color=colo[1])
#plt.bar(x_values, -(max(y_values2)-y_values2+0.5), label="cbm", color=colo[1],bottom=max(y_values2)+0.5, alpha=0.7, align='center', width=0.005)
#plt.bar(x_values, -((min(y_values)-0.5)-y_values), label="vbm", color=colo[0],bottom=min(y_values)-0.5, alpha=0.7, align='center', width=0.005)
########VBM 

start=2
end=-1
#x_subset=x_values.iloc[5:-5]
x_subset=x_values.iloc[start:end]
#y_subset=y_values.iloc[5:-5]
y_subset=y_values.iloc[start:end]
 
    # Perform linear regression to get the fit line
fit_line = np.polyfit(x_subset, y_subset, 1)
fit_line_fn = np.poly1d(fit_line)
a, b= fit_line
equation_str = f"{a:.3f}$x$ + {b:.3f}"


# Calculate R-squared
y_mean = y_subset.mean()
total_sum_squares = ((y_subset - y_mean)**2).sum()
residual_sum_squares = ((y_subset - fit_line_fn(x_subset))**2).sum()
r_squared = 1 - (residual_sum_squares / total_sum_squares)

    # Plot the fit line in a transparent color
#ax.plot(x_subset, fit_line_fn(x_subset), label=f'Fit Line equation: {equation_str}|  $R^2$ {r_squared:.3f}' , color=colo[0], alpha=0.5)


###########CBM
#x_subset=x_values.iloc[5:-5]
x_subset=x_values.iloc[start:end]
#y_subset=y_values.iloc[5:-5]
y_subset=y_values2.iloc[start:end]
 
    # Perform linear regression to get the fit line
fit_line = np.polyfit(x_subset, y_subset, 1)
fit_line_fn = np.poly1d(fit_line)
a, b= fit_line
equation_str = f"{a:.3f}$x$ + {b:.3f}"


# Calculate R-squared
y_mean = y_subset.mean()
total_sum_squares = ((y_subset - y_mean)**2).sum()
residual_sum_squares = ((y_subset - fit_line_fn(x_subset))**2).sum()
r_squared = 1 - (residual_sum_squares / total_sum_squares)

    #Plot the fit line in a transparent color
#ax.plot(x_subset, fit_line_fn(x_subset), label=f'Fit Line equation: {equation_str}|  $R^2$ {r_squared:.3f}' , color=colo[1], alpha=0.5)

#####################CBM END


#plt.axhline(y=0, color='black', linestyle='--')

# Set labels and title
ax.set_xlabel('Strain $\epsilon$')
ax.set_ylabel(f'Alpha (eV.$\AA$)')
ax.set_title(f'Rashba Coeff (eV.$\AA$) v/s Strain')

#plt.text(-0.1, 0.1, f"$Vacuum Level$", bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))
# Add legend
ax.legend()
plt.xticks(x_values[::2])
#grid
ax.grid(True)
# Show the plot
plt.savefig("plots/alpha.png")
plt.show()
