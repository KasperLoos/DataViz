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
Occurences.nunique()

# Create a dictionary with the specific renaming mappings
rename_dict = {
    #Pen 1
    222000938070: 'Miss Piggy',
    222000938175: 'Babe',
    222000938181: 'Porky',
    222000938196: 'Piglet',
    222000938228: 'Hamm',
    222000938229: 'Peppa',
    222000938265: 'Pumbaa',
    222000938282: 'Napoleon',
    222000938286: 'Snowball',
    222000938299: 'Wilbur',
    222000938311: 'Plopper',
    #Pen 2
    222000937880: 'Okkoto',
    222000937882: 'Hen Wen',
    222000937891: 'Maxwell',
    222000937905: 'Gordy',
    222000937908: 'Chris P. Bacon',
    222000938188: 'Kevin Bacon',
    222000938238: 'Ham Solo',
    222000938255: 'Hamtaro',
    222000938256: 'Piggy Smalls',
    222000938262: 'Notorious P.I.G.',
    222000938263: 'Sir Oinks-a-Lot',
    #Pen 3
    222000938014: 'Elvis Pigsley',
    222000938133: 'Piginator',
    222000938154: 'Harry Porker',
    222000938184: 'Hamlet',
    222000938189: 'Boarimir',
    222000938219: 'Hufflepork',
    222000938259: 'Frankenswine',
    222000938276: 'Pigachu',
    222000938278: 'Swinefeld',
    222000938292: 'Obi-Wan Pig-nobi',
    222000938317: 'Hammy Potter',
    #Pen 4
    222000937869: 'Oink Floyd',
    222000937870: 'Piggy Stardust',
    222000937874: 'Pigasso',
    222000937903: 'Vincent van Hog',
    222000937976: 'Swinestein',
    222000938095: 'Hamalot',
    222000938102: 'Napoleon Boarnaparte',
    222000938194: 'Pig Jagger',
    222000938266: 'Britney Squeals',
    222000938281: 'Piggy Minaj',
    222000938324: 'Arnold Schwarzenhogger',
    #Pen 5
    222000937877: 'Snoop Hoggy Hog',
    222000937926: 'Oinkerbell',
    222000937928: 'Piggy Azalea',
    222000937967: 'Brad Pig',
    222000937971: 'The Boar Identity',
    222000937974: 'Swinehouse',
    222000937986: 'Maple Bacon',
    222000938001: 'Hambert',
    222000938062: 'Prosciutto',
    222000938087: 'Sausage Roll',
    222000938247: 'Pork Chop',
    #Pen 6
    222000937980: 'Hambone',
    222000938010: 'Sir Loin',
    222000938086: 'BBQ',
    222000938190: 'Chorizo',
    222000938209: 'Pigador Dali',
    222000938226: 'Oinklet',
    222000938249: 'Baconator',
    222000938269: 'Ribs McGee',
    222000938284: 'Lard Vader',
    222000938320: 'Hamwise Gamgee',
    222000938322: 'Makin’ Bacon',
    #Pen 7
    222000937886: 'Peppa-roni',
    222000937915: 'Truffle Snout',
    222000937963: 'Hamthony Hopkins',
    222000938094: 'Pig Mac',
    222000938122: 'Oinkers',
    222000938191: 'Swinerton',
    222000938251: 'Boar-gart',
    222000938283: 'Sir Hamsalot',
    222000938302: 'The Great Hambino',
    222000938314: 'Piggly Wiggly',
    222000938325: 'Hamlet the Piglet',
    #Pen 8
    222000937876: 'Boaris Johnson',
    222000937883: 'Oinkie Minaj',
    222000937890: 'Hogzilla',
    222000937906: 'Hamlet Oinksworth',
    222000937932: 'Hamphrey',
    222000937968: 'Hogsmeade',
    222000938003: 'Pig Newton',
    222000938115: 'Babe Ruth',
    222000938183: 'Snoutorious B.I.G.',
    222000938274: 'Swine Fluencer',
    222000938293: 'Professor Pigsworth',
    #Pen 9
    222000937872: 'Lord Oinkington',
    222000937912: 'Piggle Wiggle',
    222000937934: 'Curly Trotter',
    222000937946: 'Hameo',
    222000937965: 'Oinkie Pie',
    222000938160: 'Boar-derline Genius',
    222000938163: 'Hamtastic',
    222000938240: 'Captain Pork Sparrow',
    222000938267: 'The Pork Knight Rises',
    222000938270: 'Trotsky',
    222000938297: 'Napoleon Swineaparte',
    #Pen 10
    222000937865: 'Hoggle',
    222000937972: 'Hamothy Chalamet',
    222000938000: 'Boar-inson Wells',
    222000938031: 'Piggory Dock',
    222000938090: 'Swinona Ryder',
    222000938147: 'Peppa the Hut',
    222000938152: 'The Three Little Pigsley',
    222000938171: 'Hambo',
    222000938216: 'Snorty McSnortface',
    222000938217: 'Pigtoria Beckham',
    222000938264: 'Hamberlain'
}

# Rename the 'pig' column based on the mapping
Occurences['Pig_1'] = Occurences['Pig_1'].replace(rename_dict)
Occurences['Pig_2'] = Occurences['Pig_2'].replace(rename_dict)

# option: filter on count >25
Occurences = Occurences[Occurences['Count'] > 25]

#export to excel
Occurences.to_excel('Occurences1.xlsx', index=False)

#export weights of pigs to excel file
weight = pd.read_csv("Exp1 - Pig registration all info combined.csv")
weight.head()
weight = weight[['pig', 'bodyw_end']]
weight['pig'] = weight['pig'].replace(rename_dict)
weight.to_excel('weights.xlsx', index=False)