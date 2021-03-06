# -*- coding: utf-8 -*-
"""helper_functions.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NVca7aU5lIJv2l9LPoG-zd1RnnSFhgyf
"""

import tensorflow as tf

# function to unzip file into current working directory

import zipfile

def unzip_data(filename):
  """
  Args:
    filename (str) = a filepath to a target zip folder to be unzipped
  """
  zip_file = zipfile.ZipFile(filename, "r")
  zip_file.extractall()
  zip_file.close()

# function to explore image classification directory

import os

def walk_through_dir(dir_path):
  """
  Walk through dir_path returning its contents:
    number of subdirectories,
    name of each directory,
    number of files (images) in each directory
  """

  for dirpath, dirnames, filenames in os.walk(dir_path):
    print(f"There are {len(dirnames)} directories and {len(filenames)} images in '{dirpath}'")

# function to import an image and resize it to be able to fit in the model

def load_prep_image(filename,img_shape=224, scale=True):
  """
  Read an image from filename, turn it into a tensor, and reshape it to (img_shape, img_shape, color_channel)
  --
  Parameters:
  filename (str) : filename of target image
  img_shape (int) : size of target image to be resized
  scale (boolean) : whether to scale pixal values of image to range(0,1), default=True
  """
  # read image from the target file
  img = tf.io.read_file(filename)

  # decode image into tensor
  img = tf.image.decode_jpeg(img) # color_channels=3 by default in decode_jpeg

  # resize the image to the same size as the model has been trained on
  img = tf.image.resize(img, size=[img_shape, img_shape])

  # rescale the image
  if scale:
    return img/255.
  else:
    return img

# function to plot loss and accuracy curves

import matplotlib.pyplot as plt

def plot_loss_accuracy(history):
  """
  Return loss and accuracy plot separately

  Args:
    history = tensorflow model history
  """
  loss = history.history['loss']
  val_loss = history.history['val_loss']

  accuracy = history.history['accuracy']
  val_accuracy = history.history['val_accuracy']

  epochs = range(len(history.history['loss']))

  # plot loss
  plt.plot(epochs, loss, label='train_loss')
  plt.plot(epochs, val_loss, label='val_loss')
  plt.title('Loss Curves')
  plt.xlabel('Epochs')
  plt.legend()

  # plot accuracy
  plt.figure()
  plt.plot(epochs, accuracy, label='train_accuracy')
  plt.plot(epochs, val_accuracy, label='val_accuracy')
  plt.title('Accuracy Curves')
  plt.xlabel('Epochs')
  plt.legend()

# function to compare history of the model

def compare_historys(original_history, new_history, initial_epochs=5):
    """
    Compares two TensorFlow model History objects.
    
    Args:
      original_history: History object from original model (before new_history)
      new_history: History object from continued model training (after original_history)
      initial_epochs: Number of epochs in original_history (new_history plot starts from here) 
    """
    
    # Get original history measurements
    acc = original_history.history["accuracy"]
    loss = original_history.history["loss"]

    val_acc = original_history.history["val_accuracy"]
    val_loss = original_history.history["val_loss"]

    # Combine original history with new history
    total_acc = acc + new_history.history["accuracy"]
    total_loss = loss + new_history.history["loss"]

    total_val_acc = val_acc + new_history.history["val_accuracy"]
    total_val_loss = val_loss + new_history.history["val_loss"]

    # Make plots
    plt.figure(figsize=(8, 8))
    plt.subplot(2, 1, 1)
    plt.plot(total_acc, label='Training Accuracy')
    plt.plot(total_val_acc, label='Validation Accuracy')
    plt.plot([initial_epochs-1, initial_epochs-1],
              plt.ylim(), label='Start Fine Tuning') # reshift plot around epochs
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(2, 1, 2)
    plt.plot(total_loss, label='Training Loss')
    plt.plot(total_val_loss, label='Validation Loss')
    plt.plot([initial_epochs-1, initial_epochs-1],
              plt.ylim(), label='Start Fine Tuning') # reshift plot around epochs
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.xlabel('epoch')
    plt.show()

# function to create confusion matrix

import itertools
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix

def create_confusion_matrix(y_true, y_pred, classes=None, figsize=(10,10), text_size=15, norm=False, savefig=False):
  """
  Create a labelled confusion matrix, comparing prediction and actual labels.

  Args:
    y_true = array of actual labels
    y_pred = array of predicted labels (must be same as y_true in shape)
    classes = array of class labels. 'None' : matrix will use integer as labels
    figsize = size of confusion matrix figure
    text_size = size of figure text (default = 15)
    norm = whether to normalize values (default=False)
  
  Returns
    A labelled confusion matrix plot 

  Example Usage:
    create_confusion_matrix(y_true=test_labels,
                            y_pred=y_preds,
                            classes=class_names,
                            figsize=(15,15),
                            test_size=12)
  """
  # create confusion matrix
  cm = confusion_matrix(y_true, y_pred)
  cm_norm = cm.astype("float")/cm.sum(axis=1)[:, np.newaxis] # normalizing
  n_classes = cm.shape[0] # number of classes

  # plot the figure
  fig, ax = plt.subplots(figsize=figsize)
  cax = ax.matshow(cm, cmap=plt.cm.Blues)
  fig.colorbar(cax)

  # are there a list of classes?
  if classes:
    labels=classes
  else:
    labels = np.arange(cm.shape[0])
  
  # label the axes
  ax.set(title="Confusion Matrix",
         xlabel="Predicted Label",
         ylabel="True Labek",
         xticks=np.arange(n_classes),
         yticks=np.arange(n_classes),
         xticklabels=labels,
         yticklabels=labels)
  
  # Make x-axis label appears on bottom of figure
  ax.xaxis.set_label_position("bottom")
  ax.xaxis.tick_bottom()

  # rotate xticks for readability
  plt.xticks(rotation=70, fontsize=text_size)
  plt.yticks(fontsize=text_size)

  # Set the threshold for different colors
  threshold = (cm.max() + cm.min())/2

  # set up the cell text
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    if norm:
      plt.text(j, i, f"{cm[i, j]} ({cm_norm[i, j]*100:.1f}%)",
               horizontalalignment="center",
               color="white" if cm[i,j] > threshold else "navy",
               size=text_size)
    
    else:
      plt.text(j, i, f"{cm[i, j]}",
               horizontalalignment="center",
               color="white" if cm[i,j] > threshold else "navy",
               size=text_size)
  
  # save the figure to the current working directory
  if savefig:
    fig.savefig("Confusion_matrix.png")

# function to evaluate model prediction(accuracy, precision, recall, f1-score)

from sklearn.metrics import accuracy_score, precision_recall_fscore_support

def evaluate_prediction(y_true, y_pred):
  """
  Calculates model accuracy, precision, recall and f1 score of a binary classification model.

  Args:
      y_true: true labels in the form of a 1D array
      y_pred: predicted labels in the form of a 1D array

  Returns a dictionary of accuracy, precision, recall, f1-score.
  """

  # Calculate model accuracy
  model_accuracy = accuracy_score(y_true, y_pred) * 100

  # Calculate model precision, recall and f1 score using "weighted average
  model_precision, model_recall, model_f1, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted")
  model_evaluation = {"accuracy": model_accuracy,
                      "precision": model_precision,
                      "recall": model_recall,
                      "f1": model_f1}
  return model_evaluation

# function to predict images class and plot them (multiclass case)

def pred_view(model, filename, class_names):
  """
  Import an image from filename, predict the class name with a trained model
  and plot the image with the predicted class name
  """
  # import the image and preprocess it
  img = load_prep_image(filename)

  # make a prediction
  pred = model.predict(tf.expand_dims(img, axis=0))

  # get the predicted class name
  if len(pred[0]) > 1: # checking for multiclass classification
    pred_class = class_names[pred.argmax()] # the max value is the class
  else:
    pred_class = class_names[int(tf.round(pred)[0][0])] # for binary classification
  
  # plot the image and predicted class name
  plt.imshow(img)
  plt.title(f"Prediction: {pred_class}")
  plt.axis(False)

# function to create tensorboard callback

import datetime

def create_tensorboard_callback(dir_name, experiment_name):
  """
  Store log files with the filepath:
    "dir_name/experiment_name/current_datetime/"

  Args:
    dir_name = target directory to store tensorboard log files
    experiment_name = name of experiment directory
  """
  log_dir = dir_name + "/" + experiment_name + "/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
  tensorboard_callback = tf.keras.callbacks.TensorBoard(
      log_dir=log_dir
  )
  print(f"Saving Tensorboard log files to {log_dir}")
  return tensorboard_callback


# Function to compare 2 model's performances

def compare_baseline_to_new_model(baseline_evaluation, new_model_evaluation):
  for key, value in baseline_evaluation.items():
    print(f"Baseline {key}: {value:.2f}, New_model {key}: {new_model_evaluation[key]:.2f}, Difference: {new_model_evaluation[key]-value:.2f}")

  return model_evaluation
