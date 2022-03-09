import pandas as pd
import numpy as np
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash
from dash import Dash, dash_table, dcc, html
import base64
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("./pred.csv")
df = df[df['Predicted']==0]
df = df[['candidate_user_name', 'pol_party']]
df['Count'] = df.groupby(['candidate_user_name'])['pol_party'].transform('count')
df = df.drop_duplicates()

miso_df = pd.read_csv("./misogynistic_tweets.csv")
miso_df = miso_df[['Full Name', 'candidate_user_name', 'party', 'ideology', 'leadership', 'state', 'Position']]
df = df.merge(miso_df, on='candidate_user_name')

df = df[["Full Name", "state", "party", "Position", "candidate_user_name", "ideology", "leadership", 'Count']]
df = df.sort_values(['Count'], ascending=False)
df["ideology"] = df["ideology"].round(decimals = 3)
df["leadership"] = df["leadership"].round(decimals = 3)

df_log = df.copy()
df_log['Count_l'] = np.log(df_log['Count'])

state_df = df_log[['state', 'Count_l']]
state_df = state_df.groupby(['state']).sum()
state_df = state_df.reset_index()
df = df.rename(columns={"state": "State", "party": "Party", 'ideology': 'Ideology', 'leadership':"Leadership"})


###############################################



app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)
app.title = "Women In Politics & Misogynistic Tweets"
server = app.server 

image_filename = './wordcloud.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

PAGE_SIZE = 10
background_color = '#002663'

fig = px.histogram(df_log, x="ideology", y="Count_l", nbins=5,
                hover_name="Full Name", labels=dict(ideology="Ideology Score", Count_l="Number of Tweets"))
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=True)
fig.update_yaxes(title_text='Number of Tweets (logged)')
fig.update_xaxes(range=[0, 1], tickvals=[0.2, 0.4, 0.6, 0.8, 1.0], autorange=False, 
                 tickfont=dict(color='white', size=12, family='Helvetica'))

fig.update_xaxes(title_font=dict(size=14, color='#dadfeb', family='Helvetica'))
fig.update_yaxes(title_font=dict(size=14, color='#dadfeb', family='Helvetica'))
fig.update_yaxes(tickfont=dict(color='#dadfeb', size=12, family='Helvetica'))
fig.update_layout(
    title={
        'text': "Number of Tweets By Ideology Score of Politician",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.update_layout(
    title_font_family="Helvetica",
    title_font_color="#dadfeb",
    font=dict(size=14)
)
fig.update_traces(marker_color='#2e75e6')


fig2 = px.histogram(df_log, x="leadership", y="Count_l", nbins=5,
                hover_name="Full Name", labels=dict(leadership="Leadership Score", Count_l="Number of Tweets"))
fig2.update_xaxes(showgrid=False)
fig2.update_yaxes(showgrid=True)
fig2.update_yaxes(title_text='Number of Tweets (logged)')
fig2.update_xaxes(title_font=dict(size=14, color='#dadfeb', family='Helvetica'))
fig2.update_yaxes(title_font=dict(size=14, color='#dadfeb', family='Helvetica'))
fig2.update_xaxes(range=[0, 1], tickvals=[ 0.2, 0.4, 0.6, 0.8, 1.0], autorange=False, 
                 tickfont=dict(family='Helvetica', color='#dadfeb', size=12))
fig2.update_yaxes(tickfont=dict(family='Helvetica', color='#dadfeb', size=12))
fig2.update_layout(
    title={
        'text': "Number of Tweets By Leadership Score of Politician",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
    })
fig2.update_layout(
    title_font_family="Helvetica",
    title_font_color="#dadfeb",
    font=dict(size=14)
)
fig2.update_traces(marker_color='#2e75e6')


fig3 = px.choropleth(state_df,
                    locations='state',
                    color='Count_l',
                    color_continuous_scale='blues',
                    hover_name='state',
                    locationmode='USA-states',
                    labels={'Tweets per State'},
                    scope='usa')
fig3.update_xaxes(showgrid=False)
fig3.update_yaxes(showgrid=False)
fig3.update_layout(
    title={
        'text': "Number of Tweets By State of Politician",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
    })
fig3.update_layout(
    title_font_family="Helvetica",
    title_font_color="#dadfeb",
    font=dict(size=14)
)
fig3.update_layout(coloraxis_colorbar=dict(
        title="",
        tickvals=[0.2, 5.481784],
        tickfont={"color":'#dadfeb'},
        ticktext=[
            "Least Tweets", "Most Tweets"]))





fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})

fig3.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})
fig3.update_geos(bgcolor="rgba(0, 0, 0, 0)", lakecolor="#011c47")

app.layout = html.Div(children=[
    html.Div(children=[
        html.H1(children='Women in Politics and Misogynistic Tweets: Classifying Misogyny'),
        html.H2(children='In the run up to the 2020 election, to what extent is misogynistic rhetoric directed at women running for office on Twitter in the United States?')],
    className='app__header'),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                dcc.Graph(
                    id='ideology',
                    figure=fig
                )
            ], className='half graph-container'),
            html.Div(children=[
                dcc.Graph(
                    id='map',
                    figure=fig3
                )
            ], className='half graph-container')
        ], className='row'),
        html.Div(children=[
            html.Div(children=[
                dcc.Graph(
                    id='leadership',
                    figure=fig2
                )
            ], className='half graph-container'),
            html.Div(children=[
                html.H3(children='Most Commonly Found Words in Misogynistic Tweets'),
                html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={ 'text-align': 'center', 'max-width': '80%'})
            ], className='half')
        ], className='row'),
        html.Div(children=[
            html.Div(children=[
            dash_table.DataTable(
                id='table-paging-and-sorting',
                columns=[
                    {'name': i, 'id': i, 'deletable': True} for i in sorted(df.columns)
                ],
                style_cell={'padding': '5px', 'fontSize':16, 'font-family':'Helvetica',
                           'backgroundColor': '#0c2b5c' },

                style_header={
                    'backgroundColor': '#224f99',
            },
                data=df.to_dict('records'),
                style_data={ 'border': '1px solid #dadfeb' },

                page_current=0,
                page_size=PAGE_SIZE,
                page_action='custom',

                sort_action='custom',
                sort_mode='single',
                sort_by=[]
            )],className='full')], className='row')
                 ], className='app__content')
    
], className='app__container')

@app.callback(
    Output('table-paging-and-sorting', 'data'),
    Input('table-paging-and-sorting', "page_current"),
    Input('table-paging-and-sorting', "page_size"),
    Input('table-paging-and-sorting', 'sort_by'))

def update_table(page_current, page_size, sort_by):
    if len(sort_by):
        dff = df.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = df

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')


if __name__ == '__main__':
    app.run_server()