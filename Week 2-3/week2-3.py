# %%
import pandas as pd
import altair as alt
import altair_saver
import numpy as np
alt.data_transformers.enable("json")
# %%
url = "https://raw.githubusercontent.com/byuidatascience/data4names/master/data-raw/names_year/names_year.csv"
names = pd.read_csv(url)
# %%
names.head()
names_agg = names.groupby('name')
names_agg.head()
my_name = names.query("name == 'Cameron'")
my_name.head()
# %%
cam_chart = (alt.Chart(my_name, title="I was Born at the Height of Popularity")
    .encode(
        alt.X('year:O', title = "Year"),
        alt.Y('Total:Q',title="Number of Names")
    )
    .mark_line()).properties(width=400,height=400)

# %%
my_year = pd.DataFrame({
    'year' : [1999],
    'Total' : [my_name.query("year == 1999").Total.values[0]],
    'label' : ["Birth Year"]})
    
my_year.Total = my_year.Total.astype("int64",copy=True)

text_overlay = (alt.Chart(my_year).mark_text(align='right',dy=-10,baseline='middle')
    .encode
    (
        x = alt.X('year:O'),
        y = alt.Y('Total:Q'),
        text = 'label'
    )
)

my_point = (alt.Chart(my_year).mark_circle(color = 'red')
    .encode
    (
        x = alt.X('year:O'),
        y = alt.Y('Total:Q')
    )
)

cam_point = cam_chart  + text_overlay + my_point
# %%
cam_point.save("Campoint.png")
# %%
