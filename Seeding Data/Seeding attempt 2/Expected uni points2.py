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



seedings = pd.read_csv ('Winter 2021 Seeding with estimated points(with column labels).csv')
seedings.fillna("~",inplace = True)
for column in seedings:
        if column[0:4] != "Seed" and column[0:4] != "Unna":
            seedings[column] = seedings[column].str.lower()
print(seedings)
results = pd.read_csv ('2021 Winter Games Points(with column labels).csv',encoding= 'unicode_escape')
results.fillna("~",inplace = True)
for column in results:
        if column[-1] == "1" or column[-1] == "2":
            results[column] = results[column].str.lower()
print(results)




'''
##Generate a quick and dirty way of finding which team plays for which uni
teamsDict = {}
import csv
with open('2021 Winter BUEC points.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        for index,i in enumerate(row):
            if index!= len(row)-1:
                teamsDict[i.lower()]=row[index+1].lower()
'''






#initialise the output
output = {}
externalOutput = {}
deltaOutput={}
relativeDelta={}
expectedTeamPoints={"Team":[],"University":[],"Points":[]}
expectedTeamPoints = pd.DataFrame.from_dict(expectedTeamPoints)
for uni in universities:
    output[uni] = 0
    externalOutput[uni] = [0]
    deltaOutput[uni] = [0]
    relativeDelta[uni] = [0]


overrides = pd.read_csv('Manual Overrides.csv',encoding= 'unicode_escape',index_col=0)
print(overrides)

#raw deviation from seeding by uni
errorTeams = []
counter = 0
for index1,column in enumerate(seedings):
    if column[0:4] != "Seed" and column[0:4] != "Unna":
        myColumn = column
        if column == "League of Legends.1":
            myColumn = "League of Legends"
        if column == "Rocket league.1":
            myColumn = "Rocket league"
        for index2,team in enumerate(seedings[column]):
            points = seedings.iloc[index2]["Unnamed: " + str(index1+2)]
            if points =="~":
                points = 0
            if team != "~":
                try:
                    row = results.index[results[myColumn+".1"]==team]
                    university = results.iloc[row][myColumn+".2"].values[0].lower().strip()
                    output[university] +=  float(points)
                    externalOutput[university][0] +=  float(points)
                    expectedTeamPoints = expectedTeamPoints.append({"Team":team,"University":university,"Points":points},ignore_index=True)
                except:
                    case= False
                    for i in overrides["Team"]:
                        if column+team == i[2:-2]:
                            case = True
                            
                    if case:
                        row = overrides.index[overrides["Team"]=="[\'"+column+team+"\']"]
                        try:
                            
                            row = overrides.index[overrides["Team"]=="[\'"+column+team+"\']"]
                            university = overrides.iloc[row]["University"].values[0].strip().lower()
                            university = university[2:-2]
                            output[university] +=  float(points)
                            externalOutput[university][0] +=  float(points)
                            expectedTeamPoints = expectedTeamPoints.append({"Team":team,"University":university,"Points":points},ignore_index=True)
                        except:
                            errorTeams.append(team.lower())
                    else:
                        print("Column: " + column)
                        print("Team: " + team)
                        print(points)
                        university = input("Please manually enter the university this team belongs to: ")
                        overrides = overrides.append({"Team":[column+team], "University":[university]}, ignore_index=True)
                        overrides.to_csv("Manual Overrides.csv")
                        

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
        if university.lower().strip() in universities:
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
#plt.show()

overrides.to_csv("Manual Overrides.csv")


#dataframe for external output
#df = pd.DataFrame(output,columns=["university","score"])
df = pd.DataFrame.from_dict(externalOutput)
print(df)
df.to_csv("Results.csv")

df = pd.DataFrame.from_dict(deltaOutput)
df.to_csv("deltaResults.csv")

df = pd.DataFrame.from_dict(relativeDelta)
df.to_csv("relativeDelta.csv")

expectedTeamPoints.to_csv("expectedTeamPoints.csv")

#internal plotting:
#axis = np.arange(0,151,1)

#for [name,output] in uniOutputs:
#    plt.plot(axis, output, label=name)

#plt.legend()
#plt.show()
#plt.show()

