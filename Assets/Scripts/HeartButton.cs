using UnityEngine;
using System.Collections;

public class HeartButton : MonoBehaviour {

  public MouseController.Heart heart;

  public MouseController GetMouseController() {
    return GameObject.FindObjectOfType<MouseController>();
  }

	public void MouseOver() {
    this.GetMouseController().HeartMouseOver(this.heart);
  }

	public void MouseOut() {
    this.GetMouseController().HeartMouseOut(this.heart);
  }

	public void MouseDown() {
    this.GetMouseController().HeartMouseDown(this.heart);
  }

	public void MouseUp() {
    this.GetMouseController().HeartMouseUp(this.heart);
  }
}
