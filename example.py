from cifar import cifar_ready, cifar_load_train, cifar_load_test, cifar_load_labels, cifar_download
import numpy as np

# If the data is not ready (i.e. not downloaded)
if not cifar_ready():
    cifar_download() # Download the data

# Load training/test data and label names
X_train, y_train = cifar_load_train()
X_test, y_test = cifar_load_test()
labels = cifar_load_labels()

# Print some numbers...
print("Loaded training data with shape %s and %i classes" % (X_train.shape, len(np.unique(y_train))))
print("Loaded test data with shape %s and %i classes" % (X_test.shape, len(np.unique(y_train))))

print("The labels are defined as following:")
for i in range(0, len(labels)):
    print(" - %i: %s" % (i, labels[i]))