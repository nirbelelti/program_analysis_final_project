
class Engine {
    private String fuelType;
    private int size;

    public Engine(String fuelType, int size) {
        this.fuelType = fuelType;
        this.size = size;
    }
public void doSomething() {
    // This method does not return a value.
    // You can perform actions within the method, but it does not produce a return value.
    System.out.println("Doing something...");
}

    public String getFuelType() {
        return fuelType;
    }

    public int getSize() {
        return size;
    }
}
