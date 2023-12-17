# Automated Segmentation of lumbar vertebral bodies into MRI using Mask R-CNN


This repository hosts my final paper in biomedical informatics, focused on leveraging cutting-edge computer vision and machine learning techniques to segment vertebral bodies. The study proposes the use of the Mask R-CNN Convolutional Neural Network architecture for the automated segmentation of lumbar vertebral bodies in MRI scans. This work was developed at the USP Faculty of Medicine in Ribeirão Preto, the images are not publicly available, but you can contact Prof Paulo if you need them pmarques@fmrp.usp.br

<img src="Examples\segmentation_model.gif">

# Mask R-CNN
Mask R-CNN is a versatile framework for segmenting object instances, capable of efficiently detect objects in images by generating high-performance segmentation masks quality for each instance

<img src="Examples\maskrcnn.png">

# Key Features

* Automated segmentation of lumbar vertebral bodies using Mask R-CNN.
* Application on MRI images from 63 postmenopausal female patients.
* Preprocessing includes 3D to 2D conversion, mask handling, and dimension correction.
* Model training and validation included.

# Results

* mAP (Mean Average Precision) of 0.92 for testing and 0.98 for validation.
* Dice validation scores of 0.88 for testing and 0.93 for validation.
* These metrics underscore the model's efficiency in this specific application.

  
