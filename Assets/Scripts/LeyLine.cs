using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class LeyLine : MonoBehaviour {

  public GameObject startSprite;
  public GameObject endSprite;
  public GameObject continueSprite;
  public Color color = Color.white;
  public Transform spriteParent;

  public GameObject spritePrefab;
  public SpriteRenderer signalSprite;
  public bool isPlayerLey;
  private bool hasSprites = false;
  private bool isVisible = false;

  private Beast.BeastLink link;
  private List<GameObject> pathParts = new List<GameObject>();

  public void Start() {
    this.SetVisible(this.isPlayerLey);
  }

  public void ClearPath() {
    this.SetHasSprites(false);
    foreach (GameObject part in this.pathParts) {
      GameObject.Destroy(part);
    }
    this.pathParts = new List<GameObject>();
  }

  private void SetHasSprites(bool hasSprites) {
    this.hasSprites = hasSprites;
    if (this.signalSprite != null) {
      this.signalSprite.color = new Color(1, 1, 1, hasSprites ? 1 : 0);
    }
  }

  public void Pulse() {
    Animator animator = this.GetComponent<Animator>();
    if (this.hasSprites && animator != null) {
      animator.SetTrigger("Pulse");
    }

    if (this.isVisible) {
      foreach (GameObject go in this.pathParts) {
        go.GetComponent<Animator>().SetTrigger("Pulse");
      }
    }
  }

  public void SetVisible(bool visible) {
    this.isVisible = visible;
    Animator animator = this.GetComponent<Animator>();
    if (animator != null) {
      animator.SetTrigger("ChangeVisible");
      animator.SetBool("Visible", visible);
    }
  }

  public void SetColor(Color c) {
    this.color = c;
    foreach (GameObject go in this.pathParts) {
      foreach (SpriteRenderer sr in go.GetComponentsInChildren<SpriteRenderer>()) {
        sr.color = this.color;
      }
    }
  }

  public void MouseOverPath(Beast.BeastLink path) {
    this.ClearPath();
    this.AddPath(path, this.continueSprite, this.continueSprite, this.endSprite, this.endSprite);
  }

  public void AddTutPath(Beast.BeastLink from, Beast.BeastLink to) {
    this.AddPath(to, this.continueSprite, this.continueSprite, this.endSprite, this.endSprite);
    this.AddPath(from, this.continueSprite, this.continueSprite, this.startSprite, this.startSprite);
  }

  public void AddToTutPath(Beast.BeastLink to) {
    this.AddPath(to, this.continueSprite, this.continueSprite, this.startSprite, this.startSprite);
  }

  public void AddIbiTutPath(Beast.BeastLink condA, Beast.BeastLink condB, Beast.BeastLink from, Beast.BeastLink to) {
    this.AddPath(condA, this.continueSprite, this.continueSprite, this.startSprite, this.startSprite);
    this.AddPath(condB, this.continueSprite, this.continueSprite, this.startSprite, this.startSprite);
    this.AddTutPath(from, to);
  }

	public void AddPath(Beast.BeastLink link, GameObject startSprite, GameObject continueSprite, GameObject endSprite, GameObject onlySprite = null) {
    if (onlySprite == null) {
      onlySprite = startSprite;
    }

    this.SetHasSprites(true);

    this.link = link;

    Vector3 currentPosition = this.transform.position;
    Vector3 preScale = this.spriteParent.transform.localScale;
    this.spriteParent.transform.localScale = new Vector3(1, 1, 1);

    for (int i = 0; i < link.directions.Length; i++) {
      GameObject sprite = onlySprite;
      if (link.directions.Length != 1) {
        if (i == 0) {
          sprite = startSprite;
        } else if (i == link.directions.Length - 1) {
          sprite = endSprite;
        } else {
          sprite = continueSprite;
        }
      }

      Vector3 rotation = new Vector3();
      Vector3 position = new Vector3();
      string direction = link.directions[i];
      switch (direction) {
        case "left":
          rotation = new Vector3(0, 0, 180);
          position = currentPosition + new Vector3(-0.5f, 0, 0);
          this.AddLink(sprite, rotation, position);
          currentPosition += new Vector3(-1, 0, 0);
        break;
        case "right":
          rotation = new Vector3(0, 0, 0);
          position = currentPosition + new Vector3(0.5f, 0, 0);
          this.AddLink(sprite, rotation, position);
          currentPosition += new Vector3(1, 0, 0);
        break;
        case "up":
          rotation = new Vector3(0, 0, 90);
          position = currentPosition + new Vector3(0, 0.5f, 0);
          this.AddLink(sprite, rotation, position);
          currentPosition += new Vector3(0, 1, 0);
        break;
        case "down":
          rotation = new Vector3(0, 0, 270);
          position = currentPosition + new Vector3(0, -0.5f, 0);
          this.AddLink(sprite, rotation, position);
          currentPosition += new Vector3(0, -1, 0);
        break;
      }
    }

    this.spriteParent.transform.localScale = preScale;
  }

  private void AddLink(GameObject prefab, Vector3 rotation, Vector3 position) {
    GameObject part = GameObject.Instantiate(prefab, position, Quaternion.identity) as GameObject;
    part.transform.eulerAngles = rotation;
    SpriteRenderer[] srs = part.GetComponentsInChildren<SpriteRenderer>();
    foreach (SpriteRenderer sr in srs) {
      sr.color = this.color;
    }
    part.transform.SetParent(this.spriteParent, true);
    pathParts.Add(part);
  }
}
