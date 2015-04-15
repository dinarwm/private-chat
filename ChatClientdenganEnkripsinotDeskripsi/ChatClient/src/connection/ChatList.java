/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package connection;

import forms.FormChat;
import java.util.ArrayList;

/**
 *
 * @author achmads23
 */
public class ChatList {

    public static ArrayList<String> listNama = new ArrayList<>();
    public static ArrayList<FormChat> forms = new ArrayList<>();

    public static FormChat OpenForm(String nama, String id) {
        int count = 0;
        for (String n : listNama) {
            if (n.equals(nama)) {
                return forms.get(count);
            }
            count++;
        }
        listNama.add(nama);
        FormChat form = new FormChat(nama, id);
        forms.add(form);
        return form;
    }
}
