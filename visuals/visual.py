import marimo

__generated_with = "0.11.17"
app = marimo.App(width="medium", auto_download=["ipynb"])


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import os
    import requests
    from svg import SVG, Circle, Line, Title, Path
    return Circle, Line, Path, SVG, Title, mo, os, pd, requests


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
    station_dropdown = mo.ui.dropdown(
        options=stations_AV,
        value=stations_AV[0],
        label="Select a cage (station)"
    )
    return (
        pigs_AV,
        station_dropdown,
        stations_AV,
        url2_AV,
        url_AV,
        weight_dict_AV,
        weights_AV,
    )


@app.cell
def _(mo, pigs_AV, station_dropdown):
    selected_station_AV = int(station_dropdown.value)
    station_pigs_AV = pigs_AV[pigs_AV['station'] == selected_station_AV]
    pig_ids_AV = station_pigs_AV['Pig_1'].unique().tolist()

    # Convert pig IDs to strings to handle both numeric and string IDs
    pig_ids_AV = [str(pig_id) for pig_id in pig_ids_AV]
    pig_options_AV = ["All"] + pig_ids_AV


    # UI dropdown widget for pig selection
    pig_dropdown = mo.ui.dropdown(
        options=pig_options_AV,
        value="All",
        label="Select a pig to highlight its connections"
    )
    return (
        pig_dropdown,
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
def _(Line, Title, id_to_coord_AV, pig_dropdown, pigs_AV, station_pigs_AV):
    lines_AV = []

    selected_pig_AV = pig_dropdown.value

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
        """
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
def _(mo, pig_dropdown, plot_AV, station_dropdown):
    mo.hstack([mo.Html(plot_AV.as_str()), pig_dropdown, station_dropdown], justify= "start")
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
