# Marcador de Parejas · Grupo de Vida

A scoreboard for game nights, shown on a TV or projector. It keeps score for two teams (by default **Hombres** and **Mujeres**) across several games. It has a built-in charades game, trivia buzzers on each team's phone, and an iPhone remote so the host can run everything from their hand.

It's three HTML pages plus a small Python server. No installation or build step is needed; the server only uses Python's standard library.

| File | What it is |
| --- | --- |
| `marcador.html` | The scoreboard shown on the TV |
| `remote.html` | The host's remote control (opened on an iPhone) |
| `buzzer.html` | A trivia buzzer, one phone per team |
| `server.py` | Serves the pages and connects the phones to the scoreboard over Wi‑Fi |
| `Iniciar marcador.command` | Double-click launcher for macOS |
| `Iniciar marcador.bat` | Double-click launcher for Windows |

## Features

### Scoreboard
- Two teams with editable names, plus an editable title for the night.
- Each game gets its own score, and the total for the night is added up across all games.
- **Lista de juegos de la noche**: write the night's games one per line (e.g. Charadas, Pictionary, Trivia de parejas). Each time you start a new game, it takes the next name on the list.
- Add or remove points with the keyboard, quick buttons (−1, +1, +2, +3, +5, +10), or any custom amount.
- **Undo** (up to 100 steps), plus a full reset.
- Celebration effects when points are scored (confetti, fireworks, hearts, stars and more), with sound effects that can be turned off.
- **Finale screen**: "Y el equipo ganador de la noche es…" announces the winner, or a tie.
- Three visual styles: **Noche Luxe**, **Gala Dorada** and **Estadio**.
- Full-screen mode. The mouse cursor and controls hide after a few seconds of no movement.
- Everything is saved in the browser automatically, so closing or refreshing the page doesn't lose the score.

### Control panel (key `C` or the ⚙︎ button)
Only shows on the screen while it's open. From here you can:
- Change the title, team names and the current game's name.
- Add points, start a new game, undo, reset and show the finale.
- Control charades and the trivia buzzer.
- Pick a style, toggle sound and go full screen.
- See the QR codes for the iPhone remote and the two buzzers (only when started through the server, see below).

### Charades (Charadas)
- A built-in deck of about 100 Spanish words, shuffled. Words aren't repeated until the deck runs out.
- Timed turns: 30 s, 45 s, 60 s, 90 s, 2 min, or a custom length.
- A countdown, then words show one at a time. Each word guessed is +1 point for the team on turn.
- You can skip a word, pause or resume, undo the last word guessed, or end the turn early.

### Trivia buzzer (Timbre de trivia)
- Each team opens `buzzer.html` on a phone (scan its QR code). Whoever presses first wins; the server decides who was first, so phone speed doesn't matter.
- The host marks the answer **Correcto** (points go to that team automatically) or **Incorrecto** (that team is locked out and the other team gets to try).
- Points per correct answer: 1, 2, 3 or 5.

### iPhone remote
- Scan the QR code in the control panel to open the remote on your phone.
- It shows the live score and can add or remove points, start a new game, show the finale, and run charades and the trivia buzzer.
- Actions the whole room would see (new game, finale) need two taps to confirm.
- A 4-digit code in the link keeps other people on the Wi‑Fi from controlling the scoreboard. The code is saved in `.codigo`, so phones don't need to rescan after a restart.

## Running it

The scoreboard can run in two ways:

- **With the server (recommended):** everything works, including the iPhone remote and the trivia buzzers. Needs Python 3.
- **Without the server:** double-click `marcador.html` to open it in the browser. Scoring, charades, styles and the finale all work, but the phone remote and buzzers don't.

The computer needs internet access for the fonts and QR codes. The phones must be on the **same Wi‑Fi** as the computer.

### macOS
1. Python 3 usually comes with macOS. If it asks to install "command line developer tools", accept, or install Python from [python.org](https://www.python.org/downloads/).
2. Double-click **`Iniciar marcador.command`**.
   - The first time, macOS may block it. Right-click the file → **Open** → **Open**.
   - If it says you don't have permission, run `chmod +x "Iniciar marcador.command"` in Terminal from this folder.
3. The scoreboard opens in your browser. Leave the Terminal window open while you play.

Or from Terminal: `python3 server.py`

### Windows
1. Install Python 3 from [python.org](https://www.python.org/downloads/). During setup, tick **"Add python.exe to PATH"**.
2. Double-click **`Iniciar marcador.bat`**.
3. When Windows Firewall asks, allow access on **Private networks**. Without this, the phones can't connect.
4. The scoreboard opens in your browser. Leave the black console window open while you play.

Or from a terminal: `py server.py` (or `python server.py`)

### Linux
Run `python3 server.py` from this folder.

### On the TV
1. Connect the computer to the TV (HDMI, AirPlay, etc.) and move the browser window to it.
2. Press `F` for full screen.
3. Press `C` to open the control panel, and scan the QR code for the remote (and the buzzers if you're playing trivia).
4. Press `C` again to hide the panel.

The server uses port 8000. To use another port, set the `PORT` environment variable, e.g. `PORT=8080 python3 server.py`. To stop the browser from opening automatically, set `NO_BROWSER=1`.

## Keyboard shortcuts

Press `?` on the scoreboard to see these on screen.

| Key | Action |
| --- | --- |
| `Q` / `A` | Team 1 +1 / −1 (hold `Shift` for ±5) |
| `P` / `L` | Team 2 +1 / −1 (hold `Shift` for ±5) |
| `N` | Start a new game |
| `Z` | Undo |
| `W` | Show the finale (winner) |
| `C` | Open / close the control panel |
| `T` | Next style |
| `F` | Full screen |
| `S` | Sound on / off |
| `H` | Open charades |
| `B` | Trivia: new question (turns the buzzers on) |
| `Y` / `X` | Trivia: correct / incorrect |
| `?` | Show the shortcuts |
| `Esc` | Close whatever is open |

**During charades:**

| Key | Action |
| --- | --- |
| `Space` | Start / pause |
| `→` or `Enter` | Word guessed (+1) |
| `←` | Skip word |
| `Backspace` | Undo the last word guessed |
| `1` / `2` | Choose which team's turn it is |
| `Esc` or `H` | Close charades |
