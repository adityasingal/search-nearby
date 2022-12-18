# search-nearby

In this project, I have implemented the ‘search nearby’ feature of Google maps to search for restaurants close to you in python. 
I noted that the list of restaurants remains fairly unchanged over time, while ‘search nearby’ queries are much more frequent. Therefore, it makes sense to pre-process the list of restaurants and create an appropriate data structure that enables processing ‘search nearby’ queries much faster than a brute-force search (assuming the number of “nearby” restaurants is much smaller than the total number of restaurants, which is typically the case).
I used the concept of 2 Dimensional Range Trees to x-sort and y-sort the coordinates and return query searches in O(m+log2 n) time.
This method is faster than the approach using K-D trees.
