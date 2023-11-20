public class MultiplicationTableExample {

    public static void main(String[] args) {
        // Example of a multiplication table using nested loops
        System.out.println("Multiplication Table:");

        // Outer loop for rows (multiplicands)
        for (int i = 1; i <= 5; i++) {
            // Inner loop for columns (multipliers)
            for (int j = 1; j <= 5; j++) {
                // Calculate and print the product
                int product = i * j;
                System.out.print(i + " * " + j + " = " + product + "\t");
            }
            System.out.println(); // Move to the next line after each row
        }
    }
}
