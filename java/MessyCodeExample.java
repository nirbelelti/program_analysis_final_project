import java.util.Random;

public class MessyCodeExample {

    public static void main(String[] args) {
        int input = 1; // You can change this to 2 for different behavior
        MessyCodeExample instance = new MessyCodeExample();
        String result = instance.performComplexTask(input);
        String result2 = instance.performComplexTask(2);
        System.out.println("Result:\n" + result);
        System.out.println("Resul2:\n" + result2);
    }

    public String performComplexTask(int input) {
        System.out.println("Performing complex task with input: " + input);

        StringBuilder result = new StringBuilder();

        for (int i = 0; i < 3; i++) {
            System.out.println("Iteration " + i);
            // Messy code...
            if (input == 1) {
                result.append(Class1.method1(i)).append("\n");
                result.append(Class1.method2(i)).append("\n");
            } else if (input == 2) {
                result.append(Class2.method3(i)).append("\n");
            } else {
                result.append("Default behavior for other inputs.").append("\n");
            }
            // More messy code...
        }

        return result.toString();
    }
}

class Class1 {
    static String method1(int iteration) {
        // Randomize a value
        Random random = new Random();
        int randomValue = random.nextInt(100);
        return "Class1 - Method1 - Random Value: " + randomValue + " - Iteration: " + iteration;
    }

    static String method2(int iteration) {
        // Count something based on iteration
        int count = iteration * 2;
        return "Class1 - Method2 - Count: " + count + " - Iteration: " + iteration;
    }
}

class Class2 {
    static String method3(int iteration) {
        // Base case: return the current iteration
        if (iteration == 0) {
            return "Class2 - Method3 - Iteration: " + iteration;
        } else {
            // Recursive case: call itself a random number of times between 2 and 5
            Random random = new Random();
            int numberOfCalls = random.nextInt(4) + 2; // Random number between 2 and 5
            StringBuilder result = new StringBuilder();

            for (int i = 0; i < numberOfCalls; i++) {
                result.append(method3(iteration - 1)).append("\n");
            }

            return result.toString();
        }
    }
}
