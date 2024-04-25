# EE4305
Author: Samuel EF. Tinnerholm<br />
Module: [EE4305 - Fuzzy/Neural Systems for Intelligent Robotics](https://nusmods.com/courses/EE4305/fuzzy-neural-systems-for-intelligent-robotics) <br>University: National University of Singapore

## From Feels to Keys - FUZZY SYSTEMS CRAFTING TUNES FROM NEURONS

### Abstract
This paper implements a fuzzy neural network model designed to generate piano music reflective of
specific emotional states input by a composer from scratch. The objective is to develop an intelligent system
where composers can adjust a few numerical values representing desired emotional outputs, and
consequently, the system generates music that embodies these emotions. This study explores the application
of fuzzy logic, which effectively handles degrees of truth, making it suitable for modelling the complex, often
non-binary nature of human emotions crucial for creating emotionally resonant music.

The methodology integrates emotional inputs using the Russell Circumplex Model, employing a
combination of fuzzy logic and LSTM neural networks to manage the temporal dynamics of music
composition. Despite the approach, the project did not fully achieve its objective of allowing composers to
simply alter numerical values to change the music’s emotional tone significantly, mostly due to the model’s
linear architecture.

To better meet the project's goals, alternative models with enhanced capabilities for handling user
generated inputs are recommended. Future work may include a focus on optimising these aspects to realise
the full potential of using AI in generating emotionally aligned music compositions.

### Repository Structure
The file system includes:
- **Scripts**: Contains all code including:
  - **Model Fitting**: `fit.ipynb` for adapting the model to data.
  - **Prediction**: `predict.ipynb` for generating future musical notes.
  - **Dataset**: EMOPIA-2.2 dataset information.
  - **Visuals**: Histograms and model architecture visualizations, with generation scripts.
  - **Model Selection**: Epoch-specific model weights.
- **Example WAVs**: Sample outputs named as 'Quadrant_exampleNumber'.

### Usage Instructions
To train the model, execute `fit.ipynb`. Parameters such as `random_files` can be modified for varied training.

To generate music, utilize `predict.ipynb`, with adjustable parameters including `emotions` and input content.

