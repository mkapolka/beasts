﻿using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class Tile : MonoBehaviour {

  public Beast beast;
  public Beast innerBeast;
  public SpriteRenderer newSprite;
  public SpriteRenderer oldSprite;
  public SpriteRenderer inner;
  public SpriteRenderer oldInner;
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
    bool innerChanged = this.innerBeast != current.inner;
    this.innerBeast = current.inner;
    this.beast = current;

    if (innerChanged && !beastChanged) {
      if (doAnimations) {
        StartCoroutine(this.DoInnerAnimation(directions.Count, current.inner));
      } else {
        this.SetInnerBeastSprites(current.inner);
      }
    }

    if (beastChanged) {
      if (doAnimations) {
        StartCoroutine(this.DoAnimation(directions.Count, current, lastDirection));
      } else {
        this.oldSprite.sprite = current.sprite;
        this.oldSprite.color = current.color;
        this.newSprite.sprite = current.sprite;
        this.newSprite.color = current.color;

        this.SetInnerBeastSprites(current.inner);
      }

      this.link = new Beast.BeastLink(center, directions.ToArray());
      this.UpdateLeyLines();
    }
  }

  private void SetInnerBeastSprites(Beast newInnerBeast) {
      this.oldInner.sprite = this.inner.sprite;
      this.oldInner.color = this.inner.color;

      if (newInnerBeast != this.beast) {
        this.inner.sprite = newInnerBeast.sprite;
        this.inner.color = newInnerBeast.color;
      } else {
        this.inner.sprite = null;
      }
  }

  public IEnumerator DoInnerAnimation(int distance, Beast newInnerBeast) {
    float time = distance * .05f;
    while (time > 0) {
      time -= Time.deltaTime;
      yield return null;
    }

    this.oldInner.sprite = this.inner.sprite;
    this.oldInner.color = this.inner.color;

    if (newInnerBeast != this.beast) {
      this.inner.sprite = newInnerBeast.sprite;
      this.inner.color = newInnerBeast.color;
    } else {
      this.inner.sprite = null;
    }

    this.GetComponent<Animator>().SetTrigger("InnerFill");
  }

  public IEnumerator DoAnimation(int distance, Beast newBeast, string direction) {
    float time = distance * .05f;
    while (time > 0) {
      time -= Time.deltaTime;
      yield return null;
    }

    this.SetInnerBeastSprites(newBeast.inner);
    /*if (newBeast.inner != newBeast) {
      this.inner.sprite = newBeast.inner.sprite;
      this.inner.color = newBeast.inner.color;
    } else {
      this.inner.sprite = null;
    }*/

    this.oldSprite.sprite = this.newSprite.sprite;
    this.oldSprite.color = this.newSprite.color;
    this.newSprite.sprite = newBeast.sprite;
    this.newSprite.color = newBeast.color;

    this.GetComponent<Animator>().SetTrigger("Fill");
    this.GetComponent<Animator>().SetTrigger("InnerFill");
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
