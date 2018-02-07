import java.math.BigInteger;
import java.security.NoSuchAlgorithmException;

/**
 * Vertcoin Private Key Generator
 * by Jesse Ashmore
 *
 * @version 1.0
 * @since 07/02/2018
 */

public class VertcoinPrivateKey {

    public static void main(String[] args) {
        System.out.println("\nVertcoin private key: " + generateKey());
    }

    // Generates and returns the private key
    public static String generateKey() {

        // Generate a random 64 digit hex and add "80" to the start
        String hex80 = "80" + generateHex();

        try {
            // Hash hex80 string from above, twice
            String doubleHash = SHA256.sha256(SHA256.sha256(hex80));
            // Encode hex80 with the first 8 digits of the doubleHash added to the end, in base58
            return encode58(hex80 + doubleHash.substring(0, 8));
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
            return "failed";
        }

    }

    // Generates the 64 digit hex string
    public static String generateHex() {

        char[] hex = "0123456789ABCDEF".toCharArray();
        String hexOut = "";

        while (hexOut.length() < 64) {
            // Mod a random value between 0 and 100 by 16
            // Use that as the index to add a random char from the hex array to the string 'hexOut'
            hexOut += hex[(int) (Math.random() * 100) % 16];
        }

        return hexOut;

    }

    // Encodes the incoming hex string as a base58 string.
    public static String encode58(String in) {

        char[] base58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz".toCharArray();
        // Uses BigInteger to store the very large number, when the string is converted from hex to decimal.
        BigInteger input = new BigInteger(in, 16);
        String vertOut = "";
        BigInteger num = input;
        BigInteger a = new BigInteger("58");

        while (num.compareTo(a) >= 0) { // While num >= 58
            int index = num.mod(a).intValue(); // Mod the big int to find the remainder when divided by 58.
            vertOut = base58[index] + vertOut; // Use that index to add a char from the base58 array to the start of 'out'.
            num = num.divide(a); // Divide num by 58, discarding the remainder.
        }

        if (num.compareTo(BigInteger.valueOf(0)) > 0) { // If the number is greater than 0
            int index = num.mod(a).intValue(); // Mod again
            vertOut = base58[index] + vertOut; // Add that char to the final 'vertOut' string.
        }

        return vertOut; // Return the string, which is now a valid Vertcoin private key.

    }
}
