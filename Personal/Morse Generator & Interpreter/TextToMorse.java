import java.util.*;
import javax.sound.sampled.*;

import static java.lang.Thread.sleep;

public class TextToMorse {
    private static int msLen = 55; // Unit of time in ms
    private static int freq = 1300; // Frequency in Hz
    private static double vol = 1; // Volume from 0 - 1.00
    private static HashMap<Character, String> morseMap = new HashMap<>(); // Holds the {letter : morse} pairs
    private static String input;

    public static void main(String[] args) throws LineUnavailableException, InterruptedException {
        Scanner scan = new Scanner(System.in);

        // Creates HashMap of ascii to morse
        String[] charAZ = "a b c d e f g h i j k l m n o p q r s t u v w x y z 0 1 2 3 4 5 6 7 8 9 . , ?".split(" ");
        String[] morseAZ = ".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --.. ----- .---- ..--- ...-- ....- ..... -.... --... ---.. ----. .-.-.- --..-- ..--..".split(" ");
        for (int i = 0; i < charAZ.length; i++) {
            morseMap.put(charAZ[i].charAt(0), morseAZ[i]);
        }

        // Takes user input
        System.out.print("Enter your morse code: ");
        input = scan.nextLine().toLowerCase();

        // Converts input to morse code on a per-letter basis
        String[] convertedToMorse = convertToMorse(input);

        playMorse(convertedToMorse);
    }


    public static void playMorse(String[] morse) throws LineUnavailableException, InterruptedException {

        // For each letter of the input
        for (int i = 0; i < morse.length; i++) {
            // Print current letter and morse representation.
            System.out.println("\nCurrent Letter: '" + input.charAt(i) + "'\nCurrent Morse: '" + (morse[i].equals("_______") ? " '" : "" + morse[i] + "'"));

            // For each morse symbol per letter

            // If the symbol is a space, wait for 7 units of time
            if (morse[i].equals(" ")) {
                sleep(msLen * 7);
            } else {
                for (int j = 0; j < morse[i].length(); j++) {

                    // Switch on each symbol, playing the appropriate length beep.
                    switch (morse[i].charAt(j)) {
                        case '.':
                            tone(freq, msLen, vol);
                            break;
                        case '-':
                            tone(freq, msLen * 3, vol);
                            break;
                    }
                    // If it's not the last symbol, wait for 1 unit of time
                    if (j < morse[i].length() - 1) {
                        sleep(msLen);
                    }
                }
            }

            // If it's not the last symbol, and neither the current nor the next symbol is a space
            // wait 3 units of time after each letter
            if (i < morse.length - 1 && !morse[i + 1].equals(" ") && !morse[i].equals(" ")) {
                sleep(msLen * 3);
            }
        }
    }

    public static String[] convertToMorse(String text) {

        // Array of morse letter codes
        String[] out = new String[text.length()];

        for (int i = 0; i < text.length(); i++) {
            char currentLetter = text.charAt(i);
            String currentMorse = morseMap.get(currentLetter);
            // If the current letter is a space, put a space in the array
            if (currentLetter == ' ') {
                out[i] = " ";
            } else {
                StringBuilder morseLetter = new StringBuilder();

                // Go through each symbol in the morse and build a morse code
                for (int j = 0; j < currentMorse.length(); j++) {
                    morseLetter.append(currentMorse.charAt(j));
                }
                // Put the code in the array
                out[i] = morseLetter.toString();
            }
        }
        return out;
    }


    public static void tone(int hz, int msecs, double vol) throws LineUnavailableException {
        float SAMPLE_RATE = 8000f;
        byte[] buf = new byte[1];
        AudioFormat af = new AudioFormat(SAMPLE_RATE, 8, 1, true, false);
        SourceDataLine sdl = AudioSystem.getSourceDataLine(af);
        sdl.open(af);
        sdl.start();
        for (int i = 0; i < msecs * 8; i++) {
            double angle = i / (SAMPLE_RATE / hz) * 2.0 * Math.PI;
            buf[0] = (byte) (Math.sin(angle) * 127.0 * vol);
            sdl.write(buf, 0, 1);
        }
        sdl.drain();
        sdl.stop();
    }
}

