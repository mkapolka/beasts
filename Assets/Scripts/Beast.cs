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
  public Color color;

  public Beast() {
    this.up = this;
    this.down = this;
    this.left = this;
    this.right = this;
    this.inner = this;
    this.color = new Color(Random.Range(.8f, 1.0f), Random.Range(.8f, 1.0f), Random.Range(.8f, 1.0f));
  }

  public void SetSong(string song) {
    this.song = song;
    if (this.song != null) {
      if (!GameManager.withSongs.Contains(this)) {
        GameManager.withSongs.Add(this);
      }
    } else {
      if (GameManager.withSongs.Contains(this)) {
        GameManager.withSongs.Remove(this);
      }
    }
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
        case "all":
          this.beast.left = v;
          this.beast.right = v;
          this.beast.up = v;
          this.beast.down = v;
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

    public BeastLink invert() {
      return this.reciprocate(this);
    }

    public BeastLink reciprocate(BeastLink other) {
      BeastLink output = new BeastLink(this.get(), "");
      switch (other.direction) {
        case "up":
          output.direction = "down";
        break;
        case "down":
          output.direction = "up";
        break;
        case "left":
          output.direction = "right";
        break;
        case "right":
          output.direction = "left";
        break;
        case "inner":
          output.direction = "inner";
        break;
      }
      return output;
    }

    public BeastLink extend() {
      return new BeastLink(this.get(), this.direction);
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

  public void LinkReciprocally(BeastLink from, BeastLink to) {
    from.reciprocate(to).set(to.beast);
    to.set(from.get());
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

      case "beh":
        to_name = this.ParseRelative(parts[1]);
        from_name = this.ParseRelative(parts[2]);
        this.LinkReciprocally(from_name, to_name);
      break;

      case "puk":
        to_name = this.ParseRelative(parts[1]);
        from_name = to_name.extend();
        this.LinkReciprocally(from_name, to_name);
      break;

      case "yuk":
        to_name = this.ParseRelative(parts[1]);
        from_name = this.ParseRelative(parts[1]);
        BeastLink second = to_name.extend().invert();
        this.LinkReciprocally(from_name, to_name);
        this.LinkReciprocally(second, from_name);
      break;

      case "heen": //heen wo woro = my wo becomes woro, woro's wo becomes ema
        // Reciprocal tut, tut back & clear previous
        to_name = this.ParseRelative(parts[1]);
        from_name = this.ParseRelative(parts[2]);

        to_name.invert().set(to_name.invert().beast);
        from_name.reciprocate(to_name).invert().set(from_name.reciprocate(to_name).get());

        to_name.set(from_name.get());
        from_name.reciprocate(to_name).set(to_name.beast);
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

      case "bib":
      case "ibi":
        a = this.ParseRelative(parts[1]).get();
        Beast b = this.ParseRelative(parts[2]).get();
        if (command == "ibi" ? a == b : a != b) {
          List<string> remaining = new List<string>(parts);
          remaining.RemoveRange(0, 3);
          string rest = string.Join(" ", remaining.ToArray());
          this.SingPhrase(rest);
        }
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
    }
  }

  public void Sing(string song) {
    string[] parts = song.Split(' ');
    if (parts[0] == "qub") {
      Beast.BeastLink student = this.ParseRelative(parts[1]);
      List<string> remaining = new List<string>(parts);
      remaining.RemoveRange(0, 2);
      string to_teach = string.Join(" ", remaining.ToArray());
      student.get().song = to_teach;
    } else {
      string[] phrases = song.Split(',');
      foreach (string phrase in phrases) {
         this.SingPhrase(phrase);
      }
    }
  }

  public void Sing() {
    if (this.song != null) {
      this.Sing(this.song);
    }
  }
}
