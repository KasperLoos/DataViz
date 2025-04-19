import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(
        r"""
        <style>
            svg.notebook {
                border: 1px solid;
            }
            path:hover {
                stroke: olive;
                stroke-width: 5;
                fill-opacity: 1;
            }
        </style>
        """
    )
    return


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from svg import SVG, Circle, Line, Text, Rect, Polygon, Path, Title
    #Creation of dropdowns because accessing the value of a dropdown should be in a seperate cell from the one in which it's created

    dropdown_station = mo.ui.dropdown(options=["All", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], value="All", label="Choose station")
    return (
        Circle,
        Line,
        Path,
        Polygon,
        Rect,
        SVG,
        Text,
        Title,
        dropdown_station,
        mo,
        pd,
    )


@app.cell
def _(Line, Path, SVG, Text, Title, dropdown_pig, dropdown_station, mo, pd):
    _df = pd.read_excel(r"C:\Users\kian3\Datavis\Project\Data\Oneperpig_socio_corrected_weight_increase.xlsx")

    _max_normalized=0.3502105263157895
    _min_normalized=0.0025301204819277107

    _svg_width = 1000
    _svg_height = 800

    def _rescale(x, domain_min, domain_max, range_min, range_max):
        scale = (range_max - range_min) / (domain_max - domain_min)
        return range_min + (x - domain_min) * scale

    def _scaleX(x):
        return int(_rescale(x, 0, 23, 60, _svg_width-50))

    def _scaleY(y):
        return int(_rescale(y,_min_normalized , _max_normalized , _svg_height-50, 50))

    _normalized_hourly_intake_positions = {
            "0": 750,
            "0.05": 650,
            "0.10": 550,
            "0.15": 450,
            "0.20": 350,
            "0.25": 250,
            "0.30": 150,
            "0.35": 50,
            }
    def _getY(normalized_hourly_intake):
        return _normalized_hourly_intake_positions[normalized_hourly_intake]

    _normalized_hourly_intake_values = []
    for _d in _normalized_hourly_intake_positions:
        _y = _getY(_d)
        _normalized_hourly_intake_values.append(Text(x=20, y=_y, elements=[_d], class_="fhds6"))

    _hour_positions = {
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

    #Aparte cellen aanmaak dropdowns

    if dropdown_station.value == "All" and dropdown_pig.value == None:
        _subset_station_pig = _df
    elif dropdown_station.value == "All" and dropdown_pig.value != None:
        _subset_station_pig = _df[_df["pig"] == dropdown_pig.value]
    elif dropdown_station.value != "All" and dropdown_pig.value == None:
        _subset_station_pig = _df[(_df["station"] == dropdown_station.value)]
    else: 
        _subset_station_pig = _df[_df["pig"] == dropdown_pig.value]

    _polylines = []

    for _pig_index, _pig_row in _subset_station_pig.iterrows():
        _path_commands = []

        if _pig_row['gender'] == 'gilt': 
            _polyline_color = "deeppink"
        else:
            _polyline_color = "dodgerblue"
        # De eerste geldige waarde vinden
        for _hour in range(24):
            if pd.notna(_pig_row[_hour]):  
                _hour_x = _hour_positions[str(_hour)] + 3
                _hour_y = _scaleY(_pig_row[_hour])
                _path_commands.append(f"M {_hour_x} {_hour_y}")  # Begin een nieuw pad
                break  # Stop zodra eerste geldige punt gevonden is

        # Verbind de volgende waarden
        for _hour in range(24):
            if pd.notna(_pig_row[_hour]):  
                _hour_x = _hour_positions[str(_hour)] + 3
                _hour_y = _scaleY(_pig_row[_hour])
                _path_commands.append(f"L {_hour_x} {_hour_y}")  # Verbind met vorige punt

        _polyline_path = " ".join(_path_commands)

        _polylines.append(Path(d=_polyline_path, stroke=_polyline_color, fill="none", stroke_width=1, class_="notebook", elements=[Title(elements=[f"Pignumber: {_pig_row['pig']}, station: {_pig_row['station']}, gender: {_pig_row['gender']}, weight increase: {_pig_row['Weight_increase']}"])]))

    def _getx(hour):
        return _hour_positions[hour]

    _hour_values = []
    for _e in _hour_positions:
        _x = _getx(_e)
        _hour_values.append(Text(x=_x, y=770, elements=[_e], class_="f526"))

    _hor_line = Line(x1=50, y1=750, x2=960, y2=750, stroke="black", stroke_width=2)
    _ver_line = Line(x1=50, y1=750, x2=50, y2=40, stroke="black", stroke_width=2)

    _hour_text = Text(x=456.865, y=790, elements=["Time indication: hour"])
    _intake_text = Text(x=10, y=500, elements=["Average intake in kg"], transform="rotate(270, 10, 500)")

    _svg = SVG(
        width=_svg_width,
        height=_svg_height,
        elements= _normalized_hourly_intake_values + _hour_values + _polylines + [_hor_line, _ver_line, _hour_text, _intake_text],
        class_="notebook"
    )

    mo.hstack([mo.Html(_svg.as_str()), dropdown_station, dropdown_pig], justify="start")
    return


@app.cell
def _(dropdown_station, mo, pd):
    _df = pd.read_excel(r"C:\Users\kian3\Datavis\Project\Data\Oneperpig_socio_corrected_weight_increase.xlsx")

    if dropdown_station.value == "All":
        subset_dropdown_station = _df
    else:
        subset_dropdown_station = _df[(_df["station"] == dropdown_station.value)]    
    pig_options = subset_dropdown_station["pig"].unique()
    dropdown_pig = mo.ui.dropdown(options = pig_options, label = "Choose pig")
    return dropdown_pig, pig_options, subset_dropdown_station


if __name__ == "__main__":
    app.run()
