# Trade-Savante

This is a trading application that lets users perform networks as trades.

It uses the breadth first search algorithm and uses each of the items that
are to be traded as nodes.  The search algorithm can find cycles in the graphs
and using these cycles determing if a group of people can find trades.

The app was inspired by the person who started with a pencil and traded 
their way up to a house by incrementally trading for better items.

Note that edges are added by each user since they are asked what items
they would like in return for their item.  So the graph is directed.

The program is written in python and uses DJANGO.
