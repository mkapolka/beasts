using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class Beast {
  public Beast up;
  public Beast down;
  public Beast right;
  public Beast left;
  public Beast inner;

  public string song = null;

  public Sprite sprite;

  public Beast() {
    this.up = this;
    this.down = this;
    this.left = this;
    this.right = this;
    this.inner = this;
  }

  public class BeastLink {
    public Beast beast;
    public string direction;

    public BeastLink(Beast beast, string direction) {
      this.beast = beast;
      this.direction = direction;
    }

    public void set(Beast v) {
      switch (this.direction) {
        case "up":
          this.beast.up = v;
        break;
        case "down":
          this.beast.down = v;
        break;
        case "left":
          this.beast.left = v;
        break;
        case "right":
          this.beast.right = v;
        break;
        case "inner":
          this.beast.inner = v;
        break;
        case "self":
          throw new System.Exception("Can't tut ema.");
      }
    }

    public Beast get() {
      switch (this.direction) {
        case "up":
          return this.beast.up;
        case "down":
          return this.beast.down;
        case "left":
          return this.beast.left;
        case "right":
          return this.beast.right;
        case "inner":
          return this.beast.inner;
        default:
          return this.beast;
      }
    }
  }

  public Beast.BeastLink ParseRelative(string word) {
    BeastLink current = new Beast.BeastLink(this, "self");
    if (word == "ema") {
      return current;
    }

    while (word.Length > 0) {
      if (word.StartsWith("ro")) {
        current = new Beast.BeastLink(current.get(), "right");
        word = word.Substring(2);
      } else if (word.StartsWith("go")) {
        current = new Beast.BeastLink(current.get(), "left");
        word = word.Substring(2);
      } else if (word.StartsWith("bo")) {
        current = new Beast.BeastLink(current.get(), "up");
        word = word.Substring(2);
      } else if (word.StartsWith("po")) {
        current = new Beast.BeastLink(current.get(), "down");
        word = word.Substring(2);
      } else if (word.StartsWith("wo")) {
        current = new Beast.BeastLink(current.get(), "inner");
        word = word.Substring(2);
      } else {
        throw new System.Exception("Invalid selector: " + word);
      }
    }
    return current;
  }

  public void SingPhrase(string song) {
    string[] parts = song.Trim().Split(' ');

    string command = parts[0];
    switch (command) {
      case "tut":
        Beast.BeastLink to_name = this.ParseRelative(parts[1]);
        Beast.BeastLink from_name = this.ParseRelative(parts[2]);
        to_name.set(from_name.get());
      break;

      case "vux":
        to_name = this.ParseRelative(parts[1]);
        from_name = this.ParseRelative(parts[2]);
        Beast a = to_name.get();
        to_name.set(from_name.get());
        from_name.set(a);
      break;

      case "suj":
        Beast to = this.ParseRelative(parts[1]).get();
        Beast from = this.ParseRelative(parts[2]).get();
        to.up = from.up;
        to.down = from.down;
        to.left = from.left;
        to.right = from.right;
        to.inner = from.inner;
      break;

      case "sujux":
        to = this.ParseRelative(parts[1]).get();
        from = this.ParseRelative(parts[2]).get();
        Beast tou = to.up;
        Beast tod = to.down;
        Beast tol = to.left;
        Beast tor = to.right;
        Beast toi = to.inner;
        to.up = from.up;
        to.down = from.down;
        to.left = from.left;
        to.right = from.right;
        to.inner = from.inner;
        from.up = tou;
        from.down = tod;
        from.left = tol;
        from.right = tor;
        from.inner = toi;
      break;

      case "zul":
        Beast.BeastLink student = this.ParseRelative(parts[1]);
        List<string> remaining = new List<string>(parts);
        remaining.RemoveRange(0, 2);
        string to_teach = string.Join(" ", remaining.ToArray());
        student.get().song = to_teach;
      break;
    }
  }

  public void Sing(string song) {
    string[] phrases = song.Split(',');
    foreach (string phrase in phrases) {
      this.SingPhrase(phrase);
    }
  }

  public void Sing() {
    if (this.song != null) {
      this.Sing(this.song);
    }
  }
}
