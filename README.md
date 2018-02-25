Busy Street
===========

Project Description
-------------------
Have you ever tried to take that perfect Instagram photo, but every time your friend goes to take the picture someone walks in the way, or a car passes by? Busy Street is a tool that not only allows you to remove moving objects from your picture, but also offers a host of functionality such as choosing exactly which frame you want each object to be in.

Busy Street takes a video as input, but can also use a series of images. It uses an open source deep convolutional neural network model in order to identify objects in each frame. The algorithm uses a grid framework stacked on top of the image in order to narrow down where each object is. Thus, using a conventional predictive neural network it is able to find exactly where in an image an object is. We slightly modified the model so that we could pull rectangular object outlines directly into python. Then, across frames we are use our algorithm in order to match the same objects to each other. 

![alt text](/images/Copied.png)

This way, we worry much less about things like camera shake or background changes. In order to remove an object we don't have to create a background from a mode, instead we simply replace a single object with the background.

![alt text](/images/Removed.png)

Usage
-----

Build/Installation Instructions
-------------------------------
This project was built on a Mac. Darknet is supposed to have been also tested on Linux so it should work.

It requires the following python 2.7 dependencies
* numpy
* cv2 (opencv)
* matplotlib

After cloning the repository, in the code folder type 'make'. After that you should be able to use the vp.py file in order to process any video. Currently, this requires you to go in and change the current video in the file. The default should be alright though.

Also, you need some pretrained weights using

```
wget https://pjreddie.com/media/files/yolo.weights
```

Other Sources of Documentation
------------------------------
Please See [Darknet](https://github.com/pjreddie/darknet) for their documentation on its usage.
