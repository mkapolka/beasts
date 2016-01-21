public class Utils {
  public static string GetReciprocalDirection(string direction) {
    switch (direction) {
      case "left":
        return "right";
      break;
      case "right":
        return "left";
      break;
      case "up":
        return "down";
      break;
      case "down":
        return "up";
      break;
      case "inner":
        return "inner";
      break;
    }
    throw new System.Exception("Not a valid direction");
  }
}
