import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class SHA256 {

    static String sha256(String input) throws NoSuchAlgorithmException {
        byte[] in = hexStringToByteArray(input);
        MessageDigest mDigest = MessageDigest.getInstance("SHA-256");
        byte[] result = mDigest.digest(in);
        StringBuffer sb = new StringBuffer();
        for (int i = 0; i < result.length; i++) {
            sb.append(Integer.toString((result[i] & 0xff) + 0x100, 16).substring(1));
        }
        //System.out.println(sb.toString());
        return sb.toString();
    }

    public static byte[] hexStringToByteArray(String s) {
        int len = s.length();
        byte[] data = new byte[len / 2];
        for (int i = 0; i < len; i += 2) {
            data[i / 2] = (byte) ((Character.digit(s.charAt(i), 16) << 4)
                    + Character.digit(s.charAt(i + 1), 16));
        }
        return data;
    }

    public static void main(String[] args) {
        String secret = "5JvVGV1AkvZdeQ4HCmBXK59sZaxrVgohPGGuSDYzsMJhNv47Ypx";
        try {
            System.out.println(sha256(secret));
        } catch (NoSuchAlgorithmException e) {
        }
    }
}