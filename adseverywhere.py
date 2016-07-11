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
