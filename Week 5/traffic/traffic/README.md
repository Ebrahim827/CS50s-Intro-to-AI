# Traffic Sign Classification - Experimentation

## What I tried:
I built a Convolutional Neural Network (CNN) to classify 43 types of road signs.

## Architecture:
- First Conv2D layer with 32 filters (3x3) and ReLU activation
- MaxPooling layer (2x2) to reduce dimensions
- Second Conv2D layer with 64 filters (3x3) and ReLU activation  
- Second MaxPooling layer (2x2)
- Flatten layer to convert to 1D
- Dense hidden layer with 128 units and ReLU activation
- Dropout layer (0.5) to prevent overfitting
- Output layer with 43 units and softmax activation

## Results:
- Accuracy improved each epoch from ~15% to ~95%
- Loss decreased consistently each epoch
- Final test accuracy around 95%

## What worked well:
- Two convolutional layers worked better than one
- Dropout prevented overfitting significantly
- Adam optimizer converged quickly