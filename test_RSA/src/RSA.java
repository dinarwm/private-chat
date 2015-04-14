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
    private int bitLength = 1024;
    private BigInteger p;
    private BigInteger q;
    private Random r;
    private BigInteger n;
    private BigInteger tf;
    private BigInteger e;
    private BigInteger d;

    //---ALGORITMA RSA---//
    public RSA() {
        r = new Random();
        //tentukan bilangan prima p dan q
        p = BigInteger.probablePrime(bitLength, r);
        q = BigInteger.probablePrime(bitLength, r);
        System.out.println("p = " + p);
        System.out.println("q = " + q);
        //hitung n = p x q
        n = p.multiply(q);
        System.out.println("n = " + n);
        //Totient Function TF(n) = (p-1) x (q-1)
        tf = p.subtract(BigInteger.ONE).multiply(q.subtract(BigInteger.ONE));
        System.out.println("tf(n) = " + tf);
        //cari e yg relative prime dengan TF(n) dan e < TF(n)
        //GCD (tf,e) = 1 
        e = BigInteger.probablePrime(bitLength / 2, r);
        while (tf.gcd(e).compareTo(BigInteger.ONE) > 0 && e.compareTo(tf) < 0) {
            e.add(BigInteger.ONE);
        }
        System.out.println("e = " + e);
        //Hitung d, (e x d) mod tf(n) = 1
        d = e.modInverse(tf);
        System.out.println("d = " + d);
    }
    
    //---ENKRIPSI PESAN---//
    //C = M^e mod n
    public byte[] encrypt(byte[] message) {
        return (new BigInteger(message)).modPow(e, n).toByteArray();
    }

    // DEKRIPSI PESAN
    // M = C^d mod n
    public byte[] decrypt(byte[] message) {
        return (new BigInteger(message)).modPow(d, n).toByteArray();
    }
    
    private static String bytesToString(byte[] encrypted) {
        String hasil = "";
        for (byte b : encrypted) {
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
        System.out.println("String in Bytes: " + bytesToString(pesan.getBytes()));
        //enkripsi key
        byte[] encrypt = rsa.encrypt(pesan.getBytes());
        System.out.println("Chipertext: " + bytesToString(encrypt));
        // dekripsi key
        byte[] decrypt = rsa.decrypt(encrypt);
        System.out.println("Decrypted String in Bytes: " + bytesToString(decrypt));
        System.out.println("Hail dekripsi: " + new String(decrypt));
    }
}
