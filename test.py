# Set paths for custom modules
import sys
sys.path.insert(0, './helpers')
sys.path.insert(0, './models')
from resnet50 import Resnet50_pretrained
from model_helpers import load_model
from model_helpers import predict

import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt    
import seaborn as sns
import glob
import os
import click

@click.command()
@click.option('--device', default='cpu', help='compute on cpu or cuda')
@click.option('--weights', default=None, help='{Path to Trained model weights')
@click.option('--data_csv', default=None, help='path to CSV dataset')
@click.option('--data_dir', default=None, help='directory where images are contained')
@click.option('--num_classes', default=1, help='number of classes to predict')
# @click.option('--path_format', default=dir, help='Verbose output')
# @click.option('--model', default=resnet50, help='Verbose output')
def test_model( device,weights,data_csv,data_dir,num_classes):
    # Define architecture
    res_model = Resnet50_pretrained(num_classes)
    # Load weights, set ready for prediction
    res_model = load_model(res_model, weights,True)

    # run prediction

    # Data
    test_df = pd.read_csv(data_csv)
    test_data_dir = data_dir
    paths = test_df["FilePath"]
    test_df["Label"] = pd.factorize(test_df["Label"])[0]
    true_labels = test_df["Label"].values.tolist()

    preds = []

    for path in paths:
        image = os.path.join(test_data_dir, path)
        print(image)
        preds.append(predict(res_model.model,image,device))

    print('\n---------------------------------------------')
    print('predicted values:\n')
    print(preds)
    print('\n---------------------------------------------')
    print('True Values\n')
    print(true_labels)

    cm = confusion_matrix(true_labels, preds)
    print('\n---------------------------------------------')
    print('Confusion Matrix:\n')
    print(cm)
  
    print('\n---------------------------------------------')
    print('Classification Report:\n')
    print(classification_report(true_labels, preds))

if __name__ == '__main__':
    test_model()