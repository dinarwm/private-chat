/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package connection;

import forms.FormChat;
import forms.FormLogin;
import forms.FormOnline;
import java.io.DataInputStream;
import java.io.IOException;
import java.net.Socket;
import main.ChatClient;

/**
 *
 * @author achmads23
 */
public class Receiver implements Runnable {

    private Thread thread;
    private FormLogin formLogin;
    private FormOnline formOnline;
    private final Socket conn;

    public Receiver() {
        this.conn = ChatClient.conn;
        this.formOnline = null;
        this.formLogin = null;
    }

    public void setFormLogin(FormLogin login) {
        this.formLogin = login;
    }

    public void setFormOnline(FormOnline online) {
        this.formOnline = online;
    }

    @Override
    @SuppressWarnings("empty-statement")
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
                        case "auth":
                            System.out.println("pesan (" + msg + ")");
                            if ("1:Login success.".equals(msg)) {
                                formLogin.dispose();
                                FormOnline online = new FormOnline();
                                online.setVisible(true);
                                this.setFormOnline(online);
                            }
                            break;
                        case "users":
                            while (formOnline == null);
                            System.out.println("masuk protocol users");
                            formOnline.userUpdate(msg);
                            break;
                        case "rcv":
                            while (formOnline == null);
                            parts = msg.split(":", 2);
                            String id = parts[0];
                            String nama = formOnline.getNama(id);
                            String isi = parts[1];
                            FormChat form = ChatList.OpenForm(nama, id);
                            form.chatUpdate(nama, isi);
                            break;
                    }
                }
            } catch (ArrayIndexOutOfBoundsException | IOException ex) {
                System.out.println("Error di thread: " + ex.getMessage());
            }
        }
    }

    public void start() {
        thread = new Thread(this);
        thread.start();
    }

}
