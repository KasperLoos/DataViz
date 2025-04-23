import marimo

__generated_with = "0.11.13"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    import requests
    return mo, np, pd, plt, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        """
        This README describes the datasets 'Exp? - Feeding data.csv', which contain records of pig visits to IVOG electronic feeding stations (EFSs).
            Datasets are available for four rounds of pigs, each with 10 pens. Each pen contained one IVOG EFS, to which a maximum of 11 pigs had access.
            IVOG EFSs register each visit to the feeder, along with pig RFID number and time stamp and trough weight upon entry and exit.
            These data were transferred to us on a weekly basis, via the TU Eindhoven, in .DAT format.
            The .DAT files are no longer stored, but the csv files described here are their merged equivalents; i.e. no processing has been done beyond merging the daily .DAT files together with the correct date. In addition, feeding rate was calculated, the hour upon which the visit started was extracted, the visit duration was put in a more convenient format (i.e. from 'min.s' to 's'), and empty columns were removed (see 'NOTES' below).

            A description of the variables, from left to right, is found below.
            - date: The date upon which the feeder visit occurred, in day/month/year.
            - tattoo: The tattoo number of the pig, as was linked to its RFID number.
            - pig: The RFID number of the pig visiting the feeder. Generally 12 digits, though in round 3 pigs only had 1-3 digits and the column was renamed as 'pig.short'.
            - station: The ID number of the IVOG station that recorded the visit, from 1-10. This corresponds with the pen the pig was in; see the powerpoint file that gives the floorplan of the barn.
            - weight_start: The weight of the feed in the trough (in kg) at the start of the visit. 
            - weight_end: The weight of the feed in the trough (in kg) at the end of the visit. 
            - intake: The difference in the weight of the feed in the trough between the end and start of the visit. See notes below for some details surrounding feeder fillings.
            - start: The time upon which the visit started, in 'day/month/year hour:minute:second'
            - end: The time upon which the visit ended, in 'day/month/year hour:minute:second'
            - hour: The hour within which the visit started, i.e. '11' means the visit started between 11:00:00 and 11:59:59.
            - duration: The time difference (in seconds) between the visit end and start.
            - rate: Column intake divided by column duration, multiplied by 1000 (in kg/s)

            NOTES:
            - IVOG EFS add about 600 g of feed to the trough when the trough weight goes below a certain limit (not sure what the limit is). This is generally registered as a visit with an intake of -0.6, and with 'FILLING' in column 'tattoo'.
            - Some visits with pig (RFID) number 0 were pre-marked as 'FILLING' or 'GHOST', i.e. trough fillings or pig visits lacking an RFID registration, respectively. Reasons/Rules for this are unknown to the authors.
        DO NOT OVERWRITE feed intakes with manually calculated measures. These are incorrect if a pig's feeder visit started during a feeder filling, as then the average filling size of the previous 10 fillings was deducted from the feed intake.
            - 'rate' and 'hour' were added by Jacinta; they were not present in the .DAT files.
            - There were also some empty columns in the .DAT files, which were removed.
            - In the original .DAT file, the 'duration' column was given in the unit 'min.s'. This was turned into seconds by extracting all digits before '.', multiplying these by 60, and adding all digits after '.'.
            - In experiment 3, mice were nesting beneath the IVOG load cells and chewed through the cables. This led to missing/unreliable data for station 8 from 09-07-2022 to 22-07-2022 (evening) and for station 9 from 11-06-2022 to 24-06-2022 (18:15h).
            - For a few stations, pigs were registered that were not present in the pen (i.e. more than 11 unique pigs were detected). These were pigs in neighbouring pens that were wrongfully registered. Can be corrected using the 'Pig registration' csv's.
        """
    )
    return


@app.cell
def _(pd, requests):
    # Load first dataset from local file
    dfkl1 = pd.read_csv("C:/Users/kkasp/Desktop/feedingdata.csv")

    # Load second dataset from github URL
    urlkl2 = 'https://raw.githubusercontent.com/KasperLoos/DataViz/refs/heads/main/Data/raw/correctpen.csv'
    responsekl2 = requests.get(urlkl2)

    # Save and read the second dataset
    with open('correctpen.csv', 'wb') as file:
        file.write(responsekl2.content)

    dfkl2 = pd.read_csv('correctpen.csv')

    # Clean dfkl1: remove pigs with ID 0 and drop the 'station' column
    dfkl1 = dfkl1[dfkl1['pig'] != 0]
    dfkl1 = dfkl1.drop(columns=['station'])
    return dfkl1, dfkl2, file, responsekl2, urlkl2


@app.cell
def _(dfkl2):
    dfkl2
    return


@app.cell
def _(dfkl1, dfkl2):
    #data has 123 unique pigs, pen only has 110 (as expected), who are these 13 extra pigs (we have already removed pig=0 for filling)
    unique_pigskl = dfkl1.loc[~dfkl1['pig'].isin(dfkl2['pig']), 'pig'].unique()
    print(unique_pigskl)
    #based on the readme files, these pigs were wrongfully scanned and were not actually present in the pens
    # "For a few stations, pigs were registered that were not present in the pen (i.e. more than 11 unique pigs were detected). These were pigs in neighbouring pens that were wrongfully registered. Can be corrected using the 'Pig registration' csv's."
    return (unique_pigskl,)


@app.cell
def _(dfkl1, dfkl2):
    dfkl3 = dfkl1.merge(dfkl2[['pig', 'station']], on='pig', how='left')
    dfkl3 = dfkl3.dropna(subset=['station'])
    #get the correct station for all the pigs
    return (dfkl3,)


@app.cell
def _(dfkl3, plt):
    import seaborn as sns

    # Set style for better aesthetics
    sns.set_style("whitegrid")

    # Plot histogram
    plt.figure(figsize=(8, 5))
    sns.histplot(dfkl3['intake'], bins=30, kde=True, color='blue')

    # Labels and title
    plt.xlabel("Intake")
    plt.ylabel("Frequency")
    plt.title("Histogram of Intake")

    # Set x-axis limits
    plt.xlim(-1, 5)

    # Show plot
    plt.show()
    return (sns,)


@app.cell
def _(dfkl3, pd):
    df_sortedkl = dfkl3.sort_values(by=['pig', 'start'])
    df_filteredkl = df_sortedkl[(df_sortedkl['intake'] > 0.05)]
    # Ensure 'start' and 'end' are in datetime format using .loc to avoid the warning
    df_filteredkl.loc[:, 'start'] = pd.to_datetime(df_filteredkl['start'], errors='coerce')
    df_filteredkl.loc[:, 'end'] = pd.to_datetime(df_filteredkl['end'], errors='coerce')

    # Make sure the dataframe is sorted by 'pig' and 'start' to calculate the time difference correctly
    df_filteredkl = df_filteredkl.sort_values(by=['pig', 'start'])

    # Calculate the time difference between 'start' of the current row and 'end' of the previous row
    df_filteredkl['time_before'] = df_filteredkl['start'] - df_filteredkl.groupby('pig')['end'].shift(1)
    # Calculate the time difference between 'end' of the current row and 'start' of the next row
    df_filteredkl['time_after'] = df_filteredkl.groupby('pig')['start'].shift(-1) - df_filteredkl['end']
    # Optionally, check the result
    df_filteredkl['time_after'] = pd.to_timedelta(df_filteredkl['time_after'])
    df_filteredkl['time_before'] = pd.to_timedelta(df_filteredkl['time_before'])

    # Convert timedelta to total hours
    df_filteredkl['time_after_hours'] = df_filteredkl['time_after'].dt.total_seconds() / 3600
    df_filteredkl['time_before_hours'] = df_filteredkl['time_before'].dt.total_seconds() / 3600

    df_filteredkl = df_filteredkl.dropna(subset=['time_after_hours', 'time_before_hours'])
    df_filteredkl['size'] = (df_filteredkl['intake'] / 3.2) * 500  # Scale sizes

    print(df_filteredkl[['pig', 'start', 'end', 'time_before', 'time_after', 'time_after_hours', 'time_before_hours']])
    #df_filteredkl['intake'] = df_filteredkl['intake'] + 5
    return df_filteredkl, df_sortedkl


@app.cell
def _(df_filteredkl):
    df_filteredkl
    #4measurements with time since more than 1 day (outliers)
    return


@app.cell
def _(df_filteredkl, plt, sns):
    # Set style for better aesthetics
    sns.set_style("whitegrid")

    # Plot histogram
    plt.figure(figsize=(8, 5))
    sns.histplot(df_filteredkl['size'], bins=30, kde=True, color='blue')

    # Labels and title
    plt.xlabel("Intake")
    plt.ylabel("Frequency")
    plt.title("Histogram of size")

    # Set x-axis limits
    plt.xlim(-1, 500)

    # Show plot
    plt.show()
    return


@app.cell
def _(df_filteredkl):
    z = df_filteredkl['intake'].max()
    z
    return (z,)


@app.cell
def _(df_filteredkl, dfkl2, np):
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
    dfkl4 = df_filteredkl

    def sqrt_log_x_plus_1(x):
        return np.sqrt(np.log(x + 1))

    dfkl4 = dfkl4.merge(
        dfkl2[['pig', 'gender', 'bodyw_start', 'bodyw_end']],
        on='pig',
        how='left'
    )

    # Create the new column 'bodyw_gain'
    dfkl4['bodyw_gain'] = dfkl4['bodyw_end'] - dfkl4['bodyw_start']

    # Rename the 'pig' column based on the mapping
    dfkl4['pig'] = dfkl4['pig'].replace(rename_dict)
    dfkl4 = dfkl4[(dfkl4['time_before_hours'] > 0) & (dfkl4['time_after_hours'] > 0)]
    # Group by 'station' and get unique 'pig' values for each station
    grouped_pigskl = dfkl4.groupby('station')['pig'].unique()

    dfkl4['time_before_log'] = dfkl4['time_before_hours'].apply(sqrt_log_x_plus_1)
    dfkl4['time_after_log'] = dfkl4['time_after_hours'].apply(sqrt_log_x_plus_1)
    dfkl4 = dfkl4.drop(columns=['tattoo', 'start', 'end'])

    return dfkl4, grouped_pigskl, rename_dict, sqrt_log_x_plus_1


@app.cell
def _(dfkl4):
    dfkl4#mo.ui.data_explorer(df)
    return


@app.cell
def _(dfkl4):
    dfkl4.to_csv("C:/Users/kkasp/Desktop/Processed_KL.csv", index=False)

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
