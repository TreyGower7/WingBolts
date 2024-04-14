import tensorflow as tf
import os
import random
from tensorflow.keras.layers import Rescaling

batch_size = 32

# splitting data
happy_paths = os.listdir('smiley_faces_dataset/happy')
sad_paths = os.listdir('smiley_faces_dataset/sad')

train_happy_paths = random.sample(happy_paths, int(len(happy_paths)*0.8))
test_happy_paths = [ p for p in happy_paths if p not in train_happy_paths]
# ensure no overlap:
overlap = [p for p in train_happy_paths if p in test_happy_paths]
print("len of happy overlap: ", len(overlap))


train_sad_paths = random.sample(sad_paths, int(len(sad_paths)*0.8))
test_sad_paths = [ p for p in sad_paths if p not in train_sad_paths]
# ensure no overlap:
overlap = [p for p in train_sad_paths if p in test_sad_paths]
print("len of sad overlap: ", len(overlap))

# ensure to copy the images to the directories
import shutil
for p in train_happy_paths:
    shutil.copyfile(os.path.join('smiley_faces_dataset/happy', p), os.path.join('smiley_faces_split/train/happy', p) )

for p in test_happy_paths:
    shutil.copyfile(os.path.join('smiley_faces_dataset/happy', p), os.path.join('smiley_faces_split/train/happy', p) )

for p in train_sad_paths:
    shutil.copyfile(os.path.join('smiley_faces_dataset/sad', p), os.path.join('smiley_faces_split/train/sad', p) )

for p in test_sad_paths:
    shutil.copyfile(os.path.join('smiley_faces_dataset/sad', p), os.path.join('smiley_faces_split/train/sad', p) )


img_height = 2488
img_width = 2685
batch_size = 8
train_data_dir = 'smiley_faces_split/train/'

# preprocessing
train_ds = tf.keras.utils.image_dataset_from_directory(
train_data_dir,
validation_split=0.2,
subset="training",
seed=123,
image_size=(img_height, img_width),
batch_size=batch_size
)

val_ds = tf.keras.utils.image_dataset_from_directory(
train_data_dir,
validation_split=0.2,
subset="validation",
seed=123,
image_size=(img_height, img_width),
batch_size=batch_size
)


rescale = Rescaling(scale=1.0/255)
train_rescale_ds = train_ds.map(lambda image,label:(rescale(image),label))
val_rescale_ds = val_ds.map(lambda image,label:(rescale(image),label))

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 1)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(2, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.summary()

#fit the model from image generator
model.fit(
            train_rescale_ds,
            batch_size=32,
            epochs=20,
            validation_data=val_rescale_ds
)