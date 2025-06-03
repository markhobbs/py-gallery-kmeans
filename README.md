# Introduction
Gallery search using Flask and sqllite, with a react uploader. OpenCV and Sklearn are used to detect the dominant colour of each file on upload. 

Additionally Image descriptions can be generated on the fly using clip & transformers. *Description generation is disabled by default *Enable feature flag within config.js.

# Setup Environment
python3 -m venv venv

Linux: source "venv/bin/activate" 

Windows: Call "venv/Script/activate.bat"


# Manual Install 
python3 -m pip install -r requirements.txt

python3 ./init.py

python3 ./run.py

# Import Bulk Images
cd ./static/demo
(Add your images)

Then run...http://localhost:5000/demo

(Will loop over the images and compute the colour)

# React Uploader
An additional React application has been provided as an additional form of upload.
cd react && yarn install && yarn start

# Automatic Descriptions 
Background Scheduled Image Description generated on upload *Enable feature flag within config.js 
!CUDA Enabled GPU Advised. Additional dependencies may be required for performance and specific to your ecosyste
