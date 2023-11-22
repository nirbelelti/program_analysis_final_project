import java.util.List;

public class Main {

    public static void main(String[] args) {
        Engine engine1 = new Engine("Petrol", 2000);
        Car car1 = new Car("Toyota", 2015, "Corolla", engine1);
        Engine engine2 = new Engine("Diesel", 2500);

        Car car2 = new Car("Ford", 2020, "Mustang", engine2);

        Person person = new Person("John");
        person.addCar(car1);
        person.addCar(car2);

        for (int i = 0; i < person.getCars().size(); i++) {
            Car car = person.getCars().get(i);
            car.getManufacturer();

        }

        if (person.getCars().size() > 0) {
            person.calculateInsuranceFee();
        } else if (person.getCars().size() == 0) {
            car1.getManufacturer();
        } else {
            car2.getManufacturer();
        }

        List<Car> cars = person.getCars();
        int carsAmount = cars.size();
        while (carsAmount--) {
            Car car = car2.get(carsAmount);
            System.out.println(car.getEngine());
        }

    }
}