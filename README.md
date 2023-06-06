# WaterLevel
The goal of the project is to create an add-on for water bar that allows filling 
any container without predefining its capacity.

How It works:
1. Finding the upper threshold of the container using Canny edge detection.
2. Saving the matrix representing the empty container.
3. Finding the water level using canny edge detection. To reduce 'noise', a subtraction operation is performed between the initial matrix and the 
   current frame matrix.
4. When the distance between the upper threshold of the container and the water level reaches 70 pixels, the user receives an on-screen message 
   indicating that the pouring has finished.
