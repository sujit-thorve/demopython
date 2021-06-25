# Copyright 2018 Google LLCdgdfgdfgfd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_render_template]
# [START gae_python3_render_template]




















import datetime
import hashlib
from flask import Flask, render_template
from google.cloud import datastore
import os
from flask import Blueprint, render_template
from flask import send_from_directory
from flask import request, redirect

project_id = os.getenv('GCLOUD_PROJECT')

app = Flask(__name__)


#bq_client = Client()
datastore_client = datastore.Client(project_id)
def save_question(question):
# TODO: Create a key for a Datastore entity
# whose kind is Question
    key = datastore_client.key('Question')
    

# END TODO

# TODO: Create a Datastore entity object using the key
    q_entity = datastore.Entity(key=key)
    

# END TODO

# TODO: Iterate over the form values supplied to the function

    for q_prop, q_val in question.items():

# END TODO

# TODO: Assign each key and value to the Datastore entity

        q_entity[q_prop] = q_val

# END TODO

# TODO: Save the entity

    datastore_client.put(q_entity)

# END TODO
	

'''@app.route('/')
def root():
    # For the sake of example, use static information to inflate the template.
    # This will be replaced with real information in later steps.
    dummy_times = [datetime.datetime(2018, 1, 1, 10, 0, 0),
                   datetime.datetime(2018, 1, 2, 10, 30, 0),
                   datetime.datetime(2018, 1, 3, 11, 0, 0),
                   ]

    return render_template('index.html', times=dummy_times)
'''

@app.route('/')
def root():
    return render_template('home.html')


@app.route('/add',methods=['GET', 'POST'])
def add():
    msg="msg"
    if request.method == 'GET':
        return render_template('add.html')
    elif request.method == 'POST':
        
        data = request.form.to_dict(flat=True)  
        #print(data['password'])
        password_salt = os.urandom(32).hex() 
        data['salt'] = password_salt
        password = data['password']  
        hash = hashlib.sha512()
        hash.update(('%s%s' % (password_salt, password)).encode('utf-8'))
        password_hash = hash.hexdigest()
        data['password'] =password_hash
        save_question(data)
        msg="Record added successfully"
        return render_template('add.html',msg=msg)
    else:
        msg="We cannot add the record"
        return render_template('add.html',msg=msg)

@app.route('/search',methods=['GET', 'POST'])
def fetch_employee():
    query = datastore_client.query(kind='Question')
    limit=5
    times=query.fetch(limit=limit)
    return render_template('index1.html',times=times)

@app.route('/find',methods=['GET', 'POST'])
def fetch_employee1():
    query = datastore_client.query(kind='Question')
    username1=request.form.get('username')
    times=query.add_filter("username", "=", username1).fetch(limit=1)
    return render_template('find.html',times=times)





if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
# [END gae_python3_render_template]
# [END gae_python38_render_template]
