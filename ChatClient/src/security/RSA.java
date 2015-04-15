package security;

import java.math.BigInteger;
import java.util.Random;
import java.io.*;

/*
 contekan PPT hihi
 RSA Algrithm
 C = M^e mod n
 M = C^d mod n = M^ed mod n
 */
public class RSA {

    private final int BITLENGTH = 100;
    private final BigInteger p;
    private final BigInteger q;
    private final BigInteger n;
    private final BigInteger tf;
    private final BigInteger e;
    private final BigInteger d;

    //---ALGORITMA RSA---//
    public RSA() {
        Random r = new Random();

        // tentukan bilangan prima p dan q
        p = BigInteger.probablePrime(BITLENGTH, r);
        q = BigInteger.probablePrime(BITLENGTH, r);

        // hitung n = p x q
        n = p.multiply(q);

        // Totient Function TF(n) = (p-1) x (q-1)
        tf = p.subtract(BigInteger.ONE).multiply(q.subtract(BigInteger.ONE));

        // cari e yg relative prime dengan TF(n) dan e < TF(n)
        // GCD (tf,e) = 1 
        e = BigInteger.probablePrime(BITLENGTH / 2, r);
        while (tf.gcd(e).compareTo(BigInteger.ONE) > 0 && e.compareTo(tf) < 0) {
            e.add(BigInteger.ONE);
        }

        // Hitung d, (e x d) mod tf(n) = 1
        d = e.modInverse(tf);
    }

    //---ENKRIPSI PESAN---//
    //C = M^e mod n
    public byte[] encrypt(byte[] message) {
        return (new BigInteger(message)).modPow(e, n).toByteArray();
    }

    public String encrypt(String message) {
        String s = new String(encrypt(message.getBytes()));
        return s;
        
    }

    // DEKRIPSI PESAN
    // M = C^d mod n
    public byte[] decrypt(byte[] chiper) {
        return (new BigInteger(chiper)).modPow(d, n).toByteArray();
    }

    public String decrypt(String chiper) {
        String s = new String(decrypt(chiper.getBytes()));
        return s;
    }

    public static String bytesToString(byte[] bytes) {
        String hasil = "";
        for (byte b : bytes) {
            hasil += Byte.toString(b);
        }
        return hasil;
    }

    //COBA YAAAA GAPAKE DES DULU heheh
    public static void main(String[] args) throws IOException {
        RSA rsa = new RSA();
        DataInputStream in = new DataInputStream(System.in);
        System.out.println("Plaintext : ");
        String pesan = in.readLine();
        //*
        String chiper = rsa.encrypt(pesan);
        System.out.println(chiper);
        System.out.println(rsa.decrypt(chiper));
        //*/
 
		    String example = "This is an example";
		    byte[] bytes = example.getBytes();
 
		    System.out.println("Text : " + example);
		    System.out.println("Text [Byte Format] : " + bytes);
		    System.out.println("Text [Byte Format] : " + bytes.toString());
 
		    String s = new String(bytes);
		    System.out.println("Text Decryted : " + s);
                    
        /*
        System.out.println("String in Bytes: " + bytesToString(pesan.getBytes()));
        //enkripsi key
        byte[] encrypt = rsa.encrypt(pesan.getBytes());
        System.out.println("Chipertext: " + bytesToString(encrypt));
        System.out.println("Coba: " + new String(encrypt));
        System.out.println("Bytes: " + encrypt);
        // dekripsi key
        byte[] decrypt = rsa.decrypt(encrypt);
        System.out.println("Decrypted String in Bytes: " + bytesToString(decrypt));
        System.out.println("Hail dekripsi: " + new String(decrypt));
        
        //*/
    }
}
