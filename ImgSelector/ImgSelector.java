import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.GridLayout;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.Collections;
import javax.imageio.ImageIO;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextArea;

// 画像を選択してクリップするための準備クラス
public class ImgSelector {

    JFrame frame;
    String top;
    String left;
    String height;
    String width;
    String prevTop;
    String prevLeft;
    String temporaryCoordinate;

    public ImgSelector() {}
    public ImgSelector(String filePath) {
        try {
            // 変数初期化
            top = "0";
            left = "0";
            height = "0";
            width = "0";
            prevTop = "0";
            prevLeft = "0";

            // 引数のパスから画像を読み込む
            File file = new File(filePath);
            BufferedImage image = ImageIO.read(file);
            // filePathからファイル名を取得
            String fileName = file.getName();
            // fileNameから拡張子を除外
            String fileNamePrefix = fileName.substring(0, fileName.lastIndexOf("."));

            // 画像サイズをもとにフレームを作成する
            frame = new JFrame();
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setSize(image.getWidth()+200, image.getHeight()+100);

            // 画像を表示するためのパネルを作成する
            JPanel panel1 = new JPanel() {
                @Override
                protected void paintComponent(Graphics g) {
                    super.paintComponent(g);
                    g.drawImage(image, 0, 0, null);
                }
            };

            // 現在座標を表示するためのラベル
            JLabel label1 = new JLabel("");
            label1.setHorizontalAlignment(JLabel.CENTER);
            // 第二座標選択位置を表示するためのラベル
            JLabel label2 = new JLabel("Shape = Top:" + prevTop + ", Left: " + prevLeft + ", Height: " + height + ", Width:" + width);
            label2.setHorizontalAlignment(JLabel.CENTER);
            // ファイル出力する対象を記載するテキストボックス
            JTextArea textArea = new JTextArea();
            textArea.setText(""); 
            // リセットボタン
            JButton resetButton = new JButton("リセット");
            resetButton.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    top = "0";
                    left = "0";
                    width = "0";
                    height = "0";
                    prevTop = "0";
                    prevLeft = "0";
                    label1.setText("");
                    label2.setText("Shape = Top:" + prevTop + ", Left: " + prevLeft + ", Height: " + height + ", Width:" + width);
                    textArea.setText("");
                }
            });
            // 終了ボタン
            JButton exitButton = new JButton("終了");
            exitButton.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    System.exit(0);
                }
            });
            // Label2の内容をtextAreaに設定するボタン
            JButton setButton = new JButton("座標設定");
            setButton.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    textArea.setText(textArea.getText() + temporaryCoordinate + "\n");
                }
            });
            // textAreaの内容をファイルに出力するボタン
            JButton saveButton = new JButton("CSV保存");
            saveButton.addActionListener(new ActionListener() {
                public void actionPerformed(ActionEvent e) {
                    try {
                        File file = new File("parameter.txt");
                        if (file.exists()) {
                            file.delete();
                        }
                        file.createNewFile();
                        java.io.PrintWriter pw = new java.io.PrintWriter(new java.io.BufferedWriter(new java.io.FileWriter(file)));
                        pw.print(textArea.getText());
                        pw.close();
                    } catch (Exception ex) {
                        ex.printStackTrace();
                    }
                }
            });

            // ラベルを設定するためのパネルを作成する
            JPanel panel2 = new JPanel();
            panel2.setPreferredSize(new Dimension(image.getWidth(), 100));
            panel2.setLayout(new GridLayout(6,1));
            panel2.add(label1);
            panel2.add(label2);
            panel2.add(setButton);
            panel2.add(saveButton);
            panel2.add(resetButton);
            panel2.add(exitButton);

            // UIをフレームに追加して表示する
            frame.add(panel1, BorderLayout.CENTER);
            frame.add(panel2, BorderLayout.SOUTH);
            frame.add(textArea, BorderLayout.EAST);
            frame.setUndecorated(true);
            frame.setVisible(true);

            // マウスでクリックした座標を表示するためのリスナーを追加する
            frame.addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                    int x = e.getX();
                    int y = e.getY();

                    if( x < 0 || y < 0 || x > image.getWidth() || y > image.getHeight() ) {
                        return;
                    }
                    int distanceFromTop = y;
                    int distanceFromLeft = x;

                    // ラベルに座標を表示する
                    top = String.valueOf(distanceFromTop);
                    left = String.valueOf(distanceFromLeft);
                    if(prevTop.equals("0") && prevLeft.equals("0")) {
                        prevTop = top;
                        prevLeft = left;
                    }
                    width = String.valueOf(Integer.parseInt(left) - Integer.parseInt(prevLeft));
                    height = String.valueOf(Integer.parseInt(top) - Integer.parseInt(prevTop));
                    temporaryCoordinate = prevTop + "," + prevLeft + "," + height + "," + width;
                    label2.setText("Shape = Top:" + prevTop + ", Left: " + prevLeft + ", Height: " + height + ", Width:" + width);
                    prevTop = top;
                    prevLeft = left;
            }
            });

            // マウスオーバーイベントでlabel1に現在のx, yの位置を表示する
            frame.addMouseMotionListener(new MouseAdapter() {
                @Override
                public void mouseMoved(MouseEvent e) {
                    int x = e.getX();
                    int y = e.getY();
                    label1.setText("Current X: " + x + ", Y: " + y);
                }
            });

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        try {
            // ファイル選択ダイアログを表示
            FileDialog fileDialog = new FileDialog(new JFrame(), "画像ファイルを選択してください");
            fileDialog.setMode(FileDialog.LOAD);
            fileDialog.setVisible(true);
            String filePath = fileDialog.getDirectory() + fileDialog.getFile();
            System.out.println("filePath: " + filePath);
            if (filePath == null || filePath.isEmpty() || filePath.equals("nullnull") || filePath.contains("nullnull")){
                System.out.println("ファイルが選択されていません");
                System.exit(0);
            } else {
                ImgSelector imgSelector = new ImgSelector(filePath);        
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}