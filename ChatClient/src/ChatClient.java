/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
import ChatClient.FormLogin;
import java.io.IOException;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;

/**
 *
 * @author achmads23
 */
public class ChatClient {
    static Socket conn;
    /**
     * @param args the command line arguments
     * @throws java.net.UnknownHostException
     */
    
    public static void main(String[] args) throws UnknownHostException, IOException, InterruptedException{
        conn = new Socket(InetAddress.getLocalHost(), 22001);
        FormLogin Login = new FormLogin(conn);
        Login.setVisible(true);
        
        while(Login.isActive()){
        }
        if (FormLogin.Tanda=="SUKSES"){
           System.out.print("MASUK");
        }
    }
        // TODO code application logic here
}
