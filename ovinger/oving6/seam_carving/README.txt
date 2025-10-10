Koden for sømfjerning anvender Python-biblioteket PIL (Python Image Library),
se https://github.com/python-pillow/Pillow. PIL kan installeres direkte fra
PyPI (Python Package Index), se https://pypi.org/. Dette gjøres for eksempel
ved å kjøre kommandoen `pip install Pillow` eventuelt `pip3 install Pillow`
hvis du har både Python 2 og 3 installert. Hvis du ikke vet hvordan du bruker
pip, så anbefales det at du tar en kikk i den offisielle dokumentasjonen
(https://packaging.python.org/tutorials/installing-packages/). Det finnes også
mange gode ressurser på nettet som forklarer hvordan du installere/bruker pip
på diverse operativsystemer.

Merk: Jo flere rader du skal fjerne, desto lengre tid tar det. Koden er ikke
veldig optimalisert, så hver rad tar et par sekunder å fjerne (grunnet
antallet operasjoner som utføres på bildet). Det er mulig å optimalisere
koden betraktelig.


Bildet som er inkludert i zip-mappen er en endret versjon av bildet som brukes
som eksempel på Wikipedia, se følgende lenke:
https://en.wikipedia.org/wiki/Seam_carving#/media/File:Broadway_tower_edit.jpg
lisensiert under CC BY 2.5 (https://creativecommons.org/licenses/by/2.5/).
