package com.root;

import com.root.utils.Utils;
import net.sf.tacos.util.JSONMarkupWriter;
import javax.swing.JFrame;

public class Main extends JFrame {
	public static void main(String[] args){
		System.out.println("Main func");
		new Utils();
	}

	public Main(){
		super("This is a frame");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setSize(200, 200);
		setVisible(true);
		System.out.println("Main constructor, frame should be visible");
		System.out.println("About to throw and exception");
		int[] arr = new int[10];
		try {
			arr[10] = 10;
		} catch (IndexOutOfBoundsException e){
			e.printStackTrace();
		}
		System.out.println("Buuuuuuttt, we're still chugging on");
		System.out.println("Uh oh, now theres about to be a real exception");
		arr[10] = 10;
	}
}
