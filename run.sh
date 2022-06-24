#!/usr/bin/env bash

if [[ $# -eq 0 ]] ; then
    echo 'Error - Please provide an output file name as an argument'
    exit 0
fi

var=$1

cd FeatureEngineering

python featureEngineer.py -c "$var"

cd -
cd PreProcessing

python preprocess.py -c "$var"

cd -
cd Modeling

python model.py -c "preprocessed_${var}"

open tree.png
