import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


##This generates the list of universities, if it doesn't already exist ( we are using the generated list from the team points program)
if os.path.getsize("Universities.txt")==0:
    bashCommand = "sed 's/,,//g' \"Team Points Winter 2021.csv\" | sed '/\S/!d' | cut -d, -f2 | sort -f | uniq -i > Universities.txt" 
    os.system(bashCommand)
universities = []
u = open("Universities.txt", "r")
for i in u:
    universities.append(str(i).strip().lower())
u.close()
##


##Generate a list of all the teams involved
teams = []
bashCommand = "cut -d, -f1 \"teams with seeds and points.csv\" > teams.txt"
os.system(bashCommand)
t = open("teams.txt", "r")
for i in t:
    teams.append(str(i).strip().lower())
t.close()





##Generate a quick and dirty way of finding which team plays for which uni
teamsDict = {}
import csv
with open('2021 Winter BUEC points.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        for index,i in enumerate(row):
            if index!= len(row)-1:
                teamsDict[i.lower()]=row[index+1].lower()



#initialise the output
output = {}
externalOutput = {}
deltaOutput={}
relativeDelta={}
for uni in universities:
    output[uni] = 0
    externalOutput[uni] = [0]
    deltaOutput[uni] = [0]
    relativeDelta[uni] = [0]


#raw deviation from seeding by uni
errorTeams = []
import csv
with open('teams with seeds and points.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for [team,seed,points] in reader:
        try:
            
            university = teamsDict[team.lower()]
        
            output[university] +=  float(points)
            externalOutput[university][0] +=  float(points)
        except:
            #print(team.lower())
            errorTeams.append(team.lower())
            
print("Teams whose university/points could not be found:")
print("")
print(str(len(errorTeams)) + " teams")
for t in errorTeams:
    print(t)

print("")


print("Uni with no points given n/a to avoid dividing by zero error:")
print("")
#deviation from seeding adjusted for total points
import csv
with open('Actual Results.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for [university,points] in reader:
        if university.lower() in universities:
            deltaOutput[university.lower()][0] = int(points) - externalOutput[university.lower()][0]
            if int(points) == 0:
                relativeDelta[university.lower()][0] = "n/a"
                print(university.lower())
            else:
                relativeDelta[university.lower()][0] = deltaOutput[university.lower()][0]/int(points)
        


            
#print(output)
arrayOutput = list(output.items())
arrayOutput.sort(key=lambda x: x[1])
universities = list(zip(*arrayOutput))[0]
points = list(zip(*arrayOutput))[1]
x_pos = np.arange(len(universities))

plt.bar(x_pos, points,align='center')
plt.xticks(x_pos, universities) 
plt.show()




#dataframe for external output
#df = pd.DataFrame(output,columns=["university","score"])
df = pd.DataFrame.from_dict(externalOutput)
df.to_csv("Results.csv")

df = pd.DataFrame.from_dict(deltaOutput)
df.to_csv("deltaResults.csv")

df = pd.DataFrame.from_dict(relativeDelta)
df.to_csv("relativeDelta.csv")



#internal plotting:
#axis = np.arange(0,151,1)

#for [name,output] in uniOutputs:
#    plt.plot(axis, output, label=name)

#plt.legend()
#plt.show()
#plt.show()
