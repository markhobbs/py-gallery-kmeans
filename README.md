# Introduction
Gallery Search using Flask and sqllite, with a react uploader. Opencv and sklearn are used to detect the KMeans dominant colour of each file on upload. Additionally Image descriptions are generated on the fly using clip, transformers. Description generation is disabled by default enable in run.py* 

# Setup Environment
python3 -m venv venv

Linux: source "venv/bin/activate" 

Windows: Call "venv/Script/activate.bat"

# Manual Install 
python3 -m pip install -r requirements.txt

python3 ./init.py

python3 ./run.py

# Import Bulk Images
cd ./static/input
(Add your images)

Then run...http://localhost:5000/demo 
(Will loop over the images and compute the colour)

# React Uploader
An additional React application has been provided as an additional form of upload.
cd react && yarn install && yarn start

export NODE_OPTIONS=--openssl-legacy-provider

# Automatic Descriptions  
Enable feature flag within run.py 
(* Additional dependencies may be required for performance and specific to your ecosystem, ie CUDA for NVIDIA GPU)



