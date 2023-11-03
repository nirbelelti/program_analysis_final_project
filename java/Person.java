import java.util.ArrayList;
import java.util.List;

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

    @Override
    public String toString() {
        return "Person{" +
                "name='" + name + '\'' +
                ", cars=" + cars +
                '}';
    }
}
