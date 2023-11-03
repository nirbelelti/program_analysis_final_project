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

