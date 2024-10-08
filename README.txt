# Beschreibung

"Grunzi" ist ein Action-Puzzle-Spiel aus einer Top-Down-Perspektive, in dem sie ein Schwein durch 5 Level steuern.

# Systemvoraussetzungen

Das Spiel benötigt ein 64-Bit Windows oder Linux Betriebssystem und eine Grafikkarte,
die mindestens OpenGL 3.3 unterstützt.
Es sollte auf jeder Hardware, die in den letzten 10 Jahren auf den Markt gebracht wurde, funktionieren.

# Was ist neu?

In diesem Build ist erstmals die fünfte und letzte Map enthalten, welche den Endboss enthält.
Zum Ende von Map 1 wurde eine Autofahr-Animation hinzugefügt.
Weitere Änderungen siehe CHANGES.txt.

# Spiel starten

Das Spiel kann mit einem Doppelklick auf "Grunzi.exe" gestartet werden.
Beim Start öffnet sich der Launcher, wo man die Einstellungen vornehmen kann.
Für fortgeschrittene Nutzer gibt es optional die Möglichkeit, die folgenden Start-Parameter zu übergeben:

```
  --window              Run in windowed mode
  --fullscreen          Run in fullscreen mode
  --width WIDTH         Window width in pixels
  --height HEIGHT       Window height in pixels
  --silent              Mute the sound
  --audio-backend {auto,xaudio2,directsound,openal,pulse,silent}
                        The audio backend

  --video-quality {0,1,2,3,4,5,6}
                        The video quality

  --antialiasing {0,2,4,8,16}
                        The antialiasing level
  --no-vsync            Disable V-Sync
  --debug               Enable OpenGL debugging
  -v, --verbose         Make the operation more talkative
  --skip-launcher       Skip launcher
```

Wenn der Start des Spiels mit der Fehlermeldung, dass die Datei "VCRUNTIME140.dll" fehlt, fehlschlägt, muss das
"Visual C++ Redistributable" von Microsoft installiert werden.

Es ist unter folgendem Link herunterzuladen:
https://www.microsoft.com/de-de/download/details.aspx?id=48145

# Steuerung

Das Spiel unterstützt Steuerung per Tastatur und per Controller.

## Tastatur

Die Steuerung über Tastatur kann im Hauptmenü unter "Einstellungen" - "Steuerung" eingesehen werden.

## Controller

Angeschlossene Controller werden beim Spielstart automatisch erkannt.
Der Controller muss bereits vor dem Start des Spiels mit dem Computer verbunden sein.
Die Steuerung über Controller kann im Hauptmenü unter "Einstellungen" - "Steuerung" eingesehen werden.

Derzeit werden folgende Controller unterstützt:

* Xbox 360 Controller

Weitere Modelle können funktionieren, wurden von mir aber nicht getestet.
