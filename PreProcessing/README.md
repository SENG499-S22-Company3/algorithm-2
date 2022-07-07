
## parseHistoricalData.py

Script the goes through the scraped historical data and filters out all unnecessary entries

To run

```
python parseHistoricalData.py
```

## preprocess.py

Script that does the feature engineering, one hot encoding, and imputation
Creates a data frame that can be used by the ../app/models/model.py script to train the models


To export the dataframe to a excel document:

```
python preprocess.py <output file type>
```
Output file types
- -x, excel
- -c, csv
- -j, json