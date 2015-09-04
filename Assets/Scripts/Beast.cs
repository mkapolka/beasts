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
    public Beast origin;
    public Beast beast;
    public string[] directions;

    public BeastLink(Beast origin, string[] directions) {
      this.origin = origin;
      this.directions = directions;
      this.populateBeast();
    }

    public string getLastDirection() {
      return this.directions[this.directions.Length - 1];
    }

    private void populateBeast() {
      Beast start = this.origin;
      foreach (string direction in this.directions) {
        this.beast = start;
        start = this.hop(start, direction);
      }
    }

    private Beast hop(Beast beast, string direction) {
      switch (direction) {
        case "up":
          return beast.up;
        case "down":
          return beast.down;
        case "left":
          return beast.left;
        case "right":
          return beast.right;
        case "inner":
          return beast.inner;
        default:
          return beast;
      }
    }

    public void set(Beast v) {
      switch (this.getLastDirection()) {
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
      return this.hop(this.beast, this.getLastDirection());
    }

    public BeastLink invert() {
      return this.reciprocate(this);
    }

    public BeastLink reciprocate(BeastLink other) {
      string direction = null;
      switch (other.getLastDirection()) {
        case "up":
          direction = "down";
        break;
        case "down":
          direction = "up";
        break;
        case "left":
          direction = "right";
        break;
        case "right":
          direction = "left";
        break;
        case "inner":
          direction = "inner";
        break;
      }
      return new BeastLink(this.get(), new string[]{direction});
    }

    public BeastLink extend() {
      return new BeastLink(this.get(), new string[]{this.getLastDirection()});
    }

    public static BeastLink ParseRelative(Beast origin, string word) {
      List<string> words = new List<string>();

      while (word.Length > 0) {
        if (word.StartsWith("ro")) {
          words.Add("right");
          word = word.Substring(2);
        } else if (word.StartsWith("go")) {
          words.Add("left");
          word = word.Substring(2);
        } else if (word.StartsWith("bo")) {
          words.Add("up");
          word = word.Substring(2);
        } else if (word.StartsWith("po")) {
          words.Add("down");
          word = word.Substring(2);
        } else if (word.StartsWith("wo")) {
          words.Add("inner");
          word = word.Substring(2);
        } else if (word.StartsWith("ema")) {
          words.Add("self");
          word = word.Substring(3);
        } else {
          throw new System.Exception("Invalid selector: " + word);
        }
      }
      return new BeastLink(origin, words.ToArray());
    }
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
        Beast.BeastLink to_name = BeastLink.ParseRelative(this, parts[1]);
        Beast.BeastLink from_name = BeastLink.ParseRelative(this, parts[2]);
        to_name.set(from_name.get());
      break;

      case "vux":
        to_name = BeastLink.ParseRelative(this, parts[1]);
        from_name = BeastLink.ParseRelative(this, parts[2]);
        Beast a = to_name.get();
        to_name.set(from_name.get());
        from_name.set(a);
      break;

      case "beh":
        to_name = BeastLink.ParseRelative(this, parts[1]);
        from_name = BeastLink.ParseRelative(this, parts[2]);
        this.LinkReciprocally(from_name, to_name);
      break;

      case "puk":
        to_name = BeastLink.ParseRelative(this, parts[1]);
        from_name = to_name.extend();
        this.LinkReciprocally(from_name, to_name);
      break;

      case "yuk":
        to_name = BeastLink.ParseRelative(this, parts[1]);
        from_name = BeastLink.ParseRelative(this, parts[1]);
        BeastLink second = to_name.extend().invert();
        this.LinkReciprocally(from_name, to_name);
        this.LinkReciprocally(second, from_name);
      break;

      case "heen": //heen wo woro = my wo becomes woro, woro's wo becomes ema
        // Reciprocal tut, tut back & clear previous
        to_name = BeastLink.ParseRelative(this, parts[1]);
        from_name = BeastLink.ParseRelative(this, parts[2]);

        to_name.invert().set(to_name.invert().beast);
        from_name.reciprocate(to_name).invert().set(from_name.reciprocate(to_name).get());

        to_name.set(from_name.get());
        from_name.reciprocate(to_name).set(to_name.beast);
      break;

      case "suj":
        Beast to = BeastLink.ParseRelative(this, parts[1]).get();
        Beast from = BeastLink.ParseRelative(this, parts[2]).get();
        to.up = from.up;
        to.down = from.down;
        to.left = from.left;
        to.right = from.right;
        to.inner = from.inner;
      break;

      case "bib":
      case "ibi":
        a = BeastLink.ParseRelative(this, parts[1]).get();
        Beast b = BeastLink.ParseRelative(this, parts[2]).get();
        if (command == "ibi" ? a == b : a != b) {
          List<string> remaining = new List<string>(parts);
          remaining.RemoveRange(0, 3);
          string rest = string.Join(" ", remaining.ToArray());
          this.SingPhrase(rest);
        }
      break;

      case "sujux":
        to = BeastLink.ParseRelative(this, parts[1]).get();
        from = BeastLink.ParseRelative(this, parts[2]).get();
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
      Beast.BeastLink student = BeastLink.ParseRelative(this, parts[1]);
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
