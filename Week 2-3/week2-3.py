# %%
import pandas as pd
import altair as alt
import altair_saver
import numpy as np
from datetime import timedelta
alt.data_transformers.enable("json")
# %%
url = "https://raw.githubusercontent.com/byuidatascience/data4names/master/data-raw/names_year/names_year.csv"
names = pd.read_csv(url)
# %%
names.head()
names.year = pd.to_datetime(names.year, format='%Y')
names_agg = names.groupby('name')
names_agg.head()
my_name = names.query("name == 'Cameron'")
my_name.head()
# %%
cam_chart = (alt.Chart(my_name, title="I was Born at the Height of Popularity")
    .encode(
        alt.X('year(year):T', title = "Year"),
        alt.Y('Total:Q',title="Number of Names")
    )
    .mark_line().properties(width=600,height=350)
)

# %%
my_year = pd.DataFrame({
    'year' : [1999],
    'Total' : [my_name.query("year == 1999").Total.values[0]],
    'label' : ["Birth Year"]})
    
my_year.Total = my_year.Total.astype("int64",copy=True)
my_year.year = pd.to_datetime(my_year.year,format='%Y')

text_overlay = (alt.Chart(my_year).mark_text(align='right',dy=-10,baseline='middle')
    .encode
    (
        x = alt.X('year'),
        y = alt.Y('Total:Q'),
        text = 'label'
    )
)

my_point = (alt.Chart(my_year).mark_circle(color = 'red')
    .encode
    (
        x = alt.X('year'),
        y = alt.Y('Total:Q')
    )
)

cam_point = cam_chart  + text_overlay + my_point
# %%
cam_point
# %%
cam_point.save("Campoint.png")
# %%
# Brittany
brit = names.query("name == 'Brittany'")
brit_std = pd.DataFrame({
    'year' : [brit.year.median() + (brit.year.std()),brit.year.median() - (brit.year.std()),brit.year.median()],
    'color' : ['red','green','red'],
    'text' : ["Not Guess Range","Not Guess Range","Guess Range"],
    'y' : [15000] * 3
})



# %%
base = (alt.Chart(brit, title="The Name Brittany has Been Used From 1960's - 2015")
    .mark_area(color="#ff6961")
    .encode(
        x = alt.X('year', title="Year"),
        y = alt.Y('Total', title="Number of Names")
    )
    .properties(width=600,height=350)
)
# %%
area = (alt.Chart(brit.query("(year < @brit_std.year.values[0]) & (year > @brit_std.year.values[1])"))
    .mark_area(color='#77dd77')
    .encode(
        alt.X('year'),
        alt.Y('Total')
       )
    )

overlay = (alt.Chart(brit_std)
    .mark_text()
    .encode(
        x = 'year',
        y = 'y',
        text = 'text'
    )
)

brit_final = base + area + overlay
# %%

brit_final.save("brit_final.png")
brit_final
# %%
# Christian names

christ_names = names.query("name == 'Mary' | name == 'Martha' |name == 'Peter' |name == 'Paul'")
christ_names = christ_names.query("((year >= 1920) & (year <= 2000))")
# %%
names_chart = (alt.Chart(christ_names, title="Christian are Closley Tied to Wars?")
    .encode(
        alt.X('year:T', title = "Year"),
        alt.Y('Total:Q',title="Number of Names"),
        color = 'name'
    )
    .mark_line()).properties(width=600,height=350)
# %%
wars = pd.DataFrame({
    'name' : ['World War II','Cold War', 'Korean War','Vietnam War', 'Gulf War'],
    'start' :[pd.to_datetime("1939"),pd.to_datetime("1947"),pd.to_datetime("1950"),pd.to_datetime("1959"),pd.to_datetime("1990")],
    'end' : [pd.to_datetime("1945"), pd.to_datetime("1991"),pd.to_datetime("1953"), pd.to_datetime("1975"),pd.to_datetime("1991")],
    'color' : ['black','#CD0000','#0047A0','#FFCD00',"#007A3D"],
    'y' : [33000,50000,45000,38000,10000]
})

name_overlay =(alt.Chart(wars)
    .mark_text(align='left',dy = -10)
    .encode(
    text = 'name',
    x = 'start',
    y = 'y'
    )
)
names_chart= names_chart + name_overlay

# %%
for war in wars.itertuples():
    new_data = christ_names.query("((year >= @war.start) & (year <= @war.end) & (name == 'Mary'))")
    war_chart = (alt.Chart(new_data)
    .mark_area(fill = war.color, opacity=0.4)
    .encode(
        x = 'year',
        y = 'Total',
    ))
    names_chart = names_chart + war_chart
# %%
names_chart.save("christ_names.png")
names_chart
# %%
#Movie  Names

# Famous Movie