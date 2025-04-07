---
title: Visual
marimo-version: 0.11.17
width: medium
---

```python {.marimo}
import marimo as mo
import pandas as pd
import os
import random
import math
from svg import SVG, Circle, Line, Title, Path, Ellipse
```

```python {.marimo}
os.chdir("C:/Users/32493/Google Drive/ku leuven/data analysis/data visualization")
pigs = pd.read_excel("output.xlsx")
```

```python {.marimo}
pigs.info()
```

```python {.marimo}
# Get list of unique cages (stations)
stations = sorted(pigs['station'].unique().astype(str))

# UI dropdown widget
station_dropdown = mo.ui.dropdown(
    options=stations,
    value=stations[0],
    label="Select a cage (station)"
)
```

```python {.marimo}
selected_station = int(station_dropdown.value)
station_pigs = pigs[pigs['station'] == selected_station]
pig_ids = station_pigs['Pig_1'].unique().tolist()
```

```python {.marimo}
coordinates_circles = [
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
```

```python {.marimo}
id_to_coord = dict(zip(pig_ids, coordinates_circles))
```

```python {.marimo}
circles = [
    Circle(cx=x, cy=y, r=10, class_= "group1", elements=[Title(elements=[str(pig_id)])])
    for (x, y), pig_id in zip(coordinates_circles, pig_ids)
]
```

```python {.marimo}
lines = []

for _, row in pigs.iterrows():
    pig1 = row['Pig_1']
    pig2 = row['Pig_2']
    opacity = row['Count']**2 / 250000

    # Get coordinates
    if pig1 in id_to_coord and pig2 in id_to_coord:
        x1, y1 = id_to_coord[pig1]
        x2, y2 = id_to_coord[pig2]

        lines.append(
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
```

```python {.marimo}
self_counts = pigs[pigs['Pig_1'] == pigs['Pig_2']].set_index('Pig_1')['Count'].to_dict()

paths = []
for (x, y), pig_id, angle in zip(coordinates_circles, pig_ids, 
    [-0, -30, 30, 60, -60, 90, -90, 120, -120, 180, -180]):

    count = self_counts.get(pig_id, 0)
    _opacity = (count / 2000) if count else 0.0

    paths.append(
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
```

```python {.marimo}
all_elements = circles + paths + lines
all_elements.append(svg_content)
```

```python {.marimo}
plot = SVG(
    width=1000,
    height=1000,
    elements= all_elements
)
```

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

```python {.marimo}
station_dropdown
```

```python {.marimo}
mo.Html(plot.as_str())
```

```python {.marimo}
def pig_svg(x, y, pig_id):
    scale_factor = 1.3  # Increase this value to make the pig larger

    return f'''
    <g transform="translate({x},{y})" class="group1" id="circle-{pig_id}">
        <title>{pig_id}</title>
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

pig_svgs = []
for (_x, _y), _pig_id in zip(coordinates_circles, pig_ids):
    pig_svgs.append(pig_svg(_x, _y, _pig_id))


svg_content = '''
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
for (_x, _y), _pig_id in zip(coordinates_circles, pig_ids):
    svg_content += pig_svg(_x, _y, _pig_id)

svg_content += '''
</svg>
'''
```

```python {.marimo}

```