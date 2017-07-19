
**Project Luther Files and Folders**

* Webscraping weather data  

Codes: `Weather/Code/scrape_main.py` does the webscraping. `scrape_module.py` is the module that contains the helper functions for `scrape_main.py`.   
The scrpaed data is stored in the `Weather/ScrapedData` directory.

* Taxi data  
Csv files downloaded from the Chicago City Portal Site are stored in `Taxi/RawData/`.  
'Taxi/Code/cleanRawData.py' extracts relevant information from the cvs file and stores the information in `Taxi/CleanData/`

* Features  
`/Features/Code/bin_create_features.ipynb` computes features form the weather and taxi data and creates a feature matrix for regression analysis. The features for each month is stored in ``/Features/Data/`.

* Regression models  
`Models/` contains codes for Lasso and Ridge regression models (`model_1_lasso.ipynb`, `model_1_ridge.ipynb`).
