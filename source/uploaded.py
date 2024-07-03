from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import random
import time
import  sys
from  Adafruit_IO import  MQTTClient
import io
import base64

AIO_FEED_ID = ""
AIO_USERNAME = "minique"
AIO_KEY = "aio_Hydc43vpIiNzzzlFArPxFNdQ2iwB"

def  connected(client):
    print("Connected to the AIO server!!!!")
    client.subscribe(AIO_FEED_ID)

def  subscribe(client , userdata , mid , granted_qos):
    print("Subscribed to TOPIC!!!")

def  disconnected(client):
    print("Disconnected from the AIO server!!!")
    sys.exit (1)

def  message(client , feed_id , payload):
    print("Received: " + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

# create an in-memory file to store raw image data
stream = io.BytesIO()

# Replace this with the path to your image
image = Image.open(r"D:\VGU\FY\HK2\IT\Project1\Yellow\3.jfif",'r')

# resizing the image to be at least 224x224 and then cropping from the center
size = (800, 600)
image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)


# use Python Imaging Library to optimize the final image data
optim_stream = io.BytesIO()
image.save(optim_stream, format='jpeg', quality=70, optimize=True)
optim_stream.seek(0)

# convert image binary data to base64 string
value = base64.b64encode(optim_stream.read())

client.publish('image', value)