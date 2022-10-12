* Source:     Pyomo MPS Writer
* Format:     Free MPS
*
NAME unknown
OBJSENSE
 MIN
ROWS
 N  x3
 G  c_l_x4_
 G  c_l_x5_
 G  c_l_x6_
COLUMNS
     x1 x3 3
     x1 c_l_x4_ 2
     x1 c_l_x5_ 1
     x1 c_l_x6_ 1
     x2 x3 4
     x2 c_l_x4_ 1
     x2 c_l_x5_ 2
     x2 c_l_x6_ 1
RHS
     RHS c_l_x4_ 15
     RHS c_l_x5_ 17
     RHS c_l_x6_ 10
BOUNDS
 LO BOUND x1 0
 UP BOUND x1 10
 LO BOUND x2 0
 UP BOUND x2 10
ENDATA
