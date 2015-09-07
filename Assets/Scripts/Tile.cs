using UnityEngine;
using System.Collections;

public class Tile : MonoBehaviour {

  public Beast beast;
  public SpriteRenderer newSprite;
  public SpriteRenderer oldSprite;
  public SpriteRenderer inner;

  public void Render(Beast center, bool doAnimations = false) {
    Beast current = center;

    Vector3 target = this.transform.position;

    int dy = (int)(target.y);
    int dx = (int)(target.x);

    int x_sign = dx > 0 ? 1 : -1;
    int y_sign = dy > 0 ? 1 : -1;
    float v = ((float)dy * y_sign) / (dx * x_sign);
    float f = 0;
    string lastDirection = null;
    for (int x = 0; x < dx * x_sign; x++) {
      f += v;
      while (f >= 1) {
        lastDirection = y_sign == 1 ? "up" : "down";
        current = y_sign == 1 ? current.up : current.down;
        f -= 1;
      }
      current = x_sign == 1 ? current.right : current.left;
      lastDirection = x_sign == 1 ? "right" : "left";
    }

    if (dx == 0) {
      for (int y = 0; y < dy * y_sign; y++) {
        current = y_sign == 1 ? current.up : current.down;
        lastDirection = y_sign == 1 ? "up" : "down";
      }
    }

    bool beastChanged = this.beast != current;
    this.beast = current;

    if (beastChanged) {
      this.oldSprite.sprite = this.newSprite.sprite;
      this.oldSprite.color = this.newSprite.color;
    }

    this.newSprite.sprite = current.sprite;
    this.newSprite.color = current.color;
    if (current.inner != current) {
      this.inner.sprite = current.inner.sprite;
      this.inner.color = current.inner.color;
    } else {
      this.inner.sprite = null;
    }

    if (beastChanged) {
      if (doAnimations) {
        switch (lastDirection) {
          case "down":
            this.GetComponent<Animator>().SetTrigger("DownFill");
          break;
          case "up":
            this.GetComponent<Animator>().SetTrigger("UpFill");
          break;
          case "left":
            this.GetComponent<Animator>().SetTrigger("LeftFill");
          break;
          case "right":
            this.GetComponent<Animator>().SetTrigger("RightFill");
          break;
        }
      }

      this.UpdateLeyLines();
    }

  }

  public void UpdateLeyLines() {
    LeyLine line = this.GetComponent<LeyLine>();
    if (line) {
      float aFactor = Mathf.Max(1, this.transform.position.magnitude * 2);
      Color color = this.beast.color + new Color(0, 0, 0, 0);
      color.a = (1 / aFactor);

      line.color = color;
      line.ClearPath();
      string song = this.beast.song;

      string[] phrases = song.Split(',');
      foreach (string phrase in phrases) {
        string[] words = phrase.Split(' ');
        string command = words[0].Trim();
        if (command == "tut") {
          Beast.BeastLink to = Beast.BeastLink.ParseRelative(this.beast, words[1].Trim());
          Beast.BeastLink from = Beast.BeastLink.ParseRelative(this.beast, words[2].Trim());
          line.AddTutPath(from, to);
        }

        if (command == "ibi") {
          Beast.BeastLink a = Beast.BeastLink.ParseRelative(this.beast, words[1].Trim());
          Beast.BeastLink b = Beast.BeastLink.ParseRelative(this.beast, words[1].Trim());
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
