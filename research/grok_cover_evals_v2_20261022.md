I'll generate a 16:9 banner with the robot in profile and only the four specified text strings. Checking the image-generation guidance first so the signs and CRT stay readable.The signs and CRT have to be letter-perfect, so I'll look for an existing robot reference, then build the scene and lock the text in code if the generator garbles it.The banner is generated. I'll read it back and check that the four strings are exact and nothing else is written in the frame.The signs read correctly, but the robot faces the camera and the CRT splits the status line into four small rows. I'll turn the robot into profile and replace the screen so the two required lines can be drawn exactly.The robot is finally seen from behind, and the gate signs are right. The CRT is still blank and too small for two lines at thumbnail size, so I’ll enlarge that screen and set the text in code.The gate signs are right, but the screen is too narrow for two lines at the size this banner needs. I'll restage the shot so the CRT sits close in the foreground and the robot stays in rear profile.The wide screen is in place and the gate signs read correctly. I'll set the CRT copy in code so the two lines stay exact and large.The last patch ate into the robot. I’m restoring the clean banner and only covering the letter-like neon on the left.The banner is saved at `images/8.jpg` (16:9).

The foreground screen reads exactly:

`eval rc`
`0=PASS  2=FAIL  3=CONFIG`

Those two lines are monospace phosphor green and together take about a quarter of the frame height. The gates read `RC=2 FAIL` (arm down) and `RC=0 PASS` (arm up, lane open). The robot is seen from behind, pointing down the corridor.
exit=0
