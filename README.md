# nba_prediction

Ez egy kezdetleges projekt, célja hogy szimpla statisztikai alapon, papírforma szerűen, kiszámolja hogy két megadott csapat közül,
melyik fog nagyobb valószínűséggel kikerülni győztesként a párharcból. 

A futtatásához szükséges feltételek:
  -numpy (pip install numpy)
  -nba_api (pip install npa_api)
  
A program használatához meg kell adni a két csapat nevét a file végén található két változó paraméterének (team1 és team2),
illetve a dátumot is meg kell adni, értelemszerűen a jelenlegi dátumot érdemes, hogy az eddigi összes adat segítségével tudjon számolni,
de akár lehet egy múltbéli időpont is a szezonon belül, abban az esetben viszont csak az akkori elérhető adatokkal fog számolni.
(jövőbeli dátum esetén ugyanazt az eredményt kapjuk mint a jelen napot megadva)

Végeredményként a konzolon láthatjuk hogy a csapatok hány százalékos eséllyel fognak győzni.
