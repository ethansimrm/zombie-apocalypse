# zombie-apocalypse

This recreates a zombie apocalypse within the CodeSkulptor browser-based IDE, which was created by the Rice University Department of Computer Science.

In many ways this is like the Game of Life (https://playgameoflife.com/) - the user puts down obstacles, humans, and zombies, and advances time accordingly to see how the humans flee and the zombies chase. Humans can move diagonally, while zombies cannot. So some obstacle arrangements are zombie-proof!

Both humans and zombies employ a breadth-first search using Manhattan distance fields - the former wishes to maximise their distance from the latter, while the latter wishes to minimise their distance to the former.

Due to the highly specific nature of the GUI, it only works in CodeSkulptor - you can access it at https://py2.codeskulptor.org/#user48_p4IFmmjUM0_13.py
