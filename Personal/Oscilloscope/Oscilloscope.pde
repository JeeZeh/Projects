/**
 * The CS171 Oscilloscope
 * by Jesse Ashmore
 * Student Number - 16394441
 * 07/12/2016
 *
 * All music by Jerobeam Fenderson
 *
 * Minim library by Damien Di Fede & Anderson Mills
 * ControlP5 library by Andreas Schlegal
**/

import ddf.minim.*;
import controlP5.*;

Minim minim;
AudioPlayer player;

ControlP5 cp5;
ScrollableList songlist;
Slider colour, level1, level2;
Knob gain_knob, pan_knob;
float g = 0, p = 0; // Variable for gain
color C;
PImage bg, bg_intro;
String[] songArray = new String[] {"How To Draw Mushrooms On An Oscilloscope", "Asteroids", "Spirals", "Nuclear Black Noise", "Dots"};
String song = songArray[0] + ".mp3";
int col1 = 0, col2 = 180, col3 = 0; // Oscilloscope colour values
boolean intro = true; // Allows the 'welcome screen' to run

void setup()
{
  size(1280,720);
  bg = loadImage("bg.jpg");              // Both images were made in Photoshop
  bg_intro = loadImage("bg_intro.jpg");  // Style and placement of text was MUCH simpler to do in PS than Processing
  
  minim = new Minim(this);
  player = minim.loadFile(song, 1024); // Can't seem to find a 'perfect' buffer size, 1024 doesn't lag too much with ellipses.
  
  cp5 = new ControlP5(this);          
  
        colour = cp5.addSlider("Colour")    // Colour slider for oscilloscope colour
          .setPosition(1065, 630)
          .setSize(100,20)
          .setRange(1,5)
          .setValue(1)
          .setNumberOfTickMarks(5);
        
        songlist = cp5.addScrollableList("Dropdown")  // Song list to choose a song from
          .setPosition(1020, 405)
          .setSize(200, 300)
          .setBarHeight(30)
          .setItemHeight(30)
          .addItems(songArray)
          .setColorActive(color(0,255,0))
          .setValue(0);
           
        gain_knob = cp5.addKnob("Gain") // Knob to control gain
          .setPosition(872, 100)
          .setSize(60,60)
          .setRange(-40, 6)
          .setValue(0);
          
        pan_knob = cp5.addKnob("Pan")
          .setPosition(872, 280)
          .setSize(60,60)
          .setRange(-1, 1)
          .setValue(0);
          
        level1 = cp5.addSlider("Left") // Displays the audio 'level' for the left channel
          .setPosition(880, 470)
          .setSize(20, 200)
          .setRange(0, 100)
          .setColorForeground(color(255, 50, 50));
        level2 = cp5.addSlider("Right") // Displays the audio 'level' for the left channel
          .setPosition(910, 470)
          .setSize(20, 200)
          .setRange(0, 100)
          .setColorForeground(color(255, 50, 50));
 
  C= color(255,255,0);                              // Some code to tidy up the labels on the controls
  songlist.getCaptionLabel().toUpperCase(true);     
  songlist.getCaptionLabel().set("Choose a song"); 
  songlist.getCaptionLabel().setColor(C);
 
  colour.getCaptionLabel().set("");
  pan_knob.getCaptionLabel().set("");
  gain_knob.getCaptionLabel().set("");

  level1.getValueLabel().set("");
  level2.getValueLabel().set("");

}

void draw()
{
  if(intro){              // Run the intro before anything else. I wanted to just 
    background(bg_intro); // nest this in a while loop but it wasn't having any of it.
    if(keyPressed)        // Press Any key to skip
      intro = false;
  }
  
  else{
  background(bg);
  stroke(col1, col2, col3);  // Even though the strokeWeight is 0, I've encountered strokes still drawing in the past 
  strokeWeight(0);           // so I've coloured them the same as the ellipses just in case
  
  level1.setValue(player.left.level()*150);    // Both the labels and the levels must be run in draw() 
  level2.setValue(player.right.level()*150);
  level1.getValueLabel().set("");
  level2.getValueLabel().set("");
  
  for(int i = 0; i < player.bufferSize(); i++){    // Draw ellipses from the buffer currently loaded into memory
    fill(col1,col2,col3);                          
    float x = map(player.left.get(i), 0, 1, 0, 240);    // Take and map the values from the L/R channels to the X/Y axes respectively
    float y = map(player.right.get(i), 0, 1, 0, 240);
    ellipse(400 + x + (player.getPan()*100), 350 - y, 1,1); //Draw them 'centred' but allow pan to affect X value
  }
  
  if((mouseX >= 1070 && mouseX <= 1166) && (mouseY >= 82 && mouseY <= 110) && mousePressed){
    player.play();
    player.setGain(gain_knob.getValue());  // Sets gain_knob value as gain when playing a (new) song
  }
  else if((mouseX >= 1060 && mouseX <= 1180) && (mouseY >= 162 && mouseY <= 192) && mousePressed)    // Button control
    player.pause();
  else if((mouseX >= 1060 && mouseX <= 1180) && (mouseY >= 240 && mouseY <= 280) && mousePressed){
    player.pause();
    player.rewind();  // Return to the start of the track but don't play
    }
  }
}  

void Colour(int i){
  switch(i){
    case 1 : col1 = 0;   col2 = 220;  col3 = 0;   break;  // Colour values corresponding to the slider values
    case 2 : col1 = 220; col2 = 80;   col3 = 80;  break;
    case 3 : col1 = 80;  col2 = 80;   col3 = 220; break;
    case 4 : col1 = 220; col2 = 140;  col3 = 220; break;
    case 5 : col1 = 220; col2 = 220;  col3 = 220; break;
    default : break;
  } 
}

void Dropdown(int i){
  player.pause();
  player = minim.loadFile(songArray[i] + ".mp3", 1024); // The file extension is added in a method rather than
}                                                       // kept in the name for tidiness

void Gain(float g){
  player.setGain(g);  // Sets the gain value for the player based on knob control
}

void Pan(float p){
  player.setPan(p);
}