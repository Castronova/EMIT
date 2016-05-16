# Notes on Canvas
If we decide to stay with Wx, these notes might come in handy for anyone who needs to look at this thing we call the "canvas". The canvas is the main portion of the GUI which we can drag model boxes around, create links, etc. Most of this code is in `logicCanvas.py`.

### First...

* The canvas is built with the Wx module `FloatCanvas`. [Here's the documentation.](http://wxpython.org/Phoenix/docs/html/lib.floatcanvas.FloatCanvas.html)
* We've encapsulated the objects such as `ModelBox`, `SmoothLineWithArrow`, `SmoothLine`, as their own custom `FloatCanvas` objects contained in `logicCanvasObjects.py`

## Movement

### on_model_left_clicked
All model boxes are bound to the `on_model_left_clicked` function upon being clicked:

* In here `self.MovingObject` is set to the clicked box and the `self.Moving` flag is set to `True`.
* Boundaries are also calculated so that the box can't be dragged outside of the canvas.

### on_move
Any sort of mouse movement over the canvas is bound to an important function, `on_move`:

* For every pixel the cursor moves, the on_move function is called.
* First, only if `self.Moving` is true, does it do anything since this function is only supposed to handle the dragging of objects.
* If something is moving, it does checks to see the box is within the canvas boundaries.
* The delta is calculated of how far and in what direction the cursor has moved since `on_move` was last called, and then move the object with that value.
* Then we iterate over EVERY link on the canvas, and if the selected object is part of the link, we also reset the link's points and the arrow's XY.

These things are the most important aspects to understand for canvas movement. If you ever have questions, feel free to email me at gallaghermikey@gmail.com or hit me up on Slack!