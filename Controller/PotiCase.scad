simple = true;
print = true;
Radius    = 10;
Wandung   = 2.5;
Tolleranz = -1.1;
Hoehe     = 15;
Breite    = 75;
Tiefe     = 30;
Versatz   = Wandung + Tolleranz;
Verschiebung = Wandung/2  ;
Snappos  = 4;
posx = 10;
$fn = 20;




 ViewCase();

module ViewCase()
{
  if (print)
  {
    // rotate([180,0,0]) Oberschale(); 
    rotate([180,0,0]) Kabelklemme();
     //Unterschale();
  }
  else
  {
    difference()
    {
      case();
       //translate([-10,-12,-10]) cube([300,14,100]);   // Schnitt A
       // translate([-20,-10,-10]) cube([45,450,100]);  // Schnitt B
      //translate([-10,-10,9]) cube([300,200,100]);   // Schnitt C 
    }
  }
}  

module case()
{
    Unterschale();
    translate([0,0 ,Snappos]) Oberschale();

}



module Oberschale()
{
  module Gehaeuse(size=[10,10,10])
  {
    aBreite = size[0];
    aTiefe = size[1];
    aSnappos = size[2];
    
    difference()
    {  
    linear_extrude(Hoehe-aSnappos) offset(r = Radius, $fn=40) square([aBreite+Versatz,aTiefe+Versatz]);
     
    translate([Wandung,Wandung,-Wandung]) linear_extrude(Hoehe-(aSnappos)) offset(r = Radius, $fn=20) square([aBreite+Tolleranz-Wandung,aTiefe+Tolleranz-Wandung]);  
      
    translate([Wandung,Wandung,0]) Snapin_B([aBreite+Tolleranz-Wandung,aTiefe+Tolleranz-Wandung,4.5], Feder = 0.8, Tolerance = 0.1, Offset = Radius, $fn=40);
    }
  }
  // translate([12.5,5.6,7.5]) cube([79,65.8,8]); 
   
    difference()
  {  
    union()
    {
      Gehaeuse([Breite, Tiefe, Snappos]);
      translate([Wandung+1,Wandung+posx-7,Wandung+2])  cube([10,20,4]);
    }
    translate([Wandung+6,Wandung+posx-4,Wandung+1])  cylinder(5,1,1);
    translate([Wandung+6,Wandung+posx+10,Wandung+1])  cylinder(5,1,1);
    translate([Verschiebung+Breite-Tiefe/2,Verschiebung+Tiefe/2,Wandung-4])  cylinder(16,3.5,3.5);
  
//  translate([Wandung+0.635*2,Wandung+0.635*1,Wandung+0]) color(    
//    "black") cube([2.54,5.08,7.4]); 
//  translate([Wandung+0.635*51,Wandung+0.635*-1,Wandung+0]) color("black") cube([5.08,2.54,7.4]); 
//  
//  translate([Wandung+0.635*72,Wandung+0.635*-1,Wandung+0]) color("black") cube([2.54,5.08,7.4]); 
//  
//  translate([Wandung+0.635*72,Wandung+0.635*7,Wandung+0]) color("black") cube([2.54,5.08,7.4]); 
//  
//  translate([Wandung+0.635*88,Wandung+0.635*26,Wandung+0]) color("black") cube([2.54,5.08,7.4]); 
//  
//  translate([Wandung+0.635*102,Wandung+0.635*1,Wandung+0]) color("black") cube([2.54,5.08,7.4]); 
// //CON
//  offs = 1.2;
//  translate([Wandung+0.635*94-offs/2,Wandung+0.635*9-offs/2,Wandung+3]) color("black") cube([2.54+offs,6*2.54+offs,7.4]); 
//  
// translate([Wandung+0.635*29,Wandung+0.635*-10,Wandung-2.5]) color("black") cube([0.635*14,5.08,5.5]); 
    
 translate([Wandung+12,Wandung+posx+2.5,Wandung+2]) color("silver") rotate([0,0,90]) Ausbruch(); 
// 
//// LED
// translate([Wandung+0.635*14,Wandung+0.635*7,Wandung+0]) color("black") cylinder(7.5,3,3, $fn=20);  
// 

  }
  
  
//
// Bolezenpos  = Hoehe - Snappos -Wandung ;
//  Bolzenhoehe = 7.8;
// translate([Versatz+5.5,Versatz+13,Bolezenpos-Bolzenhoehe])Podest(h = Bolzenhoehe, dir = 0); 
//
//translate([Versatz+24,Versatz+posx+3,2.2])Podest(h = 7.7, dir = 0);   
//  translate([Versatz+67,Versatz+6,2])Podest(h = 8, dir = 0);  
//
//   
}

module Unterschale()
{
    
  module Gehaeuse(size=[10,10,10])
  {
    aBreite = size[0];
    aTiefe = size[1];
    aSnappos = size[2];
    
    difference()
    {  
      linear_extrude(aSnappos)         offset(r = Radius, $fn=40) square([aBreite+  Versatz,aTiefe+Versatz]);
      translate([Wandung,Wandung,Wandung]) linear_extrude(aSnappos/*-Wandung*/)   offset(r = Radius, $fn=40) square([aBreite+Tolleranz-Wandung,aTiefe+Tolleranz-Wandung]);
    }
    translate([Wandung,Wandung,aSnappos]) Snapin_A([aBreite+Tolleranz-Wandung,aTiefe+Tolleranz-Wandung,4.5], Feder = 0.8, Tolerance = 0.1, Offset = Radius, $fn=40);  
    
  }
 // translate([0.47 + Versatz,-4.8 + Versatz,Wandung+1.9,]) boards();
  difference()
  {  
      union()
      {
        Gehaeuse([Breite, Tiefe, Snappos]);
        
        
        //translate([Versatz+15,Versatz+20,Wandung])Podest(h = 1.60, dir = 0); 
        
        //translate([Versatz+15,Versatz+7,Wandung])Podest(h = 1.60, dir = 0); 
        
        //translate([Versatz+57,Versatz+7,Wandung])Podest(h = 1.60, dir = 0);
        
        // translate([Versatz+53.6,Versatz+23,Wandung])Podest(h = 1.60, dir = 0);
      }
        

      
translate([Wandung+0,Wandung+posx+2.5,Wandung+4]) color("silver") rotate([0,0,90]) Ausbruch();


    
  }
 
}

module Kabelklemme()
{
    difference()
    {
    translate([Wandung+1,Wandung+posx-7,Wandung+2])  cube([10,20,4]);
    
    translate([Wandung+6,Wandung+posx-4,Wandung+1.5])  cylinder(5,2,2);
    translate([Wandung+6,Wandung+posx+10,Wandung+1.5])  cylinder(5,2,2);
      
       translate([Wandung+12,Wandung+posx+2.5,Wandung+0.5]) color("silver") rotate([0,0,90]) Ausbruch();

  }
}

module Ausbruch(d = 5.5)
{
  // cube([0.635*14,15.08,5.5]); 
  rotate([-90,00,0]) cylinder(30,d/2,d/2, $fn = 40); 
}

module Podest(h = 10, dir = 0)
{
  linear_extrude(h)  
  rotate(dir)  difference()
  {
    translate([-1.5,-1.5]) offset(2,$fn = 40) square(2.5, center = true);
    //circle(1.3,$fn = 10);  
  }
}    

module boards()
{
  translate([-1.4,posx,0]) 
  {
    lpsize = [36.5,18.4,1.49];
    LP1(lpsize);
    LpHalter([lpsize[0], lpsize[1], 5]);    
  }
  translate([55,4.3,0]) 
  {
    lp2size = [14,30.5,1.0];
    LP2(lp2size);
    LpHalter([lp2size[0], lp2size[1], 5]);
  }
}

module LP1(lpsize)
{
  if (!print)
  {  color("red") cube(lpsize);
    translate([-1,(18.4-7.7)/2,1.6]) color("silver") cube([9.3,7.7,3.84]);
    translate([20,(18.4-5.5)/2,1.6]) color("black") cube([10,5.5,2]);
  }  
}

module LP2(lpsize)
{
  if (!print)
  {
    color("green") cube(lpsize);
  }
}


module LpHalter(lpsize = [36.5,18.4,5])
{
  offset1 = 2;
  offset2 = 0.6;
  lpheight = 1.6;
  toleranz = 0.2;
  //color("red") cube([36.5,18.4,1.6]);
  
  difference()
  {
    translate([-offset1,-offset1,-lpsize[2]+lpheight])  cube([lpsize[0]+2*offset1, lpsize[1]+2*offset1, lpsize[2]-toleranz/2]);
    translate([-toleranz/2,-toleranz/2,-toleranz/2]) cube([lpsize[0]+toleranz, lpsize[1]+toleranz, lpsize[2]+2]);
    translate([+offset2/2,+offset2/2,-lpsize[2]+lpheight-0.2]) cube([lpsize[0]-offset2, lpsize[1]-offset2, lpsize[2]]);
    
    translate([+offset2/2-2*offset1,+lpsize[1]/4,-lpsize[2]+lpheight-0.2]) cube([lpsize[0]+4*offset1, lpsize[1]/2, lpsize[2]+1]);
    
     translate([+lpsize[0]/4,+offset2/2-2*offset1,-lpsize[2]+lpheight-0.2]) cube([ lpsize[0]/2, lpsize[1]+4*offset1, lpsize[2]+1]);
    
    translate([toleranz/2,toleranz/2,-toleranz/2]) cylinder(lpheight+toleranz,2*toleranz,2*toleranz,$fn = 20);
    translate([lpsize[0]-toleranz/2,+toleranz/2,-toleranz/2]) cylinder(lpheight+toleranz,2*toleranz,2*toleranz,$fn = 20);
    translate([-toleranz/2+lpsize[0],-toleranz/2+lpsize[1],-toleranz/2]) cylinder(lpheight+toleranz,2*toleranz,2*toleranz,$fn = 20);
    translate([+toleranz/2,-toleranz/2+lpsize[1],-toleranz/2]) cylinder(lpheight+toleranz,2*toleranz,2*toleranz,$fn = 20);
  }  
}




module SnapRoll(length = 5, r = 1, tolerance = -0.2) {
  translate([0,0,-length/2]) 
  union()
  {
    sphere(r=r+tolerance/2 , $fn = 20);
    translate([0,0,length]) sphere(r=r+tolerance/2 , $fn = 20);
    linear_extrude(length) { circle(r=r+tolerance/2 , $fn = 20); translate([ -(r+tolerance/2),tolerance]) square([2*r+tolerance,-tolerance]);
    }
  }
} 
   

module Snapin_A(Size = [30,10,4], Feder = 0.8, Tolerance = 0.1, Offset = 12) // Unnen
{

  Flaecheoeffnen = 0.1;
  union()
  {  
    difference()
    {  
      translate([-Feder,-Feder,-3*Feder]) linear_extrude(3*Feder) offset(r = Offset, $fn=40) square([Size[0]+2*Feder,Size[1]+2*Feder]);
      translate([Tolerance+Feder,Tolerance+Feder,-(2*Feder+Flaecheoeffnen)]) linear_extrude(2*Feder+2*Flaecheoeffnen) offset(r = Offset, $fn=40) square([Size[0]-2*(Tolerance+Feder),Size[1]-2*(Tolerance+Feder)]);
      translate([Size[0]/2,Size[1]/2,-(3*Feder+Flaecheoeffnen)]) 
    linear_extrude(1*Feder+1*Flaecheoeffnen, scale = [(Size[0]-2*Feder)/Size[0],(Size[1]-2*Feder)/Size[1]]) offset(r = Offset, $fn=40) square([Size[0],Size[1]], center=true);
    } 
    // Snap Spring 
    difference()
    {
      translate([Tolerance,Tolerance,0]) linear_extrude(Size[2]) offset(r = Offset, $fn=40) square([Size[0]-2*Tolerance,Size[1]-2*Tolerance]); 
       translate([Tolerance+Feder,Tolerance+Feder,-Flaecheoeffnen]) linear_extrude(Size[2]+2*Flaecheoeffnen) offset(r = Offset, $fn=40) square([Size[0]-2*(Tolerance+Feder),Size[1]-2*(Tolerance+Feder)]);  
    } 
    
    // Snap Rolls
    translate([Size[0]/2, - Offset , Size[2]-Feder+Tolerance/2]) 
     rotate([0, 90, 180]) SnapRoll(length = Size[0]/2, r = Feder, tolerance = - Tolerance );                 
    translate([Size[0]/2, Size[1] + Offset , Size[2]-Feder+Tolerance/2])
			rotate([0, 90, 0])  SnapRoll(length = Size[0]/2, r = Feder, tolerance = - Tolerance); 
    translate([- Offset , Size[1]/2 , Size[2]-Feder+Tolerance/2])
			rotate([-90, 90, 00])  SnapRoll(length =Size[1]/2, r = Feder, tolerance = - Tolerance);
    translate([Size[0] + Offset, Size[1]/2  , Size[2]-Feder+Tolerance/2])
			rotate([-90, -90, 00])    SnapRoll(length = Size[1]/2, r = Feder, tolerance = - Tolerance);
    
  }  
}  
 

module Snapin_B(Size = [10,10,10], Feder = 0.8, Tolerance = 0.1, Offset = 2)
{

    
  // Difference the Snapin_B for your Case
  Flaecheoeffnen = 0.1;
  union()
  {  
    difference()
    {
      translate([0,0,0]) linear_extrude(Size[2]) offset(r = Offset+Tolerance, $fn=40) square([Size[0],Size[1]]); 
       translate([-Tolerance+Feder,-Tolerance+Feder,-Flaecheoeffnen]) linear_extrude(Size[2]+2*Flaecheoeffnen) offset(r = Offset, $fn=40) square([Size[0]-2*(-Tolerance+Feder),Size[1]-2*(-Tolerance+Feder)]);  
    } 
    translate([Size[0]/2, - Offset , Size[2]-Feder+Tolerance/2])
    rotate([0,90,0])
        SnapRoll(length = 1.5+Size[0]/2, r = Feder, tolerance = Tolerance);
    translate([Size[0]/2, Size[1] + Offset , Size[2]-Feder+Tolerance/2])
    rotate([0,90,0])
			SnapRoll(length = 1.5+Size[0]/2, r = Feder, tolerance = Tolerance);
    
    translate([- Offset ,Size[1]/2 , Size[2]-Feder+Tolerance/2])
    rotate([90,0,0])
			SnapRoll(length = 1.5+Size[1]/2, r = Feder, tolerance = Tolerance);
    translate([Size[0] + Offset, Size[1]/2  , Size[2]-Feder+Tolerance/2])
    rotate([90,0,0])
			SnapRoll(length = 1.5+Size[1]/2, r = Feder, tolerance = Tolerance);
    
  }  
}    

