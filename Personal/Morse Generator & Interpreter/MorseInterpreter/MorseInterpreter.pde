import ddf.minim.*;
import ddf.minim.ugens.*;
import ddf.minim.analysis.*;
import java.util.Map;

Minim m;
AudioInput in;
FFT fft;

String text = "";
String binary = "";
String output = "";
float currentVol;
int last = -1;
int loud = 220;
String currentCode = "";
float lenGap;
long startBeep;
float lenBeep;
boolean timeout;
boolean beeped;
HashMap<String, Character> morseMap = new HashMap<String, Character>();

void setup(){
  size(400,400);
  background(0);
  m = new Minim(this);
  in = m.getLineIn();
  fft = new FFT(in.bufferSize(), in.sampleRate());
  String[] charAZ = "a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9 . , ?".split(" ");
  String[] morseAZ = ".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --.. ----- .---- ..--- ...-- ....- ..... -.... --... ---.. ----. .-.-.- --..-- ..--..".split(" ");
        for (int i = 0; i < charAZ.length; i++) {
            morseMap.put(morseAZ[i], charAZ[i].charAt(0));
        }
}
long lastBeepTime = 0;
void draw(){
  fft.forward( in.mix );
  background(0);
  textSize(14);
  text(fft.getFreq(1300), 20, 20);
  if(fft.getFreq(1300) > 25.0){
    if(!beeped){
      if(timeout){
        output="";
        text = "";
      }
      startBeep = System.currentTimeMillis();
      lenGap = (float)(startBeep - lastBeepTime)*0.85;
      if(lenGap > 160 && lenGap < 360){
        output+= " ";
        text += morseMap.get(currentCode);
        currentCode = "";
      }
      else if(lenGap > 430 && lenGap < 700){
        output+= " | ";
        text += morseMap.get(currentCode) + " ";
        currentCode = "";
      }
    }
    beeped = true;
    timeout = false;
    text("BEEP!", 20, 60);
  }
  else{
    if(beeped){ 
      lastBeepTime = System.currentTimeMillis();
      lenBeep = (float)(System.currentTimeMillis() - startBeep)*0.85;
      beeped = false;
      if(lenBeep > 25 && lenBeep < 180){
        currentCode+= ".";
        output+= ".";
      }
      else if(lenBeep > 180 && lenBeep < 310){
        currentCode+= "-";
        output+= "-";  
      }
      timeout = false;
    }
    if((System.currentTimeMillis() - lastBeepTime) > 800 && !timeout && lastBeepTime > 1){
      timeout = true;
      text += morseMap.get(currentCode);
      currentCode = "";
    }
  }
    text("Beep length: " + lenBeep, 20, 100);
    text("Gap length: " + lenGap, 20, 130);
    text("Morse: " + output, 20, 180);
    text("Text: " + text, 20, 210);
    text("Current: " + currentCode, 20, 240);
}