import pandas as pd
import numpy as np
from ast import literal_eval
from datetime import timedelta

# pet_pre_process takes petpy data and pre-processes for EDA, training, and predicting
# This function is meant to be used on training, test, and new data

def pet_pre_process(df):
    
    
    df = jlcap_pet_pull_dicts_from_cols(df)
    df = jlcap_pet_drop_columns(df)
    df = jlcap_pet_remove_duplicates(df)
    return df.set_index('id')




def jlcap_pet_pull_dicts_from_cols(df):
    
    data = df

    attributes = pd.DataFrame(data['attributes'].apply(literal_eval).tolist())

    breeds = pd.DataFrame(data['breeds'].apply(literal_eval).tolist())
    breeds.columns = ['breed_primary', 'breed_secondary', 'breed_mixed', 'breed_unknown']

    colors = pd.DataFrame(data['colors'].apply(literal_eval).tolist())
    colors.columns = ['color_primary', 'color_secondary', 'color_tertiary']

    environment = pd.DataFrame(data['environment'].apply(literal_eval).tolist())
    environment.columns = ['goodwith_children', 'goodwith_dogs', 'goodwith_cats']

    data = pd.concat([data, attributes, breeds, colors, environment], axis=1, join="outer")
    data.drop(columns=['attributes', 'breeds', 'colors', 'environment'], inplace=True)
    
    return data




def jlcap_pet_drop_columns(df):
    
    data = df
    
    data['hasimage'] = np.where(df['photos'] != '[]', True, False)
    data['hasvideo'] = np.where(df['videos'] != '[]', True, False)
    
    data.drop(columns=['type', 'species', 'primary_photo_cropped', 'photos', 'videos', '_links', 'organization_animal_id', 'tags', 'url', 'name', 'description', 'status', 'contact'], inplace=True)
    
    return data




def jlcap_pet_remove_duplicates(df):
    
    return df[~df['id'].duplicated()]



def jlcap_pet_add_cities(df):
    
    data = df
    
    orgs_wa = pd.read_csv('data/orgs_wa.csv', index_col='id')
    
    city_adopted = pd.DataFrame.to_dict(orgs_wa)['address.city']
    data['city'] = df['organization_id'].map(city_adopted)
    
    data.dropna(subset=['city'], inplace=True)
    data.drop(columns=['organization_id'], inplace=True)
    
    return data



def jlcal_pet_calculate_duration_as_adoptable(df):
    
    data = df
    
    dtformat = '%Y-%m-%d'

    data['published_at'] = pd.to_datetime(df['published_at'], format=dtformat)
    data['status_changed_at'] = pd.to_datetime(df['status_changed_at'], format=dtformat)
    
    time_before_adopted = data['status_changed_at'] - data['published_at']
    time_before_adopted_in_days = time_before_adopted / timedelta(days=1)
    data['duration_as_adoptable'] = time_before_adopted_in_days
    data = data[data['duration_as_adoptable'] > 0]
    
    print(data['duration_as_adoptable'].describe())
    
    data.drop(['published_at', 'status_changed_at'], axis=1, inplace=True)
    
    return data



def jlcap_pet_add_city_populations(df):
    
    data = df
    
    census = pd.read_csv('data/census_wa_cleaned.csv')
    census.set_index('index', inplace=True)
    census_pop = census.loc[:,'Total population']
    
    data = df.join(census_pop, on='city', how='left')
    data.rename(columns={'Total population':'population'}, inplace=True)
    
    return data