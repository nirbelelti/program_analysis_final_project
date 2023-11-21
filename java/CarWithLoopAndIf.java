import java.util.ArrayList;
import java.util.List;

class Engine {
    private String fuelType;
    private int size;

    public Engine(String fuelType, int size) {
        this.fuelType = fuelType;
        this.size = size;
    }

    public String getFuelType() {
        return this.fuelType;
    }

    public int getSize() {
        return this.size;
    }
}

class Car {
    private String manufacturer;
    private int manufactureYear;
    private String model;
    private Engine engine;

    public Car(String manufacturer, int manufactureYear, String model, Engine engine) {
        this.manufacturer = manufacturer;
        this.manufactureYear = manufactureYear;
        this.model = model;
        this.engine = engine;
    }

    public String getManufacturer() {
        return manufacturer;
    }

    public int getManufactureYear() {
        return manufactureYear;
    }

    public String getModel() {
        return model;
    }

    public Engine getEngine() {
        return engine;
    }
}

class Person {
    private String name;
    private List<Car> cars;

    public Person(String name) {
        this.name = name;
        this.cars = new ArrayList<>();
    }

    public void addCar(Car car) {
        cars.add(car);
    }

    public List<Car> getCars() {
        return cars;
    }

    public void removeCar(Car car){
        cars.remove(car);
    }
    public double calculateInsuranceFee() {
        double baseFee = 1000;

        if (cars.size() > 1) {
            for (int i = 1; i < cars.size(); i++) {
                baseFee += 0.8 * 1000; // 20% discount for each additional car
            }
        }

        return baseFee;
    }

    @Override
    public String toString() {
        return "Person{" +
                "name='" + name + '\'' +
                ", cars=" + cars +
                '}';
    }
}

public class Main {

    public static void main(String[] args) {
        Engine engine1 = new Engine("Petrol", 2000);
        Car car1 = new Car("Toyota", 2015, "Corolla", engine1);
        Engine engine2 = new Engine("Diesel", 2500);

        Car car2 = new Car("Ford", 2020, "Mustang", engine2);

        Person person = new Person("John");
        person.addCar(car1);
        person.addCar(car2);

        for(int i = 0; i< person.getCars().size(); i++){
           person.getCars().get(i).getManufacturer();

        }

        if(person.getCars().size()>0){
            person.calculateInsuranceFee();
        }



    }


}