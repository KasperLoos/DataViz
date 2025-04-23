

import marimo

__generated_with = "0.13.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import random
    from svg import SVG, Circle, Line, Title, Path, Ellipse, Text
    import marimo as mo
    import requests
    import matplotlib.pyplot as plt
    # Plot scatterplot with log scales and variable dot sizes, coloured by hour
    import numpy as np
    from matplotlib.colors import Normalize
    from matplotlib import cm
    import math

    return Circle, Line, SVG, Text, Title, mo, np, pd, requests


@app.cell
def _(np, pd, requests):
    urlkl = 'https://raw.githubusercontent.com/KasperLoos/DataViz/refs/heads/main/Data/processed/Processed_KL.csv'
    responsekl = requests.get(urlkl)

    # Save and read the second dataset
    with open('Processed_KL.csv', 'wb') as filekl:
        filekl.write(responsekl.content)

    dfkl = pd.read_csv('Processed_KL.csv')
    def sqrt_log_x_plus_1(x):
        return np.sqrt(np.log(x + 1))
    dfkl['displaydatekl'] = pd.to_datetime(dfkl['date']).dt.strftime('%d-%m-%Y')
    return dfkl, sqrt_log_x_plus_1


@app.cell
def _(dfkl):
    min_sizekl = dfkl['intake'].min()
    max_sizekl = dfkl['intake'].max()

    min_time_beforekl = dfkl['time_before_log'].min()
    max_time_beforekl = dfkl['time_before_log'].max()

    min_time_afterkl = dfkl['time_after_log'].min()
    max_time_afterkl = dfkl['time_after_log'].max()
    return (
        max_sizekl,
        max_time_afterkl,
        max_time_beforekl,
        min_sizekl,
        min_time_afterkl,
        min_time_beforekl,
    )


@app.cell
def _(
    max_sizekl,
    max_time_afterkl,
    max_time_beforekl,
    min_sizekl,
    min_time_afterkl,
    min_time_beforekl,
):
    def rescale(x, domain_min, domain_max, range_min, range_max):
        scale = (range_max - range_min) / (domain_max - domain_min)
        return range_min + (x - domain_min) * scale
    svg_width = 800
    svg_height = 800

    def scaleBefore(x):
        return int(rescale(x, min_time_beforekl, max_time_beforekl, 70, svg_width-70))

    def scaleAfter(y):
        return int(rescale(y, min_time_afterkl, max_time_afterkl, svg_height-70, 70))

    def scaleSize(s):
        return int(rescale(s, min_sizekl, max_sizekl, 3, 35))
    return scaleAfter, scaleBefore, scaleSize, svg_height, svg_width


@app.cell
def _(mo):
    penskl = {
        "1": ["Miss Piggy", "Babe", "Porky", "Piglet", "Hamm", "Peppa", "Pumbaa", "Napoleon", "Snowball", "Wilbur", "Plopper"],
        "2": ["Okkoto", "Hen Wen", "Maxwell", "Gordy", "Chris P. Bacon", "Kevin Bacon", "Ham Solo", "Hamtaro", "Piggy Smalls", "Notorious P.I.G.", "Sir Oinks-a-Lot"],
        "3": ["Elvis Pigsley", "Piginator", "Harry Porker", "Hamlet", "Boarimir", "Hufflepork", "Frankenswine", "Pigachu", "Swinefeld", "Obi-Wan Pig-nobi", "Hammy Potter"],
        "4": ["Oink Floyd", "Piggy Stardust", "Pigasso", "Vincent van Hog", "Swinestein", "Hamalot", "Napoleon Boarnaparte", "Pig Jagger", "Britney Squeals", "Piggy Minaj", "Arnold Schwarzenhogger"],
        "5": ["Snoop Hoggy Hog", "Oinkerbell", "Piggy Azalea", "Brad Pig", "The Boar Identity", "Swinehouse", "Maple Bacon", "Hambert", "Prosciutto", "Sausage Roll", "Pork Chop"],
        "6": ["Hambone", "Sir Loin", "BBQ", "Chorizo", "Pigador Dali", "Oinklet", "Baconator", "Ribs McGee", "Lard Vader", "Hamwise Gamgee", "Makin’ Bacon"],
        "7": ["Peppa-roni", "Truffle Snout", "Hamthony Hopkins", "Pig Mac", "Oinkers", "Swinerton", "Boar-gart", "Sir Hamsalot", "The Great Hambino", "Piggly Wiggly", "Hamlet the Piglet"],
        "8": ["Boaris Johnson", "Oinkie Minaj", "Hogzilla", "Hamlet Oinksworth", "Hamphrey", "Hogsmeade", "Pig Newton", "Babe Ruth", "Snoutorious B.I.G.", "Swine Fluencer", "Professor Pigsworth"],
        "9": ["Lord Oinkington", "Piggle Wiggle", "Curly Trotter", "Hameo", "Oinkie Pie", "Boar-derline Genius", "Hamtastic", "Captain Pork Sparrow", "The Pork Knight Rises", "Trotsky", "Napoleon Swineaparte"],
        "10": ["Hoggle", "Hamothy Chalamet", "Boar-inson Wells", "Piggory Dock", "Swinona Ryder", "Peppa the Hut", "The Three Little Pigsley", "Hambo", "Snorty McSnortface", "Pigtoria Beckham", "Hamberlain"]
    }

    station_dropdown = mo.ui.dropdown(
        options=list(penskl.keys()),
        value="1",
        label="Select a station"
    )
    return penskl, station_dropdown


@app.cell
def _(mo, penskl, station_dropdown):
    # Get pig list from current pen selection
    pig_list = penskl[station_dropdown.value]

    pig_dropdown = mo.ui.dropdown(
        options=pig_list,
        value=pig_list[0],
        label="Select a pig"
    )
    return (pig_dropdown,)


@app.cell
def _(dfkl, mo, pd):
    # Ensure 'date' column is datetime
    dfkl['date'] = pd.to_datetime(dfkl['date'])

    # Define the range of days
    min_date = dfkl['date'].min()
    max_date = dfkl['date'].max()
    total_days = (max_date - min_date).days

    # Create the range slider
    range_sliderkl = mo.ui.range_slider(
        start=0,
        stop=total_days,
        step=1,
        value=(0, total_days),
        show_value=True,
        label="Select range (days from start)",
    )
    return min_date, range_sliderkl


@app.cell
def _(dfkl, min_date, pd, pig_dropdown, range_sliderkl, station_dropdown):
    selected_station = int(station_dropdown.value)
    dfkl_station = dfkl[dfkl['station'] == selected_station]
    selected_pig_name = pig_dropdown.value  
    dfkl_pig = dfkl_station[dfkl_station['pig'] == selected_pig_name]
    number_of_visitskl = len(dfkl_pig)
    start_day, end_day = range_sliderkl.value

    start_date = min_date + pd.Timedelta(days=start_day)
    end_date = min_date + pd.Timedelta(days=end_day)

    # Filter the DataFrame
    dfkl_pig = dfkl_pig[(dfkl_pig['date'] >= start_date) & (dfkl_pig['date'] <= end_date)]
    mean_intakekl = round(dfkl_pig['intake'].mean(), 3)
    weigth_gainkl = dfkl_pig['bodyw_gain'].mean()
    print(number_of_visitskl)
    print(mean_intakekl)
    print(weigth_gainkl)
    return dfkl_pig, mean_intakekl, number_of_visitskl, weigth_gainkl


@app.cell
def _(mo):
    mo.md(
        """
        <style>
            svg.plotkasp {
                border: 1px solid;
            }
            circle.plotkasp:hover {
                fill: red;
                fill-opacity: 1;
            }
        </style>
        """
    )
    return


@app.cell
def _(dfkl_pig, scaleAfter, scaleBefore, scaleSize):
    datapointskl = [
        {
            'x': scaleBefore(row['time_before_log']),
            'y': scaleAfter(row['time_after_log']),
            'r': scaleSize(row['intake']),
            'displaydatekl' : row['displaydatekl'],
            'color' : row['hour'],
            'intake' : row['intake'],
            'duration' : row['duration']
        }
        for i, row in dfkl_pig.iterrows()
    ]
    return (datapointskl,)


@app.cell
def _(datapointskl):
    x_vals = [d['x'] for d in datapointskl]
    y_vals = [d['y'] for d in datapointskl]

    min_x, max_x = min(x_vals), max(x_vals)
    min_y, max_y = min(y_vals), max(y_vals)
    return


@app.function
def color_scale(hour):
    if 22 <= hour <= 23 or 0 <= hour <= 5:
        return "#1f77b4"  # night (blue)
    elif 6 <= hour <= 13:
        return "#2ca02c"  # morning (green)
    elif 14 <= hour <= 21:
        return "#ff7f0e"


@app.cell
def _(Circle, Title, datapointskl):
    circleskl = []

    for datapointkl in datapointskl:
        circlekl = Circle(
            cx=datapointkl['x'],
            cy=datapointkl['y'],
            r=datapointkl['r'],
            fill=color_scale(int(datapointkl['color'])),
            fill_opacity=0.5,
            stroke_width=1,
            stroke="white",
            class_="plotkasp",
            elements=[
                Title(elements=[
                    f"Date: {datapointkl['displaydatekl']}\n",
                    f"Intake: {datapointkl['intake']} kg \n",
                    f"Duration: {datapointkl['duration']} seconds"
                ])
            ]
        )
        circleskl.append(circlekl)
    return (circleskl,)


@app.cell
def _(
    Line,
    Text,
    max_time_beforekl,
    min_time_beforekl,
    pd,
    sqrt_log_x_plus_1,
    svg_height,
    svg_width,
):
    hor_linekl = Line(x1=65, y1=svg_height-65, x2=735, y2=svg_height-65, stroke="black", stroke_width=2)
    ver_linekl = Line(x1=65, y1=svg_height-65, x2=65, y2=65, stroke="black", stroke_width=2)

    xkl_text = Text(x=svg_width/2 - 100, y=790, elements=["Time before visit in sqrt(log(hours+1))"])
    ykl_text = Text(x=25, y=500, elements=["Time after visit in sqrt(log(hours+1))"], transform="rotate(270, 10, 500)")

    time_labelskl = {
        1/60: "1 min",
        1/12: "5 min",
        1/2: "30 min",
        1: "1 hr",
        3: "3 hrs",
        10: "10 hrs",
        24: "1 day",
        48: "2 days"
    }

    domain_text_minkl = min_time_beforekl
    domain_text_maxkl = max_time_beforekl

    def rescaletext(x, domain_text_minkl, domain_text_maxkl, range_min, range_max):
        scale = (range_max - range_min) / (domain_text_maxkl - domain_text_minkl)
        return range_min + (x - domain_text_minkl) * scale

    label_positionskl = []
    x_guideskl = []

    for raw_val, label in time_labelskl.items():
        if isinstance(raw_val, pd.Series):
            log_val = raw_val.apply(sqrt_log_x_plus_1)
        else:
            log_val = sqrt_log_x_plus_1(raw_val)

        x_poskl = rescaletext(log_val, domain_text_minkl, domain_text_maxkl, 90, svg_width - 90)
        label_positionskl.append((x_poskl, label))

        # Add vertical guide line
        x_guideskl.append(Line(x1=x_poskl, y1=svg_height - 65, x2=x_poskl, y2=65, stroke="grey", stroke_width=1, stroke_opacity=0.4))

    label_text_elements = [
        Text(x=pos, y=755, elements=[label], text_anchor="middle")
        for pos, label in label_positionskl
    ]

    y_label_positionskl = []
    y_guideskl = []

    for raw_val, label in time_labelskl.items():
        if isinstance(raw_val, pd.Series):
            log_val = raw_val.apply(sqrt_log_x_plus_1)
        else:
            log_val = sqrt_log_x_plus_1(raw_val)

        y_poskl = rescaletext(log_val, domain_text_minkl, domain_text_maxkl, svg_width - 90, 90)
        y_label_positionskl.append((y_poskl, label))

        # Add horizontal guide line
        y_guideskl.append(Line(x1=65, y1=y_poskl, x2=735, y2=y_poskl, stroke="grey", stroke_width=1, stroke_opacity=0.4))

    y_text_elements = [
        Text(x=55, y=pos, elements=[label], text_anchor="end", dominant_baseline="middle")
        for pos, label in y_label_positionskl
    ]
    return (
        hor_linekl,
        label_text_elements,
        ver_linekl,
        x_guideskl,
        xkl_text,
        y_guideskl,
        y_text_elements,
        ykl_text,
    )


@app.cell
def _(
    SVG,
    circleskl,
    hor_linekl,
    label_text_elements,
    svg_height,
    svg_width,
    ver_linekl,
    x_guideskl,
    xkl_text,
    y_guideskl,
    y_text_elements,
    ykl_text,
):
    plotkl = SVG(
        class_ = "plotkasp",
        id="kasp",
        width=svg_width,
        height=svg_height,
        elements=[*circleskl, hor_linekl, ver_linekl, xkl_text, ykl_text, *label_text_elements, *y_text_elements, x_guideskl, y_guideskl]
    )
    return (plotkl,)


@app.cell
def _(mo, pig_dropdown, plotkl, range_sliderkl, station_dropdown):
    mo.hstack([mo.Html(plotkl.as_str()), mo.vstack([station_dropdown, pig_dropdown, range_sliderkl], justify="start")])
    return


@app.cell
def _(
    mean_intakekl,
    mo,
    number_of_visitskl,
    pig_dropdown,
    station_dropdown,
    weigth_gainkl,
):
    mo.md(f"""
    🐽 You chose **Station {station_dropdown.value}** and pig **{pig_dropdown.value}**!

    This pig visited the feeding station **{number_of_visitskl} times** with an average intake of **{mean_intakekl} kilograms**.

    Over the span of the study, **{pig_dropdown.value}** gained **{weigth_gainkl} kilograms** 🐷.

    The colours represent the time of day at which the feeding visit took place:

    - 🟩 **Green**: Morning (06:00 – 14:00)  
    - 🟧 **Orange**: Afternoon & Evening (14:00 – 22:00)  
    - 🟦 **Blue**: Night (22:00 – 06:00)
    """)
    return


if __name__ == "__main__":
    app.run()
