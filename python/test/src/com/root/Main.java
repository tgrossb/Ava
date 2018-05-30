package com.root;

import com.root.utils.Utils;
import net.sf.tacos.util.JSONMarkupWriter;

public class Main {
	public static void main(String[] args){
		System.out.println("Main func");
		new Utils();
	}

	public Main(){
		System.out.println("Main constructor");
	}
}
