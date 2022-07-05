$fn = 100;

difference()
{
  cylinder(8,21,21);
  translate([0,0,6.5]) cylinder(10,19.5,19.5);
  translate([0,0,-2.5]) cylinder(19,11,11);
}

difference()
{
  cylinder(19.5,13,13);
  translate([0,0,18]) cylinder(19,11.5,11.5);
  translate([0,0,-2.5])Schaft();
}  

module Schaft()
{
  d = 3.075;
  cylinder(6.6,11.7/2,11.7/2);
  cylinder(8.5,4,4);
  difference()
  {
    cylinder(21,d, d);
    translate([d-(d/2),-10,10.5]) cube([20,20,20]);
  }
}  