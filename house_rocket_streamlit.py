import numpy as np
import pandas as pd
from datetime import datetime as dt
import streamlit as st
import geopandas
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px 


st.set_page_config(layout='wide')
st.title('House Rocket Company Properties Analysis')
st.header('Properties Overview')

@st.cache(allow_output_mutation=True)
def data_collect(path):
    df = pd.read_csv(path)
    return df

@st.cache( allow_output_mutation=True )
def get_geofile( url ):
 geofile = geopandas.read_file( url )
 return geofile

def quantile_30(x):
    return x.quantile(0.3)
def quantile_40(x):
    return x.quantile(.4)
def quantile_60(x):
    return x.quantile(.6)
def quantile_75(x):
    return x.quantile(.75)


def buying_propeties(df):
    df2 = df[['buying_price','zipcode','condition_type']].groupby(['zipcode','condition_type'])\
    .agg(['median',quantile_30,quantile_40]).droplevel(0,axis=1).reset_index()
    df = df.merge(df2, on=['zipcode','condition_type'])
    for i in range(0,len(df)):
        if df.loc[i,'condition_type'] == 'bad':
            if df.loc[i,'buying_price'] < df.loc[i,'quantile_40']:
                df.loc[i,'decision'] = 'buy'
            else:
                df.loc[i,'decision'] = 'not buy'
        elif df.loc[i,'condition_type'] == 'regular':
            if df.loc[i,'buying_price'] < df.loc[i,'quantile_40']:
                df.loc[i,'decision'] = 'buy'
            else:
                df.loc[i,'decision'] = 'not buy'
        elif df.loc[i,'condition_type'] == 'good':
            if df.loc[i,'buying_price'] < df.loc[i,'quantile_40']:
                df.loc[i,'decision'] = 'buy'
            else:
                df.loc[i,'decision'] = 'not buy'
    df = df.drop(['median','quantile_30','quantile_40'],axis=1)
    return df

def max_cost_improvement(df):
    df2 = df.loc[df['condition_type'] == 'good',['buying_price','zipcode']].groupby('zipcode')\
    .agg(quantile_30)\
    .reset_index().rename({'buying_price':'quantile_30'},axis=1)
    
    df3 = df.loc[(df['condition_type'] == 'regular')\
    ,['buying_price','zipcode']].groupby('zipcode')\
    .agg([quantile_40]).reset_index().droplevel(0,axis=1)\
    .rename({'':'zipcode'},axis=1)
    
    for i in range(0,len(df)):
        if df2['zipcode'].isin([df['zipcode'][i]]).any():
            if (df.loc[i,'condition_type'] == 'bad') & (df.loc[i,'decision'] == 'buy') & \
                (pd.merge(df,df2,how='left', on='zipcode')\
                .loc[i,'quantile_30'] - df.loc[i,'buying_price'] >= 0):
                    df.loc[i,'max_budget_improvement'] = pd.merge(df,df2,how='left', on='zipcode')\
                    .loc[i,'quantile_30'] - df.loc[i,'buying_price'] 
            else:
                df.loc[i,'max_budget_improvement'] = 0
        else:
            if (df.loc[i,'condition_type'] == 'bad') & (df.loc[i,'decision'] == 'buy') & \
            (pd.merge(df,df3,how='left', on='zipcode')\
            .loc[i,'quantile_40'] - df.loc[i,'buying_price'] >= 0):
                    df.loc[i,'max_budget_improvement'] = pd.merge(df,df3,how='left', on='zipcode')\
                    .loc[i,'quantile_40'] - df.loc[i,'buying_price']
            else:
                df.loc[i,'max_budget_improvement'] = 0
                                
    return df

def min_selling_price(df):
    df2 = df.loc[(df['condition_type'] == 'good')\
    ,['buying_price','zipcode']].groupby('zipcode')\
    .agg([quantile_40,'median',quantile_60]).reset_index().droplevel(0,axis=1).rename({'':'zipcode'},axis=1)
    
    df3 = df.loc[(df['condition_type'] == 'regular')\
    ,['buying_price','zipcode']].groupby('zipcode')\
    .agg([quantile_40,'median',quantile_60]).reset_index().droplevel(0,axis=1).rename({'':'zipcode'},axis=1)
      
    for i in range(0,len(df)):
        if (df.loc[i,'condition_type'] == 'bad') & (df.loc[i,'decision'] == 'buy'):
            if df2['zipcode'].isin([df['zipcode'][i]]).any():
                df.loc[i,"min_selling_price"] = pd.merge(df,df2, how='left',on='zipcode')\
                .loc[i,'quantile_40']
            else:
                df.loc[i,"min_selling_price"] = pd.merge(df,df3, on='zipcode')\
                .loc[i,'median']
        elif (df.loc[i,'condition_type'] == 'regular') & (df.loc[i,'decision'] == 'buy'):
            if df3['zipcode'].isin([df['zipcode'][i]]).any():
                df.loc[i,"min_selling_price"] = pd.merge(df,df3, how='left',on='zipcode')\
                .loc[i,'median']
            else:
                df.loc[i,"min_selling_price"] = pd.merge(df,df2, how='left',on='zipcode')\
                .loc[i,'quantile_40']
        elif (df.loc[i,'condition_type'] == 'good') & (df.loc[i,'decision'] == 'buy'):
            if df2['zipcode'].isin([df['zipcode'][i]]).any():
                df.loc[i,"min_selling_price"] = pd.merge(df,df2, how='left',on='zipcode').loc[i,'median']
            else:
                df.loc[i,"min_selling_price"] = pd.merge(df,df3, how='left',on='zipcode').loc[i,'quantile_60']
        else:
            df.loc[i,"min_selling_price"] = 0
                
    return df

def suggested_selling_price(df):
    df2 = df.loc[(df['condition_type'] == 'good')\
    ,['buying_price','zipcode']].groupby('zipcode')\
    .agg([quantile_40,'median',quantile_60]).reset_index().droplevel(0,axis=1).rename({'':'zipcode'},axis=1)
    
    df3 = df.loc[(df['condition_type'] == 'regular')\
    ,['buying_price','zipcode']].groupby('zipcode')\
    .agg([quantile_40,'median',quantile_60, quantile_75]).reset_index().droplevel(0,axis=1).rename({'':'zipcode'},axis=1)
     
    for i in range(0,len(df)):
        if (df.loc[i,'condition_type'] == 'bad') & (df.loc[i,'decision'] == 'buy'):
            if df2['zipcode'].isin([df['zipcode'][i]]).any():
                df.loc[i,"suggested_selling_price"] = pd.merge(df,df2, how='left',on='zipcode')\
                .loc[i,'median']
            else:
                df.loc[i,"suggested_selling_price"] = pd.merge(df,df3, on='zipcode')\
                .loc[i,'quantile_60']
        elif (df.loc[i,'condition_type'] == 'regular') & (df.loc[i,'decision'] == 'buy'):
            if df3['zipcode'].isin([df['zipcode'][i]]).any():
                df.loc[i,"suggested_selling_price"] = pd.merge(df,df3, how='left',on='zipcode')\
                .loc[i,'quantile_60']
            else:
                df.loc[i,"suggested_selling_price"] = pd.merge(df,df2, how='left',on='zipcode')\
                .loc[i,'quantile_40']
        elif (df.loc[i,'condition_type'] == 'good') & (df.loc[i,'decision'] == 'buy'):
            if df2['zipcode'].isin([df['zipcode'][i]]).any():
                df.loc[i,"suggested_selling_price"] = pd.merge(df,df2, how='left',on='zipcode')\
                .loc[i,'quantile_60']
            else:
                df.loc[i,"suggested_selling_price"] = pd.merge(df,df3, how='left',on='zipcode')\
                .loc[i,'quantile_75']
        else:
            df.loc[i,"suggested_selling_price"] = 0
                
    return df

def profits(df):
    for i in range(0,len(df)):
        if (df.loc[i,'decision'] == 'buy') & \
        ((df.loc[i,'min_selling_price'] - df.loc[i,'buying_price']) > 0):
            df.loc[i,'min_profit'] = df.loc[i,'min_selling_price'] - df.loc[i,'buying_price']
            df.loc[i,'expected_profit'] = df.loc[i,'suggested_selling_price'] - df.loc[i,'buying_price']
        else:
            df.loc[i,'min_profit'] = 0
            df.loc[i,'expected_profit'] = 0
    return df.sort_values(by='expected_profit',ascending=False)

def data_transform(df):
    df['id'] = df['id'].astype(str)
    df['condition'] = df['condition'].astype(int)
    df['price'] = df['price'].astype(float).round(2)
    df['sqft_living'] = df['sqft_living'].astype(float).round(2)
    df['sqft_lot'] = df['sqft_lot'].astype(float).round(2)
    df['sqft_above'] = df['sqft_above'].astype(float).round(2)
    df['sqft_basement'] = df['sqft_basement'].astype(float).round(2)
    df['sqft_living15'] = df['sqft_living15'].astype(float).round(2)
    df['sqft_lot15'] = df['sqft_lot15'].astype(float).round(2)
    df['floors'] = df['floors'].apply(lambda x: 1 if 1 <= x < 2 else 2 if 2 <= x < 3 else 3).astype(int)
    df['bathrooms'] = df['bathrooms'].apply(lambda x: round(x,0)).astype(int)
    df2 = df[['price','zipcode']].groupby('zipcode').median().reset_index().rename({'price':'median_buying_price'}, axis=1)
    df = pd.merge(df,df2, on='zipcode', how='inner')
    df = df.rename({'price':'buying_price', 'date':'buying_avaliable_date'},axis=1)
    
    df['buying_avaliable_date'] = pd.to_datetime(df['buying_avaliable_date']).dt.strftime('%Y-%m-%d')
    df['season'] = pd.to_datetime(df['buying_avaliable_date']).dt.strftime('%m-%d').apply(lambda x:
                'Spring' if '03-21' <= x < '06-21'
                else 'Summer' if '06-21' <= x < '09-21'                                                   
                else 'Autunm' if '09-21' <= x < '12-21'
                else 'Winter' )
    
    df['house_age'] = np.where(df['yr_built'] >= 2010, 'new', 'old')
    df['yr_built'] = pd.to_datetime(df['yr_built'], format= "%Y").dt.strftime('%Y').astype(str)


    
    df['condition_type'] = df['condition'].apply(lambda x: 'bad' if x <= 2
                                                else 'regular' if (x ==3) | (x==4)
                                                else 'good')
    
    df['yr_renovated'] = (df['yr_renovated'].apply(
    lambda x: pd.to_datetime('1900-01-01', format = '%Y-%m-%d') if x == 0 
    else pd.to_datetime(x, format= "%Y-%m-%d"))).dt.strftime('%Y').astype(int)
    df['is_renovated'] = df['yr_renovated'].apply(lambda x: 'no' if x == 1900 else 'yes')
    df['is_waterfront'] = df['waterfront'].apply(lambda x: 'yes' if x == 1 else 'no')
    df = df.drop(['view','grade','condition','waterfront','yr_renovated'],axis=1)
    
    season_filter = st.sidebar.selectbox('Choose season you want to sold the house', df['season'].unique())
    df = df.loc[df['season'] == season_filter, df.columns != 'season']
    df = buying_propeties(df)
    df = max_cost_improvement(df)
    df = min_selling_price(df)
    df = suggested_selling_price(df)
    df = profits(df)
    
    return df

 
def data_load(df):
    f_columns = st.sidebar.multiselect('Choose columns you want to see', df.columns)
    f_zipcode = st.sidebar.multiselect('Select zipcode', df['zipcode'].unique())
    
    if (f_zipcode != []) & (f_columns != []):
        df = df.loc[df['zipcode'].isin(f_zipcode), f_columns]
    
    elif (f_zipcode != []) & (f_columns == []):
        df=df.loc[df['zipcode'].isin(f_zipcode), :]
    
    elif (f_zipcode == []) & (f_columns != []):
        df = df.loc[:,f_columns]
    
    else: 
        df = df.copy()
    
    st.sidebar.subheader('Phisical Filters')
    f_bath = st.sidebar.selectbox(' Max Number of Bathrooms', sorted(df['bathrooms'].unique()), index=len(df['bathrooms'].unique()) - 1)
    f_bed = st.sidebar.selectbox('Max Number of Bedrooms', sorted(df['bedrooms'].unique()), index=len(df['bedrooms'].unique()) - 1)
    f_floors = st.sidebar.selectbox('Max Number of Floors', sorted(df['floors'].unique()), index=len(df['floors'].unique()) - 1)
    f_waterfront = st.sidebar.selectbox('Is waterfront?', sorted(df['is_waterfront'].unique()))
    f_age = st.sidebar.selectbox('House age (Considering old as built before 2010', sorted(df['house_age'].unique()), index=1)
    f_condition = st.sidebar.selectbox('Condition', sorted(df['condition_type'].unique()), index=1)
    f_renovated = st.sidebar.selectbox('Is renovated?', sorted(df['is_renovated'].unique()))
    
    st.sidebar.subheader('Commercial Filters')
    f_decision = st.sidebar.selectbox('Show properties suggested to buy', sorted(df['decision'].unique()))
    f_suggested_price = st.sidebar.slider('Max Suggested Selling Price', int(df['suggested_selling_price'].min()), 
                    int(df['suggested_selling_price'].max()),
                    int(df['suggested_selling_price'].max()))
    f_minimum_price = st.sidebar.slider('Max Minimum Selling Price', int(df['min_selling_price'].min()), 
                                        int(df['min_selling_price'].max()),
                                        int(df['min_selling_price'].max()))
    f_max_improvement = st.sidebar.slider('Max budget improvement', int(df['max_budget_improvement'].min()), int(df['max_budget_improvement'].max()),
                    int(df['max_budget_improvement'].max()))
    
    st.sidebar.subheader('Profit Filters')
    f_suggested_profit = st.sidebar.slider('Max expected profit', int(df['expected_profit'].min()), 
                    int(df['expected_profit'].max()),int(df['expected_profit'].max()))
    f_min_profit = st.sidebar.slider('Max minimum expected profit', int(df['min_profit'].min()), 
                    int(df['min_profit'].max()),int(df['min_profit'].max()))
   
    df = df[df['decision'] == str(f_decision)]
    df = df[df['bathrooms'] <= f_bath]
    df = df[df['bedrooms'] <= f_bed]
    df = df[df['floors'] <= f_floors]
    df = df[df['is_waterfront'] == str(f_waterfront)]
    df = df[df['house_age'] == str(f_age)]
    df = df[df['condition_type'] == str(f_condition)]
    df = df[df['is_renovated'] == str(f_renovated)]
    df = df[df['suggested_selling_price'] <= f_suggested_price]
    df = df[df['min_selling_price'] <= f_minimum_price]
    df = df[df['max_budget_improvement'] <= f_max_improvement]
    df = df[df['expected_profit'] <= f_suggested_profit]
    df = df[df['min_profit'] <= f_min_profit]
    
    return df

def map_overview(df,geofile):
    c1,c2= st.columns([1,1])
    c1.subheader('Portfolio Density')
    c2.subheader('Buying Price Density')
    density_map = folium.Map( location=[df['lat'].mean(), df['long'].mean() ], default_zoom_start=15)
    marker_cluster = MarkerCluster().add_to( density_map )
    for index, row in df.iterrows():
        folium.Marker(location=[ row['lat'],row['long'] ], popup="Buying Price $:{0} \n\n Number of bedrooms: {1} \n\n Number of bathrooms: {2} \n\n \
        Number of floors: {3} \n\n Waterfront: {4} \n\n Condition: {5} \n\n House Age: {6}".format(row['buying_price'],row['bedrooms'], 
        row['bathrooms'], row['floors'], row['is_waterfront'], row['condition_type'], row['house_age'], end='\n\n'),
        icon=folium.Icon(color='orange',icon='home') ).add_to(marker_cluster)
    
    with c1: 
        folium_static(density_map, width=550,height=450)
    
    
    buying_price_map = folium.Map(location=[df['lat'].mean(), df['long'].mean()], default_zoom_start=15)
    df_buying_price = df[['buying_price', 'zipcode']].groupby('zipcode').median().reset_index()
    df_buying_price.columns = ['ZIPCODE','PRICE']
    df_buying_price['ZIPCODE'] = df_buying_price['ZIPCODE'].astype('str')
    geofile_buying_price = geofile[geofile['ZIPCODE'].isin(df_buying_price['ZIPCODE'].tolist() )]
    buying_price_map.choropleth(geo_data = geofile_buying_price,data=df_buying_price, columns=['ZIPCODE', 'PRICE'],key_on='feature.properties.ZIPCODE', fill_color='YlOrRd', 
        fill_opacity=.7,line_opacity=.2, legend_name='Median Buying Price')
    folium.GeoJson( geofile_buying_price.merge(df_buying_price,on='ZIPCODE'),tooltip=folium.GeoJsonTooltip(fields=['ZIPCODE','PRICE'],
    aliases=['zipcode', 'Median Buying Price $'], labels=True,sticky=False) ).add_to(buying_price_map)
    
    with c2:
        folium_static(buying_price_map, width=550,height=450)
    
    d1,d2 = st.columns([1,1])
    d1.subheader('Selling Price Density')
    d2.subheader('Profit Density')
       
    selling_price_map = folium.Map(location=[df['lat'].mean(), df['long'].mean()], default_zoom_start=15)
    df_selling_price = df[['suggested_selling_price', 'zipcode']].groupby('zipcode').median().reset_index()
    df_selling_price.columns = ['ZIPCODE','PRICE']
    df_selling_price['ZIPCODE'] = df_selling_price['ZIPCODE'].astype('str')
    geofile_selling_price = geofile[geofile['ZIPCODE'].isin(df_selling_price['ZIPCODE'].tolist() )]
    
    selling_price_map.choropleth(geo_data = geofile_selling_price,data=df_selling_price, columns=['ZIPCODE', 'PRICE'],key_on='feature.properties.ZIPCODE', fill_color='YlOrRd', 
        fill_opacity=.7,line_opacity=.2, legend_name='Suggested Buying Price Median')
    
    folium.GeoJson( geofile_selling_price.merge(df_selling_price,on='ZIPCODE'),tooltip=folium.GeoJsonTooltip(fields=['ZIPCODE','PRICE'],
    aliases=['zipcode', 'Suggested Buying Price Median $'], labels=True,sticky=False) ).add_to(selling_price_map)
    
    with d1:
        folium_static(selling_price_map, width=550,height=450)

    profit_price_map = folium.Map(location=[df['lat'].mean(), df['long'].mean()], default_zoom_start=15)
    df_profit_price = df[['expected_profit', 'zipcode']].groupby('zipcode').median().reset_index()
    df_profit_price.columns = ['ZIPCODE','PRICE']
    df_profit_price['ZIPCODE'] = df_profit_price['ZIPCODE'].astype('str')
    geofile_profit_price = geofile[geofile['ZIPCODE'].isin(df_profit_price['ZIPCODE'].tolist() )]
    
    profit_price_map.choropleth(geo_data = geofile_profit_price,data=df_profit_price, columns=['ZIPCODE', 'PRICE'],key_on='feature.properties.ZIPCODE', 
    fill_color='YlOrRd', fill_opacity=.7,line_opacity=.2, legend_name='Profit Median')
    
    folium.GeoJson( geofile_profit_price.merge(df_profit_price,on='ZIPCODE'),tooltip=folium.GeoJsonTooltip(fields=['ZIPCODE','PRICE'],
    aliases=['zipcode', 'Profit Median $'], labels=True,sticky=False) ).add_to(profit_price_map)
    
    with d2:
        folium_static(profit_price_map, width=550,height=450)
            
    return None

    
if __name__ == '__main__':
    data_raw = data_collect('datasets/kc_house_data.csv')
    geofile = get_geofile(url='https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson')
    data_processing = data_transform(data_raw)
    df = data_load(data_processing)
    st.dataframe(df.style.format(precision=2,thousands=','))
    map_overview(df, geofile)
    


    
