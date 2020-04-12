import requests
import pandas as pd
from plotly.subplots import make_subplots
from plotly import graph_objects as go

url = "https://covid-19-data.p.rapidapi.com/country/all"

headers = {
    'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
    'x-rapidapi-key': "896405cd4dmsh37ab260e7e7121dp1bdf68jsnb713de9f2bb8"
}
br = '<br>'


def refresh_data():
    global df, df_region, df_subregion, table, table_num, table_per, text
    response = requests.request("GET", url, headers=headers)
    region = pd.read_csv('mapping.csv')
    region.columns = ['country', 'id', 'region', 'sub-region']
    df = pd.DataFrame(data=response.json())
    df.drop(['latitude', 'longitude'], axis=1, inplace=True)
    df = pd.merge(df, region, on=['country'])
    df.dropna(inplace=True)
    df = df[df['confirmed'] != 0]
    df = df.sort_values(['region', 'sub-region'])
    df_region = df.groupby(by=['region'], as_index=False).sum()
    df_subregion = df.groupby(by=['region', 'sub-region'], as_index=False).sum()

    def add_columns(df):
        df['active'] = df.confirmed - df.recovered - df.critical - df.deaths
        df['a'] = round(df.active / df.confirmed, 2)
        df['b'] = round(df.recovered / df.confirmed, 2)
        df['c'] = round(df.critical / df.confirmed, 2)
        df['d'] = round(df.deaths / df.confirmed, 2)
        return df

    def add_columns_region(df):
        df['active'] = df.confirmed - df.recovered - df.critical - df.deaths
        df['a'] = round(df.active / df.confirmed, 3) * 100
        df['b'] = round(df.recovered / df.confirmed, 3) * 100
        df['c'] = round(df.critical / df.confirmed, 3) * 100
        df['d'] = round(df.deaths / df.confirmed, 3) * 100
        return df

    def table_format_percentage(column):
        column = column.astype(int).astype(str) + ' %'

    def table_format_separator(column):
        table[column] = table.apply(lambda x: f'{x[column]:,}', axis=1)

    df = add_columns(df)
    df_region = add_columns_region(df_region)
    df_subregion = add_columns_region(df_subregion)
    table = df_subregion.copy()
    table.columns = ['Region', 'Sub-Region', 'Confirmed', 'Recovered', 'Critical', 'Deaths',
                     'Active', '% Active', '% Recovered', '% Critical', '% Death']
    table_format_separator('Confirmed')
    table_format_separator('Recovered')
    table_format_separator('Critical')
    table_format_separator('Deaths')
    table_format_separator('Active')
    table_format_percentage(table['% Active'])
    table_format_percentage(table['% Recovered'])
    table_format_percentage(table['% Critical'])
    table_format_percentage(table['% Death'])
    table_num = table[['Region', 'Sub-Region', 'Confirmed', 'Active', 'Recovered', 'Critical', 'Deaths']]
    table_per = table[['Region', 'Sub-Region', '% Active', '% Recovered', '% Critical', '% Death']]

    text = (
            df['country'] + br + br +
            'Confirmed  : ' + df.apply(lambda x: f'{x.confirmed:,}', axis=1) + br +
            'Active         : ' + df.apply(lambda x: f'{x.active:,}', axis=1) + br +
            'Recovered  : ' + df.apply(lambda x: f'{x.recovered:,}', axis=1) + br +
            'Critical        : ' + df.apply(lambda x: f'{x.critical:,}', axis=1) + br +
            'Deaths        : ' + df.apply(lambda x: f'{x.deaths:,}', axis=1) + br +
            '% Active         : ' + df.apply(lambda x: f"{x.a:.0%}", axis=1) + br +
            '% Recovered : ' + df.apply(lambda x: f"{x.b:.0%}", axis=1) + br +
            '% Critical        : ' + df.apply(lambda x: f"{x.c:.0%}", axis=1) + br +
            '% Deaths       : ' + df.apply(lambda x: f"{x.d:.0%}", axis=1)
    )

def generate_geo():
    geo_fig = go.Figure(data=go.Choropleth(
        locationmode='country names',
        locations=df['country'],
        z=df['confirmed'],
        colorscale='bupu',
        marker_line_color='darkgrey',
        marker_line_width=1,
        colorbar_title='Confirmed Cases',
        zmax=df.confirmed.quantile(q=0.95),
        zmin=0,
        text=text,
        name='',
        hovertemplate = '%{text}',
    ))

    geo_fig.update_layout(
        title_text='World Wide COVID-19 Cases',
        geo=dict(showframe=False,
                 showcoastlines=False,
                 projection_type='natural earth')
    )

    geo_fig.update_geos(
        lataxis_showgrid=False,
        lonaxis_showgrid=False,
        showocean=True,
        oceancolor="rgba(114, 0, 230,0)",
    )

    return geo_fig

def generate_pie():
    colors = ['orange','green','red','black']
    labels = ['% Active','% Recovered','% Critical','% Death']
    specs = [[{'type':'domain'} for i in range(5)]]
    pie_fig = make_subplots(rows=1, cols=5, specs=specs, subplot_titles=df_region['region'])
    val = 0
    row = 1
    col = 1
    for val in range(5):
        pie_fig.add_trace(
            go.Pie(
                labels=labels,
                values=[df_region.a[val], df_region.b[val],df_region.c[val],df_region.d[val]] ,
                name=df_region.region[val],
                title=f'{df_region.confirmed[val]:,}'+br+'Cases',
                textinfo='none'
            ),
            row, val+1
        )

    pie_fig.update_traces(
        hole=.6,
        hoverinfo="label+percent+name",
        marker=dict(colors = colors)
    )
    pie_fig.update_layout(
        autosize=True,
        paper_bgcolor="rgba(0,0,0,0)",
        )
    return pie_fig


def generate_bar():
    values = ['% Active', '% Recovered', '% Critical','% Death']
    colors = ['orange','green','red','black']
    bar_fig = go.Figure()
    for i in range(4):
        fig.add_trace(go.Bar(
            y=table_per['Sub-Region'].iloc[::-1],
            x=table_per[values[i]],
            name=values[i],
            orientation='h',
            marker=dict(
                color = colors[i],
                line=dict(color='rgba(255, 255, 255, 1)', width=1)
            )
        ))


    bar_fig.update_layout(
        barmode='stack',
        legend_orientation="h",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return bar_fig

