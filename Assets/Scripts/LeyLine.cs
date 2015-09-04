using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class LeyLine : MonoBehaviour {

  public Sprite horizontalSprite;
  public Sprite verticalSprite;
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

	public void SetPath(Beast.BeastLink link) {
    this.link = link;

    Vector3 currentPosition = this.transform.position;

    foreach (string direction in link.directions) {
      switch (direction) {
        case "left":
          this.AddLink(this.horizontalSprite, currentPosition + new Vector3(-0.5f, 0, 0));
          currentPosition += new Vector3(-1, 0, 0);
        break;
        case "right":
          this.AddLink(this.horizontalSprite, currentPosition + new Vector3(0.5f, 0, 0));
          currentPosition += new Vector3(1, 0, 0);
        break;
        case "up":
          this.AddLink(this.verticalSprite, currentPosition + new Vector3(0, 0.5f, 0));
          currentPosition += new Vector3(0, 1, 0);
        break;
        case "down":
          this.AddLink(this.verticalSprite, currentPosition + new Vector3(0, -0.5f, 0));
          currentPosition += new Vector3(0, -1, 0);
        break;
      }
    }
  }

  private void AddLink(Sprite sprite, Vector3 position) {
    GameObject part = GameObject.Instantiate(this.spritePrefab, position, Quaternion.identity) as GameObject;
    SpriteRenderer sr = part.GetComponent<SpriteRenderer>();
    sr.sprite = sprite;
    sr.color = this.color;
    part.transform.SetParent(this.transform, true);
    pathParts.Add(part);
  }
}
