import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
# from homelessness_national_prep_work import abbrev_to_state_dict, state_to_abbrev_dict
import dash_bootstrap_components as dbc

# Uncomment to display entire dataframe for troubleshooting purposes
# pd.set_option("display.max_rows", None, "display.max_columns", None)

abbrev_to_state_dict = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona', 'CA': 'California',
                        'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida',
                        'GA': 'Georgia', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois',
                        'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
                        'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan',
                        'MN': 'Minnesota', 'MO': 'Missouri', 'MS': 'Mississippi', 'MT': 'Montana',
                        'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire',
                        'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio',
                        'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
                        'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
                        'UT': 'Utah', 'VA': 'Virginia', 'VI': 'Virgin Islands', 'VT': 'Vermont',
                        'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming', 'Total': 'Total'}

state_to_abbrev_dict = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
                        "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL",
                        "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN",
                        "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME",
                        "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
                        "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
                        "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
                        "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
                        "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
                        "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
                        "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
                        "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "Total": "Total"}




app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])  # ['bootstrap.min.css'])
app.title = "CTP-Homelessness"

relevant_data_qa_table = pd.read_csv('data/national_homeless_cleaned_up_data.csv')
relevant_data_qa_table.set_index('State', inplace=True)
master_df_national = pd.read_csv('data/master_df_national.csv')
master_df_national.set_index('State', inplace=True)
demo_data = pd.read_csv('data/national_homeless_cleaned_up_data_for_demographics.csv')

server = app.server

def create_pie_chart_gender(selected_year_state, state):
    genders = \
        demo_data[
            (demo_data['Year'] == int(selected_year_state)) & (demo_data['State'] == state_to_abbrev_dict[state])][
            ['State', 'Overall Homeless - Female',
             'Overall Homeless - Male',
             'Overall Homeless - Transgender', 'Overall Homeless - Gender Non-Conforming'
             ]].copy()

    genders.rename(columns=lambda x: x[19:] if x not in ['State'] else x, inplace=True)
    genders.rename(columns={'State': 'Category'}, inplace=True)
    genders = genders.set_index('Category').transpose()
    genders.rename(columns={state_to_abbrev_dict[state]: 'Number'}, inplace=True)
    genders.index.rename("Gender", inplace=True)
    fig = px.pie(genders, values='Number', names=genders.index, title='<b>By Gender   </b>')
    fig.update_layout(margin_autoexpand=False)
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.75
    ), margin_l=100)
    return fig


def create_pie_chart_age(selected_year, state):
    age_groups = \
        demo_data[(demo_data['Year'] == int(selected_year)) & (demo_data['State'] == state_to_abbrev_dict[state])][
            ['State',
             'Overall Homeless - Age 18 to 24',
             'Overall Homeless - Over 24',
             'Overall Homeless - Under 18'
             ]].copy()

    age_groups.rename(columns=lambda x: x[19:] if x not in ['State'] else x, inplace=True)
    age_groups.rename(columns={'State': 'Category'}, inplace=True)
    age_groups = age_groups.set_index('Category').transpose()
    age_groups.rename(columns={state_to_abbrev_dict[state]: 'Number'}, inplace=True)
    age_groups.index.rename("Age group", inplace=True)
    fig = px.pie(age_groups, values='Number', names=age_groups.index, title='<b>By Age Group</b>',
                 color_discrete_sequence=px.colors.sequential.Turbo)
    fig.update_layout(margin_autoexpand=False)
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.75
    ), margin_l=100)
    return fig


def create_pie_chart_ethnicity(selected_year, state):
    ethnicities = \
        demo_data[(demo_data['Year'] == int(selected_year)) & (demo_data['State'] == state_to_abbrev_dict[state])][
            ['State',
             'Overall Homeless - Non-Hispanic/Non-Latino',
             'Overall Homeless - Hispanic/Latino'
             ]].copy()

    ethnicities.rename(columns=lambda x: x[19:] if x not in ['State'] else x, inplace=True)
    ethnicities.rename(columns={'State': 'Category'}, inplace=True)
    ethnicities = ethnicities.set_index('Category').transpose()
    ethnicities.rename(columns={state_to_abbrev_dict[state]: 'Number'}, inplace=True)
    ethnicities.index.rename("Ethnicity", inplace=True)
    fig = px.pie(ethnicities, values='Number', names=ethnicities.index, title='<b>By Ethnicity</b>',
                 color_discrete_sequence=px.colors.sequential.dense)
    fig.update_layout(margin_autoexpand=False)
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.75
    ), margin_l=100)
    return fig


def create_pie_chart_race(selected_year, state):
    races = demo_data[(demo_data['Year'] == int(selected_year)) & (demo_data['State'] == state_to_abbrev_dict[state])][
        ['State',
         'Overall Homeless - White',
         'Overall Homeless - Black or African American',
         'Overall Homeless - Asian',
         'Overall Homeless - American Indian or Alaska Native',
         'Overall Homeless - Native Hawaiian or Other Pacific Islander',
         'Overall Homeless - Multiple Races'
         ]].copy()

    races.rename(columns=lambda x: x[19:] if x not in ['State'] else x, inplace=True)
    races.rename(columns={'State': 'Category'}, inplace=True)
    races = races.set_index('Category').transpose()
    races.rename(columns={state_to_abbrev_dict[state]: 'Number'}, inplace=True)
    races.index.rename("Race", inplace=True)
    fig = px.pie(races, values='Number', names=races.index, title='<b>By Race</b>',
                 color_discrete_sequence=px.colors.sequential.Purpor)
    fig.update_layout(margin_autoexpand=False)
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.75
    ), margin_l=100)

    return fig


def create_pie_chart_sheltered(selected_year, state):
    locations = \
        demo_data[(demo_data['Year'] == int(selected_year)) & (demo_data['State'] == state_to_abbrev_dict[state])][
            ['State',
             'Sheltered ES Homeless',
             'Overall Homeless',
             ]].copy()

    locations.rename(columns={'State': 'Category', 'Sheltered ES Homeless': 'In Emergency Shelter'}, inplace=True)
    locations['Unsheltered'] = locations['Overall Homeless'] - locations['In Emergency Shelter']
    locations.drop(columns=['Overall Homeless'], inplace=True)
    locations = locations.set_index('Category').transpose()
    locations.rename(columns={state_to_abbrev_dict[state]: 'Number'}, inplace=True)
    locations.index.rename("Location", inplace=True)
    fig = px.pie(locations, values='Number', names=locations.index, title='<b>By Sheltered vs. Unsheltered</b>',
                 color_discrete_sequence=px.colors.sequential.Jet)
    fig.update_layout(margin_autoexpand=False)
    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.75
    ), margin_l=100)

    return fig


@app.callback(
    Output(component_id='piechart1US', component_property='figure'),
    [Input(component_id='selected_year_US', component_property='value')]
)
def create_pie_chart_total_US_gender(selected_year_US):
    return create_pie_chart_gender(selected_year_US, 'Total')


@app.callback(
    Output(component_id='piechart2US', component_property='figure'),
    [Input(component_id='selected_year_US', component_property='value')]
)
def create_pie_chart_total_US_age(selected_year_US):
    return create_pie_chart_age(selected_year_US, 'Total')


@app.callback(
    Output(component_id='piechart3US', component_property='figure'),
    [Input(component_id='selected_year_US', component_property='value')]
)
def create_pie_chart_total_US_ethnicity(selected_year_US):
    return create_pie_chart_ethnicity(selected_year_US, 'Total')


@app.callback(
    Output(component_id='piechart4US', component_property='figure'),
    [Input(component_id='selected_year_US', component_property='value')]
)
def create_pie_chart_total_US_race(selected_year_US):
    return create_pie_chart_race(selected_year_US, 'Total')


@app.callback(
    Output(component_id='piechart5US', component_property='figure'),
    [Input(component_id='selected_year_US', component_property='value')]
)
def create_pie_chart_total_US_sheltered(selected_year_US):
    return create_pie_chart_sheltered(selected_year_US, 'Total')


@app.callback(
    Output(component_id='piechart1state', component_property='figure'),
    [Input(component_id='selected_year_state', component_property='value'),
     Input(component_id='state', component_property='value')]
)
def create_pie_chart_state_gender(selected_year, state):
    return create_pie_chart_gender(selected_year, state)


@app.callback(
    Output(component_id='piechart2state', component_property='figure'),
    [Input(component_id='selected_year_state', component_property='value'),
     Input(component_id='state', component_property='value')]
)
def create_pie_chart_state_age(selected_year_state, state):
    return create_pie_chart_age(selected_year_state, state)


@app.callback(
    Output(component_id='piechart3state', component_property='figure'),
    [Input(component_id='selected_year_state', component_property='value'),
     Input(component_id='state', component_property='value')]
)
def create_pie_chart_state_ethnicity(selected_year_state, state):
    return create_pie_chart_ethnicity(selected_year_state, state)


@app.callback(
    Output(component_id='piechart4state', component_property='figure'),
    [Input(component_id='selected_year_state', component_property='value'),
     Input(component_id='state', component_property='value')]
)
def create_pie_chart_state_race(selected_year_state, state):
    return create_pie_chart_race(selected_year_state, state)


@app.callback(
    Output(component_id='piechart5state', component_property='figure'),
    [Input(component_id='selected_year_state', component_property='value'),
     Input(component_id='state', component_property='value')]
)
def create_pie_chart_state_sheltered(selected_year_state, state):
    return create_pie_chart_sheltered(selected_year_state, state)


def display_qa_table():
    relevant_data_qa_table['Year'] = relevant_data_qa_table['Year'].astype(str)
    national_average_2010 = round(
        relevant_data_qa_table[relevant_data_qa_table.Year == '2010']['Percent_Homeless'].mean(), 2)
    min_percent_homeless_2010 = relevant_data_qa_table[relevant_data_qa_table.Year == '2010']['Percent_Homeless'].min()
    min_percent_homeless_2010_state = abbrev_to_state_dict[
        relevant_data_qa_table[relevant_data_qa_table.Year == '2010']['Percent_Homeless'].idxmin()]
    max_percent_homeless_2010 = relevant_data_qa_table[relevant_data_qa_table.Year == '2010']['Percent_Homeless'].max()
    max_percent_homeless_2010_state = abbrev_to_state_dict[
        relevant_data_qa_table[relevant_data_qa_table.Year == '2010']['Percent_Homeless'].idxmax()]

    national_total_nominal_2010 = relevant_data_qa_table[relevant_data_qa_table.Year == '2010'][
        'Overall_Homeless'].sum()
    min_nominal_homeless_2010 = relevant_data_qa_table[relevant_data_qa_table.Year == '2010']['Overall_Homeless'].min()
    min_nominal_homeless_2010_state = abbrev_to_state_dict[
        relevant_data_qa_table[relevant_data_qa_table.Year == '2010']['Overall_Homeless'].idxmin()]
    max_nominal_homeless_2010 = relevant_data_qa_table[relevant_data_qa_table.Year == '2010']['Overall_Homeless'].max()
    max_nominal_homeless_2010_state = abbrev_to_state_dict[
        relevant_data_qa_table[relevant_data_qa_table.Year == '2010']['Overall_Homeless'].idxmax()]

    national_average_2020 = round(
        relevant_data_qa_table[relevant_data_qa_table.Year == '2020']['Percent_Homeless'].mean(), 2)
    min_percent_homeless_2020 = relevant_data_qa_table[relevant_data_qa_table.Year == '2020']['Percent_Homeless'].min()
    min_percent_homeless_2020_state = abbrev_to_state_dict[
        relevant_data_qa_table[relevant_data_qa_table.Year == '2020']['Percent_Homeless'].idxmin()]
    max_percent_homeless_2020 = relevant_data_qa_table[relevant_data_qa_table.Year == '2020']['Percent_Homeless'].max()
    max_percent_homeless_2020_state = abbrev_to_state_dict[
        relevant_data_qa_table[relevant_data_qa_table.Year == '2020']['Percent_Homeless'].idxmax()]

    national_total_nominal_2020 = relevant_data_qa_table[relevant_data_qa_table.Year == '2020'][
        'Overall_Homeless'].sum()
    min_nominal_homeless_2020 = relevant_data_qa_table[relevant_data_qa_table.Year == '2020']['Overall_Homeless'].min()
    min_nominal_homeless_2020_state = abbrev_to_state_dict[
        relevant_data_qa_table[relevant_data_qa_table.Year == '2020']['Overall_Homeless'].idxmin()]
    max_nominal_homeless_2020 = relevant_data_qa_table[relevant_data_qa_table.Year == '2020']['Overall_Homeless'].max()
    max_nominal_homeless_2020_state = abbrev_to_state_dict[
        relevant_data_qa_table[relevant_data_qa_table.Year == '2020']['Overall_Homeless'].idxmax()]

    gb = relevant_data_qa_table.groupby('State')
    gb_agg_results_percent = gb['Percent_Homeless'].agg(['count', 'min', 'max', 'mean', 'median', 'std'])
    gb_agg_results_nomimal = gb['Overall_Homeless'].agg(['count', 'min', 'max', 'mean', 'median', 'std'])

    national_average_2010_to_2020 = round(gb_agg_results_percent['mean'].mean(), 2)
    min_percent_homeless_2010_to_2020 = round(gb_agg_results_percent['mean'].min(), 2)
    min_percent_homeless_2010_to_2020_state = abbrev_to_state_dict[gb_agg_results_percent['mean'].idxmin()]
    max_percent_homeless_2010_to_2020 = round(gb_agg_results_percent['mean'].max(), 2)
    max_percent_homeless_2010_to_2020_state = abbrev_to_state_dict[gb_agg_results_percent['mean'].idxmax()]

    gb_year = relevant_data_qa_table.groupby('Year')
    gb_year_results = gb_year['Overall_Homeless'].agg(['count', 'sum'])

    national_total_nominal_2010_to_2020 = int(gb_year_results[
                                                  'sum'].mean())
    min_nominal_homeless_2010_to_2020 = int(gb_agg_results_nomimal['mean'].min())
    min_nominal_homeless_2010_to_2020_state = abbrev_to_state_dict[gb_agg_results_nomimal['mean'].idxmin()]
    max_nominal_homeless_2010_to_2020 = int(gb_agg_results_nomimal['mean'].max())
    max_nominal_homeless_2010_to_2020_state = abbrev_to_state_dict[gb_agg_results_nomimal['mean'].idxmax()]

    fig = go.Figure(data=[go.Table(header=dict(values=['Question', 'Answer'], font=dict(color='black', size=15),
                                               fill_color='lightsalmon'),
                                   cells=dict(
                                       values=[['What was the national average percent of homelessness in 2010?',
                                                'What state had the lowest percentage of homelessness in 2010?',
                                                'What state had the largest percentage of homelessness in 2010?',
                                                'What was the total number of homeless nationally in 2010?',
                                                'What state had the lowest nominal number of homeless in 2010?',
                                                'What state had the largest nominal number of homeless in 2010?',
                                                'What was the national average percent of homelessness in 2020?',
                                                'What state had the lowest percentage of homelessness in 2020?',
                                                'What state had the largest percentage of homelessness in 2020?',
                                                'What was the total number of homeless nationally in 2020?',
                                                'What state had the lowest nominal number of homeless in 2020?',
                                                'What state had the largest nominal number of homeless in 2020?',
                                                'What was the national average percent of homelessness overall between 2010 and 2020?',
                                                'What state had the lowest percentage of homelessness overall between 2010 and 2020?',
                                                'What state had the largest percentage of homelessness overall between 2010 and 2020?',
                                                'What was the total number of homeless nationally between 2010 and 2020 on average?',
                                                'What state had the lowest nominal number of homeless between 2010 and 2020 on average?',
                                                'What state had the largest nominal number of homeless between 2010 and 2020 on average?'
                                                ],
                                               [str(national_average_2010) + '%',
                                                min_percent_homeless_2010_state + ' with ' + str(
                                                    min_percent_homeless_2010) + '%',
                                                max_percent_homeless_2010_state + ' with ' + str(
                                                    max_percent_homeless_2010) + '%',
                                                "{:,}".format(national_total_nominal_2010),
                                                str(min_nominal_homeless_2010_state) + ' with ' + str(
                                                    "{:,}".format(min_nominal_homeless_2010)),
                                                str(max_nominal_homeless_2010_state) + ' with ' + str(
                                                    "{:,}".format(max_nominal_homeless_2010)),
                                                str(national_average_2020) + '%',
                                                min_percent_homeless_2020_state + ' with ' + str(
                                                    min_percent_homeless_2020) + '%',
                                                max_percent_homeless_2020_state + ' with ' + str(
                                                    max_percent_homeless_2020) + '%',
                                                "{:,}".format(national_total_nominal_2020),
                                                str(min_nominal_homeless_2020_state) + ' with ' + str(
                                                    "{:,}".format(min_nominal_homeless_2020)),
                                                str(max_nominal_homeless_2020_state) + ' with ' + str(
                                                    "{:,}".format(max_nominal_homeless_2020)),
                                                str(national_average_2010_to_2020) + '%',
                                                min_percent_homeless_2010_to_2020_state + ' with ' + str(
                                                    min_percent_homeless_2010_to_2020) + '%',
                                                max_percent_homeless_2010_to_2020_state + ' with ' + str(
                                                    max_percent_homeless_2010_to_2020) + '%',
                                                "{:,}".format(national_total_nominal_2010_to_2020),
                                                str(min_nominal_homeless_2010_to_2020_state) + ' with ' + str(
                                                    "{:,}".format(min_nominal_homeless_2010_to_2020)),
                                                str(max_nominal_homeless_2010_to_2020_state) + ' with ' + str(
                                                    "{:,}".format(max_nominal_homeless_2010_to_2020)),
                                                ]],

                                       line_color='darkslategray',
                                       fill_color='lightcyan',
                                       align='left', height=40))
                          ])
    fig.update_layout(width=1000, height=975, title='Table Summarizing Insights Into the Data: ')

    return fig


def display_timelapse():
    relevant_data_new = relevant_data_qa_table.copy()
    relevant_data_new.rename(columns={'Percent_Homeless': 'Percent Homeless', 'Full_State': 'State'}, inplace=True)

    fig_percent_each_year = px.bar(relevant_data_new, x='State', y='Percent Homeless',
                                   color='Percent Homeless',
                                   animation_frame='Year', width=1200, height=700)

    fig_percent_each_year.update_xaxes(
        tickangle=60,
        title_text='State Name',
        title_font={'size': 20},
        tickfont_family='Arial Black',
        tickfont={'size': 14},
        title_standoff=10)

    fig_percent_each_year.update_layout(updatemenus=[dict(type='buttons',
                                                          showactive=False,
                                                          y=-0.60,
                                                          x=0,
                                                          xanchor='left',
                                                          yanchor='bottom')
                                                     ])
    fig_percent_each_year.update_layout(yaxis_range=[0, relevant_data_new['Percent Homeless'].max()])
    fig_percent_each_year.update_yaxes(fixedrange=False)
    fig_percent_each_year.update_yaxes(title_text='Percent Homeless', title_font={'size': 20},
                                       tickfont_family='Arial Black', )
    fig_percent_each_year['layout']['sliders'][0]['pad'] = dict(r=10, t=150, )

    return fig_percent_each_year


def display_line_chart():
    list_of_years = []
    list_of_total_homeless = []
    years_range = range(2010, 2021)
    for year in years_range:
        list_of_years.append(str(year))
        list_of_total_homeless.append(
            int(master_df_national[master_df_national.Year == year].loc['Total']['Overall Homeless']))

    df_total_homeless_per_year = pd.DataFrame(
        {'Year': list_of_years, 'Total Homeless Population': list_of_total_homeless})
    df_total_homeless_per_year.columns.name = df_total_homeless_per_year.index.name
    df_total_homeless_per_year.index.name = None
    df_total_homeless_per_year.set_index('Year', inplace=True)
    fig = px.line(df_total_homeless_per_year, x=df_total_homeless_per_year.index, y='Total Homeless Population')
    fig.update_layout(title_font_size=30)
    fig.update_xaxes(title_font_size=20)
    fig.update_yaxes(title_font_size=20)

    return fig


app.layout = html.Div([
    html.H1("Data on Homelessness in the United States",
            style={'text-align': 'center'}),
    html.Hr(),
    html.Br(),
    html.H4('Interactive Timelapse of Variation in Percent Homeless from 2010-2020 [Press Play Below]',
            style={'text-align': 'center'}),
    html.Div(
        children=[
            dcc.Graph(
                id="timelapse",
                figure=display_timelapse(), style={"margin-left": "auto",
                                                   "margin-right": "auto", 'text-align': 'center'})
        ]
    ),
    html.Br(),
    html.Hr(),
    html.H4('Interactive Heatmap of Percent Homeless in each State in 2020 (may take a while to load)',
            style={'text-align': 'center'}),
    html.Div(html.Iframe(id='map', srcDoc=open('data/heatmap.html', 'r').read(), width='100%', height=600),
             style={'display': 'center'}),
    html.Br(),
    html.Hr(),
    html.H4('Line Chart of Total Homeless Population From 2010-2020',
            style={'text-align': 'center'}),
    html.Div(
        children=[
            dcc.Graph(
                id="linechart",
                figure=display_line_chart(), style={"display": "block",
                                                    "margin-left": "auto",
                                                    "margin-right": "auto", 'text-align': 'center', 'width': '50%'}
            )
        ]
    ),
    html.Br(),
    html.Hr(),
    html.H4('Homeless Demographic Breakdown of the United States Overall (all 50 states) [Select Year]',
            style={'text-align': 'center'}),
    html.Div(children=[dcc.Dropdown(id="selected_year_US",
                                    options=[
                                        {"label": "2020", "value": 2020},
                                        {"label": "2019", "value": 2019},
                                        {"label": "2018", "value": 2018},
                                        {"label": "2017", "value": 2017},
                                    ],
                                    value=2020,
                                    multi=False,
                                    style={'width': "40%"}
                                    ), html.H5("Year", style={'display': 'inline-block', 'text-align': 'right'})]),

    html.Br(),
    html.Div(children=[
        dcc.Graph(
            id="piechart1US",
            figure={}, style={"margin-left": "auto",
                              "margin-right": "auto", 'text-align': 'center'}
        )]),
    html.Div(children=[
        dcc.Graph(
            id="piechart2US",
            figure={}, style={"margin-left": "auto",
                              "margin-right": "auto", 'text-align': 'center'}
        )])

    ,
    html.Div(children=[dcc.Graph(
        id="piechart3US",
        figure={}, style={"margin-left": "auto",
                          "margin-right": "auto", 'text-align': 'center'}
    )]),
    html.Div(children=[
        dcc.Graph(
            id="piechart4US",
            figure={}, style={"margin-left": "auto",
                              "margin-right": "auto", 'text-align': 'center'},
        )]),
    html.Div(children=[
        dcc.Graph(
            id="piechart5US",
            figure={}, style={"margin-left": "auto",
                              "margin-right": "auto", 'text-align': 'center'},
        )]),
    html.Br(),
    html.Hr(),
    html.H4('Homeless Demographic Breakdown of the United States Per State [Select Year and State]',
            style={'text-align': 'center'}),
    html.Div(children=[dcc.Dropdown(id="selected_year_state",
                                    options=[
                                        {"label": "2020", "value": 2020},
                                        {"label": "2019", "value": 2019},
                                        {"label": "2018", "value": 2018},
                                        {"label": "2017", "value": 2017},
                                    ],
                                    value=2020,
                                    multi=False,
                                    style={'width': "40%"}
                                    ), html.H5("Year", style={'display': 'inline-block', 'text-align': 'right'})]),
    html.Div(children=[
        dcc.Dropdown(
            id="state",
            options=[{"label": x, "value": x}
                     for x in state_to_abbrev_dict.keys() if x != 'Total'],
            value='New York',
            style={'width': "40%"},
            clearable=False), html.H5("State", style={'display': 'inline-block', 'text-align': 'right'})]),

    html.Div(
        children=[
            dcc.Graph(
                id="piechart1state",
                figure={}, style={"margin-left": "auto",
                                  "margin-right": "auto", 'text-align': 'center'},
            )]),

    html.Div(
        children=[
            dcc.Graph(
                id="piechart2state",
                figure={}, style={"margin-left": "auto",
                                  "margin-right": "auto", 'text-align': 'center'},
            )])

    ,
    html.Div(children=[dcc.Graph(
        id="piechart3state",
        figure={}, style={"margin-left": "auto",
                          "margin-right": "auto", 'text-align': 'center'},
    )]),
    html.Div(children=[
        dcc.Graph(
            id="piechart4state",
            figure={}, style={"margin-left": "auto",
                              "margin-right": "auto", 'text-align': 'center'},
        )]),
    html.Div(children=[
        dcc.Graph(
            id="piechart5state",
            figure={}, style={"margin-left": "auto",
                              "margin-right": "auto", 'text-align': 'center'},
        )]),
    html.Hr(),
    html.Div(
        children=[
            dcc.Graph(
                id="QA_table",
                figure=display_qa_table(),
                style={'display': 'center'}),
        ]
    ),
    html.Hr(),
    html.H6(
        '*NOTE*: NATIONAL DATA IS FOR THE 50 STATES ONLY (it does not include Washington D.C., Puerto Rico, '
        'or any non-state territory.)',
        style={'font-weight': 'bold', 'font-style': 'italic'}),

    html.Div(id='output_container', children=[]),

])

if __name__ == '__main__':
    app.run_server(debug=False, port=6969)
