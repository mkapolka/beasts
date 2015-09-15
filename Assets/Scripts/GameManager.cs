using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using System.Collections.Generic;

public class GameManager : MonoBehaviour {
  public enum MouseMode {
    Move, Look
  }

  public const float MOVE_TIME = .1f;
  public const float TICK_TIME = 1.0f;

  public static List<Beast> withSongs = new List<Beast>();

  public Dictionary<string, Beast> beasts = new Dictionary<string, Beast>();
	public Beast playerBeast;
	public Beast lurkerBeast;
  public Tile centerTile;
  private float moveTimer = MOVE_TIME;
  private float tickTimer = TICK_TIME;

  public InputField songField;
  public Image upImage;
  public Image downImage;
  public Image leftImage;
  public Image rightImage;
  public Animator borderAnimator;
  public GameObject eyeBall;

  public LeyLine playerLey;

  public Text tileSong;

  private bool leyLinesActive = true;

  public Beast LoadBeasts() {
    string data = Resources.Load<TextAsset>("output").text;
    string[] lines = data.Split('\n');
    //Dictionary<string, Beast> beasts = new Dictionary<string, Beast>();
    foreach (string line in lines) {
      if (line.Length < 1 || line[0] == '#') {
        continue;
      }
      string[] parts = line.Split(',');
      string id = parts[0];
      string resource = parts[1];
      Sprite sprite = Resources.Load<Sprite>(resource);
      Beast b = new Beast();
      b.sprite = sprite;
      this.beasts.Add(id, b);
    }

    foreach (string line in lines) {
      if (line.Length < 1 || line[0] == '#') {
        continue;
      }
      string[] parts = line.Split(',');
      string id = parts[0];
      Beast b = this.beasts[id];
      b.right = this.beasts[parts[2]];
      b.up = this.beasts[parts[3]];
      b.left = this.beasts[parts[4]];
      b.down = this.beasts[parts[5]];
      b.inner = this.beasts[parts[6]];
      b.SetSong(parts[7].Replace('/', ','));
      b.tickTime = float.Parse(parts[8]);
      b.currentTickTime = float.Parse(parts[8]);
    }

    return this.beasts["player"];
  }

  public void Start() {
    this.playerBeast = this.LoadBeasts();
    this.lurkerBeast = this.beasts["player_lurker"];

    this.RefreshScreen();
  }

  public void RefreshScreen(bool doAnimations = false) {
    foreach (Tile tile in GameObject.FindObjectsOfType<Tile>()) {
      tile.Render(this.playerBeast.inner, doAnimations);
    }
    this.upImage.sprite = this.playerBeast.up.sprite;
    this.downImage.sprite = this.playerBeast.down.sprite;
    this.leftImage.sprite = this.playerBeast.left.sprite;
    this.rightImage.sprite = this.playerBeast.right.sprite;

    this.upImage.color = this.upImage.sprite == null ? Color.clear : Color.white;
    this.downImage.color = this.downImage.sprite == null ? Color.clear : Color.white;
    this.leftImage.color = this.leftImage.sprite == null ? Color.clear : Color.white;
    this.rightImage.color = this.rightImage.sprite == null ? Color.clear : Color.white;

    this.tileSong.text = this.playerBeast.inner.song;
  }

  public bool DoKeys() {
    if (Input.GetKey("left")) {
      this.playerBeast.Sing("tut wo wogo");
      return true;
    }
    if (Input.GetKey("right")) {
      this.playerBeast.Sing("tut wo woro");
      return true;
    }
    if (Input.GetKey("up")) {
      this.playerBeast.Sing("tut wo wobo");
      return true;
    }
    if (Input.GetKey("down")) {
      this.playerBeast.Sing("tut wo wopo");
      return true;
    }
    if (Input.GetKey(">")) {
      this.playerBeast.Sing("tut wo wowo");
      return true;
    }

    return false;
  }

  public void Update() {
    if (Input.GetKeyUp("left") || Input.GetKeyUp("right") || Input.GetKeyUp("down") || Input.GetKeyUp("up")) {
      this.moveTimer = 0;
    }

    this.moveTimer -= Time.deltaTime;
    this.tickTimer -= Time.deltaTime;
    if (Input.GetKeyDown(KeyCode.Return)) {
      if (!this.songField.interactable) {
        this.songField.text = "";
        this.songField.Select();
        this.songField.interactable = true;
        this.songField.ActivateInputField();
        this.songField.GetComponent<CanvasGroup>().alpha = 1;
      } else {
        this.UISing(this.songField.text);
        this.songField.interactable = false;
        this.songField.DeactivateInputField();
        this.songField.GetComponent<CanvasGroup>().alpha = 0;
      }
    }
    if (this.moveTimer < 0) {
      bool reset = this.DoKeys();
      if (reset) {
        this.moveTimer = GameManager.MOVE_TIME;
        this.lurkerBeast.Sing();
        this.PulseBorder();
        this.PulsePlayerLey();
        this.RefreshScreen(true);
      }
    }

    this.Tick();
    this.RefreshScreen(true);
  }

  public void Tick() {
    Dictionary<Beast, List<Tile>> linkies = new Dictionary<Beast, List<Tile>>();
    foreach (Tile tile in GameObject.FindObjectsOfType<Tile>()) {
      if (!linkies.ContainsKey(tile.beast)) {
        linkies.Add(tile.beast, new List<Tile>(new Tile[]{tile}));
      } else {
        linkies[tile.beast].Add(tile);
      }
    }

    foreach (Beast beast in GameManager.withSongs) {
      beast.currentTickTime -= Time.deltaTime;
      if (beast.currentTickTime < 0) {
        beast.currentTickTime = beast.tickTime;
        beast.Sing();
        if (linkies.ContainsKey(beast)) {
          foreach (Tile tile in linkies[beast]) {
            tile.line.Pulse();
          }
        }
      }
    }
  }

  public Tile TileAt(int x, int y) {
    foreach (Tile tile in FindObjectsOfType(typeof(Tile))) {
      if (tile.transform.position.x == x && tile.transform.position.y == y) {
        return tile;
      }
    }
    return null;
  }

  public void MouseOver(Beast.BeastLink link) {
    this.playerLey.MouseOverPath(link);
  }

  public void PulseBorder() {
    this.borderAnimator.SetTrigger("Pulse");
  }

  public void PulsePlayerLey() {
    this.playerLey.Pulse();
  }

  public void UISing(string song) {
    this.playerBeast.Sing(song);
    this.lurkerBeast.Sing();
    this.RefreshScreen();
    this.PulseBorder();
  }

  public void ClickEyeball() {
    this.leyLinesActive = !this.leyLinesActive;
    foreach (Tile tile in GameObject.FindObjectsOfType<Tile>()) {
      tile.SetLeyLineEnabled(this.leyLinesActive);
    }
    this.playerLey.gameObject.SetActive(this.leyLinesActive);
    this.eyeBall.GetComponent<Animator>().SetBool("Enabled", this.leyLinesActive);
  }
}
