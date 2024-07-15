// Gmsh project created on Fri Dec 20 20:36:50 2019
SetFactory("OpenCASCADE");
Point(1) = {0, 0, 0, 1.0};
Point(2) = {1, 0, 0, 1.0};
Point(3) = {1, 1, 0, 1.0};
Point(4) = {0, 1, 0, 1.0};
Point(5) = {0, 0, 1, 1.0};
Point(6) = {1, 0, 1, 1.0};
Point(7) = {1, 1, 1, 1.0};
Point(8) = {0, 1, 1, 1.0};
Point(9) = {1, 1, 1, 1.0};
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Line(5) = {1, 5};
Line(6) = {2, 6};
Line(7) = {3, 7};
Line(8) = {4, 8};
Line(9) = {8, 7};
Line(10) = {7, 6};
Line(11) = {6, 5};
Line(12) = {5, 8};
Curve Loop(1) = {1, 2, 3, 4};
Surface(1) = {1};
Curve Loop(3) = {3, 8, 9, -7};
Surface(2) = {3};
Curve Loop(5) = {4, 5, 12, -8};
Surface(3) = {5};
Curve Loop(7) = {7, 10, -6, 2};
Surface(4) = {7};
Curve Loop(9) = {1, 6, 11, -5};
Surface(5) = {9};
Curve Loop(11) = {9, 10, 11, 12};
Surface(6) = {11};
Surface Loop(1) = {6, 2, 4, 5, 1, 3};
Volume(1) = {1};