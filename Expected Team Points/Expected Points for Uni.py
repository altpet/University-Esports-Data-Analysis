import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

##This generates the list of universities, if it doesn't already exist
if os.path.getsize("Universities.txt")==0:
    bashCommand = "sed 's/,,//g' \"expectedTeamPoints.csv\" | sed '/\S/!d' | cut -d, -f2 | sort -f | uniq -i > Universities.txt" 
    os.system(bashCommand1)
universities = []
u = open("Universities.txt", "r")
for i in u:
    universities.append(str(i).strip())
u.close()
##

#output for external plotting
data = {}
#outputs for internal plotting
uniOutputs=[]


for uni in universities:
    #linux command to clean the data set and grab the points for a given uni
    bashCommand = "sed 's/,,//g' \"expectedTeamPoints.csv\" | sed '/\S/!d' | sort -k3 -t ',' -n -r | grep -n -i \"," + uni + ",\" | cut -d, -f3 > temp.txt"
    os.system(bashCommand)
    f = open("temp.txt", "r")
    output = []
    total = 0
    array = []
    for x in f:
        array.append(float(x))

    for i in range(0,151,1):
        for j in array:
            if j<=i:
                total +=j
                array.remove(j)
                
        output.append(total)
    f.close()
    data[uni]=output
    #for internal plotting:
    #uniOutputPair = [uni,output]
    #uniOutputs.append(uniOutputPair)



#dataframe for external output
df = pd.DataFrame(data,columns=universities)
df.to_csv("Results.csv")




#internal plotting:
#axis = np.arange(0,151,1)

#for [name,output] in uniOutputs:
#    plt.plot(axis, output, label=name)

#plt.legend()
#plt.show()
#plt.show()
