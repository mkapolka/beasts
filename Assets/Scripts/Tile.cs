using UnityEngine;
using System.Collections;

public class Tile : MonoBehaviour {

  public Beast beast;
  public SpriteRenderer inner;

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

    this.beast = current;
    this.GetComponent<SpriteRenderer>().sprite = current.sprite;
    this.GetComponent<SpriteRenderer>().color = current.color;
    if (current.inner != current) {
      this.inner.sprite = current.inner.sprite;
      this.inner.color = current.inner.color;
    } else {
      this.inner.sprite = null;
    }

    this.UpdateLeyLines();
  }

  public void UpdateLeyLines() {
    LeyLine line = this.GetComponent<LeyLine>();
    if (line) {
      line.color = this.beast.color;
      line.ClearPath();
      string song = this.beast.song;

      string[] phrases = song.Split(',');
      foreach (string phrase in phrases) {
        string[] words = phrase.Split(' ');
        string command = words[0].Trim();
        if (command == "tut") {
          Beast.BeastLink from = Beast.BeastLink.ParseRelative(this.beast, words[1].Trim());
          Beast.BeastLink to = Beast.BeastLink.ParseRelative(this.beast, words[2].Trim());
          line.SetPath(from);
          line.SetPath(to);
        }
      }
    }
  }

  public void OnMouseDown() {
    GameManager gm = FindObjectOfType<GameManager>();
    gm.playerBeast.inner = this.beast;
    gm.RefreshScreen();
  }
}
