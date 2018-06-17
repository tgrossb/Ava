package com.root;

import com.root.utils.Utils;
import net.sf.tacos.util.JSONMarkupWriter;
import javax.swing.JFrame;

public class Main extends JFrame {
	public static void main(String[] args){
		String s = "Nothing";
		if (args.length > 0)
			s = args[0];
		System.out.println("Main func got: " + s);
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
