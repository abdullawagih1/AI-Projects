import cv2
import numpy as np
import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import EfficientNetB3, preprocess_input as efficientnet_b3_preprocess_input

# Load Moedl
model = tf.keras.models.load_model("E:/Asta/META-Health team/Project/01/Data/EfficientNetB3-Brain Tumors-No.h5")

# Load File
uploaded_file = st.file_uploader("Choose An Image File", type=["jpg", "png", "jpeg"])

map_dict = {0: 'glioma_tumor',
            1: 'meningioma_tumor',
            2: 'no_tumor',
            3: 'pituitary_tumor'}


if uploaded_file is not None:
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(opencv_image,(224,224))

    # Now do something with the image! For example, let's display it:
    st.image(opencv_image, channels="RGB")

    resized = efficientnet_b3_preprocess_input(resized)
    img_reshape = resized[np.newaxis,...]

    Genrate_pred = st.button("Generate Prediction")    
    if Genrate_pred:
        prediction = model.predict(img_reshape).argmax()
        st.title("Predicted Label for the image is {}".format(map_dict [prediction]))