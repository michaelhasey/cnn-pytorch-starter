#%%
##########################
# Imports 
##########################

# import system libraries
import sys
import os
import glob

# import Data Libraries
import click
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt                        

# %matplotlib inline

# Set paths for custom modules
sys.path.insert(0, './helpers')
sys.path.insert(0, './models')

# Data Loader functions
from data_loader import dir_loader_stack
from data_loader import csv_loader_stack
from data_loader import image_plot
from data_loader import val_train_split

# Model classes
from resnet50 import Resnet50_pretrained

# Model helpers
from model_helpers import train
from model_helpers import predict
from model_helpers import plot_train_history

# torch
import torch.nn as nn
import torch.optim as optim
import torch

@click.command()
@click.option('--verbose', default=False, help='Verbose output')
@click.option('--device', default='cpu', help='compute on cpu or cuda')
@click.option('--num_classes', default=1, help='number of classes to predict')
@click.option('--n_epochs', default=3, help='number of epochs')
@click.option('--learn_rate', default=0.001, help='learning rate')
@click.option('--save_path', default=None, help='save path for model and history')
@click.option('--csv_labels', default=None, help='path to CSV dataset')
@click.option('--img_size', default=244, help='resize images')
@click.option('--batch_size', default=8, help='Batch size for training')
@click.option('--num_workers', default=0, help='num workers for pytorch')
@click.option('--data_dir', default=None, help='directory where images are contained')
def load_train(verbose, device, num_classes, n_epochs, learn_rate, save_path,
                csv_labels, img_size,batch_size, num_workers, data_dir):
    '''
    TODO: 
        - Doc string
        - model option in click
        - run folder check and create
    '''

    # Labels from CSV
    df_lab = pd.read_csv(csv_labels)

    # One hot encoding
    df_lab.Label = pd.Categorical(pd.factorize(df_lab.Label)[0])

    if verbose:
        print(f"df_lab shape:  {df_lab.shape}")

    # Create Train & Validation split
    train_df, val_df = val_train_split(df_lab, 0.2)

    # Create Data loaders
    train_loader = csv_loader_stack(data_dir,train_df, 'FilePath', 'Label',
                            img_size,batch_size,num_workers,True)

    val_loader = csv_loader_stack(data_dir,val_df, 'FilePath', 'Label',
                            img_size,batch_size,num_workers,False)

    loaders = {
        'train':train_loader,
        'valid':val_loader
    }
  
    # verify images before training
    if verbose: 
        # Train Data sample
        print("\nTraining images")
        image_plot(train_loader)

    if verbose: 
        # validation data sample
        print("\nValidation images")
        image_plot(val_loader)

    # Create model

    # create model from model class
    res_model = Resnet50_pretrained(num_classes)

    # Train Model
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(res_model.model.fc.parameters(), lr=learn_rate)
    # save_path = 'trained_models/test_train_tmp'

    # Train 
    H = train(res_model.model, n_epochs, loaders, optimizer,
                        criterion, device, save_path)
 
    if verbose:
        # Train Log
        plot_train_history(H,n_epochs)

if __name__ == '__main__':
    load_train()