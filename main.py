import pandas as pd  # (versio0.24.2)
import dash, dash_table  # (version 1.0.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np

df = pd.read_csv("01 renewable-share-energy.csv")
df4 = pd.read_csv("04 share-electricity-renewables.csv")
df5 = pd.read_csv("05 hydropower-consumption.csv")
df6 = pd.read_csv("06 hydro-share-energy.csv")
df7 = pd.read_csv("07 share-electricity-hydro.csv")
df8 = pd.read_csv("08 wind-generation.csv")
df9 = pd.read_csv("09 cumulative-installed-wind-energy-capacity-gigawatts.csv")
df10 = pd.read_csv("10 wind-share-energy.csv")
df11 = pd.read_csv("11 share-electricity-wind.csv")
df12 = pd.read_csv("12 solar-energy-consumption.csv")
df13 = pd.read_csv("13 installed-solar-PV-capacity.csv")
df14 = pd.read_csv("14 solar-share-energy.csv")
df15 = pd.read_csv("15 share-electricity-solar.csv")
df16 = pd.read_csv("16 biofuel-production.csv")
df17 = pd.read_csv("17 installed-geothermal-capacity.csv")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
server = app.server

app.layout = dbc.Container([
    dbc.Row(
        [
            dbc.Col(html.H4("Global Renewable Energy Progress (1965-2022)", className="ml-2",
                            style={"font-family": "Times New Roman", "font-weight": "bold", 'color': '#3a3733',
                                   'marginTop': 20})),
            dbc.Col([
                dbc.Button(
                    "Code",
                    href="https://github.com/jatinmahour/US-urban-tree-analysis/blob/main/dashboard.py",
                    # download="my_data.txt",
                    external_link=True,
                    target="_blank",
                    color="dark",
                    style={"font-family": "Times New Roman", 'margin-left': '770px', 'margin-top': '10px',
                           "width": 60}
                )
            ]),
        ], style={'background-color': '#08F075 '}
    ),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.H5("Select Entity", className="ml-2",
                        style={"font-family": "Times New Roman", "font-weight": "bold",'color': '#3a3733', 'marginTop': 20, 'padding': 5,
                               'marginLeft': 10
                               }),
                dcc.Dropdown(id='select_entity', options=[
                    {'label': x, 'value': x} for x in sorted(df.Entity.unique())
                ],
                             optionHeight=35,  # height/space between dropdown options
                             value=('China', 'India', 'Japan', 'Germany', 'United States'),
                             # dropdown value selected automatically when page loads
                             disabled=False,  # disable dropdown value selection
                             multi=True,  # allow multiple dropdown values to be selected
                             searchable=True,  # allow user-searching of dropdown values
                             search_value='',  # remembers the value searched in dropdown
                             placeholder='Please select...',
                             # gray, default text shown when no option is selected
                             clearable=True,  # allow user to removes the selected value
                             style={'width': "100%"}
                             )
            ]),
            dbc.Row([
                html.H5('Choose Analytics',
                        style={"font-family": "Times New Roman","font-weight": "bold", 'color': '#3a3733', 'marginTop': 20, 'padding': 5,
                               'marginLeft': 10
                               }),
                dcc.Dropdown(id='options', options=[
                    {'label': 'Renewables (% equivalent primary energy)',
                     'value': 'Renewables (% equivalent primary energy)'},
                    {'label': 'Renewables (% electricity)',
                     'value': 'Renewables (% electricity)'},
                    {'label': 'Electricity from hydro (TWh)',
                     'value': 'Electricity from hydro (TWh)'},
                    {'label': 'Hydro (% equivalent primary energy)',
                     'value': 'Hydro (% equivalent primary energy)'},
                    {'label': 'Hydro (% electricity)',
                     'value': 'Hydro (% electricity)'},
                    {'label': 'Electricity from wind (TWh)',
                     'value': 'Electricity from wind (TWh)'},
                    {'label': 'Wind Energy Capacity (GW)',
                     'value': 'Wind Capacity'},
                    {'label': 'Wind (% equivalent primary energy)',
                     'value': 'Wind (% equivalent primary energy)'},
                    {'label': 'Wind (% electricity)',
                     'value': 'Wind (% electricity)'},
                    {'label': 'Electricity from solar (TWh)',
                     'value': 'Electricity from solar (TWh)'},
                    {'label': 'Solar Capacity',
                     'value': 'Solar Capacity'},
                    {'label': 'Solar (% equivalent primary energy)',
                     'value': 'Solar (% equivalent primary energy)'},
                    {'label': 'Solar (% electricity)',
                     'value': 'Solar (% electricity)'},
                    {'label': 'Biofuels Production - TWh - Total',
                     'value': 'Biofuels Production - TWh - Total'},
                    {'label': 'Geothermal Capacity',
                     'value': 'Geothermal Capacity'},
                ],
                             optionHeight=35,  # height/space between dropdown options
                             value='Renewables (% equivalent primary energy)',
                             # dropdown value selected automatically when page loads
                             disabled=False,  # disable dropdown value selection
                             multi=False,  # allow multiple dropdown values to be selected
                             searchable=True,  # allow user-searching of dropdown values
                             search_value='',  # remembers the value searched in dropdown
                             placeholder='Please select...',
                             # gray, default text shown when no option is selected
                             clearable=True,  # allow user to removes the selected value
                             style={'width': "100%"}
                             )
            ])
        ], md=4),
        dbc.Col([
            html.Div([
                dbc.Row(
                    html.H3(
                        "Renewable energy sources are growing quickly and will play a vital role in tackling climate change.",
                        className="ml-2",
                        style={"font-family": "Times New Roman", 'color': '#C51B1B', "font-weight": "bold",
                               'padding': 10,
                               'font-style': ' oblique',
                               'marginLeft': 30,
                               'marginTop': 20})
                ),
                dbc.Row(
                    html.H5(
                        "Renewable energy will play a key role in decarbonizing our energy systems in the coming decades."
                        " But how rapidly is our production of renewable energy changing? What technologies look most promising"
                        " in transforming our energy mix? "
                        "In this dashboard we look at the data on renewable energy technologies across the world, "
                        "the combination of hydropower, solar, wind, geothermal, and modern biofuels; what share of energy "
                        "they account for today, and how quickly this is changing.", className="mb-4",
                        style={"font-family": "Times New Roman", 'color': '#3a3733', "font-weight": "bold",
                               'marginLeft': 30})),
                html.H5(
                    "We have selected the top five global economies and compared their renewable energy"
                    " generation and consumption over the years. There are many entities to choose from including "
                    "high-income countries, upper middle-income countries, lower middle-income countries, OECD(BP) etc..", className="mb-4",
                    style={"font-family": "Times New Roman", 'color': '#3a3733',
                           "font-weight": "bold",
                           'marginLeft': 30})

            ])
        ], md=8)
    ]),
    html.Hr(),

    dbc.Row(html.Div([dcc.Graph(id="chart", figure={})])),
    dbc.Row(
        html.H6("Dashboard: By Jatin Mahaur")
    )
], fluid=True)


@app.callback(
    Output(component_id='chart', component_property='figure'),
    [Input(component_id='select_entity', component_property='value'),
     Input(component_id='options', component_property='value')]
)
def update_output(value_chosen, option_chosen):
    # ----------Renewables (% equivalent primary energy)----------#

    if option_chosen == 'Renewables (% equivalent primary energy)':
        if type(value_chosen) != str:
            dff = df[df["Entity"].isin(value_chosen)]
        else:
            dff = df[df["Entity"] == value_chosen]
        fig = px.line(dff, x="Year", y="Renewables (% equivalent primary energy)",
                      color='Entity', markers=True,color_discrete_sequence=px.colors.qualitative.G10,
                      width=1800, height=600)
        fig.update_layout(
            title='Share of primary energy consumption from renewable sources',
            title_font=dict(size=30,
                            color='#3a3733',
                            family='Times New Roman'),
            title_x=0.055,  # Title aligned with grid
            title_y=0.88,  # Title positioned near the top vertically
            plot_bgcolor='#F5F7FA',
            yaxis_ticksuffix = "%"
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='white'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.add_annotation(dict(font=dict(color='#3a3733', size=20, family='Times New Roman'),
                                x=0.01,
                                y=0.89,
                                showarrow=False,
                                text="Measured as a percentage of primary energy using the substitution method. "
                                     "Renewables include hydropower, solar, wind,"
                                     "geothermal and bio-fuels.",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))


    # ----------Renewables (% electricity)----------#

    elif option_chosen == 'Renewables (% electricity)':
        if type(value_chosen) != str:
            dff = df4[df4["Entity"].isin(value_chosen)]
        else:
            dff = df4[df4["Entity"] == value_chosen]
        fig = px.line(dff, x="Year", y=['Renewables (% electricity)'], color='Entity', markers=True,
                      color_discrete_sequence=px.colors.qualitative.G10,
                      width=1800, height=600)
        fig.update_layout(
            title='Share of electricity production from renewable sources',
            title_font=dict(size=30,
                            color='#3a3733',
                            family='Times New Roman'),
            title_x=0.055,  # Title aligned with grid
            title_y=0.88,  # Title positioned near the top vertically
            plot_bgcolor='#F5F7FA',
            yaxis_ticksuffix = "%"
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='white'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.add_annotation(dict(font=dict(color='#3a3733', size=20, family='Times New Roman'),
                                x=0.01,
                                y=0.89,
                                showarrow=False,
                                text="Renewables include hydropower, solar, wind,"
                                     "geothermal and bio-fuels.",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))



    # ----------Electricity from hydro (TWh)----------#

    elif option_chosen == 'Electricity from hydro (TWh)':
        if type(value_chosen) != str:
            dff = df5[df5["Entity"].isin(value_chosen)]
        else:
            dff = df5[df5["Entity"] == value_chosen]
        fig = px.line(dff, x="Year", y=['Electricity from hydro (TWh)'], color='Entity', markers=True,
                      color_discrete_sequence=px.colors.qualitative.G10,
                      width=1800, height=600)
        fig.update_layout(
            title='Hydropower generation',
            title_font=dict(size=30,
                            color='#3a3733',
                            family='Times New Roman'),
            title_x=0.073,  # Title aligned with grid
            title_y=0.88,  # Title positioned near the top vertically
            plot_bgcolor='#F5F7FA',
            yaxis_ticksuffix = " (TWh)"
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='white'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.add_annotation(dict(font=dict(color='#3a3733', size=20, family='Times New Roman'),
                                x=0.01,
                                y=0.89,
                                showarrow=False,
                                text="Annual hydropower generation is measured in terawatt-hours (TWh).",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

    # ----------Hydro (% equivalent primary energy)----------#

    elif option_chosen == 'Hydro (% equivalent primary energy)':
        if type(value_chosen) != str:
            dff = df6[df6["Entity"].isin(value_chosen)]
        else:
            dff = df6[df6["Entity"] == value_chosen]
        fig = px.line(dff, x="Year", y=['Hydro (% equivalent primary energy)'], color='Entity', markers=True,
                      color_discrete_sequence=px.colors.qualitative.G10,
                      width=1800, height=600)
        fig.update_layout(
            title='Share of primary energy consumption from hydroelectric power',
            title_font=dict(size=30,
                            color='#3a3733',
                            family='Times New Roman'),
            title_x=0.80,  # Title aligned with grid
            title_y=0.88,  # Title positioned near the top vertically
            plot_bgcolor='#F5F7FA',
            yaxis_ticksuffix="%"

        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='white'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.add_annotation(dict(font=dict(color='#3a3733', size=20, family='Times New Roman'),
                                x=0.38,
                                y=0.89,
                                showarrow=False,
                                text="Measured as a percentage of the total primary energy using the substitution method.",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

    # ----------Hydro (% electricity)----------#

    elif option_chosen == 'Hydro (% electricity)':
        if type(value_chosen) != str:
            dff = df7[df7["Entity"].isin(value_chosen)]
        else:
            dff = df7[df7["Entity"] == value_chosen]
        fig = px.line(dff, x="Year", y=['Hydro (% electricity)'], color='Entity', markers=True,
                      color_discrete_sequence=px.colors.qualitative.G10,
                      width=1800, height=600)
        fig.update_layout(
            title='Share of electricity production from hydropower',
            title_font=dict(size=30,
                            color='#3a3733',
                            family='Times New Roman'),
            title_x=0.15,  # Title aligned with grid
            title_y=0.88,  # Title positioned near the top vertically
            plot_bgcolor='#F5F7FA',
            yaxis_ticksuffix="%"
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='white'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.add_annotation(dict(font=dict(color='#3a3733', size=20, family='Times New Roman'),
                                x=0.12,
                                y=0.89,
                                showarrow=False,
                                text="Measured as a percentage of total electricity.",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

    # ----------Electricity from wind (TWh)----------#

    elif option_chosen == 'Electricity from wind (TWh)':
        if type(value_chosen) != str:
            dff = df8[df8["Entity"].isin(value_chosen)]
        else:
            dff = df8[df8["Entity"] == value_chosen]
        fig = px.line(dff, x="Year", y=['Electricity from wind (TWh)'], color='Entity', markers=True,
                      color_discrete_sequence=px.colors.qualitative.G10,
                      width=1800, height=600)
        fig.update_layout(
            title='Wind power generation',
            title_font=dict(size=30,
                            color='#3a3733',
                            family='Times New Roman'),
            title_x=0.07,  # Title aligned with grid
            title_y=0.88,  # Title positioned near the top vertically
            plot_bgcolor='#F5F7FA',
            yaxis_ticksuffix=" (TWh)"

        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='white'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.add_annotation(dict(font=dict(color='#3a3733', size=20, family='Times New Roman'),
                                x=0.01,
                                y=0.89,
                                showarrow=False,
                                text="Annual electricity generation from wind is measured in terawatt-hours (TWh) per year."
                                     " This includes both onshore and offshore wind sources.",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        # ----------Wind Energy Capacity (GW)----------#

    elif option_chosen == 'Wind Capacity':
        if type(value_chosen) != str:
            dff = df9[df9["Entity"].isin(value_chosen)]
        else:
            dff = df9[df9["Entity"] == value_chosen]
        fig = px.line(dff, x="Year", y=['Wind Capacity'], color='Entity', markers=True,
                      color_discrete_sequence=px.colors.qualitative.G10,
                      width=1800, height=600)
        fig.update_layout(
            title='Installed wind energy capacity',
            title_font=dict(size=30,
                            color='#3a3733',
                            family='Times New Roman'),
            title_x=0.07,  # Title aligned with grid
            title_y=0.88,  # Title positioned near the top vertically
            plot_bgcolor='#F5F7FA',
            yaxis_ticksuffix=" (GW)"
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='white'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.add_annotation(dict(font=dict(color='#3a3733', size=20, family='Times New Roman'),
                                x=0.01,
                                y=0.89,
                                showarrow=False,
                                text="Cumulative installed wind energy capacity including both onshore and offshore "
                                     "wind sources, measured in gigawatts (GW).",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        # ----------Wind (% equivalent primary energy)----------#

    elif option_chosen == 'Wind (% equivalent primary energy)':
        if type(value_chosen) != str:
            dff = df10[df10["Entity"].isin(value_chosen)]
        else:
            dff = df10[df10["Entity"] == value_chosen]
        fig = px.line(dff, x="Year", y=['Wind (% equivalent primary energy)'], color='Entity', markers=True,
                      color_discrete_sequence=px.colors.qualitative.G10,
                      width=1800, height=600)
        fig.update_layout(
            title='Share of primary energy consumption from wind',
            title_font=dict(size=30,
                            color='#3a3733',
                            family='Times New Roman'),
            title_x=0.055,  # Title aligned with grid
            title_y=0.88,  # Title positioned near the top vertically
            plot_bgcolor='#F5F7FA',
            yaxis_ticksuffix="%"
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='white'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.add_annotation(dict(font=dict(color='#3a3733', size=20, family='Times New Roman'),
                                x=0.01,
                                y=0.89,
                                showarrow=False,
                                text="Measured as a percentage of primary energy using the substitution method.",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

    # ----------Wind (% electricity)----------#

    elif option_chosen == 'Wind (% electricity)':
        if type(value_chosen) != str:
            dff = df11[df11["Entity"].isin(value_chosen)]
        else:
            dff = df11[df11["Entity"] == value_chosen]
        fig = px.line(dff, x="Year", y=['Wind (% electricity)'], color='Entity', markers=True,
                      color_discrete_sequence=px.colors.qualitative.G10,
                      width=1800, height=600)
        fig.update_layout(
            title='Share of electricity production from wind',
            title_font=dict(size=30,
                            color='#3a3733',
                            family='Times New Roman'),
            title_x=0.055,  # Title aligned with grid
            title_y=0.88,  # Title positioned near the top vertically
            plot_bgcolor='#F5F7FA',
            yaxis_ticksuffix="%"
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='white'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.add_annotation(dict(font=dict(color='#3a3733', size=20, family='Times New Roman'),
                                x=0.01,
                                y=0.89,
                                showarrow=False,
                                text="Measured as a percentage of total electricity.",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

    # ----------Electricity from solar (TWh)----------#

    elif option_chosen == 'Electricity from solar (TWh)':
        if type(value_chosen) != str:
            dff = df12[df12["Entity"].isin(value_chosen)]
        else:
            dff = df12[df12["Entity"] == value_chosen]
        fig = px.line(dff, x="Year", y=['Electricity from solar (TWh)'], color='Entity', markers=True,
                      color_discrete_sequence=px.colors.qualitative.G10,
                      width=1800, height=600)
        fig.update_layout(
            title='Solar power generation',
            title_font=dict(size=30,
                            color='#3a3733',
                            family='Times New Roman'),
            title_x=0.07,  # Title aligned with grid
            title_y=0.88,  # Title positioned near the top vertically
            plot_bgcolor='#F5F7FA',
            yaxis_ticksuffix=" (TWh)"
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='white'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.add_annotation(dict(font=dict(color='#3a3733', size=20, family='Times New Roman'),
                                x=0.01,
                                y=0.89,
                                showarrow=False,
                                text="Electricity generation from solar, measured in terawatt-hours (TWh) per year.",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

    # ----------Solar Capacity----------#

    elif option_chosen == 'Solar Capacity':
        if type(value_chosen) != str:
            dff = df13[df13["Entity"].isin(value_chosen)]
        else:
            dff = df13[df13["Entity"] == value_chosen]
        fig = px.line(dff, x="Year", y=['Solar Capacity'], color='Entity', markers=True,
                      color_discrete_sequence=px.colors.qualitative.G10,
                      width=1800, height=600, )
        fig.update_layout(
            title='Installed solar energy capacity',
            title_font=dict(size=30,
                            color='#3a3733',
                            family='Times New Roman'),
            title_x=0.07,  # Title aligned with grid
            title_y=0.88,  # Title positioned near the top vertically
            plot_bgcolor='#F5F7FA',
            yaxis_ticksuffix=" (GW)"
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='white'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.add_annotation(dict(font=dict(color='#3a3733', size=20, family='Times New Roman'),
                                x=0.01,
                                y=0.89,
                                showarrow=False,
                                text="Cumulative installed solar capacity, measured in gigawatts (GW).",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

    # ----------Solar (% equivalent primary energy)----------#

    elif option_chosen == 'Solar (% equivalent primary energy)':
        if type(value_chosen) != str:
            dff = df14[df14["Entity"].isin(value_chosen)]
        else:
            dff = df14[df14["Entity"] == value_chosen]
        fig = px.line(dff, x="Year", y=['Solar (% equivalent primary energy)'], color='Entity', markers=True,
                      color_discrete_sequence=px.colors.qualitative.G10,
                      width=1800, height=600)
        fig.update_layout(
            title='Share of primary energy consumption from solar',
            title_font=dict(size=30,
                            color='#3a3733',
                            family='Times New Roman'),
            title_x=0.055,  # Title aligned with grid
            title_y=0.88,  # Title positioned near the top vertically
            plot_bgcolor='#F5F7FA',
            yaxis_ticksuffix="%"
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='white'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.add_annotation(dict(font=dict(color='#3a3733', size=20, family='Times New Roman'),
                                x=0.01,
                                y=0.89,
                                showarrow=False,
                                text="Measured as a percentage of primary energy, using the substitution method.",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

    # ----------Solar (% electricity)----------#

    elif option_chosen == 'Solar (% electricity)':
        if type(value_chosen) != str:
            dff = df15[df15["Entity"].isin(value_chosen)]
        else:
            dff = df15[df15["Entity"] == value_chosen]
        fig = px.line(dff, x="Year", y=['Solar (% electricity)'], color='Entity', markers=True,
                      color_discrete_sequence=px.colors.qualitative.G10,
                      width=1800, height=600)
        fig.update_layout(
            title='Share of electricity production from solar',
            title_font=dict(size=30,
                            color='#3a3733',
                            family='Times New Roman'),
            title_x=0.055,  # Title aligned with grid
            title_y=0.88,  # Title positioned near the top vertically
            plot_bgcolor='#F5F7FA',
            yaxis_ticksuffix="%"
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='white'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.add_annotation(dict(font=dict(color='#3a3733', size=20, family='Times New Roman'),
                                x=0.01,
                                y=0.89,
                                showarrow=False,
                                text="Measured as a percentage of total electricity.",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

    # ----------Biofuels Production - TWh - Total----------#

    elif option_chosen == 'Biofuels Production - TWh - Total':
        if type(value_chosen) != str:
            dff = df16[df16["Entity"].isin(value_chosen)]
        else:
            dff = df16[df16["Entity"] == value_chosen]
        fig = px.line(dff, x="Year", y=['Biofuels Production - TWh - Total'], color='Entity', markers=True,
                      color_discrete_sequence=px.colors.qualitative.G10,
                      width=1800, height=600)
        fig.update_layout(
            title='Biofuel energy production',
            title_font=dict(size=30,
                            color='#3a3733',
                            family='Times New Roman'),
            title_x=0.07,  # Title aligned with grid
            title_y=0.88,  # Title positioned near the top vertically
            plot_bgcolor='#F5F7FA',
            yaxis_ticksuffix = " (TWh)"
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='white'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.add_annotation(dict(font=dict(color='#3a3733', size=20, family='Times New Roman'),
                                x=0.01,
                                y=0.89,
                                showarrow=False,
                                text="Total biofuel production is measured in terawatt-hours (TWh) per year. "
                                     "Biofuel production includes both bioethanol and biodiesel.",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

    # ----------Geothermal Capacity----------#

    elif option_chosen == 'Geothermal Capacity':
        if type(value_chosen) != str:
            dff = df17[df17["Entity"].isin(value_chosen)]
        else:
            dff = df17[df17["Entity"] == value_chosen]
        fig = px.line(dff, x="Year", y=['Geothermal Capacity'], color='Entity', markers=True,
                      color_discrete_sequence=px.colors.qualitative.G10,
                      width=1800, height=600)
        fig.update_layout(
            title='Installed geothermal energy capacity',
            title_font=dict(size=30,
                            color='#3a3733',
                            family='Times New Roman'),
            title_x=0.51,  # Title aligned with grid
            title_y=0.88,  # Title positioned near the top vertically
            plot_bgcolor='#F5F7FA',
            yaxis_ticksuffix=" (MW)"
        )
        fig.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='white'
        )
        fig.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        fig.add_annotation(dict(font=dict(color='#3a3733', size=20, family='Times New Roman'),
                                x=0.38,
                                y=0.89,
                                showarrow=False,
                                text="Cumulative installed capacity of geothermal energy, measured in megawatts.",
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
