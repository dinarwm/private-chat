package main;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
import forms.FormLogin;
import connection.Receiver;
import java.io.IOException;
import java.net.Socket;

/**
 *
 * @author achmads23
 */
public class ChatClient {

    public static Socket conn;
    public static String username;

    /**
     * @param args the command line arguments
     * @throws java.io.IOException
     */
    public static void main(String[] args) throws IOException {
        conn = new Socket("10.151.34.139", 22001);
        System.out.println(conn);

        Receiver receiver = new Receiver();
        receiver.start();

        FormLogin login = new FormLogin();
        login.setVisible(true);
        receiver.setFormLogin(login);
    }
}
