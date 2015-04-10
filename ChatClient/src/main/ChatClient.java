package main;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import forms.FormLogin;
import forms.FormOnline;
import connection.Receiver;
import java.io.DataInputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.net.Socket;

/**
 *
 * @author achmads23
 */
public class ChatClient {

    public static Socket conn;

    /**
     * @param args the command line arguments
     * @throws java.io.IOException
     */
    public static void main(String[] args) throws IOException {
        conn = new Socket(InetAddress.getLocalHost(), 22001);
        System.out.println(conn);
        DataInputStream dis;
        dis = new DataInputStream(conn.getInputStream());
        FormLogin Login = new FormLogin(conn);
        Login.setVisible(true);
        while (Login.isActive()) {
        }
        if ("SUKSES".equals(FormLogin.Tanda)) {
            FormOnline online = new FormOnline();
            online.setVisible(true);
            Receiver receiver = new Receiver(online);
            receiver.start();
        }

    }
}
