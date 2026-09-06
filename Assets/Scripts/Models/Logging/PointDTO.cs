using System;

[Serializable]
public class PointDto
{
    public int X;
    public int Y;

    public PointDto() { }

    public PointDto(Point point)
    {
        X = point.X;
        Y = point.Y;
    }

    public Point ToPoint()
    {
        return new Point(X, Y);
    }
}