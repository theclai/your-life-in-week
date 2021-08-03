# import libraries
import pandas as pd
import math
from datetime import date
import altair as alt

# create useful constants
c_label_lived = "lived weeks"
c_label_remaining = "remaining weeks"
c_label_current = "this week"

c_width = 1080 / 2.2
c_height = 1500 / 2.2

life_exp = 63
birth_year = 1981
birth_month = 10
birth_day = 2
current_date = date.today()
day_of_birth = date(year=birth_year, month=birth_month, day=birth_day)
day_of_death = date(year=birth_year + life_exp, month=birth_month, day=birth_day)

lived_life = current_date - day_of_birth
rest_of_life = day_of_death - current_date

lived_life_years = (lived_life.days / 365.25)
lived_life_years_floor = math.floor(lived_life_years)

lived_life_weeks = (lived_life_years - lived_life_years_floor) * 365.25 / 7
lived_life_weeks_floor = math.floor(lived_life_weeks)

rest_of_life_years = (rest_of_life.days / 365.25)
rest_of_life_years_floor = math.floor(rest_of_life_years)

df_ll_weeks = pd.DataFrame(columns=['week', 'year', 'label'])

for week in range(lived_life_weeks_floor):
    df_ll_weeks = df_ll_weeks.append(pd.DataFrame({
        'week': [week],
        'year': [lived_life_years_floor],
        'label': [c_label_lived]
    }))

df_ll_weeks = df_ll_weeks.append(pd.DataFrame({
    'week': [lived_life_weeks_floor],
    'year': [lived_life_years_floor],
    'label': [c_label_current]
}))

for week in range(lived_life_weeks_floor + 1, 52):
    df_ll_weeks = df_ll_weeks.append(pd.DataFrame({
        'week': [week],
        'year': [lived_life_years_floor],
        'label': [c_label_remaining]
    }))

df_ll = pd.DataFrame(columns=['week', 'year', 'label'])

for year in range(0, lived_life_years_floor + 0):
    for week in range(52):
        df_ll = df_ll.append(pd.DataFrame({
            'week': [week],
            'year': [year],
            'label': [c_label_lived]
        }))

df_rl = pd.DataFrame(columns=['week', 'year', 'label'])

for year in range(lived_life_years_floor + 1, lived_life_years_floor + rest_of_life_years_floor + 1):
    for week in range(52):
        df_rl = df_rl.append(pd.DataFrame({
            'week': [week],
            'year': [year],
            'label': [c_label_remaining]
        }))

chart = (
    alt.Chart(pd.concat([df_ll, df_rl, df_ll_weeks]))
        .mark_square(
        color="black",
        size=100 / 2
    ).encode(
        x=alt.X("week", axis=None),
        y=alt.Y("year", axis=None),
        # color = alt.Color("label", legend = alt.Legend(orient = "bottom"), title = ""),
        # shape=alt.ShapeValue(person)
    ).properties(
        width=c_width,
        height=c_height
    ).properties(
        title="Your Life in Weeks"
    )
)

chart = chart + (
    alt.Chart(pd.concat([df_ll, df_rl, df_ll_weeks]))
        .mark_square(
        filled=True,
        opacity=1,
        # color = "black",
        size=60 / 2
    ).encode(
        x=alt.X("week", axis=None),
        y=alt.Y("year", axis=None),
        color=alt.Color(
            "label", scale=alt.Scale(range=["black", "white", "red"]),
            legend=alt.Legend(orient="bottom"), title=""
        )
    ).properties(
        width=c_width,
        height=c_height
    ).properties(
        title="Your Life in Weeks"
    )
)

chart_config = (
    chart
        .configure_title(
        fontSize=40,
        font="Staatliches",
        align="center",
        color="black",
        baseline="bottom",
        dy=40
    ).configure_view(
        strokeWidth=0
    )
)

chart_config.save("output.html")