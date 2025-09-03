# Texture Feature Interpretation and Analysis Notebooks

This repository contains functions for performing Haralick texture feature extraction on various different types of data, simulating texture, and analysing the results.

Feature Analysis with OCT and Slide Data- This notebook takes in a large number of preprocessed OCT and Slide data images, segments them, performs Haralick texture feature extraction on the segments and then performs analysis and provides visualization of the distribution of feature values and feature correlation.

GLCM_Visualization_and_Feature_Analysis- This notebook provides various techniques for GLCM and texture feature visualization and analyis. Among these- a function which takes an image and plots it side by side with its GLCM. For a given image the features can be calculated over a set number of pixels instead of the whole image- both convolutionaly and through reduction of resolution. Can also work with a set of images to extract the Haralick texture features from each, then order the images by feature value to provide visualization of the range of images across a linear sampling of the sensitivity of each feature, as well as correlation analysis based on the direction of GLCM calculation.

Real Data Preprocessing- This notebook can aid in the preproccessiong of H&E slide image data through with automated bright backgroud masking, and three dimensional optical coherence tomography through taking two dimensional slices at a designated number of pixels through the sample data.

Simulating_Texture- This notebook presents various different techniques for simulating texture over varying parameters.

Texture_Functions- This is a set of functions which are called upon by some of the other notebooks. The functions included are more generalized versions of the functions laid out in the GLCM_Visualization_and_Feature_Analysis notebook. 

Images Folder- This folder contains sample images from Optical Coherence Tomography datasets (OCTims) and H&E slide images before and after preprocessing (SlideTestSet) as well as a sample preprocessed slide image- Slidesampim.png, sample simulated texture image- Textim24.png and a file- greymap3.png to be used to make a color map for the visualization of GLCM's where there are often a lot of very small values and several larger ones. This color map dramatically reduces the contrast of the image to maximize the amount of values which are visible in an image.
