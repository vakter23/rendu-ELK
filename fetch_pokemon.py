import requests
import json

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

for i in range(1,1025):
	pokemon_data = get_pokemon_data(i)
	
	with open(f"pokemons/data{i}.json", 'w') as f:
		json.dump(pokemon_data, f)

