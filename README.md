# ELK Rendu projet 

This repository is inspired by the work of [labynocle/elk-demo](https://github.com/labynocle/elk-demo).

Data have been generated thanks to [PokeAPI](https://pokeapi.co)

## Compose the stack

The suggested stack is composed by:
* an ElasticSearch instance which expose 2 ports: 9200 (HTTP for the Rest API) and 9300 (for the transport module)
* a Logstash instance which expose the 5000 port (TCP input to let you easily inject data)
* a Kibana instance which expose the 5601 port (HTTP for the dashboard web interface)
* a Cerebro instance which expose the 9000 port (HTTP for the admin web interface)


## Requirements

Vous devez être sur une machine Linux et avoir :
* [docker](https://docs.docker.com/engine/installation/linux/)
* [Python](https://python.org) (Veuillez importer la librairie **requests** et **json**)

## How to use it?

Pour lancer la stack il faut éxecuter les commandes suivantes :
```bash
cd elk-demo
sudo docker compose up
```

Ensuite il faux éxecuter le script BASH :
```bash
chmod +x scriptAutomatisation.sh
./scriptAutomatisation.sh
```

Puis il faut :
* http://127.0.0.1:9000 to manage the created index (just choose to connect to `http://elasticsearch:9200`)
* http://127.0.0.1:5601 to start to play with Kibana

## Introduction
Notre groupe est composé de Théo RENIER et Volkan AKTER.
L'objectif de notre projet est d'automatiser la récupération de Pokemon depuis l'API [PokeAPI](https://pokeapi.co) puis de l'intégrer dans Kibana pour créer des visualisations sur les caractéristiques des pokemons.

## Script qui récupère et traite les données 
On dispose de deux scripts, un script bash et un script python, 
### Script Bash
Le script Bash est notre script principal et il fonctionne de la façon suivante : 
1. Il va créer un répertoire ***pokemons*** s'il n'existe pas :
```bash
mkdir -p pokemons
```
2. Il va lancer le script python **fetch_pokemon.py** qui va générer les fichiers json des pokémons dans le répertoire ***pokemons***
```python
python3 fetch_pokemon.py
```
3. Pour chaque fichier pokemon généré dans le répertoire ***pokemons*** on envoie le fichier dans cerbero avec netcat
```bash
for file in pokemons/data*.json; do 
	nc localhost 5000 -w0 < $file
done
```
### Script Python
Le script python s'occupe de générer un fichier json avec les informations d'un pokemon.
1. On importe les librairies json et requests qui vont nous servir pour appeler l'API et générer les fichiers JSON.
```python
import requests
import json
```
2. On a notre fonction ***get_pokemon_data*** qui récupère le numéro d'identifiant du pokemon puis il appelle l'API pour récupérer les informations suivantes : nom, taille, poids, types et génération.\
L'information de la génération se trouve dans une URL différrente que celle des autres informations, c'est pour cela qu'on effectue un deuxième appel vers ***https://pokeapi.co/api/v2/pokemon-species***.
```python
def get_pokemon_data(pokemon_id):

	url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
	response = requests.get(url)
	response.raise_for_status()
	
	data = response.json()
	
	urlGetGeneration = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"
	responseGeneration = requests.get(urlGetGeneration)
	responseGeneration.raise_for_status()
	
	dataGeneration = responseGeneration.json()
	
	dataPokemon={"id": pokemon_id, "name": data["name"], "height": data["height"], "weight" : data["weight"], "types" : data["types"], "generation": dataGeneration["generation"]["name"]}
	print("Le pokemon "+str(pokemon_id)+" a été ajouté")
	return dataPokemon
```
3. Avec la fonction on fait une boucle allant de 1 à 1025 pokemons (nombres actuels de pokemons existants) puis on génère un fichier JSON avec les données de chaque pokemon, et on place le fichier dans le répertoire pokemons.
```python
for i in range(1,1025):
	pokemon_data = get_pokemon_data(i)
	
	with open(f"pokemons/data{i}.json", 'w') as f:
		json.dump(pokemon_data, f)
```

## Logstash
On a configuré le logstash pour seulement supprimé le champs ***message***.
```bash
input {
	tcp {
		port => 5000
	}
}

filter {
	json {
		source => "message"
	}
	date {
		match => [ "[date]", "ISO8601" ]
		target => "[date]"
		timezone => "UTC"
	}
	mutate{
		remove_field => [ "message" ]
	}
}
output {
	elasticsearch {
		hosts => "elasticsearch:9200"
	}
}
```
## Schema explicitant toute la chaîne data
![Q3](https://github.com/vakter23/rendu-ELK/assets/60293356/0fd7e6df-dc38-4184-bfa9-c297594e4938)

## Screenshots des visualisations
### Le nombre de pokemon par générations
<img width="1887" alt="Capture0" src="https://github.com/vakter23/rendu-ELK/assets/60293356/fd26d4e5-bb9d-4b58-96cc-f4a545cb51b9">

### Le nombre de pokemon par types
<img width="1849" alt="Capture1" src="https://github.com/vakter23/rendu-ELK/assets/60293356/3a339817-0405-41d1-8fb5-5521e4c561d0">

### Le nombre de type de pokemon selon la génération
<img width="1883" alt="Capture2" src="https://github.com/vakter23/rendu-ELK/assets/60293356/b5761072-2130-404a-90c2-0948e30c8510">

### Le poids moyen de tous les pokemons (en hectogrammes)
<img width="1238" alt="Capture3" src="https://github.com/vakter23/rendu-ELK/assets/60293356/08eb7a99-8292-44aa-8e06-112ed107046c">

### La taille moyenne de tous les pokemons (en décimètres)
<img width="1212" alt="Capture4" src="https://github.com/vakter23/rendu-ELK/assets/60293356/3cec3eb5-3cb3-4845-a7d2-8a311ce5de20">

### Les types les plus présents parmis les pokémons qui ont deux types
<img width="1886" alt="Capture5" src="https://github.com/vakter23/rendu-ELK/assets/60293356/6187bccb-00f6-4e3b-9dc7-9605eacdd218">

### Notre Dashboard
<img width="1887" alt="Capture" src="https://github.com/vakter23/rendu-ELK/assets/60293356/fa724ac3-76ec-483b-a8c5-feea769dabc3">
