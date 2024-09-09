# utils.py

import config
import re
import cv2
import glob
import math
import numpy as np
import sqlite3
import shutil
from sklearn.cluster import KMeans
from werkzeug.utils import secure_filename

if config.options['enable_autodesc']:
	from PIL import Image
	import torch
	# if torch.cuda.is_available():
	# print("GPU is available")
	import open_clip
	try:
		model, _, transform = open_clip.create_model_and_transforms(model_name="coca_ViT-L-14", pretrained="mscoco_finetuned_laion2B-s13B-b90k")
	except:
		print("Clip, something went wrong when download")
	finally:
		print("Clip, downloaded models")
	#else:
	#	print("GPU is not available")

def centroid_histogram(clt):
	# grab the number of different clusters and create a histogram
	# based on the number of pixels assigned to each cluster
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)
	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()
	# return the histogram
	return hist

def plot_colors(hist, centroids):
	# initialize the bar chart representing the relative frequency
	# of each of the colors
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0
	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
	    # plot the relative percentage of each cluster
	    endX = startX + (percent * 300)
	    cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
	        color.astype("uint8").tolist(), -1)
	    startX = endX
	# return the bar chart
	return bar

def get_bar(img):
	image = cv2.imread(img)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	image = image.reshape((image.shape[0] * image.shape[1], 3))
	clt = KMeans(n_clusters = config.options['clusters'])
	clt.fit(image)
	# utils.centroid_histogram(clt)
	# utils.plot_colors(hist, clt.cluster_centers_)
	hist = centroid_histogram(clt)  
	bar = plot_colors(hist, clt.cluster_centers_) 
	bar_unique_axis0 = np.unique(bar, axis=0)
	bar_unique_axis1 = np.unique(bar_unique_axis0, axis=1)
	return bar_unique_axis1

def get_db():
    conn = sqlite3.connect(config.filepaths['dbfile'])
    return conn

def get_description(img):
	if img:
		# if torch.cuda.is_available():
		im = Image.open(img).convert("RGB")
		im = transform(im).unsqueeze(0)
		with torch.no_grad(), torch.cuda.amp.autocast():
			generated = model.generate(im)
		return open_clip.decode(generated[0]).split("<end_of_text>")[0].replace("<start_of_text>", "")
		# else:
		#	print("GPU is not available")
		#	return img
	else:
		return "Image Required"

def get_files(search):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT `uid`, `filename`, `type`, `ext`, `colors`, `description`, `timestamp` FROM `images` WHERE `filename` LIKE ? OR description LIKE ? ORDER BY Timestamp DESC"
    if search != "": 
        cursor.execute(statement, ["%"+search+"%", "%"+search+"%"])
    else:
        cursor.execute(statement, ["%%", "%%"])
    results = cursor.fetchall()
    db.close()
    return results

def get_files_json():
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT `uid`, `filename`, `type`, `ext`, `description`, `timestamp` FROM `images` ORDER BY Timestamp DESC"
    cursor.execute(statement)
    results = cursor.fetchall()
    return [results]

def job_desc_empty(text):
	db = get_db()
	cursor = db.cursor()
	statement = "SELECT `uid`, `filename` FROM `images` WHERE `description` = ? ORDER BY Timestamp DESC Limit ?"
	cursor.execute(statement, ["pending", config.options['job_limit']])
	results = cursor.fetchall()
	for result in results:
		description = get_description(config.filepaths['gallery'] + result[1])
		statement = "UPDATE `images` SET `description` = ? WHERE uid = ?"
		cursor.execute(statement, [description, result[0]])
	db.commit()
	db.close()

def flatten(iterable, flattened):
	try:
		iter(iterable)
		for item in iterable:
			flatten(item, flattened)
	except:
		flattened.append(iterable)
	return flattened

def upload_file(data):
	savepath = config.filepaths['gallery'] + secure_filename(data.filename)
	data.save(savepath)
	bar = get_bar(savepath)

	if config.options['enable_autodesc']:
		description = "pending"
	else:
		description = data.filename
	db = get_db()
	cursor = db.cursor()
	statement = "INSERT INTO `images` (filename, type, ext, colors, description) VALUES (?, ?, ?, ?, ?)"
	cursor.execute(statement, [data.filename, 'image', 'jpg', bar, description])
	db.commit()
	db.close()

def upload_files():
	db = get_db()
	cursor = db.cursor()
	arr_uploaded = []
	for ext in ("jpg", "jpeg", "png", "gif", "webp"):
		for img in glob.iglob(config.filepaths['demo'] + '*.' + ext):
			filename = img.split('/')[3]
			bar = get_bar(img)
			if config.options['enable_autodesc']:
				description = "pending"
			else:
				description = filename
			statement = "INSERT INTO `images` (filename, type, ext, colors, description) VALUES (?, ?, ?, ?, ?)"
			cursor.execute(statement, [filename, 'image', ext, bar, description])
			shutil.copy(img, config.filepaths['gallery'])
			arr_uploaded.append(filename)
	db.commit()
	db.close()
	return arr_uploaded

def delete_file(uid):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM `images` WHERE uid = ?"
    cursor.execute(statement, [uid])
    db.commit()
    db.close()
    return [uid, "deleted"]
