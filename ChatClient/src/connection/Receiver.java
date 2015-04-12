/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package connection;

import forms.FormChat;
import forms.FormOnline;
import java.io.DataInputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.logging.Level;
import java.util.logging.Logger;
import main.ChatClient;

/**
 *
 * @author achmads23
 */
public class Receiver implements Runnable {

    private Thread thread;
    private final FormOnline formonline;
    private final Socket conn;

    public Receiver(FormOnline online) {
        conn = ChatClient.conn;
        this.formonline = online;
    }

    @Override
    public void run() {
        while (true) {
            try {
                DataInputStream dis;
                dis = new DataInputStream(conn.getInputStream());
                String string = dis.readLine().trim();
                System.out.println("server: (" + string + ")");
                String[] parts = string.split(":", 2);
                String protocol = parts[0];
                String msg = parts[1];
                if (null != protocol) {
                    switch (protocol) {
                        case "users":
                            System.out.println("masuk protocol users");
                            formonline.userUpdate(msg);
                            break;
                        case "rcv":
                            parts = msg.split(":", 2);
                            String id = parts[0];
                            String nama = formonline.getNama(id);
                            FormChat form = ChatList.OpenForm(nama, id);
                            form.chatUpdate(nama + "\t: " + parts[1]);
                            break;
                    }
                }
            } catch (IOException ex) {
                Logger.getLogger(Receiver.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }

    public void start() {
        thread = new Thread(this);
        thread.start();
    }

}
