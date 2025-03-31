#packages
import pandas as pd
import os
from itertools import combinations

# set working directory and load data
os.chdir("C:/Users/32493/Google Drive/ku leuven/data analysis/data visualization")
pigs = pd.read_csv("Exp1 - Feeding data.csv")

# load pig registration data
id_pigs = pd.read_csv("Exp1 - Pig registration all info combined.csv")
id = id_pigs["pig"]

# filter on pigs ID 
pigs_filtered = pigs[pigs['pig'].isin(id)]
pigs_filtered.reset_index(drop = True, inplace = True)

#steps to get excel file with count of interaction between pigs
# Step 1: Sort by Start_Time
pigs_sorted = pigs_filtered.sort_values(by=['station','start'])

# Step 2: Create a new column with the previous pig
pigs_sorted['prev_pig'] = pigs_sorted.groupby('station')['pig'].shift(1)

# Step 3: Drop the first row 
pigs_sorted = pigs_sorted.dropna()

# Step 4: Create pairs and count occurrences
pigs_sorted['Pig_Pair'] = pigs_sorted.apply(lambda row: tuple(sorted((int(row['pig']), int(row['prev_pig'])))), axis=1)

# Step 5: Count occurrences of each pair
Occurences = pigs_sorted.groupby(['station','Pig_Pair']).size().reset_index(name = 'Count')

# Step 6: Split tuple into two columns for clarity
Occurences[['Pig_1', 'Pig_2']] = pd.DataFrame(Occurences['Pig_Pair'].tolist(), index=Occurences.index)

# Step 7: Drop the original tuple column
Occurences = Occurences.drop(columns=['Pig_Pair'])

print(Occurences)

# option: filter on count >25
Occurences = Occurences[Occurences['Count'] > 25]

#export to excel
Occurences.to_excel('Occurences.xlsx', index=False)