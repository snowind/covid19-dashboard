import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime as dt
from pandas import to_datetime

dash_link = 'https://plotly.com/dash/'
twitter_link = 'https://developer.twitter.com/en/docs/api-reference-index'
ln_link = 'https://www.linkedin.com/in/kevin-sukaria-23a155137/'

header = \
    html.Div([
        html.H1('COVID-19 Tweet Streamer', style={'text-align': 'center'}),
        html.P([
            "This is a simple ",
            html.A(html.Strong('Dash'), href=dash_link),
            " web application that streams today's tweets about COVID-19 through ",
            html.A(html.Strong('official Twitter API'), href=twitter_link),
            ", Timezone used : GMT+7"],
        ),
        html.P(
            ['Creator : ',
             html.A(html.Strong('Kevin Sukaria'), href=ln_link)],
        )])

interval = \
    dcc.Interval(
        id='interval-component',
        interval=5 * 1000,  # in milliseconds
        n_intervals=0
    )


def news_cards_generator(news_feed):
    news_cards = \
        [
            dbc.Card([
                dbc.CardImg(src=val['img']),
                dbc.CardHeader(val['title']),
                dbc.CardBody(val['desc']),
                html.Em((to_datetime(val['published']) + dt.timedelta(hours=7)).strftime('%A %d %B %Y | %H:%M GMT+7'),
                        style={'text-align': 'right'})
            ])
            for val in news_feed]

    news_container = html.Div(news_cards, id='news-feeds')
    return news_container


def news_carousel(news_feed):
    carousel_items = []
    i = 0
    state = ' active'
    for val in news_feed:
        if i > 0:
            state = ''

        item = \
            html.Div([
                html.Img(src=val['img']),
                html.Div([
                    html.A(html.H3(val['title']), href=val['url']),
                    html.P(val['desc']),
                    html.Em(
                        (to_datetime(val['published']) + dt.timedelta(hours=7)).strftime('%A %d %B %Y | %H:%M GMT+7'))
                ]),

            ], className="carousel-item" + state)
        carousel_items.append(item)
        i += 1

    carousel_inner = html.Div(carousel_items, className="carousel-inner")

    prev = html.A(html.Span(className="carousel-control-prev-icon"),
                  className="carousel-control-prev",
                  href="#news-carousel",
                  role="button",
                  **{'data-slide': 'prev'})

    next = html.A(html.Span(className="carousel-control-next-icon"),
                  className="carousel-control-next",
                  href="#news-carousel",
                  role="button",
                  **{'data-slide': 'next'})

    news_carousel = html.Div([
        carousel_inner,
        prev,
        next
    ], id='news-carousel', className="carousel slide", **{'data-ride': 'carousel'})
    return news_carousel


def update_cards(df):
    confirmed = f'{df.confirmed.sum():,}'
    active = f'{df.active.sum():,}'
    recovered = f'{df.recovered.sum():,}'
    critical = f'{df.critical.sum():,}'
    deaths = f'{df.deaths.sum():,}'
    cards = dbc.CardGroup(
        [
            dbc.Card(
                dbc.CardBody([
                        html.H1(confirmed, className="card-title"),
                        html.P("Confirmed", className="card-text", ),
                    ])
            ),
            dbc.Card(
                dbc.CardBody([
                    html.H1(active, className="card-title"),
                    html.P("Active", className="card-text", ),
                ])
            ),
            dbc.Card(
                dbc.CardBody([
                    html.H1(recovered, className="card-title"),
                    html.P("Recovered", className="card-text", ),
                ])
            ),
            dbc.Card(
                dbc.CardBody([
                    html.H1(critical, className="card-title"),
                    html.P("Critical", className="card-text", ),
                ])
            ),
            dbc.Card(
                dbc.CardBody([
                    html.H1(deaths, className="card-title"),
                    html.P("Deaths", className="card-text", ),
                ])
            ),
        ]
    )
    return cards
