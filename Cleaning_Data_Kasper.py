import marimo

__generated_with = "0.11.13"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    return mo, np, pd, plt


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
def _(pd):
    data = pd.read_csv("C:/Users/kkasp/Desktop/feedingdata.csv")
    data = data[data['pig'] != 0]
    pen = pd.read_csv("C:/Users/kkasp/Desktop/correctpen.csv")
    data = data.drop(columns=['station'])
    # https://data.mendeley.com/datasets/2mbw72m3g8/1
    return data, pen


@app.cell
def _(data):
    data
    return


@app.cell
def _(data, pen):
    #data has 123 unique pigs, pen only has 110 (as expected), who are these 13 extra pigs (we have already removed pig=0 for filling)
    unique_pigs = data.loc[~data['pig'].isin(pen['pig']), 'pig'].unique()
    print(unique_pigs)
    #based on the readme files, these pigs were wrongfully scanned and were not actually present in the pens
    # "For a few stations, pigs were registered that were not present in the pen (i.e. more than 11 unique pigs were detected). These were pigs in neighbouring pens that were wrongfully registered. Can be corrected using the 'Pig registration' csv's."
    return (unique_pigs,)


@app.cell
def _(data, pen):
    df = data.merge(pen[['pig', 'station']], on='pig', how='left')
    df = df.dropna(subset=['station'])
    #get the correct station for all the pigs
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _(df, plt):
    import seaborn as sns

    # Set style for better aesthetics
    sns.set_style("whitegrid")

    # Plot histogram
    plt.figure(figsize=(8, 5))
    sns.histplot(df['intake'], bins=30, kde=True, color='blue')

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
def _(df, pd):
    df_sorted = df.sort_values(by=['pig', 'start'])
    df_filtered = df_sorted[(df_sorted['intake'] > 0.02)]
    # Ensure 'start' and 'end' are in datetime format using .loc to avoid the warning
    df_filtered.loc[:, 'start'] = pd.to_datetime(df_filtered['start'], errors='coerce')
    df_filtered.loc[:, 'end'] = pd.to_datetime(df_filtered['end'], errors='coerce')

    # Make sure the dataframe is sorted by 'pig' and 'start' to calculate the time difference correctly
    df_filtered = df_filtered.sort_values(by=['pig', 'start'])

    # Calculate the time difference between 'start' of the current row and 'end' of the previous row
    df_filtered['time_since'] = df_filtered['start'] - df_filtered.groupby('pig')['end'].shift(1)
    # Calculate the time difference between 'end' of the current row and 'start' of the next row
    df_filtered['time_to'] = df_filtered.groupby('pig')['start'].shift(-1) - df_filtered['end']
    # Optionally, check the result
    df_filtered['time_to'] = pd.to_timedelta(df_filtered['time_to'])
    df_filtered['time_since'] = pd.to_timedelta(df_filtered['time_since'])

    # Convert timedelta to total hours
    df_filtered['time_to_hours'] = df_filtered['time_to'].dt.total_seconds() / 3600
    df_filtered['time_since_hours'] = df_filtered['time_since'].dt.total_seconds() / 3600

    df_filtered = df_filtered.dropna(subset=['time_to_hours', 'time_since_hours'])

    print(df_filtered[['pig', 'start', 'end', 'time_since', 'time_to', 'time_to_hours', 'time_since_hours']])
    return df_filtered, df_sorted


@app.cell
def _(df_filtered):
    df_filtered
    return


@app.cell
def _():
    return


@app.cell
def _(df_filtered):
    df_filtered
    return


@app.cell
def _(df_filtered):
    df_filtered.to_csv('C:/Users/kkasp/Desktop/cleaned_df.csv', index=False)
    return


@app.cell
def _():
    #mo.ui.data_explorer(df)
    return


@app.cell
def _():
    #For future reference
    """
    df_stat1 = df[(df['station'] == 1) & (df['pig'] == 222000938228)]
    df_stat1 = df_stat1.sort_values('start').copy()  # Sort by start time
    df_stat1['start'] = pd.to_datetime(df_stat1['start'])
    # Compute time deltas
    df_stat1['time_before'] = (df_stat1['start'].shift(-1) - df_stat1['start']).dt.total_seconds() / 3600  # Next start
    df_stat1['time_to'] = (df_stat1['start'] - df_stat1['start'].shift(1)).dt.total_seconds() / 3600  # Previous start
    # Drop NaN values (first row has no previous, last row has no next)
    df_stat1 = df_stat1.dropna()
    df_stat1
    # Plot scatterplot
    df_stat1['size'] = df_stat1['intake'] / df_stat1['intake'].max() * 200  # Scale sizes

    # Plot scatterplot with log scales and variable dot sizes
    plt.figure(figsize=(8, 5))
    plt.scatter(df_stat1['time_before'], df_stat1['time_to'], s=df_stat1['size'], alpha=0.7, edgecolors='k')
    plt.xscale('log')  # Log transformation for x-axis
    plt.yscale('log')  # Log transformation for y-axis
    plt.xlabel('Time To Next Feed?? (log scale, hours)')
    plt.ylabel('Time Since Previous Feed (log scale, hours)')
    plt.title('Scatterplot of Log(Time Before) vs Log(Time Since Previous)')
    plt.grid(False)  # Grid for better readability
    plt.show()
    #add interaction with dropdown 'choose pen & choose pig?'
    #size of dots based on 'intake' or 'duration'?
    #hover over a dot to get the values?
    """
    return


@app.cell
def _():
    from svg import SVG, Circle
    plot = SVG(
        width=60,
        height=60,
        elements=[
            Circle(
                cx=30, cy=30, r=20,
                stroke="red",
                fill="white",
                stroke_width=2,
            ),
        ],
    )
    print(plot)
    return Circle, SVG, plot


@app.cell
def _(mo, plot):
    mo.Html(plot.as_str())
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        <style>
            svg {
                border: 0px; #willaddtoall
                border-style: solid;
            }
            circle {
                fill: steelblue;
                opacity: 0.5;
            }
            circle:hover {
                fill: red;
                opacity: 1;
            }
            rect {
                fill: green;
                stroke: red;
            }
        </style>

        <svg width="300" height="300">
            <circle cx="45" cy="50" r="30"/>
            <rect x="100" y="200" width="70" height="30" />
        </svg>
        has to be markdown cell
        """
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
