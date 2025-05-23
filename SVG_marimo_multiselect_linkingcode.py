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
    #Start linking part
    return


@app.cell
def _():
    #cssKP = """
    #svg.notebook {
    #    border: 1px solid;
    #}
    #path.brushed:hover {
    #    stroke: olive;
    #    stroke-width: 5;
    #}
    #""" 

    return


app._unparsable_cell(
    r"""
    brushable_KP = BrushableWidget(svg=svgKP.as_str(), _css=cssKP, selected_ids = get_selected())
    brushable_... = BrushableWidget(svg=svg....as_str(), _css=css..., selected_ids = get_selected())
    brushable_... = BrushableWidget(svg=svg....as_str(), _css=css..., selected_ids = get_selected())

    mo_brushable_KP = mo.ui.anywidget(brushable_KP)
    mo_brushable_... = mo.ui.anywidget(brushable_...)
    mo_brushable_... = mo.ui.anywidget(brushable_...)

    traitlets.link((brushable_KP, \"selected_ids\"),(brushable_.., \"selected_ids\"), (brushable_.., \"selected_ids\"))

    mo.hstack([
        # Linkerkant: SVG's onder elkaar
        mo.vstack([
            mo.Html(brushable_KP),  # Eerste SVG
            mo.Html(brushable_...),
            mo.Html(brushable_...)], justify=\"start\"),
    
        # Rechterkant: multiselects and dropdown
        mo.vstack([
            multiselect_station,
            multiselect_pig,
            dropdown_gender], justify=\"start\")
    ], justify=\"between\", align=\"start\")

    traitlets.link((brushable_KP, \"selected_ids\"),(brushable_.., \"selected_ids\"), (brushable_.., \"selected_ids\"))
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    mo_brushable_KP.widget.selected_ids
    mo_brushable_....widget.selected_ids
    mo_brushable_....widget.selected_ids
    mo.ui.text_area(\"Selected IDs: \" + str(mo_brushable_....widget.selected_ids))
    #End linking part
    """,
    name="_"
)


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import anywidget, traitlets
    from brushable_widget import BrushableWidget
    from svg import SVG, Circle, Line, Text, Rect, Polygon, Path, Title
    #Creation of dropdowns because accessing the value of a dropdown should be in a seperate cell from the one in which it's created

    # dropdown_station = mo.ui.dropdown(options=["All", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], value="All", label="Choose station")
    return (
        BrushableWidget,
        Circle,
        Line,
        Path,
        Polygon,
        Rect,
        SVG,
        Text,
        Title,
        anywidget,
        mo,
        pd,
        traitlets,
    )


@app.cell
def _(mo):
    _options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    multiselect_station = mo.ui.multiselect(options=_options , label="Choose station(s)")
    return (multiselect_station,)


@app.cell
def _(pd):
    df = pd.read_excel(r"C:\Users\kian3\Datavis\Project\Data\Processed_KP.xlsx")

    #if dropdown_station.value == "All":
        #subset_dropdown_station = _df
    #else:
        #subset_dropdown_station = _df[(_df["station"] == dropdown_station.value)]    
    #pig_options = subset_dropdown_station["pig"].unique()
    #dropdown_pig = mo.ui.dropdown(options = pig_options, label = "Choose pig")
    return (df,)


@app.cell
def _(mo, multiselect_station, pd):
    _df = pd.read_excel(r"C:\Users\kian3\Datavis\Project\Data\Processed_KP.xlsx")

    if multiselect_station.value == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] :
        subset_dropdown_station = _df
    else:
        subset_dropdown_station = _df[_df["station"].isin(multiselect_station.value)]
    multiselect_pig_options = subset_dropdown_station["pig"].unique()
    multiselect_pig = mo.ui.multiselect(options = multiselect_pig_options, label = "Choose pig(s)")
    return multiselect_pig, multiselect_pig_options, subset_dropdown_station


@app.cell
def _():
    #if dropdown_station.value == "All" and dropdown_pig.value == None:
        #_gender_options = ["gilt", "barrow"]
    #else:
        #_gender_options = []
    #dropdown_gender = mo.ui.dropdown(options = _gender_options, label = "Choose gender")
    return


@app.cell
def _(mo, multiselect_pig, multiselect_station, pd):
    _df = pd.read_excel(r"C:\Users\kian3\Datavis\Project\Data\Processed_KP.xlsx")
    if len(multiselect_station.value) > 1 and len(multiselect_pig.value) > 1:
        _gender_options = ["gilt", "barrow"]
    else:
        _gender_options = []
    dropdown_gender = mo.ui.dropdown(options = _gender_options, label = "Choose gender")
    return (dropdown_gender,)


@app.cell
def _(
    Line,
    Path,
    SVG,
    Text,
    Title,
    dropdown_gender,
    mo,
    multiselect_pig,
    multiselect_station,
    pd,
):
    _df = pd.read_excel(r"C:\Users\kian3\Datavis\Project\Data\Processed_KP.xlsx")

    _max_normalized= 0.3502105263157895
    _min_normalized= 0.0025301204819277107

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

    #Dropdowns station and pig has been created in two seperate cells above

    if len(multiselect_station.value) > 0 and multiselect_pig.value is not None and dropdown_gender.value is None:
        _subset_station_pig = _df[_df["pig"].isin(multiselect_pig.value)]
    elif len(multiselect_station.value) > 0 and multiselect_pig.value is not None and dropdown_gender.value is not None:
        _subset_station_pig = _df[(_df["pig"].isin(multiselect_pig.value)) & (_df["gender"] == dropdown_gender.value)]
    else: 
        _subset_station_pig = _df

    _polylines = []

    for _pig_index, _pig_row in _subset_station_pig.iterrows():
        _path_commands = []

        if _pig_row['gender'] == 'gilt': 
            _polyline_color = "deeppink"
        else:
            _polyline_color = "dodgerblue"

        for _hour in range(24):
            if pd.notna(_pig_row[_hour]):  
                _hour_x = _hour_positions[str(_hour)] + 3
                _hour_y = _scaleY(_pig_row[_hour])
                _path_commands.append(f"M {_hour_x} {_hour_y}")  
                break  

        for _hour in range(24):
            if pd.notna(_pig_row[_hour]):  
                _hour_x = _hour_positions[str(_hour)] + 3
                _hour_y = _scaleY(_pig_row[_hour])
                _path_commands.append(f"L {_hour_x} {_hour_y}")  

        _polyline_path = " ".join(_path_commands)

        _polylines.append(Path(d=_polyline_path, stroke=_polyline_color, fill="none", stroke_width=1, class_="notebook brushable", id = _pig_row['pig'], elements=[Title(elements=[f"Pigname: {_pig_row['pig']}, station: {_pig_row['station']}, gender: {_pig_row['gender']}, weight increase: {_pig_row['Weight_increase']}"])]))

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

    svgKP = SVG(
        width=_svg_width,
        height=_svg_height,
        elements= _normalized_hourly_intake_values + _hour_values + _polylines + [_hor_line, _ver_line, _hour_text, _intake_text],
        class_="notebook"
    )

    mo.hstack([mo.Html(svgKP.as_str()), multiselect_station, multiselect_pig, dropdown_gender], justify="start")
    return (svgKP,)


@app.cell
def _():
    print(id)
    return


if __name__ == "__main__":
    app.run()
