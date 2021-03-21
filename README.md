## Comdirect Postbox Downloader in Python
* Getestet unter MX-Linux 19 (Debian10-Derivat), python 3.7.3

### Notwendige Pakete
* python3-selenium
* chromedriver
* chromium

### Bedienung
* Im Script oben Download-Pfad und Zugangsnummer eintragen
* Im Terminal starten mit:  

      python3 -i cddl.py  

* Im Python-Terminal (nicht im Browser) die PIN eingeben  
(Die PIN wird während der Eingabe nicht angezeigt, um ein Auto-cachen auf dem Rechner zu verhindern)
* Im Browser dann Photo-TAN eingeben

Heruntergeladen werden alle PDFs im Posteingang mit Ausnahme der Links, die "Termingebundenes" enthalten, weil hier die Comdirect trotz .pdf-Endung manchmal einen HTML-Link versteckt und das Script dann durcheinanderkäme.

Nach Beendigung wird die Python-Shell nicht geschlossen. Man kann beliebig in der Postbox suchen und dann die letzte Script-Zeile
 
    cddlGetPdf(drv)
 
nochmals eingeben, um weitere PDFs, z. B. im Archiv, herunterzuladen.

### Mögliche Probleme
Es gab bei meiner Distribution zeitweise das Problem, dass der Chromdriver nicht zum Chromium-Browser passte. In dem Fall

* Paket python3-pip installieren (apt install python3-pip o.ä.)
* Python Paket webdriver-manager installieren (pip3 install webdriver-manager)
* Die auskommentierten Zeile "from webdriver_manager ..." einkommentieren
* Die Zeile "driver = ..." durch die darunterstehende, auskommentierte Zeile ersetzen.
