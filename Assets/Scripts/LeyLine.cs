using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class LeyLine : MonoBehaviour {

  public GameObject startSprite;
  public GameObject endSprite;
  public GameObject continueSprite;
  public Color color;

  public GameObject spritePrefab;

  private Beast.BeastLink link;
  private List<GameObject> pathParts = new List<GameObject>();

  public void ClearPath() {
    foreach (GameObject part in this.pathParts) {
      GameObject.Destroy(part);
    }
    this.pathParts = new List<GameObject>();
  }

  public void AddTutPath(Beast.BeastLink from, Beast.BeastLink to) {
    this.AddPath(to, this.endSprite, this.continueSprite, this.continueSprite, this.endSprite);
    this.AddPath(from, this.continueSprite, this.continueSprite, this.startSprite, this.startSprite);
  }

	public void AddPath(Beast.BeastLink link, GameObject startSprite, GameObject continueSprite, GameObject endSprite, GameObject onlySprite = null) {
    if (onlySprite == null) {
      onlySprite = startSprite;
    }

    this.link = link;

    Vector3 currentPosition = this.transform.position;

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
  }

  private void AddLink(GameObject prefab, Vector3 rotation, Vector3 position) {
    GameObject part = GameObject.Instantiate(prefab, position, Quaternion.identity) as GameObject;
    part.transform.eulerAngles = rotation;
    SpriteRenderer sr = part.GetComponent<SpriteRenderer>();
    sr.color = this.color;
    part.transform.SetParent(this.transform, true);
    pathParts.Add(part);
  }
}
