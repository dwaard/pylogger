Je programmeert in python. Inspringen met 2 spaties en engelstalige variabelen en comments. 
Je hebt een reeks csv bestanden in een folder met de naam `.out`. Er staan ook andere bestanden in deze folder.
Sommige CSV bestanden hebben het formaat:
2025-04-10 20:54:12.647230;25.00;28.20;0.50
2025-04-10 20:54:13.336364;25.00;28.20;0.50
2025-04-10 20:54:15.334621;25.00;28.20;0.50
2025-04-10 20:54:15.339755;25.00;28.20;0.50
2025-04-10 20:54:16.336366;25.00;28.20;0.50
2025-04-10 20:54:17.340435;25.00;28.20;0.50
Andere CSV bestanden hebben het formaat:
[datetime.datetime(2025, 4, 20, 13, 41, 16, 242739), 25.0, 22.0, 5.0]
[datetime.datetime(2025, 4, 20, 13, 41, 21, 243380), 25.0, 22.0, 5.0]
[datetime.datetime(2025, 4, 20, 13, 41, 26, 251700), 25.0, 22.0, 5.0]
[datetime.datetime(2025, 4, 20, 13, 41, 31, 252934), 25.0, 22.0, 5.0]
[datetime.datetime(2025, 4, 20, 13, 41, 36, 258283), 25.0, 22.0, 5.0]
Dit laatste is een probleem. Je maakt een Python script die met alle CSV bestanden die in dat laatste formaat staan het volgende doet:
1. Hernoemt dit bestand naar bestandsnaam.old
1. De inhoud van het originele bestand omzet naar het eerste formaat
Geef de code van dit script

Je wilt meer inzicht. Pas het script aan zodat:
- Het oude bestand niet meer wordt hernoemd en overschreven. In plaats daarvan moet het nieuwe bestand worden weggeschreven in een folder .temp doe mogelijk nog niet bestaat en dus mogelijk moet worden aangemaakt
- Bij het openen van elk bestand een betekenisvolle tekst met daarin de bestandsnaam wordt geprint

Je krijgt heel vaak een melding als Line skipped (no match): [datetime.datetime(2025, 4, 19, 22, 33, 36, 156294), 21.0, 21.0, 32.62, 1.63].
De oorzaak is dat er in de array ofwel 3 of 4 getallen achter de datetime staan. 