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
2) Just bad condition type properties were worth making renovation.
3) If a house is in a bad condition, the company is going to spend money making improvements on it in order to sell them as good condition ones.

## Dataset overview

The dataset used to deal with this case was avaliable at [Kraggle](https://www.kaggle.com/code/lucascapovilla/house-rocket/data). 
These are the variables in dataset, including some created by feature engineering: 

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
* is_waterfront - A dummy variable for whether the property was overlooking the waterfront or not
* is_renovated - A dummy variable for whether the property was renovated or not
* season - Home sale season
* house_age -  A dummy variable for whether the property was new (built after 2010) or old.
* condition_type - The condition of house (bad,regular or good)
* decision - A dummy variable telling if a house would be bought or not.
* Minimum_selling_price - Minimium selling price for that property
* Suggested_selling_price - Suggested_selling_price for that property
* Minimum_profit - Minimium profit company would make selling that house
* Expected_profit - Expected Profit company would make selling house
* Max_improvement_cost - The maximum cost company should spent in renovating a house
* Min_profit_margin - Minimium profit margin company would make selling that house
* Expected_profit_margin - Expected Profit margin company would make selling house

## Planning Soluction

**Step 1.** Business understanding

**Step 2.** Data understanding

**Step 3.** Data preparation

**Step 4.** Exploratory Data Analysis

**Step 5.** Business Hypothesis testing

**Step 6.** Answering business questions

**Step 7.** App creation

**Step 8.** Checking results and conclusion

## Top insights

**H1: Properties which are in good and regular condition and was renovated is 20% more expensive, on median, than regular or good condition properties which was not.**

True. In fact, renovated good contition properties are 26% more expensive than the not renovated ones. This means that the company could acquire some non renovated houses, make some improvements on them that cost at most 13% of their selling price, for instance.

After that, selling them for 25% more than their selling price. Doing that they could make good profit

![image](https://user-images.githubusercontent.com/27966951/166744674-95ef4314-0c15-494e-8235-039c0b75ed01.png)

**H2: New houses without renovation is 15% more expensive, on median, than old renovated houses.**

False. Old renovation houses seems to be more worthy than new houses who has not been made improvements by approximately 10%. A house is considered new when it was built at least at 2010. It confirms that there are good opportunities in getting a old house for a lower price, making improvements on them and selling them with a higher price than new ones.

![image](https://user-images.githubusercontent.com/27966951/166745158-259fa058-712e-4d9a-abc9-3b2630880f9b.png)

**H3: Properties prices on spring is 15% higher than prices on summer, on median.**

False. Actually is approximately 4% higher than summer median. This could happen due to high demand after winter season. These season should have the highest company buying prices. The company could consider that there is no differences in prices between theses season and selling properties with same price.

![image](https://user-images.githubusercontent.com/27966951/166745423-d42dac76-be8b-492e-9216-4b7b4f13b5e7.png)

**H4: Properties prices on Spring is 10% higher than prices on autunm, on median.**

False. In fact, is approximately 7,32% higher than autumn median. Here, a suggestion is putting different selling prices for these seasons.

![image](https://user-images.githubusercontent.com/27966951/166745561-8dd1c1f8-5cf5-480e-927b-6f5fb0a9ee4a.png)

## Soluction proposal

To define what houses to buy, it was considered the following:

* **The company should buy houses that worth at most the 40th decile of properties price, which is calculated considering its region and its condition type.**

To limit how much company should spend renovating bad condition houses, it was proposed the following:

* **The company would spend at most the 30th decile of good condition properties of its region minus its buying price.**

To define for how much the property would be sell, it was considered two scenarios, a minimum selling price and a suggested selling price:

* Minimum Selling Price
  1) **If it is a bad condition house which is renovated, the selling price would be the 40th decile of good properties buying price of its region, considering the   season which the house will be selled as well.**
  2) **If it is a regular condition house, the selling price would be the median of regular properties buying price of its region, considering the season which the house will be selled as well.**
  3) **If it is a good condition house, the selling price would be the median of good properties buying price of its region, considering the season which the house will be selled as well.**

* Suggested Selling Price
  1) **If it is a bad condition house which is renovated, the selling price would be the median of good properties buying price of its region, considering the season which the house will be selled as well.**
  2) **If it is a regular condition house, the selling price would be the 60th decile of regular properties buying price of its region, considering the season which the house will be selled as well. In case there is no regular condition properties on sold in some region, will be considered the 40th decile of good condition properties buying prices of this region.**
  3) **If it is a good condition house, the selling price would be the 60th decile of good properties buying price of its region, considering the season which the house will be selled as well. In case there is no good condition properties on sold in some region, will be considered the 3rd quantile of regular condition properties buying prices of this region.**

To check how much profit company would make, it was considered two scenarios as well:

* **Minimum profit: The difference between the minimum selling price minus buying price of that property. It was calculated minimum profit margin as well.**
* **Expected profit The difference between the suggested selling price minus buying price of that property.  It was calculated expected profit margin as well.**

## Business results

It was found approximately 9000 out of nearly 22000 properties on sold that were suggested for buying them. The dataframe was sorted in descending order of expected profit margin. Considering selling houses on summer, if company get the 15 properties with the greatest expected profits margins, for instance, company would expect to make around $ 6,174,935 and a minimum profit of $ 5,241,350 selling these houses.

## Next steps

* Making a classification machine learning algorithm to detect more precisely which properties company should buy.
* Making a regression machine learning algorithm to define more precisely for how much properties should be sold.




