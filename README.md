╔══════════════════════════════════════════════════════════╗
║           📡 LocalDrop — Wireless File Transfer           ║
╚══════════════════════════════════════════════════════════╝

Transfer files between your iPhone and PC over Wi-Fi.
No internet. No cables. No apps to install on iPhone.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • Python 3.8 or newer  (comes built-in on most PCs/Macs)
  • iPhone and PC on the SAME Wi-Fi network
  • Optional: pip install qrcode   (for a QR code in terminal)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  HOW TO START
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. Double-click  start_localdrop.bat  (Windows)
     — or —
     Open Terminal and run:  python3 server.py

  2. A URL like  http://192.168.x.x:8765  will appear.

  3. Scan the QR code with your iPhone camera
     — or type the URL into Safari manually.

  4. Transfer files!


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TRANSFER FILES: iPhone → PC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  On your iPhone:
  → Tap "Send to PC" tab
  → Tap the upload area and pick photos/files
  → Files are saved to:  ~/LocalDrop_Received/


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TRANSFER FILES: PC → iPhone
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  On your PC:
  → Copy files into the folder:  ~/LocalDrop_Share/

  On your iPhone:
  → Tap "Get from PC" tab
  → Tap "Save" next to any file to download it


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  OPTIONAL: QR Code in terminal
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  pip install qrcode
  Then restart the server — a scannable QR code appears!


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  STOP THE SERVER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Press  Ctrl + C  in the terminal window.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  "iPhone can't connect"
  → Make sure PC and iPhone are on the SAME Wi-Fi network
  → Windows: allow Python through Windows Firewall when prompted

  "Port already in use"
  → Open server.py and change PORT = 8765 to another number

  "Photos not showing in iPhone library after download"
  → In Safari, tap the downloaded file → tap Share → Save Image
