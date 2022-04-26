from geopy.geocoders import Nominatim
import time
def collect_geodata(df,address_info_columns):
    geolocator = Nominatim(user_agent='my_application')
    
    lat_and_long = df[['lat', 'long']].apply(lambda x: [x['lat'],x['long']] , axis=1)
    index,row = lat_and_long.iteritems()
    time.sleep(2)
    
    response = geolocator.reverse(query=row)
    for i in range(len(address_info_columns)):
                   df[address_info_columns[i]] = response.raw['address'][address_info_column[i]] if address_info_columns in response.raw['address'] else 'NA'
    
    return df
    