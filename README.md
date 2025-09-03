# Texture Feature Interpretation and Analysis Notebooks

This repository contains functions for performing Haralick texture feature extraction on various different types of data, simulating texture, and analysing the results.

Feature Analysis with OCT and Slide Data- This notebook takes in a large number of preprocessed OCT and Slide data images, segments them, performs Haralick texture feature extraction on the segments and then performs analysis and provides visualization of the distribution of feature values and feature correlation.

GLCM_Visualization and Feature Analysis- This notebook provides various techniques for GLCM and texture feature visualization and analyis. Among these- a function which takes an image and plots it side by side with its GLCM. For a given image the features can be calculated over a set number of pixels instead of the whole image- both convolutionaly and through reduction of resolution. Can also work with a set of images to extract the Haralick texture features from each, then order the images by feature value to provide visualization of the range of images across a linear sampling of the sensitivity of each feature, as well as correlation analysis based on the direction of GLCM calculation.

Real Data Preprocessing- This notebook can aid in the preproccessiong of H&E slide image data through with automated bright backgroud masking, and three dimensional optical coherence tomography through taking two dimensional slices at a designated number of pixels through the sample data.
