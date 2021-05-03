# Texas Experimental Geometry Lab
This is the code repository for UT Austin's TXGL Project 2 (https://sites.cns.utexas.edu/geometry_lab/project-2)

In this project, we study the actions of SL2(R) matrix groups on RP1. Given a finitely presented group G, we want to algorithmically determine whether the homomorphism from G into one of these matric groups is faithful.

## Faithful Group Actions
A group action is considered faithful if there are no elements g in G for which gx = x other than the identity. We can naively check if the action of a group is non-faithful by recursively checking if any word made by the generators is the identity (search the Cayley graph until we find some product of generators which gives us 1). This method will not work if we are given a faithful group action though, since we will never find such a word.

## Ping Pong Lemma
<img src="./imgs/pingpong.jpg" width="400">
