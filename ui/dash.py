from pymongo import MongoClient
from dash.dependencies import Input, Output, State
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go 
import numpy as np 
import requests, json
import pandas as pd
import service

client = MongoClient()
db = client.flat_renting
collection = db.offer
data = pd.DataFrame(list(collection.find()))
data_std = data[ (data['price'] > 0) &  (data['surface'] > 0) & (np.abs(data.price-data.price.mean()) <= (2*data.price.std())) ]

data["feats_num"]=data["feats"].apply(lambda x: len(x))
data["pics_num"]=data["images"].apply(lambda x: len(x))

data_std["feats_num"]=data_std["feats"].apply(lambda x: len(x))
data_std["pics_num"]=data_std["images"].apply(lambda x: len(x))

print(data.columns)

app = dash.Dash()


general_counts = html.Div(className='substats', children=[
    html.Div(className='list_element', children="Number of offers: "+str(data['_id'].count())),
    html.Div(className='list_element', children="Number of sites: "+str(len(data['site'].unique()))),
    html.Div(className='list_element', children="Number of cities: "+str(len(data['city'].unique()))),
    html.Div(className='list_element', children="Number of zones: "+str(len(data['zone'].unique()))),
    html.Div(className='list_element', children="Number of companies: "+str(len(data['company'].unique())))
])

price_stats = html.Div(className='substats', children=[
    html.Div(className='list_element', children='Price mean: '+ str(data['price'].mean())),
    html.Div(className='list_element', children='Price median: '+ str(data['price'].median())),
    html.Div(className='list_element', children='Price variance: '+ str(data['price'].var())),
    html.Div(className='list_element', children='Price min: '+ str(data['price'].min())),
    html.Div(className='list_element', children='Price max: '+ str(data['price'].max())),
    html.Div(className='list_element', children='Total number of money: '+ str(data['price'].sum())),
])

surface_stats = html.Div(className='substats',children=[
    html.Div(className='list_element', children='Surface mean: '+ str(data['surface'].mean())),
    html.Div(className='list_element', children='Surface median: '+ str(data['surface'].median())),
    html.Div(className='list_element', children='Surface variance: '+ str(data['surface'].var())),
    html.Div(className='list_element', children='Surface min: '+ str(data['surface'].min())),
    html.Div(className='list_element', children='Surface max: '+ str(data['surface'].max())),
    html.Div(className='list_element', children='Total number of m2 offered: '+ str(data['surface'].sum())),
])

rooms_stats = html.Div(className='substats', children=[
    html.Div(className='list_element', children='Rooms mean: '+ str(data['rooms'].mean())),
    html.Div(className='list_element', children='Rooms median: '+ str(data['rooms'].median())),
    html.Div(className='list_element', children='Rooms variance: '+ str(data['rooms'].var())),
    html.Div(className='list_element', children='Rooms min: '+ str(data['rooms'].min())),
    html.Div(className='list_element', children='Rooms max: '+ str(data['rooms'].max())),
    html.Div(className='list_element', children='Total number of rooms offered: '+ str(data['rooms'].sum())),
])

toilets_stats = html.Div(className='substats',children=[
    html.Div(className='list_element', children='Toilets mean: '+ str(data['toilets'].mean())),
    html.Div(className='list_element', children='Toilets median: '+ str(data['toilets'].median())),
    html.Div(className='list_element', children='Toilets variance: '+ str(data['toilets'].var())),
    html.Div(className='list_element', children='Toilets min: '+ str(data['toilets'].min())),
    html.Div(className='list_element', children='Toilets max: '+ str(data['toilets'].max())),
    html.Div(className='list_element', children='Total number of toilets offered: '+ str(data['toilets'].sum())),
])

feats_stats = html.Div(className='substats', children=[
    html.Div(className='list_element', children='Feats mean: '+ str(data['feats_num'].mean())),
    html.Div(className='list_element', children='Feats median: '+ str(data['feats_num'].median())),
    html.Div(className='list_element', children='Feats variance: '+ str(data['feats_num'].var())),
    html.Div(className='list_element', children='Feats min: '+ str(data['feats_num'].min())),
    html.Div(className='list_element', children='Feats max: '+ str(data['feats_num'].max())),
    html.Div(className='list_element', children='Total number of Feats offered: '+ str(data['feats_num'].sum())),
])

images_stats = html.Div(className='substats', children=[
    html.Div(className='list_element', children='Images mean: '+ str(data['pics_num'].mean())),
    html.Div(className='list_element', children='Images median: '+ str(data['pics_num'].median())),
    html.Div(className='list_element', children='Images variance: '+ str(data['pics_num'].var())),
    html.Div(className='list_element', children='Images min: '+ str(data['pics_num'].min())),
    html.Div(className='list_element', children='Images max: '+ str(data['pics_num'].max())),
    html.Div(className='list_element', children='Total number of Images offered: '+ str(data['pics_num'].sum())),
])

general_stats = [price_stats, surface_stats, rooms_stats, toilets_stats, feats_stats, images_stats]

price_histogram = html.Div([
    dcc.Graph(id='price_histogram', 
        figure = {'data': [
            go.Histogram(
            x=data_std['price']
    )],
    'layout':go.Layout(title='Price histogram (corrected to max 2std <-->)')
    })
])

surface_histogram = html.Div([
    dcc.Graph(id='surface_histogram', 
        figure = {'data': [
            go.Histogram(
            x=data_std['surface']
    )],
    'layout':go.Layout(title='Surface histogram (corrected to max 2std <-->)')
    })
])

histograms = [price_histogram, surface_histogram]

price_boxplot = html.Div([
    dcc.Graph(id='price_boxplots', 
        figure = {'data': [

            go.Box(
                y=data_std[data_std.site=='pisoscom']['price'],
                name="pisos.com"          
            ),
            
            go.Box(
                y=data_std[data_std.site=='habitaclia']['price'],
                name="habitaclia"          
            )
        ],
    'layout':go.Layout(title='Price boxplots for each site (corrected to max 2std <-->)')
    })
])


numeric_columns = [
    {'label':'price','value':'price'},
    {'label':'surface','value':'surface'},
    {'label':'rooms','value':'rooms'},
    {'label':'toilets','value':'toilets'},
    {'label':'num_feats','value':'feats_num'},
    {'label':'num_images','value':'pics_num'}
]
multi_scatter = html.Div([
    html.H1('Feature comparision'),
    html.Div([
        html.H3('Select feature(x): ', style={'paddingRight':'30px'}),
        dcc.Dropdown(
            id='feat_a',
            options=numeric_columns,
            value=numeric_columns[0],
            multi=False

        )
    ], style={'display':'inline-block','verticalAlign':'top','width':'25%'}),
    html.Div([
        html.H3('Select another feature(y): '),
        dcc.Dropdown(
            id='feat_b',
            options=numeric_columns,
            value=numeric_columns[1],
            multi=False

        )
    ], style={'display':'inline-block','verticalAlign':'top','width':'25%'} ),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':24, 'marginLeft':'30px','marginTop':'60px'}
        ),
    ], style={'display':'inline-block'}),
    dcc.Graph(
        id='general_scatter',
        figure={
            'data': [
                {'x':data_std['surface'], 'y':data_std['price'], 'mode':'markers'}
            ]
        }
    )    
])


@app.callback(
    Output('general_scatter', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('feat_a', 'value'),
    State('feat_b', 'value')])
def update_graph(n_clicks,  value_a, value_b):
    title = str(value_a) + " - " + str(value_b)
    fig = {
        'data': [
                {'x':data[value_a], 'y':data[value_b], 'mode':'markers'}
        ],
        'layout': {'title': title}
    }
    return fig




# CLUSTERING ANALYSIS

# numclusters=6, numpca=3, vals=['price','surface','rooms','toilets','feats','images'], algorithm="elkan"

cluster_features = [
    {'label':'price','value':'price'},
    {'label':'surface','value':'surface'},
    {'label':'rooms','value':'rooms'},
    {'label':'feats','value':'feats_num'},
    {'label':'images','value':'pics_num'},

]

algorithms = [
    {'label':'elkan','value':'elkan'},
    {'label':'auto','value':'auto'},
    {'label':'full','value':'full'}
]
clustering_form = html.Div([
    html.H3('Clustering analysis'),
    html.H4('Features to analyse'),
    dcc.Dropdown(
        id='cluster_features',
        options=cluster_features,
        value=cluster_features[1],
        multi=True
    ),
    html.H4('Algortithm'),
    dcc.Dropdown(
        id='algorithm',
        options=algorithms,
        value=algorithms[1],
        multi=False
    ),
    html.H4('Number of clusters'),
    dcc.Input(
        id='num_clusters',
        type='number',
        placeholder='1'
    ),
    html.H4('Number of principal components'),
    dcc.Input(
        id='num_pca',
        type='number',
        placeholder='2'
    ),
    html.Button(
        id='submit-clustering',
        n_clicks=0,
        children='Make clusters'
    ),
    html.Div(
        id='clustering-results',
        children=html.Pre(id='clustering-id-results', children='')
    ),
    html.Div(
        id='clustering-results-container',
        children=dcc.Graph(
        id='cluster-scat',
        figure={
            'data':[
                {'x':[], 'y':[]}
            ]
        }
    )
    )
])


def assign_category(val, categories):
    tag = "unknown"
    for c in categories:
        c=(categories[c])
        minval = c["minval"]
        maxval = c["maxval"]
        tag = c["tag"]
        if val > minval and val <= maxval:
            return tag
    
    return tag

@app.callback(
    Output('cluster-scat','figure'),
    [Input('submit-clustering','n_clicks')],
    [State('cluster_features','value'),
    State('algorithm','value'),
    State('num_clusters','value'),
    State('num_pca','value')]
)
def gen_clusters(n_clicks, cluster_features, algorithm, num_clusters, num_pca):
    #def make_clusters(d, numclusters=6, numpca=3, vals=['price','surface','rooms','toilets','feats','images'], algorithm="elkan"):
    clusters = service.make_clusters(data_std, numclusters=num_clusters, numpca=num_pca, vals=cluster_features, algorithm=algorithm)
    price_index = cluster_features.index('price')
    
    
    clusters_object = {
        'tags':cluster_features,
        'clusters':clusters,
        'numpca':num_pca,
        'algorithm:':algorithm
    }
    if "price" in cluster_features:
        prices = []
        for c in clusters:
            prices.append(c[price_index])
        categories = service.make_categories(prices)
        clusters_object['categories'] = categories
        data_std["price_tag"] =  data_std.apply(lambda row: assign_category(row.price, categories), axis = 1) 
    
    data_std["price_tag"]  = pd.Categorical(data_std["price_tag"], categories=data_std["price_tag"].unique()).codes
    clusters_json = json.dumps(clusters_object, indent=4)

    print(np.random.randn(len(data_std["price_tag"].unique())))
    figure={
            'data':[
                {'y':data_std["price"], 'x':data_std["surface"],
                'mode':'markers',
                'marker':{
                    'color':data_std["price_tag"],
                    'colorscale':'Viridis',
                    'showscale':True
                }}
            ]
    }
    return figure
    #categories = make_categories(clusters)


clustering = [clustering_form]

app.layout = html.Div([
    html.Div(id='counts',children=general_counts, style={'width':'500px', 'float':'left'}),
    html.Div(id='stats', children=general_stats, style={'width':'500px', 'float':'left'}),
    html.Div(id='histograms', children=histograms, style={'width':'500px', 'float':'left'}),
    html.Div(id='boxplots', children=price_boxplot, style={'width':'500px', 'float':'left'}),
    html.Div(id='scatterplots', children=multi_scatter, style={'width':'500px', 'float':'left'}),
    html.Div(id='clustering', children=clustering_form, style={'width':'500px','float':'left'})
]
)

if __name__ == '__main__':
    app.run_server()
