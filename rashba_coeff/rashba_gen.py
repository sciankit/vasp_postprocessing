import os
import sys
# Open the file
with open('rashba_band.dat', 'r') as file:
    lines = file.readlines()


# Initialize lists to store the data
x_values = []
y_values = []
sys_name=sys.argv[4]
NKPTS= float(sys.argv[3])



current_file= sys.argv[1]
with open(current_file, "w") as file:
    file.write(f"{sys_name}\t0\t0\t0\t0" + "\n")



# Skip the first line starting with '#'
for line in lines[1:]:
    # Split the line by whitespace and convert the values to float
    values = line.split()
    x_values.append(float(values[0]))
    y_values.append(float(values[1]))
    

# Display or use the extracted data
#print("X values:", x_values)
#print("Y values:", y_values)
#print(y_values.index(min(y_values)))
min_index = y_values.index(min(y_values))

#print("Index of the minimum value:", min_index)
#print("Minimum value without VASPKIT -1 :", y_values[min_index]-1)


def finder(index):
    zero_count=0
    i=0
    output=[index]
    CenterValue=y_values[index]
    slope_pos=[]
    slope_neg=[]
    posList=[]
    negList=[]

    #slope change finder
    while True:
        i+=1
        if (index+i+1)>NKPTS or (index-i<0):
            
            break

        if i>NKPTS:break
        #positive branch
        #print(len(y_values))
        #print(index+i)
        pos=y_values[index+i]>y_values[index+i-1]
        if slope_pos==[]: slope_pos=pos
        if slope_pos!=pos:
            if x_values[index+i]==x_values[index+i+1]:pass
            else:posList.append(index+i-1);slope_pos=pos
        if len(posList)>1:break

        pos=y_values[index-i]>y_values[index-i+1]
        #print("pos -->",pos)
        if slope_neg==[]: slope_neg=pos
        #print("slope -->", slope_neg)
        if slope_neg!=pos:
            if x_values[index-i]==x_values[index-i-1]:pass
            else:negList.append(index-i+1); slope_neg=pos
        if len(negList)>1:break
    
    #print("This is posList -->", posList)
    #print("This is Negative List -->", negList)


    mainList=negList
    if len(posList)>len(negList):mainList=posList
    output.extend(mainList)
    output.sort()
    if x_values[index]<x_values[index-1]:
        output[0],output[2]=output[2],output[0]
    #print(f"THIS IS OUTPU {output}")
    return(output)


        

indices=finder(min_index)
#print("These are indices", indices)
# print(f"""1 --> {x_values[indices[0]]}, {y_values[indices[0]]}
#       2 --> {x_values[indices[1]]}, {y_values[indices[1]]}
#       3 --> {x_values[indices[2]]}, {y_values[indices[2]]}
      
#       """)

alpha=[0,0]
delE1=0
delE2=0
if len(indices)>1:
    alpha[0]=2*(y_values[indices[1]]-y_values[indices[0]])/(x_values[indices[1]]-x_values[indices[0]])
    alpha[1]=2*(y_values[indices[2]]-y_values[indices[1]])/(x_values[indices[2]]-x_values[indices[1]])
    delE1=(y_values[indices[1]]-y_values[indices[0]])
    delE2=(y_values[indices[2]]-y_values[indices[1]])


with open(current_file, "w") as file:
    file.write(f"{sys_name}\t{alpha[0]}\t{alpha[1]}\t{delE1}\t{delE2}" + "\n")

current_file= sys.argv[2]
with open(current_file, "w") as file:
    out=max(abs(delE1), abs(delE2))
    file.write(f" {out}   " + "\n")


