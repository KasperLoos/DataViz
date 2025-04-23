import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
        # Visual of the feeding patterns of the pigs
        This visual tries to give you both a general overview of pigs' daily feeding patterns on an hourly basis and to give you the opportunity to inspect deviating feeding patterns of some pigs. One line corresponds to one pigs' average daily feeding pattern across the whole study. When hovering over a line, you can easily follow the feeding pattern of the pig of interest. It also provides you with a tooltip with information about its gender, station, body weight increase over the study and his name. A rose line corresponds to a gilt (female pig) and a blue line to a barrow (male pig). Next to the figure you have the opportunity to select station(s), pig(s), gender(s) of interest.  
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import requests
    from svg import SVG, Line, Text, Path, Title
    return Line, Path, SVG, Text, Title, mo, pd, requests


@app.cell
def _(mo):
    mo.md(
        r"""
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

        polylinesKP.append(Path(d=polyline_pathKP, stroke=polyline_colorKP, fill="none", stroke_width=1, class_="notebook brushable", id = pig_rowKP['pig'], elements=[Title(elements=[f"Pigname: {pig_rowKP['pig']}, station: {pig_rowKP['station']}, gender: {pig_rowKP['gender']}, weight increase: {pig_rowKP['Weight_increase']}"])]))

    # Creation of the svg

    svgKP = SVG(
        width=svg_widthKP,
        height=svg_heightKP,
        elements= normalized_hourly_intake_valuesKP + hour_valuesKP + polylinesKP + [hor_lineKP, ver_lineKP, hour_textKP, intake_textKP],
        class_="notebook"
    )

    # Outputting svg, multiselects and dropdown
    mo.hstack([mo.Html(svgKP.as_str()), mo.vstack([multiselect_stationKP, multiselect_pigKP, dropdown_genderKP], justify="start")], justify="start")
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
        rescaleKP,
        scaleXKP,
        scaleYKP,
        subset_station_pigKP,
        svgKP,
        svg_heightKP,
        svg_widthKP,
        ver_lineKP,
        xKP,
        yKP,
    )


if __name__ == "__main__":
    app.run()
