using UnityEngine;
using System.Collections;

public class Tile : MonoBehaviour {

  public Beast beast;

  public void Render(Beast center) {
    Beast current = center;
    Vector3 target = this.transform.position;

    int dy = (int)(target.y);
    int dx = (int)(target.x);

    int x_sign = dx > 0 ? 1 : -1;
    int y_sign = dy > 0 ? 1 : -1;
    float v = ((float)dy * y_sign) / (dx * x_sign);
    float f = 0;
    for (int x = 0; x < dx * x_sign; x++) {
      f += v;
      while (f >= 1) {
        current = y_sign == 1 ? current.up : current.down;
        f -= 1;
      }
      current = x_sign == 1 ? current.right : current.left;
    }

    if (dx == 0) {
      for (int y = 0; y < dy * y_sign; y++) {
        current = y_sign == 1 ? current.up : current.down;
      }
    }

    this.GetComponent<SpriteRenderer>().sprite = current.sprite;
  }
}
