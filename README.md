# Texas Experimental Geometry Lab
This is the code repository for UT Austin's TXGL Project 2 (https://sites.cns.utexas.edu/geometry_lab/project-2)

In this project, we study the actions of SL2(R) matrix groups on RP1. Given a finitely presented group G, we want to algorithmically determine whether the homomorphism from G into one of these matrix groups is faithful.

## Faithful Group Actions
A group action is considered faithful if there are no elements g in G for which gx = x for all x in X other than the identity. We can naively check if the action of a group is non-faithful by recursively checking if any word made by the generators is the identity (search the Cayley graph until we find some product of generators which gives us 1). This method will not work if we are given a faithful group action though, since we will never find such a word.

## Ping Pong Lemma
With the use of a lemma, we can solve this problem. The Ping Pong Lemma essentailly tells us that if we can find some collection of disjoint sets of RP1 depending on G, we are able to make a finite number of calculations to determine that the group action is faithful.

<p align='center'>
  <img src='./images/pingpong.JPG' width='600'>
</p>

Our algorithm can now search for these collections of intervals and then check the conditions of the lemma instead of using the brute force approach. There are some things we know about the intervals which lowers the number of cases we need to search but we will not enumerate all of them here. One example is that the intervals must contain the eigenvectors of the matrix generators.

Below is an example of such intervals in RP1 which contain the images of the other intervals. Since these are disjoint and we have full containment, we know that the matrices corresponding to these intervals generate a group with a faithful action on RP1.

<p align='center'>
  <img src='./images/good_intervals.JPG' width='400'>
</p>

## The Code
The main programs to look at in this repository are main.py and interface.py. To test the algorithm on a free group on n generators in main.py, change the line in main 'generators = free_group_generators(6, val = 0.5)' to include the number of generators you want followed by the range of values you want to appear in the randomly generated matrices. If you want a guided walkthrough of input options, use interface.py.

## Setting up Python / Jupyter Notebook (CURRENTLY UPDATING)
If you want to run the program for yourself but don't use Python or GitHub, follow these instructions:
  - Download the latest version of Python here: https://www.python.org/downloads/ (Be sure to click the checkbox 'ADD PYTHON TO PATH' when installing)
  - Open Command Prompt and type 'pip install jupyterlab'
  - Download the generalized_pingpong.ipynb file
  - In Command Prompt, type 'jupyter notebook' to open jupyter in your browser
  - Open the generalized_pingpong.ipynb file and run using the 'play all button'
