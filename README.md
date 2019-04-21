# FooBar Factory

## Sujet

But: avoir 100 robots
Tu commences avec 2 robots dans ton usine.
Chaque robot peut effectué les actions suivantes:

Se déplacer, dure 2 secondes
Miner du Foo, dure 2 secondes
Miner du Bar, dure entre 0.5 et 2 secondes
Assembler un FooBar: dure 2 secondes et utilise un Foo et un Bar. 60% de chance de succès, Le Foo et perdu le Bar peut être réutilisé
Vendre de 1 à 5 FooBar pour 1$: dure 1 seconde
Acheter un robot pour 3$ et 6 foo: instantané

## Approche
Ma technique d'approche a été de créer dans un premier temps 10 robots travailleurs.<br>
Chaque robots (anciens et nouveau) aidant à la creation<br>

Ensuite ces 10 robots vont oeuvrer ensemble à la création des resources nécessaires à l'achat de nouveaux robots.


## Les Applications
Deux applications sont executables:
1. L'algorithme python simple (main.py)
2. Une application flask (app.py)


## Lancer les scripts
### Sous votre environnement
Je conseille d'utiliser en environnement virtuel. Auquel cas il suffira d'exécuter la commande:
```
$ pip install -r requirements.txt
```
Lancer ensuite l'algorithme simple..
```
$ python3 main.py
```
..ou l'application flask (ouvrir http://localhost:5000/ dans votre navigateur)
```
$ python3 app.py
```
### Docker
Un Dockerfile est disponnible pour construire et lancer l'application Flask
```
$ docker build -t cs_factory .
$ docker run -d -p 5000:5000 cs_factory
```
Cependant une image de cette application est disponnible sur mon DockerHub, je conseille donc pour une exécution plus rapide de la télécharger directement:
```
$ docker pull clementtr/cs_factory
$ docker run -p 5000:5000 clementtr/cs_factory
```
