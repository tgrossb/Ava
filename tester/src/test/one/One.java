package test.one;

import test.two.Two;
import test.two.three.Three;

public class One {
	public static void main(String[] args){
		System.out.println("Two: " + (new Two()).two() + ", three: " + (new Three()).three());
	}
}
