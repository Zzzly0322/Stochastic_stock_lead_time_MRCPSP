************************************************************************
file with basedata            : md129_.bas
initial value random generator: 2013382565
************************************************************************
projects                      :  1
jobs (incl. supersource/sink ):
horizon                       :  111
RESOURCES
  - renewable                 :  2   R
  - nonrenewable              :  2   N
  - doubly constrained        :  0   D
************************************************************************
PROJECT INFORMATION:
pronr.  #jobs rel.date duedate tardcost  MPM-Time
    1     14      0       16       10       16
************************************************************************
PRECEDENCE RELATIONS:
jobnr.    #modes  #successors   successors
   1        1          3           2   3   4
   2        3          2           5   6
   3        3          2           6  10
   4        3          2          10  14
   5        3          3           7   8  12
   6        3          3           9  12  15
   7        3          3          10  11  15
   8        3          2           9  15
   9        3          2          11  13
  10        3          1          13
  11        3          1          14
  12        3          2          13  14
  13        3          1          16
  14        3          1          16
  15        3          1          16
  16        1          0        
************************************************************************
REQUESTS/DURATIONS:
jobnr. mode duration  R 1  R 2  N 1  N 2
------------------------------------------------------------------------
  1      1     0       0    0    0    0
  2      1     4      10    0    0    7
         2    10      10    0    3    0
         3    10      10    0    0    5
  3      1     5       0    4    0    3
         2     6       0    4    6    0
         3    10       5    0    6    0
  4      1     5       0    6    5    0
         2     9       3    0    0    8
         3    10       0    3    0    2
  5      1     2       0   10    4    0
         2     2       0    9    0    4
         3     7       0    8    0    3
  6      1     4       0    8    0    9
         2     5       7    0    0    5
         3     8       0    7    4    0
  7      1     2       9    0    2    0
         2     6       7    0    0    6
         3     7       4    0    1    0
  8      1     2       7    0    9    0
         2     4       6    0    2    0
         3     6       4    0    0    6
  9      1     2       5    0    0    3
         2     4       0    1    1    0
         3     6       4    0    1    0
 10      1     2       7    0    3    0
         2     5       0    4    2    0
         3    10       0    3    0    5
 11      1     2       5    0    7    0
         2     4       0    7    6    0
         3     5       0    5    0    3
 12      1     4       0    2    0    1
         2     4       0    2    7    0
         3     9       0    2    3    0
 13      1     2       0    7    9    0
         2     3       0    5    9    0
         3     5       2    0    8    0
 14      1     3       2    0    0    9
         2     6       0    4    0    4
         3     8       0    1    0    2
 15      1     2      10    0    2    0
         2     5      10    0    0    5
         3    10       0    4    2    0
 16      1     0       0    0    0    0
************************************************************************
RESOURCEAVAILABILITIES:
  R 1  R 2  N 1  N 2
   14   11   22   19
************************************************************************
