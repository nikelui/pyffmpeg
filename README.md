# pyffmpeg
A FFmpeg GUI in Python and Qt4
Developed under ubuntu 18.04.

## Dependances
- python 2.7 or higher (python3 does not like QStrings, this should be fixed)
- FFmpeg v.3.4.2 or higher (can be found at https://www.ffmpeg.org/download.html). If you use
pre-compiled binaries, they have to be put inside the same folder as the script.
- PyQt4 (on ubuntu repos: `sudo apt install pyqt4-dev-tools`)

## CHANGELOG
### v0.2
- Added video resize filter
- Able to set video quality with crf (for now fixed at 23)
- Cleaner ffmpeg command concatenation
- (0.2.1) Added tooltips
- (0.2.2) Fixed tooltips stylesheet
- (0.2.3) Better organization of StyleSheet
- (0.2.4) Fixed dependances and compatibility with python3 (still needs work)
- (0.2.5) Inserted text edit to adjust video quality with CRF.  
  Changed launcher in order to always start a terminal. For now it uses the `x-terminal-emulator`
  command, which might not start the preferred terminal emulator.
- (0.2.6) Added status bar (still empty) with size grip for resizing. Added images folder.
