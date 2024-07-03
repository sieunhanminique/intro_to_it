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

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model(r"D:\VGU\FY\HK2\IT\Project1\source\converted_keras\keras_model.h5", compile=False)

# Load the labels
class_names = open(r"D:\VGU\FY\HK2\IT\Project1\source\converted_keras\labels.txt", "r").readlines()

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
image = Image.open(r"D:\VGU\FY\HK2\IT\Project1\Test\3.jpg").convert("RGB")

# resizing the image to be at least 224x224 and then cropping from the center
size = (224, 224)
image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

# turn the image into a numpy array
image_array = np.asarray(image)

# Normalize the image
normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

# Load the image into the array
data[0] = normalized_image_array

# Predicts the model
prediction = model.predict(data)
index = np.argmax(prediction)
class_name = class_names[index]
confidence_score = prediction[0][index]

# Convert image to base64
stream = io.BytesIO();
image.save(stream, format="JPEG")
image_uploaded = base64.b64encode(stream.getvalue())

# Print prediction and confidence score
print("Class:", class_name[2:], end="")
print("Confidence Score:", confidence_score)

# Use it in your AI
client.publish("image", image_uploaded)
client.publish("nekotype", class_name[2:])
client.publish("neko", float(confidence_score)*100)