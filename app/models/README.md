
## train_model.py

Script that trains a model using training_data generated from preprocess.py

To train a model, run

```
python train_data.py <model type flag> <input file type flag>
```

Model flags
- -dt, Decesion Tree Regressor
- -rf, Random Forest Regressor
- -xgb, Gradient Boosted Regressor

Output file types
- -x, excel
- -c, csv
- -j, json

