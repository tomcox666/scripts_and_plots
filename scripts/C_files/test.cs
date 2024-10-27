public interface IMovable
{
    void Move(int distance);
}

public class Car : IMovable
{
    public void Move(int distance)
    {
        Console.WriteLine($"Car moved {distance} meters.");
    }
}
                  

IMovable movable = new Car();
movable.Move(100);  // Outputs: Car moved 100 meters.