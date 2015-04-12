/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package forms;

import connection.ChatList;
import java.util.ArrayList;

/**
 *
 * @author achmads23
 */
public class FormOnline extends javax.swing.JFrame {

    private Object jTextField1;
    private final ArrayList<String> namas;
    private final ArrayList<String> ids;

    /**
     * Creates new form FormOnline
     */
    public FormOnline() {
        initComponents();
        namas = new ArrayList<>();
        ids = new ArrayList<>();
        taListOnline.setEditable(false);
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        lblListOnline = new javax.swing.JLabel();
        jScrollPane1 = new javax.swing.JScrollPane();
        taListOnline = new javax.swing.JTextArea();
        lblWith = new javax.swing.JLabel();
        tfChat = new javax.swing.JTextField();
        btnChat = new javax.swing.JButton();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        lblListOnline.setText("List Online");

        taListOnline.setColumns(20);
        taListOnline.setRows(5);
        taListOnline.setName(""); // NOI18N
        jScrollPane1.setViewportView(taListOnline);

        lblWith.setText("Chat with");

        tfChat.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                tfChatActionPerformed(evt);
            }
        });

        btnChat.setText("Chat");
        btnChat.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                btnChatActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addComponent(jScrollPane1)
                    .addComponent(lblListOnline)
                    .addGroup(layout.createSequentialGroup()
                        .addComponent(lblWith)
                        .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(tfChat))
                    .addComponent(btnChat, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(lblListOnline)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 163, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                    .addComponent(lblWith)
                    .addComponent(tfChat, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(btnChat)
                .addContainerGap())
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    private void tfChatActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_tfChatActionPerformed
        // TODO add your handling code here:
    }//GEN-LAST:event_tfChatActionPerformed

    private void btnChatActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_btnChatActionPerformed
        String chat = tfChat.getText();
        for (int i = 0; i < namas.size(); i++) {
            if (namas.get(i).equals(chat)) {
                String id = ids.get(i);
                ChatList.OpenForm(namas.get(i), id);
                System.out.println("Cool!");
                return;
            }
        }
        System.out.println("Wrong name.");
    }//GEN-LAST:event_btnChatActionPerformed

    /**
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException | InstantiationException | IllegalAccessException | javax.swing.UnsupportedLookAndFeelException ex) {
            System.out.println("Error formonline main: " + ex.getMessage());
        }
        //</editor-fold>

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(new Runnable() {
            @Override
            public void run() {
                new FormOnline().setVisible(true);
            }
        });
    }

    public String getNama(String id) {
        for (int i = 0; i < ids.size(); i++) {
            if (id.equals(ids.get(i))) {
                return namas.get(i);
            }
        }
        return null;
    }

    public void userUpdate(String users) {
        taListOnline.setText("");
        namas.clear();
        ids.clear();
        int n = 0;
        for (String retval : users.split(":")) {
            String[] idnama = retval.split("#");
            namas.add(idnama[1]);
            ids.add(idnama[0]);
            taListOnline.append(idnama[1] + "\n");
        }
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton btnChat;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JLabel lblListOnline;
    private javax.swing.JLabel lblWith;
    private javax.swing.JTextArea taListOnline;
    private javax.swing.JTextField tfChat;
    // End of variables declaration//GEN-END:variables
}
