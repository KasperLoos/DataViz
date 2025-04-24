import marimo

__generated_with = "0.11.13"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import requests
    import random
    from svg import SVG, Circle, Line, Title, Path, Ellipse, Text, Path
    import numpy as np
    import math
    import os
    return (
        Circle,
        Ellipse,
        Line,
        Path,
        SVG,
        Text,
        Title,
        math,
        mo,
        np,
        os,
        pd,
        random,
        requests,
    )


@app.cell
def _(mo):
    mo.md(
        """
        <style>
            svg.notebook {
                border: 1px solid;
            }
            path.notebook.brushable:hover {
                stroke: olive;
                stroke-width: 5;
                fill-opacity: 1;
            }
        </style>
        """
    )
    return


@app.cell
def _(mo):
    # Creation multiselect for stations

    optionsKP = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    multiselect_stationKP = mo.ui.multiselect(options=optionsKP , label="Choose station(s)")
    return multiselect_stationKP, optionsKP


@app.cell
def _(mo, multiselect_stationKP, pd, requests):
    # Creation multiselect for pigs

    urlKP = 'https://raw.githubusercontent.com/KasperLoos/DataViz/main/Data/processed/Processed_KP.xlsx'

    responseKP = requests.get(urlKP)

    # Save the content of the file
    with open('Processed_KP.xlsx', 'wb') as fileKP:
        fileKP.write(responseKP.content)

    dfKP = pd.read_excel("Processed_KP.xlsx")

    if multiselect_stationKP.value == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] :
        subset_dropdown_stationKP = dfKP
    else:
        subset_dropdown_stationKP = dfKP[dfKP["station"].isin(multiselect_stationKP.value)]
    multiselect_pig_optionsKP = subset_dropdown_stationKP["pig"].unique()
    multiselect_pigKP = mo.ui.multiselect(options = multiselect_pig_optionsKP, label = "Choose pig(s)")
    return (
        dfKP,
        fileKP,
        multiselect_pigKP,
        multiselect_pig_optionsKP,
        responseKP,
        subset_dropdown_stationKP,
        urlKP,
    )


@app.cell
def _(mo, multiselect_pigKP, multiselect_stationKP):
    # Creation dropdown for gender

    if len(multiselect_stationKP.value) > 1 and len(multiselect_pigKP.value) > 1:
        gender_optionsKP = ["gilt", "barrow"]
    else:
        gender_optionsKP = []
    dropdown_genderKP = mo.ui.dropdown(options = gender_optionsKP, label = "Choose gender")
    return dropdown_genderKP, gender_optionsKP


@app.cell
def _(
    Line,
    Path,
    SVG,
    Text,
    Title,
    dfKP,
    dropdown_genderKP,
    mo,
    multiselect_pigKP,
    multiselect_stationKP,
    pd,
):
    # Rescaling of datapoints functions

    max_normalizedKP= 0.3502105263157895
    min_normalizedKP= 0.0025301204819277107

    svg_widthKP = 1000
    svg_heightKP = 800

    def rescaleKP(x, domain_min, domain_max, range_min, range_max):
        scale = (range_max - range_min) / (domain_max - domain_min)
        return range_min + (x - domain_min) * scale

    def scaleXKP(x):
        return int(rescaleKP(x, 0, 23, 60, svg_widthKP-50))

    def scaleYKP(y):
        return int(rescaleKP(y,min_normalizedKP , max_normalizedKP , svg_heightKP-50, 50))

    # Values for normalized hourly intake on y-axis
    normalized_hourly_intake_positionsKP = {
               "0": 750,
                "0.05": 650,
                "0.10": 550,
                "0.15": 450,
                "0.20": 350,
                "0.25": 250,
                "0.30": 150,
                "0.35": 50,
                }
    def getYKP(normalized_hourly_intake):
        return normalized_hourly_intake_positionsKP[normalized_hourly_intake]

    normalized_hourly_intake_valuesKP = []
    for dKP in normalized_hourly_intake_positionsKP:
        yKP = getYKP(dKP)
        normalized_hourly_intake_valuesKP.append(Text(x=20, y=yKP, elements=[dKP], class_="fhds6"))

    # Values for hour on x-axis
    hour_positionsKP = {
            "0": 56,
            "1": 95.13,
            "2": 133.26,
            "3": 172.39,
            "4": 209.52,
            "5": 248.65,
            "6": 287.78,
            "7": 326.91,
            "8": 366.04,
            "9": 406.17,
            "10": 439.30,
            "11": 478.43,
            "12": 515.57,
            "13": 554.70,
            "14": 593.83,
            "15": 632.96,
            "16": 672.09,
            "17": 711.22,
            "18": 750.34,
            "19": 789.48,
            "20": 827.61,
            "21": 866.74,
            "22": 905.87,
            "23": 944,
    }

    def getxKP(hour):
        return hour_positionsKP[hour]

    hour_valuesKP = []
    for eKP in hour_positionsKP:
        xKP = getxKP(eKP)
        hour_valuesKP.append(Text(x=xKP, y=770, elements=[eKP], class_="f526"))

    # x- and y-axis plus their labels

    hor_lineKP = Line(x1=50, y1=750, x2=960, y2=750, stroke="black", stroke_width=2)
    ver_lineKP = Line(x1=50, y1=750, x2=50, y2=40, stroke="black", stroke_width=2)

    hour_textKP = Text(x=456.865, y=790, elements=["Time indication: hour"])
    intake_textKP = Text(x=10, y=500, elements=["Average intake in kg"], transform="rotate(270, 10, 500)")

    # add guidelines

    x_guidesKP = []

    for labelKP, raw_valKP in hour_positionsKP.items():
        x_guideKP = raw_valKP + 3
        x_guidesKP.append(Line(x1=x_guideKP, y1=750, x2=x_guideKP, y2=40, stroke="grey", stroke_width=1, stroke_opacity=0.4))

    y_guidesKP = []

    for ylabelKP, yraw_valKP in normalized_hourly_intake_positionsKP.items():
        y_guideKP = yraw_valKP
        y_guidesKP.append(Line(x1=50, y1=y_guideKP, x2=960, y2=y_guideKP, stroke="grey", stroke_width=1, stroke_opacity=0.4))

    # Multiselects station and pig, and dropdown gender have been created in three seperate cells above

    # Subsetting based on the multiselects and dropdown values 

    if len(multiselect_stationKP.value) > 0 and multiselect_pigKP.value is not None and dropdown_genderKP.value is None:
        subset_station_pigKP = dfKP[dfKP["pig"].isin(multiselect_pigKP.value)]
    elif len(multiselect_stationKP.value) > 0 and multiselect_pigKP.value is not None and dropdown_genderKP.value is not None:
        subset_station_pigKP = dfKP[(dfKP["pig"].isin(multiselect_pigKP.value)) & (dfKP["gender"] == dropdown_genderKP.value)]
    else: 
        subset_station_pigKP = dfKP

    # Creation of the pigs' feeding patterns via polylines

    polylinesKP = []

    for pig_indexKP, pig_rowKP in subset_station_pigKP.iterrows():
        path_commandsKP = []

        if pig_rowKP['gender'] == 'gilt': 
            polyline_colorKP = "deeppink"
        else:
            polyline_colorKP = "dodgerblue"

        for hourKP in range(24):
            if pd.notna(pig_rowKP[hourKP]):  
                hour_xKP = hour_positionsKP[str(hourKP)] + 3
                hour_yKP = scaleYKP(pig_rowKP[hourKP])
                path_commandsKP.append(f"M {hour_xKP} {hour_yKP}")  
                break  

        for hourKP in range(24):
            if pd.notna(pig_rowKP[hourKP]):  
                hour_xKP = hour_positionsKP[str(hourKP)] + 3
                hour_yKP = scaleYKP(pig_rowKP[hourKP])
                path_commandsKP.append(f"L {hour_xKP} {hour_yKP}")  

        polyline_pathKP = " ".join(path_commandsKP)

        polylinesKP.append(Path(d=polyline_pathKP, stroke=polyline_colorKP, fill="none", stroke_width=1, class_="notebook brushable", id = pig_rowKP['pig'], elements=[Title(elements=[f"pigname: {pig_rowKP['pig']} \n", f"station: {pig_rowKP['station']}\n", f"gender: {pig_rowKP['gender']}\n", f"weight increase: {pig_rowKP['Weight_increase']} kg"])]))

    # Creation of the svg

    svgKP = SVG(
        width=svg_widthKP,
        height=svg_heightKP,
        elements= normalized_hourly_intake_valuesKP + hour_valuesKP + polylinesKP + x_guidesKP + y_guidesKP+ [hor_lineKP, ver_lineKP, hour_textKP, intake_textKP],
        class_="notebook"
    )

    # Create text about gender

    textKP = mo.md(f"""
    The colour of the line represents the gender of the pig:

    -  ♀ *rose*: gilt (female)  
    -  ♂ *Blue*: barrow (male)
    """)

    # Outputting svg, multiselects and dropdown
    mo.hstack([mo.Html(svgKP.as_str()), mo.vstack([multiselect_stationKP, multiselect_pigKP, dropdown_genderKP, textKP], justify="start")], justify="start")
    return (
        dKP,
        eKP,
        getYKP,
        getxKP,
        hor_lineKP,
        hourKP,
        hour_positionsKP,
        hour_textKP,
        hour_valuesKP,
        hour_xKP,
        hour_yKP,
        intake_textKP,
        labelKP,
        max_normalizedKP,
        min_normalizedKP,
        normalized_hourly_intake_positionsKP,
        normalized_hourly_intake_valuesKP,
        path_commandsKP,
        pig_indexKP,
        pig_rowKP,
        polyline_colorKP,
        polyline_pathKP,
        polylinesKP,
        raw_valKP,
        rescaleKP,
        scaleXKP,
        scaleYKP,
        subset_station_pigKP,
        svgKP,
        svg_heightKP,
        svg_widthKP,
        textKP,
        ver_lineKP,
        xKP,
        x_guideKP,
        x_guidesKP,
        yKP,
        y_guideKP,
        y_guidesKP,
        ylabelKP,
        yraw_valKP,
    )


@app.cell
def _():
    #VISUAL 2
    return


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
    return dfkl, filekl, responsekl, sqrt_log_x_plus_1, urlkl


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
    return rescale, scaleAfter, scaleBefore, scaleSize, svg_height, svg_width


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
    return pig_dropdown, pig_list


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
    return max_date, min_date, range_sliderkl, total_days


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
    return (
        dfkl_pig,
        dfkl_station,
        end_date,
        end_day,
        mean_intakekl,
        number_of_visitskl,
        selected_pig_name,
        selected_station,
        start_date,
        start_day,
        weigth_gainkl,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
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
    return max_x, max_y, min_x, min_y, x_vals, y_vals


@app.cell
def _():
    def color_scale(hour):
        if 22 <= hour <= 23 or 0 <= hour <= 5:
            return "#1f77b4"  # night (blue)
        elif 6 <= hour <= 13:
            return "#2ca02c"  # morning (green)
        elif 14 <= hour <= 21:
            return "#ff7f0e"
    return (color_scale,)


@app.cell
def _(Circle, Title, color_scale, datapointskl):
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
    return circlekl, circleskl, datapointkl


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
        domain_text_maxkl,
        domain_text_minkl,
        hor_linekl,
        label,
        label_positionskl,
        label_text_elements,
        log_val,
        raw_val,
        rescaletext,
        time_labelskl,
        ver_linekl,
        x_guideskl,
        x_poskl,
        xkl_text,
        y_guideskl,
        y_label_positionskl,
        y_poskl,
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


@app.cell
def _():
    # Visual 3
    return


@app.cell
def _(mo, pd):
    # URL of the raw file
    url_AV = "https://raw.githubusercontent.com/KasperLoos/DataViz/main/Data/processed/Occurences_Arthur.xlsx"
    # Reading the Excel file directly into a DataFrame
    pigs_AV = pd.read_excel(url_AV)
    url2_AV = "https://raw.githubusercontent.com/KasperLoos/DataViz/main/Data/processed/weights_Arthur.xlsx"
    weights_AV = pd.read_excel(url2_AV)
    weight_dict_AV = weights_AV.set_index('pig')['bodyw_end'].to_dict()

    # Get list of unique cages (stations_AV)
    stations_AV = sorted(pigs_AV['station'].unique().astype(str))

    # UI dropdown widget
    station_dropdownav = mo.ui.dropdown(
        options=stations_AV,
        value=stations_AV[0],
        label="Select a cage (station)"
    )
    return (
        pigs_AV,
        station_dropdownav,
        stations_AV,
        url2_AV,
        url_AV,
        weight_dict_AV,
        weights_AV,
    )


@app.cell
def _(mo, pigs_AV, station_dropdownav):
    selected_station_AV = int(station_dropdownav.value)
    station_pigs_AV = pigs_AV[pigs_AV['station'] == selected_station_AV]
    pig_ids_AV = station_pigs_AV['Pig_1'].unique().tolist()

    # Convert pig IDs to strings to handle both numeric and string IDs
    pig_ids_AV = [str(pig_id) for pig_id in pig_ids_AV]
    pig_options_AV = ["All"] + pig_ids_AV


    # UI dropdown widget for pig selection
    pig_dropdownav = mo.ui.dropdown(
        options=pig_options_AV,
        value="All",
        label="Select a pig to highlight its connections"
    )
    return (
        pig_dropdownav,
        pig_ids_AV,
        pig_options_AV,
        selected_station_AV,
        station_pigs_AV,
    )


@app.cell
def _(pig_ids_AV):
    coordinates_circles_AV = [
        (500,100),
        (325,175),
        (675,175),
        (850,300),
        (150,300),
        (900,550),
        (100,550),
        (800,750),
        (200,750),
        (600,900),
        (400,900),

    ]

    id_to_coord_AV = dict(zip([str(pig_id) for pig_id in pig_ids_AV], coordinates_circles_AV))
    return coordinates_circles_AV, id_to_coord_AV


@app.cell
def _(Line, Title, id_to_coord_AV, pig_dropdownav, pigs_AV, station_pigs_AV):
    lines_AV = []

    selected_pig_AV = pig_dropdownav.value

    if selected_pig_AV == "All":
        for _, row in pigs_AV.iterrows():
            pig1 = str(row['Pig_1'])
            pig2 = str(row['Pig_2'])
            opacity = row['Count']**2 / 250000

        # Get coordinates
            if pig1 in id_to_coord_AV and pig2 in id_to_coord_AV:
                x1, y1 = id_to_coord_AV[pig1]
                x2, y2 = id_to_coord_AV[pig2]

                lines_AV.append(
                    Line(
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2,
                        class_= "group1",
                        elements=[Title(elements=[str(row['Count'])])],
                        stroke_opacity=opacity,
                    )
                )
    else:
        # Show only connections for selected pig
        pig_interactions_AV = station_pigs_AV[
            (station_pigs_AV['Pig_1'].astype(str) == selected_pig_AV) | 
            (station_pigs_AV['Pig_2'].astype(str) == selected_pig_AV)
        ]

        for _, row in pig_interactions_AV.iterrows():
            pig1 = str(row['Pig_1'])
            pig2 = str(row['Pig_2'])
            opacity = row['Count']**2 / 250000

            if pig1 in id_to_coord_AV and pig2 in id_to_coord_AV:
                x1, y1 = id_to_coord_AV[pig1]
                x2, y2 = id_to_coord_AV[pig2]

                lines_AV.append(
                    Line(
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2,
                        class_="group1",
                        elements=[Title(elements=[str(row['Count'])])],
                        stroke_opacity=opacity,
                        stroke="red" if selected_pig_AV in (pig1, pig2) else "black"
                    )
                )
    return (
        lines_AV,
        opacity,
        pig1,
        pig2,
        pig_interactions_AV,
        row,
        selected_pig_AV,
        x1,
        x2,
        y1,
        y2,
    )


@app.cell
def _(
    Path,
    Title,
    coordinates_circles_AV,
    id_to_coord_AV,
    pig_ids_AV,
    pigs_AV,
    selected_pig_AV,
):
    self_counts_AV = pigs_AV[pigs_AV['Pig_1'] == pigs_AV['Pig_2']].set_index('Pig_1')['Count'].to_dict()

    paths_AV = []

    if selected_pig_AV == "All":
        for (x, y), pig_id, angle in zip(coordinates_circles_AV, pig_ids_AV, 
            [-0, -30, 30, 60, -60, 90, -90, 120, -120, 180, -180]):

            count = self_counts_AV.get(pig_id, 0)
            _opacity = (count / 2000) if count else 0.0

            if _opacity > 0:
                paths_AV.append(
                   Path(
                    d=f"M {x},{y} C {x-100},{y-75} {x+100},{y-75} {x},{y}",
                    transform=f"rotate({angle} {x} {y})",
                    stroke="purple",
                    stroke_opacity=_opacity,
                    fill="none",
                    class_ = "group1",
                    elements=[Title(elements=[str(count)])]
                )
            )

    else:
        # Show only self-count path for selected pig
        if selected_pig_AV in id_to_coord_AV:
            idx = pig_ids_AV.index(selected_pig_AV)
            x, y = coordinates_circles_AV[idx]
            angle = [-0, -30, 30, 60, -60, 90, -90, 120, -120, 180, -180][idx]

            count = self_counts_AV.get(selected_pig_AV, 0)
            _opacity = (count / 2000) if count else 0.0

            if _opacity > 0:
                paths_AV.append(
                    Path(
                        d=f"M {x},{y} C {x-100},{y-75} {x+100},{y-75} {x},{y}",
                        transform=f"rotate({angle} {x} {y})",
                        stroke="purple",
                        stroke_opacity=_opacity,
                        fill="none",
                        class_="group1",
                        elements=[Title(elements=[str(count)])]
                    )
                )
    return angle, count, idx, paths_AV, pig_id, self_counts_AV, x, y


@app.cell
def _(SVG, lines_AV, paths_AV, svg_content_AV):
    all_elements_AV = paths_AV + lines_AV
    all_elements_AV.append(svg_content_AV)

    plot_AV = SVG(
        width=1000,
        height=1000,
        elements= all_elements_AV
    )
    return all_elements_AV, plot_AV


@app.cell
def _(mo):
    mo.md(
        r"""
        <style>
        line.group1 {
                stroke : black;
                stroke-width: 3;
                cursor: pointer;
        }

        line.group1:hover {
            stroke: red;
            stroke-width: 6;
        }

        path.group1 {
                stroke : black;
                stroke-width: 3;
                cursor: pointer;
        }

        path.group1:hover {
            stroke: red;
            stroke-width: 6;
        }
        </style>
        """
    )
    return


@app.cell
def _(mo, pig_dropdownav, plot_AV, station_dropdownav):
    mo.hstack([mo.Html(plot_AV.as_str()), mo.vstack([ station_dropdownav, pig_dropdownav], justify= "start")])
    return


@app.cell
def _(coordinates_circles_AV, pig_ids_AV, weight_dict_AV):
    def pig_svg(x, y, pig_id, weight_dict_AV):
        scale_factor = 1.3  # Increase this value to make the pig larger
        weight = weight_dict_AV.get(pig_id, 'N/A')  # Get weight from dictionary

        return f'''
        <g transform="translate({x},{y})" class="group1" id="circle-{pig_id}">
            <title>Pig ID: {pig_id}\nWeight: {weight} kg</title>
            <!-- Pig Body (scaled) -->
            <circle cx="0" cy="0" r="{12 * scale_factor}" fill="pink" stroke="black" />

            <!-- Ears (scaled) -->
            <path d="M {-8 * scale_factor},{-10 * scale_factor} Q {-10 * scale_factor},{-15 * scale_factor} {-5 *        scale_factor},{-12 * scale_factor}" fill="pink" stroke="black"/>
            <path d="M {8 * scale_factor},{-10 * scale_factor} Q {10 * scale_factor},{-15 * scale_factor} {5 * scale_factor},{-12 * scale_factor}" fill="pink" stroke="black"/>

            <!-- Eyes (scaled) -->
            <circle cx="{-4 * scale_factor}" cy="{-3 * scale_factor}" r="{1.5 * scale_factor}" fill="black"/>
            <circle cx="{4 * scale_factor}" cy="{-3 * scale_factor}" r="{1.5 * scale_factor}" fill="black"/>

            <!-- Nose (scaled) -->
            <ellipse cx="0" cy="{4 * scale_factor}" rx="{5 * scale_factor}" ry="{3 * scale_factor}" fill="#ffcccc" stroke="black"/>
            <circle cx="{-2 * scale_factor}" cy="{4 * scale_factor}" r="{0.5 * scale_factor}" fill="black"/>
            <circle cx="{2 * scale_factor}" cy="{4 * scale_factor}" r="{0.5 * scale_factor}" fill="black"/>
        </g>
        '''

    svg_content_AV = '''
    <svg width="1000" height="1000">
        <style>
            .group1 {
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .group1:hover circle {
                fill: red;  # Change the body color on hover
            }

            .group1:hover path {
                stroke: red;  # Change the ears color on hover
            }

            .group1:hover circle, .group1:hover ellipse {
                fill: #ff6666;  # Change eyes and nose color
            }
        </style>
    '''

    # Loop through coordinates and pig IDs, and append the pig SVG for each position
    for (_x, _y), _pig_id in zip(coordinates_circles_AV, pig_ids_AV):
        svg_content_AV += pig_svg(_x, _y, _pig_id, weight_dict_AV)

    svg_content_AV += '''
    </svg>
    '''
    return pig_svg, svg_content_AV


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
