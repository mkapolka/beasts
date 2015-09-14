using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class Tile : MonoBehaviour {

  public Beast beast;
  public SpriteRenderer newSprite;
  public SpriteRenderer oldSprite;
  public SpriteRenderer inner;
  public LeyLine line;

  public Beast.BeastLink link;

  public void Start() {
    //this.SetLeyLineVisibility(false);
  }

  public void Render(Beast center, bool doAnimations = false) {
    Beast current = center;
    List<string> directions = new List<string>();

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
        directions.Add(lastDirection);
        current = y_sign == 1 ? current.up : current.down;
        f -= 1;
      }
      current = x_sign == 1 ? current.right : current.left;
      lastDirection = x_sign == 1 ? "right" : "left";
      directions.Add(lastDirection);
    }

    if (dx == 0) {
      for (int y = 0; y < dy * y_sign; y++) {
        current = y_sign == 1 ? current.up : current.down;
        lastDirection = y_sign == 1 ? "up" : "down";
        directions.Add(lastDirection);
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

      this.link = new Beast.BeastLink(center, directions.ToArray());
      this.UpdateLeyLines();
    }

  }

  public void UpdateLeyLines() {
    if (this.line) {
      this.line.SetColor(this.beast.color);
      this.line.ClearPath();
      string song = this.beast.song;

      string[] phrases = song.Split(',');
      foreach (string phrase in phrases) {
        string[] words = phrase.Split(' ');
        string command = words[0].Trim();
        if (command == "tut") {
          Beast.BeastLink to = Beast.BeastLink.ParseRelative(this.beast, words[1].Trim());
          Beast.BeastLink from = Beast.BeastLink.ParseRelative(this.beast, words[2].Trim());
          this.line.AddTutPath(from, to);
        }

        if (command == "ibi") {
          Beast.BeastLink a = Beast.BeastLink.ParseRelative(this.beast, words[1].Trim());
          Beast.BeastLink b = Beast.BeastLink.ParseRelative(this.beast, words[2].Trim());
          string c2 = words[3];
          Beast.BeastLink c = Beast.BeastLink.ParseRelative(this.beast, words[4].Trim());
          Beast.BeastLink d = Beast.BeastLink.ParseRelative(this.beast, words[5].Trim());
          this.line.AddIbiTutPath(a, b, d, c);
        }
      }
    }
  }

  public void SetLeyLineVisibility(bool visible) {
    this.line.SetVisible(visible);
  }

  public void SetLeyLineEnabled(bool enabled) {
    this.line.gameObject.SetActive(enabled);
    if (enabled) {
      this.SetLeyLineVisibility(false);
    }
  }

  public void MouseDown() {
    FindObjectOfType<MouseController>().TileMouseDown(this);
  }

  public void MouseOver() {
    FindObjectOfType<MouseController>().TileMouseOver(this);
  }

  public void MouseOut() {
    FindObjectOfType<MouseController>().TileMouseOut(this);
  }

  public void MouseUp() {
    FindObjectOfType<MouseController>().TileMouseUp(this);
  }
}
