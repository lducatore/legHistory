This project aims at creating an animated map representing the expansion of the leg server.

**How to use**

- Use utils/map_editing.py to clean an already filled map.


- Launch the GUI with utils/window_widget.py.

 -- In the main menu :
   - *l* will load the last regions object, which stores the positions, names and relationships between 
regions of the map.

 - *s* will save the current regions object.
 
 - *i* will launch insertion mode, which allow the user to add more regions to the database.
 
 - *ESC* will quit.

In insertion mode, use right-click to flood fill, ESC to quit.

Dependencies:
- openCV