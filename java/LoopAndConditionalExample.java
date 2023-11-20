public class LoopAndConditionalExample {

    public static void main(String[] args) {
        // Example of a for loop
        System.out.println("Example of a for loop:");
        for (int i = 1; i <= 5; i++) {
            System.out.println("Iteration " + i);
        }

        System.out.println("\nExample of if-else statements:");
        // Example of if-else statements
        int number = 10;

        if (number > 0) {
            System.out.println(number + " is a positive number.");
        } else if (number < 0) {
            System.out.println(number + " is a negative number.");
        } else {
            System.out.println(number + " is zero.");
        }

        // Example of a while loop
        System.out.println("\nExample of a while loop:");
        int count = 1;
        while (count <= 3) {
            System.out.println("Count: " + count);
            count++;
        }
    }
}
