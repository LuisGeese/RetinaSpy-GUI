import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.utils import to_categorical
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense



def preprocess_data(img_dir, target_size=(224, 224)):
    images = []
    labels = []
    for class_dir in os.listdir(img_dir):
        class_path = os.path.join(img_dir, class_dir)
        for image_file in os.listdir(class_path):
            image_path = os.path.join(class_path, image_file)
            label = 0 if class_dir == "No_DR" else 1
            image = load_img(image_path, target_size=target_size)
            image_array = img_to_array(image) / 255.0
            images.append(image_array)
            labels.append(label)
    return np.array(images), np.array(labels)



train_img_dir = "E:/Rentina_spy_codes/Data_base/Training_data_set"
val_img_dir = "E:/Rentina_spy_codes/Data_base/Validation_data_set"
test_img_dir = "E:/Rentina_spy_codes/Data_base/Testing_data_set"



train_images, train_labels = preprocess_data(train_img_dir)
val_images, val_labels = preprocess_data(val_img_dir)
test_images, test_labels = preprocess_data(test_img_dir)



train_labels = to_categorical(train_labels)
val_labels = to_categorical(val_labels)
test_labels = to_categorical(test_labels)



model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(2, activation='softmax')
])



model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])



model.fit(train_images, train_labels, epochs=10, batch_size=32, validation_data=(val_images, val_labels))



model.save("rentiaspy_brain.keras")



predicted_probabilities = model.predict(test_images)
predicted_classes = np.argmax(predicted_probabilities, axis=1)
true_classes = np.argmax(test_labels, axis=1)
