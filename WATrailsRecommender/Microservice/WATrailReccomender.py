import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image


# Load the csv file as a dataframe
df_labeled = pd.read_csv("labeled_hikes.csv")
df = pd.read_csv('hikes.csv')

# Reccomender
def reccomend(hike1, hike2, hike3, opt):
    hikes = [hike1, hike2, hike3]
    results = []
    for hike in hikes:
        # Get the label of the hike
        label = df_labeled[df_labeled["TITLE"] == hike]['LABEL'].values[0]
        # Find all other hikes with same label 
        same_labels = df_labeled[df_labeled["LABEL"] == label]
        if opt == 'random':
            res = same_labels.sample().TITLE.values[0]
            results.append(res)  
        else:
            res = same_labels[same_labels["DIFFICULTY"] == opt].sample().TITLE.values[0]
            results.append(res)  
    return results

def display_hike_info(hike):
    data = df[df.TITLE == hike]
    # Set up the dictionaries
    general_info = {}
    for feature in other_features:
        if data[feature].values[0] is not np.nan:
            general_info[feature] = data[feature].values[0]
        else:        
            general_info[feature] = None
    features_info = {}
    for feature in physical_features:
        if data[feature].values[0] == 1:
            features_info[feature] = feature.lower()
        else:
            features_info[feature] = None
    st.write("[%s](%s)" %(hike, general_info['URL']))

    # Write out the general features of trail
    if general_info["SPECIFIC REGION"] is None:
        st.write("* Location: %s" %(general_info['REGION']))
    else:
        st.write("* Location: %s -- %s" %(general_info['REGION'], general_info['SPECIFIC REGION']))
    if general_info['DISTANCE'] is not None:
        if general_info['DIST_TYPE'] == 'one-way':
            length = general_info['DISTANCE'] * 2
        else:
            length = general_info['DISTANCE']
        st.write("* Length: %d miles" %length)
    if general_info['GAIN'] is not None:
        st.write("* Elevation gain: %d ft." %general_info['GAIN'])
    if general_info['REQUIRED PASSES'] is not None:
        st.write("* Required pass: %s" %general_info['REQUIRED PASSES'])

    # Write out the physical features of trail 
    features = []
    for feature in features_info.keys():
        if features_info[feature] is not None:
            features.append(feature.lower())
    if len(features) > 0:
        features = ', '.join(features)
        st.write("* Features include: %s" %features)

def isNaN(num):
    return num != num
    
def get_avg_rating_subregion(region):
    ratings={}
    subregions = df[df["REGION"] == region]["SPECIFIC REGION"].unique()
    subregions = [x for x in subregions if not isNaN(x)]
    for region in subregions:
        avg = df[df["SPECIFIC REGION"] == region]['RATING'].mean()
        ratings[region] = avg
    return ratings

def get_top_n_hikes(df, k):
    most_pop = []
    df = df.dropna(axis=0, how='any', subset=['RATING', 'RATING_COUNT'])
    sorted_df = df.sort_values(by=['RATING']).sort_values(by=['RATING_COUNT'])
    return sorted_df.iloc[(k*-1)-1:-1]
        

# Set the page title and sidebar 
st.title("Washington Trails Reccomender")
st.sidebar.title("Input three trails below.")
hike1 = st.sidebar.selectbox("Hike 1", df_labeled['TITLE'].unique())
hike2 = st.sidebar.selectbox("Hike 2", df_labeled['TITLE'].unique())
hike3 = st.sidebar.selectbox("Hike 3", df_labeled['TITLE'].unique())
# Can set what type of hikes to be returned - a random one or most popular 
opt = st.sidebar.selectbox("Difficulty type", ["random", "easy", "moderate", "moderately strenuous", "strenuous", "very strenuous"])

other_features = ['REGION', 'SPECIFIC REGION', 'DISTANCE', 'DIST_TYPE', 'GAIN', 'REQUIRED PASSES', 'URL']
physical_features = ["COAST","RIVERS","LAKES","WATERFALLS","OLD GROWTH","FALL FOLIAGE","WILDFLOWERS/MEADOWS","MOUNTAIN VIEWS","SUMMITS","WILDLIFE","RIDGES"]

if st.sidebar.button('Reccomend me some trails!'):
    results = reccomend(hike1, hike2, hike3, opt)
    # Display the hikes on a map
    for hike in results:
        display_hike_info(hike)
        data = df[df.TITLE == hike]
        st.map(data)


# Main page
st.header("Looking to get outside?")
st.write("Use the sidebar to get some hikes reccomended to you based on trails \
    you've either hiked in the past and/or are interested in hiking in the future. If nothing \
    comes to mind, then check out some stats below to help you narrow your search down by region or simply get the most popular hikes.")
st.write("\n\n")

### Display plots
st.subheader("Distribution of hikes throughout WA")
st.map(df.dropna(axis=0, how='any', subset=['lat', 'lon']), zoom=4)
st.write('\n\n')

# Displaying regions and their avg rated hikes 
st.subheader("Average trail rating by region")
st.image("all_regions_avg.png")
st.write("\n\n")

# Display avg trail rating by subregion )
st.subheader("Average trail rating by subregion")
region = st.selectbox("Select a region", df_labeled['REGION'].unique())
if region:
    st.image('%s.png' %region)
st.write("\n\n")


# Display n most popular hikes
st.subheader("Top 10 rated trails in WA")
n = st.slider('Number of trails to be returned', min_value = 1, max_value=10)
if n:
    res = get_top_n_hikes(df, n)
    hikes = res['TITLE'].values
    for hike in reversed(hikes):
        display_hike_info(hike)        








        




