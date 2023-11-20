public class NestedLoopExample {

    public static void main(String[] args) {
        // Example of nested loops
        System.out.println("Example of nested loops:");

        // Outer loop
        for (int i = 1; i <= 3; i++) {
            System.out.println("Outer loop iteration: " + i);

            // Inner loop
            for (int j = 1; j <= 4; j++) {
                System.out.println("   Inner loop iteration: " + j);
            }
        }

        // Example of nested loops with if-else statements
        System.out.println("\nExample of nested loops with if-else statements:");

        // Outer loop
        for (int row = 1; row <= 3; row++) {
            // Inner loop
            for (int col = 1; col <= 4; col++) {
                if (col % 2 == 0) {
                    System.out.print("EVEN\t");
                } else {
                    System.out.print("ODD\t");
                }
            }
            System.out.println(); // Move to the next line after each row
        }
    }
}
