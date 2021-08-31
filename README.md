# apg_flask
Flask wrapper around the [audio program generator](https://github.com/jeffwright13/audio_program_generator) module

# Current status
beta+ ... meaning, it runs out of the box:
  - locally on my Macbook Pro w/ Catalina 10.15.7,
    with ffmpeg version 4.4 installed via homebrew;
  - on Heroku, with ffmpeg buildpack installed
    (https://elements.heroku.com/buildpacks/jonathanong/heroku-buildpack-ffmpeg-latest)
This code also runs on AWS Lambda but requires mods (see branch
"heroku" (2a4684c).

# Prerequisites
* Some relatively recent version of Python (3.7+)
* FFMPEG with at least the ability to read mp3s and wavs, and write mp3s

# Prep for execution
* clone the repo
* cd into it
* create a virtual environment
* pip install -r requirements.txt
* vi .env
* set your environment variables:
    * DEBUG=[True/False]

# Run locally (localhost)
* cd into top directory of repo
* flask run
* point browser at http://127.0.0.1:5000/
* fill out the form, submit, and wait for browser to serve up your freshly mixed mp3 file :-)

# Run on Heroku
* create new app on Heroku
* install ffmpeg buildpack as above
* point your app at the [apg_flask](https://github.com/jeffwright13/apg_flask) repo on GitHub
* deploy
* point browser at your app's url
* fill out the form, submit, and wait for browser to serve up your freshly mixed mp3 file :-)

# Process files in AWS using a task queue
* Checkout the `celery` branch (which branches off `lambda2`)
* Set the AWS\* env variables and install the additional requirements
* Run Celery: `celery -A app.tasks.celery worker --loglevel=info`
* To monitor tasks, run Flower: `celery -A app.tasks.celery flower`

# Author:
Jeff Wright <jeff.washcloth@gmail.com>
