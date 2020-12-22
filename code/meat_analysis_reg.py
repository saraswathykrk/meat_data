# -*- coding: utf-8 -*-
"""Meat_analysis_reg.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZNtQ71j6OGT5mbiZMnnjz8GPDZMQgZBu

<img src="https://github.com/saraswathykrk/meat_data/blob/main/images.jpeg?raw=true" width="630" height="450" />

# LINEAR REGRESSION

## Table of Content

1. [Problem Statement](#section1)<br>
2. [Data Loading and Description](#section2)<br>
3. [Exploratory Data Analysis](#section3)<br>
4. [Introduction to Linear Regression](#section4)<br>
    - 4.1 [Linear Regression Equation with Errors in consideration](#section401)<br>
        - 4.1.1 [Assumptions of Linear Regression](#sectionassumptions)<br>
    - 4.2 [Preparing X and y using pandas](#section402)<br>
    - 4.3 [Splitting X and y into training and test datasets](#section403)<br>
    - 4.4 [Linear regression in scikit-learn](#section404)<br>
    - 4.5 [Interpreting Model Coefficients](#section405)<br>
    - 4.3 [Using the Model for Prediction](#section406)<br>
5. [Model evaluation](#section5)<br>
    - 5.1 [Model evaluation using metrics](#section501)<br>
    - 5.2 [Model Evaluation using Rsquared value.](#section502)<br>
6. [Feature Selection](#section6)<br>
7. [Handling Categorical Features](#section7)<br>

<a id=section1></a>

## 1. Goal

1.   __Total_CO2_emission__ (in metric tonnes) for a particular country as a __function__ of __Total Meat Consumption__ (in tonnes).
2.   __Total_water_use__ (in litres) for a particular country as a __function__ of __Total Meat Consumption__ (in tonnes).
3.   __Total_land_use__ (in hectares) for a particular country as a __function__ of __Total Meat Consumption__ (in tonnes).


- We have to find a function that, given the input for each country (i.e., the predicted values for the next 13/14 years) for __Total_Meat_Consumption__, __predicts the output Total_CO2_emission, Total_water_use, Total_land_use__.

- Visualize the __relationship__ between the _input features_ and the _output response_ using scatter plots.

<a id=section3></a>

## 2. Data Loading and Description

The dataset captures Total_CO2_emission generated, Total_land_use, Total_water_use for each country and its relation to the Total_Meat_Consumption.
- Total_Meat_Consumption        
- Total_CO2_emission
- Total_population
- Total_land_use
- Total_water_use

__Importing Packages__
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
from sklearn import metrics
import numpy as np
from sklearn.preprocessing import StandardScaler
from matplotlib.pylab import rcParams
# allow plots to appear directly in the notebook
# %matplotlib inline
#from google.colab import files
import os
import shutil

# Supress Warnings

import warnings
warnings.filterwarnings('ignore')

"""#### Importing the Dataset"""

dataset_final = pd.read_csv('top_25_countries_predictions.csv')
dataset_final.head()

dataset1 = dataset_final.copy()
dataset2 = dataset_final.copy()


filter = dataset2['Year']>2018

dataset2.where(dataset2['Year']>2017, inplace = True)

list_countries = dataset2['Entity'].dropna().unique().tolist()
print('list of countries:',list_countries)
#list_countries = ['China','Canada']


curr_dir = os.getcwd()
reg_dict = {}

excel = False

for country_name in list_countries:


    path = os.path.join(curr_dir,country_name)
    print(path,curr_dir)


    if not os.path.exists(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)           # Removes all the subdirectories!
        os.makedirs(path)

    os.chdir(path)

    data1 = dataset_final.loc[dataset_final.Entity == country_name].copy()
    data1 = data1.sort_values(by=['Year'], ascending=True)

    data_year = data1.copy()

    data1 = data1.drop(["Year"], axis = 1)

    data = data1.copy()
    data_bkup = data1.copy()

    data = data[:-14]
    data.tail()

    """What are the **features**?
    - Total_Meat_Consumption: Total_Meat_Consumption for a country for the past 50 years and predicted values for the next ten years (in tonnes)

    What is the **response**?
    - Total_CO2_emission: Total_CO2_emission for a country (in tonnes)
    - Total_land_use: Total_land_use for a country (in hectares)
    - Total_water_use: Total_water_use for a country (in litres)

    <a id=section3></a>

    ## 3. Exploratory Data Analysis
    """

    data.shape

    data.info()

    data.describe()

    """There are 57 **observations**, which we will use for training the model and remaining 14 years predicted values of **Total_Meat_Consumption**, we will use for predicting the __Total_CO2_emission__, __Total_water_use__, __Total_land_use__ for the country.

    __Distribution of Features__
    """

    rcParams['figure.figsize']  =  10, 5

    sns_plot = sns.histplot(data.Total_population, color="b")
    sns_plot.figure.savefig(country_name + "_Total_population.png")

    sns_plot = sns.histplot(data.Total_Meat_Consumption, color="r")
    sns_plot.figure.savefig(country_name + "_Total_Meat_Consumption.png")

    sns_plot = sns.histplot(data.Total_water_use, color="g")
    sns_plot.figure.savefig(country_name + "_Total_water_use.png")

    sns_plot = sns.histplot(data.Total_land_use, color="m")
    sns_plot.figure.savefig(country_name + "_Total_land_use.png")

    sns_plot = sns.histplot(data.Total_CO2_emission, color="y")
    sns_plot.figure.savefig(country_name + "_Total_CO2_emission.png")

    """### Is there a relationship between Total_CO2_emission and Total_Meat_Consumption, between Total_land_use and Total_Meat_Consumption, and between Total_water_use and Total_Meat_Consumption?"""

    sns_plot  = sns.jointplot("Total_Meat_Consumption", "Total_water_use", data=data, kind='reg')
    sns_plot.savefig(country_name + "_Meat_Water.png")

    sns_plot =  sns.jointplot("Total_Meat_Consumption", "Total_land_use", data=data, kind='reg')
    sns_plot.savefig(country_name + "_Meat_land.png")

    sns_plot =  sns.jointplot("Total_Meat_Consumption", "Total_CO2_emission", data=data, kind='reg')
    sns_plot.savefig(country_name + "_Meat_CO2.png")

    """__Observation__<br/>
    _Total_CO2_emission and Total_Meat_Consumption_ is __not__ highly correlated.
    _Total_water_use and Total_Meat_Consumption_ is highly correlated.
    _Total_land_use and Total_Meat_Consumption_ is correlated.

    ### Visualising Pairwise correlation
    """

    sns_plot = sns.pairplot(data, height = 2, aspect = 1.5)
    sns_plot.savefig(country_name + "_PAIR_PLOT.png")

    sns_plot = sns.pairplot(data, hue = "Total_Meat_Consumption")
    sns_plot.savefig(country_name + "_PAIR_PLOT1.png")

    sns_plot = sns.pairplot(data,hue="Total_Meat_Consumption", diag_kind="hist")
    sns_plot.savefig(country_name + "_PAIR_PLOT2.png")

    sns_plot = sns.pairplot(data,kind="kde")
    sns_plot.savefig(country_name + "_PAIR_PLOT3.png")

    sns_plot = sns.pairplot(data, kind = 'hist')
    sns_plot.savefig(country_name + "_PAIR_PLOT4.png")

    sns_plot = sns.pairplot(
        data,
        x_vars=["Total_population","Total_Meat_Consumption"],
        y_vars=["Total_population","Total_Meat_Consumption","Total_CO2_emission", "Total_land_use","Total_water_use"],
    )
    sns_plot.savefig(country_name + "_PAIR_PLOT5.png")

    sns_plot = sns.pairplot(data, corner=True)
    sns_plot.savefig(country_name + "_PAIR_PLOT6.png")

    sns_plot = sns.pairplot(
        data,
        plot_kws=dict(marker="+", linewidth=1),
        diag_kws=dict(fill=False),
    )
    sns_plot.savefig(country_name + "_PAIR_PLOT7.png")

    g = sns.pairplot(data, diag_kind="kde")
    g.map_lower(sns.kdeplot, levels=4, color=".2")
    g.savefig(country_name + "_PAIR_PLOT8.png")




    sns_plot = sns.pairplot(data, x_vars=["Total_population","Total_Meat_Consumption"],
        y_vars=["Total_population","Total_Meat_Consumption"],
        height=4, aspect=1, kind='reg')
    sns_plot.savefig(country_name + "_PAIR_PLOT_REG1.png")

    sns_plot = sns.pairplot(data, x_vars=["Total_water_use","Total_Meat_Consumption"],
        y_vars=["Total_water_use","Total_Meat_Consumption"],
        height=4, aspect=1, kind='reg')
    sns_plot.savefig(country_name + "_PAIR_PLOT_REG2.png")

    sns_plot = sns.pairplot(data, x_vars=["Total_land_use","Total_Meat_Consumption"],
        y_vars=["Total_land_use","Total_Meat_Consumption"],
        height=4, aspect=1, kind='reg')
    sns_plot.savefig(country_name + "_PAIR_PLOT_REG3.png")

    sns_plot = sns.pairplot(data, x_vars=["Total_CO2_emission","Total_Meat_Consumption"],
        y_vars=["Total_CO2_emission","Total_Meat_Consumption"],
        height=4, aspect=1, kind='reg')
    sns_plot.savefig(country_name + "_PAIR_PLOT_REG4.png")
    """__Observation__

    - Strong relationship between Total_Meat_Consumption ads and Total_CO2_emission
    - Weak relationship between Total_Meat_Consumption and Total_land_use
    - Strong relationship between Total_Meat_Consumption and Total_water_use
    - Weak relationship between Total_Meat_Consumption and Total_population

    ### Calculating and plotting heatmap correlation
    """
    

    data.corr()
    plt.clf()

    rcParams['figure.figsize']  =  10, 10

    fig = plt.figure(figsize=(10, 8))
    plt.tight_layout()
    #fig, ax = plt.subplots(figsize=(10,8))  
    fig.subplots_adjust(left=0.3)
    ax1 = fig.add_axes([0.2,0.2,0.7,0.7])
   
    heat_map = sns.heatmap( data.corr(), square = True, annot=True, ax=ax1,linewidths=.5);
    heat_map.set_xticklabels(heat_map.get_xticklabels(), rotation=45);
    heat_map.set_yticklabels(heat_map.get_yticklabels(), rotation=45);
    plt.savefig(country_name + "_HEAT_MAP.png")

    

    """__Observation__

    - The diagonal of the above matirx shows the auto-correlation of the variables. It is always 1. You can observe that the correlation between __Total_Meat_Consumption and Total_CO2_emission is high, i.e. 0.96__ and then between __Total_Meat_Consumption and Total_water_use is 1__ and between __Total_Meat_Consumption and Total_population is 0.92__ and between __Total_Meat_Consumption and Total_land_use is also 1__.

    - Correlations can vary from -1 to +1. Closer to +1 means strong positive correlation and close -1 means strong negative correlation. Closer to 0 means not very strongly correlated. variables with __strong correlations__ are mostly probably candidates for __model building__.

    <a id=section4></a>

    ## 4. Introduction to Linear Regression

    __Linear regression__ is a _basic_ and _commonly_ used type of __predictive analysis__.  The overall idea of regression is to examine two things: 
    - Does a set of __predictor variables__ do a good job in predicting an __outcome__ (dependent) variable?  
    - Which variables in particular are __significant predictors__ of the outcome variable, and in what way they do __impact__ the outcome variable?  

    These regression estimates are used to explain the __relationship between one dependent variable and one or more independent variables__.  The simplest form of the regression equation with one dependent and one independent variable is defined by the formula :<br/>
    $y = \beta_0 + \beta_1x$

    What does each term represent?
    - $y$ is the response
    - $x$ is the feature
    - $\beta_0$ is the intercept
    - $\beta_1$ is the coefficient for x


    Three major uses for __regression analysis__ are: 
    - determining the __strength__ of predictors,
        - Typical questions are what is the strength of __relationship__ between _dose and effect_, _Total_CO2_emission and Total_Meat_Consumption_, or _age and income_.
    - __forecasting__ an effect, and
        - how much __additional Total_CO2_emission is released__ for each additional 1000 tonnes increase in Meat consumption for each country?
        - how much __additional land has been used__ for each additional 1000 tonnes increase in Meat consumption for each country?
        - how much __additional water has been used__ for each additional 1000 tonnes increase in Meat consumption for each country?
    - __trend__ forecasting.
        - what will the __Total_CO2_emission__ be for the next _10 years_?
        - what will the __Total_land_use__ be for the next _10 years_?
        - what will the __Total_water_use__ be for the next _10 years_?

    <a id=section401></a>

    ### 4.1 Linear Regression Equation with Errors in consideration

    Generally speaking, coefficients are estimated using the **least squares criterion**, which means we are find the line (mathematically) which minimizes the **sum of squared residuals** (or "sum of squared errors"):

    How do the model coefficients relate to the least squares line?
    - $\beta_0$ is the **intercept** (the value of $y$ when $x$ = 0)
    - $\beta_1$ is the **slope** (the change in $y$ divided by change in $x$)

    <a id = sectionassumptions></a>

    #### 4.1.1 Assumptions of Linear Regression

    1. There should be a linear and additive relationship between dependent (response) variable and independent (predictor) variable(s). A linear relationship suggests that a change in response Y due to one unit change in X¹ is constant, regardless of the value of X¹. An additive relationship suggests that the effect of X¹ on Y is independent of other variables.
    2. There should be no correlation between the residual (error) terms. Absence of this phenomenon is known as Autocorrelation.
    3. The independent variables should not be correlated. Absence of this phenomenon is known as multicollinearity.
    4. The error terms must have constant variance. This phenomenon is known as homoskedasticity. The presence of non-constant variance is referred to heteroskedasticity.
    5. The error terms must be normally distributed.

    <a id=section402></a>

    ## 5. Predicting Total_CO2_emission

    ### 5.1 Preparing X and y using pandas for Total_CO2_emission

    - __Standardization__. <br/>
    Standardize features by removing the _mean_ and scaling to _unit standard deviation_.
    """

    data = data1.drop(["Entity","Total_population",	"Total_land_use","Total_water_use"], axis = 1)
    data.head()

    scaler = StandardScaler().fit(data)
    data1 = scaler.transform(data)
    #data1 = data.copy()

    data = pd.DataFrame(data1)
    data.tail()


    data.columns = ['Total_Meat_Consumption','Total_CO2_emission']
    data.head()

    feature_cols = ['Total_Meat_Consumption']              # create a Python list of feature names
    X = data[feature_cols]                            # use the list to select a subset of the original DataFrame-+

    """- Checking the type and shape of X."""

    print(type(X))
    print(X.shape)

    y = data.Total_CO2_emission
    y.head()

    """- Check the type and shape of y"""

    print(type(y))
    print(y.shape)

    """<a id=section403></a>

    ### 5.2 Splitting X and y into training and test datasets.
    """

    X_train = X[:-14]
    X_test = X[-14:]
    y_train = y[:-14]
    y_test = y[-14:]

    #X_train, X_test, y_train, y_test=split(X,y)
    print('Train cases as below')
    print('X_train shape: ',X_train.shape)
    print('y_train shape: ',y_train.shape)
    print('\nTest cases as below')
    print('X_test shape: ',X_test.shape)
    print('y_test shape: ',y_test.shape)

    """<a id=section404></a>

    ### 5.3 Linear regression in scikit-learn

    To apply any machine learning algorithm on your dataset, basically there are 4 steps:
    1. Load the algorithm
    2. Instantiate and Fit the model to the training dataset
    3. Prediction on the test set
    4. Calculating Root mean square error 
    The code block given below shows how these steps are carried out:<br/>

    ``` from sklearn.linear_model import LinearRegression
        linreg = LinearRegression()
        linreg.fit(X_train, y_train) 
        RMSE_test = np.sqrt(metrics.mean_squared_error(y_test, y_pred_test))```
    """

    def linear_reg( X, y, gridsearch = False):
        
        X_train, X_test, y_train, y_test = X[:-14],X[-14:],y[:-14],y[-14:]

        from sklearn.linear_model import LinearRegression
        linreg = LinearRegression()
        
        if not(gridsearch):
            linreg.fit(X_train, y_train) 

        else:
            from sklearn.model_selection import GridSearchCV
            parameters = {'normalize':[True,False], 'copy_X':[True, False]}
            linreg = GridSearchCV(linreg,parameters, cv = 10)
            linreg.fit(X_train, y_train)                                                           # fit the model to the training data (learn the coefficients)
            print("Mean cross-validated score of the best_estimator : ", linreg.best_score_)  
            
            y_pred_test = linreg.predict(X_test)                                                   # make predictions on the testing set

            RMSE_test = (metrics.mean_squared_error(y_test, y_pred_test))                          # compute the RMSE of our predictions
            print('RMSE for the test set is {}'.format(RMSE_test))

        return linreg


    X = data['Total_Meat_Consumption']
    y = data.Total_CO2_emission
    X = X.values.reshape(-1, 1)
    y = y.values.reshape(-1, 1)
    linreg = linear_reg(X,y)

    """<a id=section405></a>

    ### 5.4 Interpreting Model Coefficients
    """

    print('Intercept:',linreg.intercept_)                                           # print the intercept 
    print('Coefficients:',linreg.coef_)
    
    CO2_intercept = linreg.intercept_[0]
    CO2_coeff = linreg.coef_[0][0]
    

    """Its hard to remember the order of the feature names, we so we are __zipping__ the features to pair the feature names with the coefficients"""

    feature_cols.insert(0,'Intercept')
    coef = linreg.coef_.tolist()
    coef.insert(0, linreg.intercept_)

    eq1 = zip(feature_cols, coef)

    for c1,c2 in eq1:
        print(c1,c2)

    """__y = 0.67148542 + 1.685238646105934 `*` Total_Meat_Consumption__

    How do we interpret the Total_Meat_Consumption coefficient (_1.6852_)
    - A "unit" increase in Total_Meat_Consumption is **associated with** a _"1.6852_ unit" increase in Total_CO2_emission.
    - Or more clearly: An additional 1,000 tonne increase on Total_Meat_Consumption is **associated with** an increase in Total_CO2_Emission of 1685.2 widgets.

    Important Notes:
    - This is a statement of __association__, not __causation__.
    - If an increase in Total_Meat_Consumption was associated with a __decrease__ in Total_CO2_emission,  β1  would be __negative.__

    ### 5.5 Using the Model for Prediction
    """

    y_pred_train = linreg.predict(X_train)

    y_pred_test = linreg.predict(X_test)                                                         # make predictions on the testing set
    y_pred_test

    """**Visualizing the fit on the dataset**"""

    inv_df_train = pd.DataFrame(X_train.values,columns = ['Total_Meat_Consumption'])
    inv_df_train.insert(1,'y_pred',y_pred_train)
    
    inversed_train = scaler.inverse_transform(inv_df_train)
    

    inv_df_test = pd.DataFrame(X_test.values,columns = ['Total_Meat_Consumption'])
    inv_df_test.insert(1,'y_pred',y_pred_test)
    
    inversed_test = scaler.inverse_transform(inv_df_test)


    plt.clf()
    plt.scatter(X_train,y_train,color='yellow')
    plt.plot(X_train, CO2_intercept + CO2_coeff * X_train, 'b')
    plt.plot(X_test, CO2_intercept + CO2_coeff * X_test, 'r')
    plt.savefig(country_name + '_Total_CO2_reg.png')

    """**Inserting into the dataframe for output csv**"""

    """**Creating the dataframe for output csv**"""

    #x = np.arange(1,10,1).reshape(-1,1)
    df_train=pd.DataFrame(data_year['Year'][:-14])
    df=pd.DataFrame(data_year['Year'][-14:])

    df_train.insert(0, 'Entity', country_name)
    df_train.insert(1,'Total_Meat_Consumption',inversed_train[:,[0]],True)
    df_train.insert(2,'Total_CO2_emission',inversed_train[:,[1]],True)
    df_train

    df.insert(0, 'Entity', country_name)
    df.insert(1,'Total_Meat_Consumption',inversed_test[:,[0]],True)
    df.insert(2,'Total_CO2_emission',inversed_test[:,[1]],True)
    df

    """**- We need an evaluation metric in order to compare our predictions with the actual values.**"""

    #So lets again split our train and test using only X_train and y_train
    X_train = X_train[:-10]
    X_test = X_train[-10:]
    y_train = y_train[:-10]
    y_test = y_train[-10:]

    y_pred_train = linreg.predict(X_train)
    y_pred_test = linreg.predict(X_test)

    """<a id=section5></a>

    ### 5.5 Model evaluation

    __Error__ is the _deviation_ of the values _predicted_ by the model with the _true_ values.<br/>

    Below are the types of error we will be calculating for our _linear regression model_:
    - Mean Absolute Error
    - Mean Squared Error
    - Root Mean Squared Error

    <a id=section501></a>

    #### 5.5.1 Model Evaluation using __metrics.__

    __Mean Absolute Error__ (MAE) is the mean of the absolute value of the errors:
    $$\frac 1n\sum_{i=1}^n|y_i-\hat{y}_i|$$
    Computing the MAE for our Total_CO2_emission predictions
    """

    MAE_train = metrics.mean_absolute_error(y_train, y_pred_train)
    MAE_test = metrics.mean_absolute_error(y_test, y_pred_test)

    print('MAE for training set is {}'.format(MAE_train))
    print('MAE for test set is {}'.format(MAE_test))

    """__Mean Squared Error__ (MSE) is the mean of the squared errors:
    $$\frac 1n\sum_{i=1}^n(y_i-\hat{y}_i)^2$$

    Computing the MSE for our Total_CO2_emission predictions
    """

    MSE_train = metrics.mean_squared_error(y_train, y_pred_train)
    MSE_test = metrics.mean_squared_error(y_test, y_pred_test)

    print('MSE for training set is {}'.format(MSE_train))
    print('MSE for test set is {}'.format(MSE_test))

    """__Root Mean Squared Error__ (RMSE) is the square root of the mean of the squared errors:

    $$\sqrt{\frac 1n\sum_{i=1}^n(y_i-\hat{y}_i)^2}$$

    Computing the RMSE for our Total_CO2_emission predictions
    """

    RMSE_train = np.sqrt( metrics.mean_squared_error(y_train, y_pred_train))
    RMSE_test = np.sqrt(metrics.mean_squared_error(y_test, y_pred_test))

    print('RMSE for training set is {}'.format(RMSE_train))
    print('RMSE for test set is {}'.format(RMSE_test))

    """Comparing these metrics:

    - __MAE__ is the easiest to understand, because it's the __average error.__ 
    - __MSE__ is more popular than MAE, because MSE "punishes" larger errors.
    - __RMSE__ is even more popular than MSE, because RMSE is _interpretable_ in the "y" units.
        - Easier to put in context as it's the same units as our response variable.

    <a id=section502></a>

    #### 5.5.2 Model Evaluation using Rsquared value.

    - There is one more method to evaluate linear regression model and that is by using the __Rsquared__ value.<br/>
    - R-squared is the **proportion of variance explained**, meaning the proportion of variance in the observed data that is explained by the model, or the reduction in error over the **null model**. (The null model just predicts the mean of the observed response, and thus it has an intercept and no slope.)

    - R-squared is between 0 and 1, and higher is better because it means that more variance is explained by the model. But there is one shortcoming of Rsquare method and that is **R-squared will always increase as you add more features to the model**, even if they are unrelated to the response. Thus, selecting the model with the highest R-squared is not a reliable approach for choosing the best linear model.

    There is alternative to R-squared called **adjusted R-squared** that penalizes model complexity (to control for overfitting).
    """

    feature_cols = ['Total_Meat_Consumption']                                                          # create a Python list of feature names
    X = data[feature_cols][:-14]  
    y = data.Total_CO2_emission[:-14]

    X_train, X_test, y_train, y_test = X[:-10],X[-10:],y[:-10],y[-10:]

    X_train = X_train.values.reshape(-1,1)
    X_test = X_test.values.reshape(-1,1)
    y_train = y_train.values.reshape(-1,1)
    y_test = y_test.values.reshape(-1,1)

    yhat = linreg.predict(X_train)
    SS_Residual = sum((y_train-yhat)**2)
    SS_Total = sum((y_train-np.mean(y_train))**2)
    r_squared = 1 - (float(SS_Residual))/SS_Total
    adjusted_r_squared = 1 - (1-r_squared)*(len(y_train)-1)/(len(y_train)-X_train.shape[1]-1)
    print(r_squared, adjusted_r_squared)

    yhat = linreg.predict(X_test)
    SS_Residual = sum((y_test-yhat)**2)
    SS_Total = sum((y_test-np.mean(y_test))**2)
    r_squared = 1 - (float(SS_Residual))/SS_Total
    adjusted_r_squared = 1 - (1-r_squared)*(len(y_test)-1)/(len(y_test)-X_test.shape[1]-1)
    print(r_squared, adjusted_r_squared)

    """<a id=section6></a>

    ### 6. __Total_Land_use__

    ### 6.1 Preparing X and y using pandas
    """

    data = data_bkup.copy()
    data = data.drop(["Entity","Total_population",	"Total_CO2_emission","Total_water_use"], axis = 1)
    data.head()

    scaler = StandardScaler().fit(data)
    data1 = scaler.transform(data)
    data = pd.DataFrame(data1)
    data.tail()

    data.columns = ['Total_Meat_Consumption','Total_land_use']
    data.head()

    feature_cols = ['Total_Meat_Consumption']              
    X = data[feature_cols]
    print(type(X))
    print(X.shape)

    y = data.Total_land_use
    y.head()

    print(type(y))
    print(y.shape)

    """### 6.2 Splitting X and y into training and test datasets."""

    X_train = X[:-14]
    X_test = X[-14:]
    y_train = y[:-14]
    y_test = y[-14:]

    #X_train, X_test, y_train, y_test=split(X,y)
    print('Train cases as below')
    print('X_train shape: ',X_train.shape)
    print('y_train shape: ',y_train.shape)
    print('\nTest cases as below')
    print('X_test shape: ',X_test.shape)
    print('y_test shape: ',y_test.shape)

    """### 6.3 Performing Linear Regression"""

    X = data['Total_Meat_Consumption']
    y = data.Total_land_use
    X = X.values.reshape(-1, 1)
    y = y.values.reshape(-1, 1)
    linreg = linear_reg(X,y)

    """### 6.4 Interpreting Model Coefficients"""

    print('Intercept:',linreg.intercept_)                                           # print the intercept 
    print('Coefficients:',linreg.coef_)

    land_intercept = linreg.intercept_[0]
    land_coeff = linreg.coef_[0][0]

    """__y = 0.69900332 + 1.75430078 `*` Total_land_use__

    How do we interpret the Total_Meat_Consumption coefficient (1.7543)

    A "unit" increase in Total_Meat_Consumption is associated with a "1.7543 unit" increase in Total_land_use.

    ### 6.5 Using the Model for Prediction
    """

    y_pred_train = linreg.predict(X_train)
    y_pred_test = linreg.predict(X_test)

    """**Visualizing the fit on the dataset**"""

    inv_df_train = pd.DataFrame(X_train.values,columns = ['Total_Meat_Consumption'])
    inv_df_train.insert(1,'y_pred',y_pred_train)
    
    inversed_train = scaler.inverse_transform(inv_df_train)
    

    inv_df_test = pd.DataFrame(X_test.values,columns = ['Total_Meat_Consumption'])
    inv_df_test.insert(1,'y_pred',y_pred_test)
    
    inversed_test = scaler.inverse_transform(inv_df_test)


    plt.clf()
    plt.scatter(X_train,y_train,color='yellow')
    plt.plot(X_train, land_intercept + land_coeff * X_train, 'b')
    plt.plot(X_test, land_intercept + land_coeff * X_test, 'r')
    plt.savefig(country_name + '_Total_land_use_reg.png')

    """**Inserting into the dataframe for output csv**"""

    df_train.insert(3, 'Total_land_use', inversed_train[:,[1]],True)
    df.head()

    df.insert(3, 'Total_land_use', inversed_test[:,[1]],True)
    df.head()

    #So lets again split our train and test using only X_train and y_train, as we need to evaluate the model
    X_train = X_train[:-10]
    X_test = X_train[-10:]
    y_train = y_train[:-10]
    y_test = y_train[-10:]

    y_pred_train = linreg.predict(X_train)
    y_pred_test = linreg.predict(X_test)

    """### 6.6 Model evaluation

    #### 6.6.1 Computing the **MAE** for Total_land_use predictions
    """

    MAE_train = metrics.mean_absolute_error(y_train, y_pred_train)
    MAE_test = metrics.mean_absolute_error(y_test, y_pred_test)
    print('MAE for training set is {}'.format(MAE_train))
    print('MAE for test set is {}'.format(MAE_test))

    """#### 6.6.2 Computing the **MSE** for Total_land_use predictions"""

    MSE_train = metrics.mean_squared_error(y_train, y_pred_train)
    MSE_test = metrics.mean_squared_error(y_test, y_pred_test)
    print('MSE for training set is {}'.format(MSE_train))
    print('MSE for test set is {}'.format(MSE_test))

    """#### 6.6.3 Computing the **RMSE** for Total_land_use predictions"""

    RMSE_train = np.sqrt( metrics.mean_squared_error(y_train, y_pred_train))
    RMSE_test = np.sqrt(metrics.mean_squared_error(y_test, y_pred_test))
    print('RMSE for training set is {}'.format(RMSE_train))
    print('RMSE for test set is {}'.format(RMSE_test))

    """### 6.7 Model Evaluation using Rsquared value."""

    feature_cols = ['Total_Meat_Consumption']                                                          # create a Python list of feature names
    X = data[feature_cols][:-14]  
    y = data.Total_land_use[:-14]

    X_train, X_test, y_train, y_test = X[:-10],X[-10:],y[:-10],y[-10:]

    X_train = X_train.values.reshape(-1,1)
    X_test = X_test.values.reshape(-1,1)
    y_train = y_train.values.reshape(-1,1)
    y_test = y_test.values.reshape(-1,1)

    yhat = linreg.predict(X_train)
    SS_Residual = sum((y_train-yhat)**2)
    SS_Total = sum((y_train-np.mean(y_train))**2)
    r_squared = 1 - (float(SS_Residual))/SS_Total
    adjusted_r_squared = 1 - (1-r_squared)*(len(y_train)-1)/(len(y_train)-X_train.shape[1]-1)
    print(r_squared, adjusted_r_squared)

    yhat = linreg.predict(X_test)
    SS_Residual = sum((y_test-yhat)**2)
    SS_Total = sum((y_test-np.mean(y_test))**2)
    r_squared = 1 - (float(SS_Residual))/SS_Total
    adjusted_r_squared = 1 - (1-r_squared)*(len(y_test)-1)/(len(y_test)-X_test.shape[1]-1)
    print(r_squared, adjusted_r_squared)

    """### 7. __Total_water_use__

    ### 7.1 Preparing X and y using pandas
    """

    data = data_bkup.copy()
    data = data.drop(["Entity","Total_population",	"Total_CO2_emission","Total_land_use"], axis = 1)
    data.head()

    scaler = StandardScaler().fit(data)
    data1 = scaler.transform(data)
    data = pd.DataFrame(data1)
    data.tail()

    data.columns = ['Total_Meat_Consumption','Total_water_use']
    data.head()

    feature_cols = ['Total_Meat_Consumption']              
    X = data[feature_cols]
    print(type(X))
    print(X.shape)

    y = data.Total_water_use
    y.head()

    print(type(y))
    print(y.shape)

    """### 7.2 Splitting X and y into training and test datasets."""

    X_train = X[:-14]
    X_test = X[-14:]
    y_train = y[:-14]
    y_test = y[-14:]

    #X_train, X_test, y_train, y_test=split(X,y)
    print('Train cases as below')
    print('X_train shape: ',X_train.shape)
    print('y_train shape: ',y_train.shape)
    print('\nTest cases as below')
    print('X_test shape: ',X_test.shape)
    print('y_test shape: ',y_test.shape)

    """### 7.3 Performing Linear Regression"""

    X = data['Total_Meat_Consumption']
    y = data.Total_water_use
    X = X.values.reshape(-1, 1)
    y = y.values.reshape(-1, 1)
    linreg = linear_reg(X,y)

    """### 7.4 Interpreting Model Coefficients"""

    print('Intercept:',linreg.intercept_)                                           # print the intercept 
    print('Coefficients:',linreg.coef_)

    water_intercept = linreg.intercept_[0]
    water_coeff = linreg.coef_[0][0]

    """__y = 0.69900332 + 1.75430078 `*` Total_water_use__

    How do we interpret the Total_Meat_Consumption coefficient (1.7543)

    A "unit" increase in Total_Meat_Consumption is associated with a "1.7543 unit" increase in Total_water_use.

    ### 7.5 Using the Model for Prediction
    """

    y_pred_train = linreg.predict(X_train)
    y_pred_test = linreg.predict(X_test)

    """**Visualizing the fit on the dataset**"""

    inv_df_train = pd.DataFrame(X_train.values,columns = ['Total_Meat_Consumption'])
    inv_df_train.insert(1,'y_pred',y_pred_train)
    
    inversed_train = scaler.inverse_transform(inv_df_train)
    

    inv_df_test = pd.DataFrame(X_test.values,columns = ['Total_Meat_Consumption'])
    inv_df_test.insert(1,'y_pred',y_pred_test)
    
    inversed_test = scaler.inverse_transform(inv_df_test)


    plt.clf()
    plt.scatter(X_train,y_train,color='yellow')
    plt.plot(X_train, water_intercept + water_coeff  * X_train, 'b')
    plt.plot(X_test, water_intercept + water_coeff  * X_test, 'r')
    plt.savefig(country_name + '_Total_water_use_reg.png')

    """**Inserting into the dataframe for output csv**"""

    df_train.insert(4, 'Total_water_use', inversed_train[:,[1]],True)
    df

    df.insert(4, 'Total_water_use', inversed_test[:,[1]],True)
    df

    #So lets again split our train and test using only X_train and y_train, as we need to evaluate the model
    X_train = X_train[:-10]
    X_test = X_train[-10:]
    y_train = y_train[:-10]
    y_test = y_train[-10:]

    y_pred_train = linreg.predict(X_train)
    y_pred_test = linreg.predict(X_test)

    """### 7.6 Model evaluation

    #### 7.6.1 Computing the **MAE** for Total_water_use predictions
    """

    MAE_train = metrics.mean_absolute_error(y_train, y_pred_train)
    MAE_test = metrics.mean_absolute_error(y_test, y_pred_test)
    print('MAE for training set is {}'.format(MAE_train))
    print('MAE for test set is {}'.format(MAE_test))

    """#### 7.6.2 Computing the **MSE** for Total_water_use predictions"""

    MSE_train = metrics.mean_squared_error(y_train, y_pred_train)
    MSE_test = metrics.mean_squared_error(y_test, y_pred_test)
    print('MSE for training set is {}'.format(MSE_train))
    print('MSE for test set is {}'.format(MSE_test))

    """#### 7.6.3 Computing the **RMSE** for Total_water_use predictions"""

    RMSE_train = np.sqrt( metrics.mean_squared_error(y_train, y_pred_train))
    RMSE_test = np.sqrt(metrics.mean_squared_error(y_test, y_pred_test))
    print('RMSE for training set is {}'.format(RMSE_train))
    print('RMSE for test set is {}'.format(RMSE_test))

    """### 7.7 Model Evaluation using Rsquared value."""

    feature_cols = ['Total_Meat_Consumption']                                                          # create a Python list of feature names
    X = data[feature_cols][:-14]  
    y = data.Total_water_use[:-14]

    X_train, X_test, y_train, y_test = X[:-10],X[-10:],y[:-10],y[-10:]

    X_train = X_train.values.reshape(-1,1)
    X_test = X_test.values.reshape(-1,1)
    y_train = y_train.values.reshape(-1,1)
    y_test = y_test.values.reshape(-1,1)

    yhat = linreg.predict(X_train)
    SS_Residual = sum((y_train-yhat)**2)
    SS_Total = sum((y_train-np.mean(y_train))**2)
    r_squared = 1 - (float(SS_Residual))/SS_Total
    adjusted_r_squared = 1 - (1-r_squared)*(len(y_train)-1)/(len(y_train)-X_train.shape[1]-1)
    print(r_squared, adjusted_r_squared)

    yhat = linreg.predict(X_test)
    SS_Residual = sum((y_test-yhat)**2)
    SS_Total = sum((y_test-np.mean(y_test))**2)
    r_squared = 1 - (float(SS_Residual))/SS_Total
    adjusted_r_squared = 1 - (1-r_squared)*(len(y_test)-1)/(len(y_test)-X_test.shape[1]-1)
    print(r_squared, adjusted_r_squared)

    """Since we are having high R-squared and adjusted R-squared values, the model is performing well.

    **Download the output csv file**
    """

    #files.download(country_name + '.csv')
    
    list_coeffs = [{'CO2_intercept':CO2_intercept},{'CO2_coeff':CO2_coeff},
                            {'land_intercept':land_intercept},{'land_coeff':land_coeff},
                            {'water_intercept':water_intercept},{'water_coeff':water_coeff}]

    reg_dict[country_name] = list_coeffs
    #print("dict:",reg_dict)

    os.chdir(curr_dir)
    if excel == False:
        df_train.to_csv('regression.csv')
        df.to_csv('regression.csv',mode='a', header=False)
        excel = True
    else:
        df_train.to_csv('regression.csv',mode='a', header=False)
        df.to_csv('regression.csv',mode='a', header=False)
    #writer.save()
print("dict:",reg_dict)
