import numpy as np
import pandas as pd
import csv
import struct
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.font_manager import FontProperties
import matplotlib.ticker as tkr
import warnings
warnings.simplefilter('ignore')
matplotlib.rcParams.update({'font.size':14})

# from datetime import datetime, timedelta
import tensorflow as tf
from tensorflow import keras
import statistics as sts

from keras import Sequential
from keras.layers import Dense
from keras.optimizers import RMSprop, Adam
from keras import layers
from keras import regularizers
from sklearn.model_selection import train_test_split
from keras.models import Sequential, model_from_json
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint

from sklearn.preprocessing import LabelEncoder, StandardScaler, scale
from sklearn.decomposition import PCA

from datetime import datetime, timedelta