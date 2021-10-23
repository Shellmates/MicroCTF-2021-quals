import java.security.MessageDigest;
import java.util.*;
import java.util.stream.Collectors;
import java.io.UnsupportedEncodingException;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

class Vault {
    public static void main(String args[]) throws Exception {
 
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter vault password: ");
        String password=scanner.next();
        List<Integer> p = password.chars().mapToObj(e->  0xCafe + (int)e).collect(Collectors.toList());
        
        if(
        		 p.get(0) == 52037 &&
        		 p.get(6) == 52081 &&
        		 p.get(5) == 52063 &&
        		 p.get(1) == 52077 &&
        		 p.get(9) == 52077 &&
        	     p.get(10) == 52080 &&
        	     p.get(4) == 52046 &&
        	     p.get(3) == 52066 &&
        	     p.get(8) == 52085 &&
        	     p.get(7) == 52081 &&
        	     p.get(2) == 52077 &&
        	     p.get(11)== 52066){
        	
	            String decryptedString = AES.decrypt("k1dSIjeXHWc+zaO1Ip5qt1TNgwnOtIMVjyF/uyA5rZt03masuqUP/QaK0PH/xcju",password);
	            System.out.println("Flag: "+decryptedString);
        	  } else {
        		 System.out.print("Wrong Password");
        	  }  


    }
    
 
     
    public static class AES {
     
        private static SecretKeySpec secretKey;
        private static byte[] key;
     
        public static void setKey(String myKey) 
        {
            MessageDigest sha = null;
            try {
                key = myKey.getBytes("UTF-8");
                sha = MessageDigest.getInstance("SHA-1");
                key = sha.digest(key);
                key = Arrays.copyOf(key, 16); 
                secretKey = new SecretKeySpec(key, "AES");
            } 
            catch (NoSuchAlgorithmException e) {
                e.printStackTrace();
            } 
            catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
        }
     
        public static String encrypt(String strToEncrypt, String secret) 
        {
            try
            {
                setKey(secret);
                Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
                cipher.init(Cipher.ENCRYPT_MODE, secretKey);
                return Base64.getEncoder().encodeToString(cipher.doFinal(strToEncrypt.getBytes("UTF-8")));
            } 
            catch (Exception e) 
            {
                System.out.println("Error while encrypting: " + e.toString());
            }
            return null;
        }
     
        public static String decrypt(String strToDecrypt, String secret) 
        {
            try
            {
                setKey(secret);
                Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5PADDING");
                cipher.init(Cipher.DECRYPT_MODE, secretKey);
                return new String(cipher.doFinal(Base64.getDecoder().decode(strToDecrypt)));
            } 
            catch (Exception e) 
            {
                System.out.println("Error while decrypting: " + e.toString());
            }
            return null;
        }
    }
    

}