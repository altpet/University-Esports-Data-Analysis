import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

##This generates the list of universities, if it doesn't already exist
if os.path.getsize("Universities.txt")==0:
    bashCommand = "sed 's/,,//g' \"Team Points Winter 2021.csv\" | sed '/\S/!d' | cut -d, -f2 | sort -f | uniq -i > Universities.txt" 
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
bins = []
for i in range(15):
    bins.append(range((10*i+1),(10*(i+1)+1)))
binnedData={}  



for uni in universities:
    #linux command to clean the data set and grab the points for a given uni
    bashCommand = "sed 's/,,//g' \"Team Points Winter 2021.csv\" | sed '/\S/!d' | sort -k3 -t ',' -n -r | grep -n -i \"," + uni + ",\" | cut -d, -f3 > temp.txt"
    os.system(bashCommand)
    f = open("temp.txt", "r")
    output = []
    binnedOutput = [0]*15
    total = 0
    temp=0
    array = []
    for x in f:
        array.append(int(x))

    for i in range(0,151,1):
        for j in array:
            if j<=i:
                for k,b in enumerate(bins):
                    if j in b:
                        
                        binnedOutput[k] = binnedOutput[k]+ j
                total +=j
                array.remove(j)
                
        output.append(total)
    f.close()
    data[uni]=output
    binnedData[uni] = binnedOutput
    #for internal plotting:
    #uniOutputPair = [uni,output]
    #uniOutputs.append(uniOutputPair)



#dataframe for external output
df = pd.DataFrame(data,columns=universities)
df.to_csv("Results.csv")

df = pd.DataFrame(binnedData,columns=universities)
df.to_csv("binnedResults.csv")

#internal plotting:
#axis = np.arange(0,151,1)

#for [name,output] in uniOutputs:
#    plt.plot(axis, output, label=name)

#plt.legend()
#plt.show()
#plt.show()
