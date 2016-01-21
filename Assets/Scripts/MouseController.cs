using UnityEngine;
using System.Collections;

public class MouseController : MonoBehaviour {

  public enum ClickState {
    Idle, TileDown, HeartDown
  }

  public enum Heart {
    Left, Right, Up, Down, None
  }

  public LeyLine playerLey;

  public Animator leftHeartAnimator;
  public Animator rightHeartAnimator;
  public Animator upHeartAnimator;
  public Animator downHeartAnimator;

  private ClickState currentState = ClickState.Idle;
  private Tile clickedTile = null;
  private Tile overTile = null;
  private Heart clickedHeart = Heart.None;
  private Heart overHeart = Heart.None;

  public LeyLine GetPlayerLey() {
    return this.playerLey;
  }

  public Beast GetPlayer() {
    return GameObject.FindObjectOfType<GameManager>().playerBeast;
  }

  public void TileMouseOver(Tile tile) {
    this.overTile = tile;
    this.overHeart = Heart.None;
    switch (this.currentState) {
      case ClickState.Idle:
        this.GetPlayerLey().MouseOverPath(tile.link);
        tile.SetLeyLineVisibility(true);
      break;

      case ClickState.TileDown:
        this.UpdateLey();
      break;

      case ClickState.HeartDown:
        this.UpdateLey();
      break;
    }
  }

  public void TileMouseOut(Tile tile) {
    tile.SetLeyLineVisibility(false);
  }

  public void TileMouseDown(Tile tile) {
    this.currentState = ClickState.TileDown;
    this.clickedTile = tile;
  }

  private Beast.BeastLink GetHeartLink(Heart heart) {
    switch (heart) {
      case Heart.Left:
        return new Beast.BeastLink(this.GetPlayer(), new string[]{"left"});
      case Heart.Right:
        return new Beast.BeastLink(this.GetPlayer(), new string[]{"right"});
      case Heart.Up:
        return new Beast.BeastLink(this.GetPlayer(), new string[]{"up"});
      case Heart.Down:
        return new Beast.BeastLink(this.GetPlayer(), new string[]{"down"});
    }
    return null;
  }

  public void TileMouseUp(Tile tile) {
    if (this.overTile != null) {
      if (this.clickedTile == this.overTile) {
        this.GetPlayer().inner = this.overTile.beast;
      } else {
        Debug.Log(this.clickedTile.link.origin);
        this.overTile.link.set(this.clickedTile.link.get());
      }
      this.PulseBorder();
      this.PulsePlayerLey();
      this.RefreshScreen();
    }

    if (this.overHeart != Heart.None) {
      this.GetHeartLink(this.overHeart).set(this.clickedTile.beast);
      this.PulseHeart(this.overHeart);
      this.PulsePlayerLey();
      this.RefreshScreen();
    }

    this.clickedTile = null;
    this.currentState = ClickState.Idle;
  }

  private Animator GetHeartAnimator(Heart heart) {
    switch (heart) {
      case Heart.Left:
        return this.leftHeartAnimator;
      case Heart.Right:
        return this.rightHeartAnimator;
      case Heart.Up:
        return this.upHeartAnimator;
      case Heart.Down:
        return this.downHeartAnimator;
    }
    return null;
  }

  public Heart stringToHeart(string input) {
    switch (input) {
      case "left":
        return Heart.Left;
      case "right":
        return Heart.Right;
      case "up":
        return Heart.Up;
      case "down":
        return Heart.Down;
    }
    return Heart.Left;
  }

  public void PulseHeart(Heart heart) {
    this.GetHeartAnimator(heart).SetTrigger("Pulse");
  }

  public void HeartMouseOver(Heart heart) {
    this.overHeart = heart;
    this.overTile = null;
    this.GetHeartAnimator(heart).SetBool("Visible", true);
    this.GetHeartAnimator(heart).SetBool("Throbbing", true);
    this.UpdateLey();
  }

  public void HeartMouseOut(Heart heart) {
    if (this.currentState != ClickState.HeartDown) {
      this.GetHeartAnimator(heart).SetBool("Visible", false);
    }
    this.GetHeartAnimator(heart).SetBool("Throbbing", false);
  }

  public void HeartMouseDown(Heart heart) {
    this.currentState = ClickState.HeartDown;
    this.clickedHeart = heart;
    this.overTile = null;
    this.GetHeartAnimator(heart).SetBool("Clenched", true);
  }

  public void HeartMouseUp(Heart heart) {
    if (this.overTile != null) {
      this.overTile.link.set(this.GetHeartLink(this.clickedHeart).get());
      this.RefreshScreen();
      this.GetHeartAnimator(heart).SetBool("Visible", false);
      this.PulseHeart(heart);
    }

    if (this.overHeart != Heart.None) {
      if (this.overHeart == this.clickedHeart) {
        this.GetPlayer().inner = this.GetHeartLink(this.clickedHeart).get();
        this.RefreshScreen();
        this.PulseHeart(this.clickedHeart);
        this.PulseBorder();
      } else {
        this.GetHeartLink(this.overHeart).set(this.GetHeartLink(this.clickedHeart).get());
        this.PulseHeart(this.clickedHeart);
        this.PulseHeart(this.overHeart);
      }
    }
    this.PulsePlayerLey();

    this.currentState = ClickState.Idle;
    this.clickedHeart = Heart.None;
    this.GetHeartAnimator(heart).SetBool("Clenched", false);
  }

  public void UpdateLey() {
    LeyLine playerLey = this.GetPlayerLey();
    playerLey.ClearPath();

    if (this.clickedTile) {
      playerLey.AddFromTutPath(this.clickedTile.link);
    }

    if (this.overTile) {
      playerLey.AddToTutPath(this.overTile.link);
    }

    if (this.clickedHeart != Heart.None) {
      playerLey.AddFakeHeartPath(this.GetFakeHeartLinkPath(this.clickedHeart));
    }

    if (this.overHeart != Heart.None) {
      playerLey.AddFakeHeartPath(this.GetFakeHeartLinkPath(this.overHeart));
    }
  }

  public void PulseBorder() {
    GameObject.FindObjectOfType<GameManager>().PulseBorder();
  }
  
  public void PulsePlayerLey() {
    GameObject.FindObjectOfType<GameManager>().PulsePlayerLey();
  }

  public void RefreshScreen() {
    GameObject.FindObjectOfType<GameManager>().RefreshScreen(true);
  }

  public Beast.BeastLink GetFakeHeartLinkPath(Heart heart) {
    string[] directions = null;
    switch (heart) {
      case Heart.Left:
        directions = new string[]{"left", "left", "left", "left", "left", "left", "left"};
      break;
      case Heart.Right:
        directions = new string[]{"right", "right", "right", "right", "right", "right", "right"};
      break;
      case Heart.Up:
        directions = new string[]{"up", "up", "up", "up", "up", "up", "up"};
      break;
      case Heart.Down:
        directions = new string[]{"down", "down", "down", "down", "down", "down", "down"};
      break;
    }
    return new Beast.BeastLink(this.GetPlayer(), directions);
  }
}
