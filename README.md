# KC House Data Insights

The resulting app can be acessed [here](https://house-rocket-streamlit-project.herokuapp.com/)

## Project description and Business Problem

KC House is a company that makes money getting good opportunities of buying properties and sell them. It also may make improvements in some properties bought
to increase their values before selling. The issue arise in picking out such good opportunities to maximize their profit. It needs to know which houses to buy
and for how much it ought to sell them.

Therefore, the company would like to answer the following questions:

1) What properties we should buy?
2) After buying, which properties must need improvements and how much we could spend on these reforms?
3) When and for how much we sell them?

## Business assumptions

1) Region (zipcode), condition type and season were the most influent variables of property price.

## Dataset overview

The dataset used to deal with this case was avaliable at [Kraggle](https://www.kaggle.com/code/lucascapovilla/house-rocket/data). 
These are the variables in dataset: 

* id - Unique ID for each home sold
* date - Date of the home sale
* price - Price of each home sold
* bedrooms - Number of bedrooms
* bathrooms - Number of bathrooms, where .5 accounts for a room with a toilet but no shower
* sqft_living - Square footage of the apartments interior living space
* sqft_lot - Square footage of the land space
* floors - Number of floors
* waterfront - A dummy variable for whether the apartment was overlooking the waterfront or not
* view - An index from 0 to 4 of how good the view of the property was
* condition - An index from 1 to 5 on the condition of the apartment,
* grade - An index from 1 to 13, where 1-3 falls short of building construction and design, 7 as an average level of construction and design, and 11-13 have a high quality level of construction and design.
* sqft_above - The square footage of the interior housing space that is above ground level
* sqft_basement - The square footage of the interior housing space that is below ground level
* yr_built - The year the house was initially built
* yr_renovated - The year of the house’s last renovation
* zipcode - What zipcode area the house is in
* lat - Lattitude
* long - Longitude
* sqft_living15 - The square footage of interior housing living space for the nearest 15 eighbors
* sqft_lot15 - The square footage of the land lots of the nearest 15 neighbors

## Planning Soluction

* Business understanding
* Data understanding
* Data preparation
* Exploratory Data Analysis 

To define what houses to buy, we consider the following:

* If a house 
