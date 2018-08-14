# Forum thingy

## Setup

You'll want to do a few things
* install python 2.x
* install pip for python 2.x
* install depencies
* initialize the database
* run the server

## Installing python 2.x and pip

If you use apt and have mirrors that host python and pip run the following:
```apt install python python-pip -y```
Otherwise google probably holds the how to install guide

## Install depencies

To install the depencies, we're using pip. Run the following:
```pip install -r requirements.txt```

## Run the server

It's a python script, by default when you clone from this repo it'll be running at [127.0.0.1](127.0.0.1)

```python app.py```