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
  private Tile clickedTile;
  private Tile overTile;
  private Heart clickedHeart;
  private Heart overHeart;

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
        this.GetPlayerLey().ClearPath();
        this.GetPlayerLey().AddTutPath(tile.link, this.clickedTile.link);
      break;

      case ClickState.HeartDown:
        this.GetPlayerLey().ClearPath();
        this.GetPlayerLey().AddToTutPath(tile.link);
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
        this.overTile.link.set(this.clickedTile.link.get());
      }
      this.PulseBorder();
      this.RefreshScreen();
    }

    if (this.overHeart != Heart.None) {
      this.GetHeartLink(this.overHeart).set(this.clickedTile.beast);
      this.PulseHeart(this.overHeart);
      this.RefreshScreen();
    }

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

  public void HeartMouseOver(string input) {
    this.overHeart = this.stringToHeart(input);
    this.overTile = null;
    this.GetHeartAnimator(stringToHeart(input)).SetBool("Visible", true);
    this.GetHeartAnimator(stringToHeart(input)).SetBool("Throbbing", true);
  }

  public void HeartMouseOut(string input) {
    if (this.currentState != ClickState.HeartDown) {
      this.GetHeartAnimator(stringToHeart(input)).SetBool("Visible", false);
    }
    this.GetHeartAnimator(stringToHeart(input)).SetBool("Throbbing", false);
  }

  public void HeartMouseDown(string input) {
    this.currentState = ClickState.HeartDown;
    this.clickedHeart = this.stringToHeart(input);
    this.overTile = null;
    this.GetHeartAnimator(stringToHeart(input)).SetBool("Clenched", true);
  }

  public void HeartMouseUp(string input) {
    if (this.overTile != null) {
      this.overTile.link.set(this.GetHeartLink(this.clickedHeart).get());
      this.RefreshScreen();
      this.GetHeartAnimator(stringToHeart(input)).SetBool("Visible", false);
      this.PulseHeart(stringToHeart(input));
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

    this.currentState = ClickState.Idle;
    this.GetHeartAnimator(stringToHeart(input)).SetBool("Clenched", false);
  }

  public void PulseBorder() {
    GameObject.FindObjectOfType<GameManager>().PulseBorder();
  }

  public void RefreshScreen() {
    GameObject.FindObjectOfType<GameManager>().RefreshScreen();
  }
}
