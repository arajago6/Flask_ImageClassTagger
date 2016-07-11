import os
import time
import optparse
from flask import Flask, render_template, request, redirect, session
from config.main_config import *
from boto.s3.connection import S3Connection
from boto.s3.key import Key
conn = S3Connection(AWS_S3_ACCESS_KEY, AWS_S3_SECRET_KEY)
bucket = conn.get_bucket(AWS_S3_BUCKET_NAME)

app = Flask(__name__, static_url_path = APP_STATIC_URL_PATH, static_folder = APP_STATIC_FOLDER)
app.secret_key = APP_SESSION_SECRET_KEY
home_path = AWS_S3_HOME_URL
folder_path = TARGET_DIRPATH_FROM_HOME


@app.route('/')
def index():
  try:
    print session['image_url'], session['info_placeholder']
  except KeyError:
    session['image_url'] = PDF_PLACEHOLDER_IMAGE_PATH 
    session['info_placeholder'] = INFO_PLACEHOLDER_DEFAULT
  return render_template('index.html', image_url=session['image_url'], info_placeholder=session['info_placeholder'])
  

@app.route('/clear')
def clearsession():
    session.clear()
    return redirect('/')


@app.route('/run', methods = ['POST'])
def adornot():
  try:
    if 'NOTAD' in request.form:
      key = bucket.get_key(session['image_url'].split(AWS_S3_BUCKET_NAME+"/")[1])
      key.get_contents_to_filename('notad.png')
      #bucket.delete_key(key)
      k = bucket.new_key("notads/%s-%s-%s.png" %(session['pdfname'][:-4],str(session['currfile']),str(session['currpage'])))
      k.set_contents_from_filename('notad.png')
      os.remove('notad.png')
    elif 'AD' in request.form:
      key = bucket.get_key(session['image_url'].split(AWS_S3_BUCKET_NAME+"/")[1])
      key.get_contents_to_filename('ad.png')
      #bucket.delete_key(key)
      k = bucket.new_key("ads/%s-%s-%s.png" %(session['pdfname'][:-4],str(session['currfile']),str(session['currpage'])))
      k.set_contents_from_filename('ad.png')
      os.remove('ad.png')
      
      
    numfiles = len(list(bucket.list(folder_path+session['pdfname'][:-4]+"/Page"+str(session['currpage'])+"/segmentedAds/","/")))
    if session['currfile'] < numfiles-1:
      session['currfile'] += 1
      session['image_url'] = home_path+session['pdfname'][:-4]+"/Page"+str(session['currpage'])+"/segmentedAds/"+str(session['currfile'])+".png"
      session['info_placeholder'] = "Input "+session['pdfname']+" has "+str(session['numpages'])+" page(s). Displaying file "+str(session['currfile'])+" from Page "+str(session['currpage'])+"..."
      if session['currfile'] == numfiles-1:
        session['currpage'] += 1
        session['currfile'] = -1
    else:
      session['image_url'] = PDF_PLACEHOLDER_IMAGE_PATH
      session['info_placeholder'] = INFO_PLACEHOLDER_DEFAULT
      
  except:
    pass
  
  return redirect('/')
  
