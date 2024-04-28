# !/bin/bash

mkdir -p pokemons

python3 fetch_pokemon.py

for file in pokemons/data*.json; do 
	nc localhost 5000 -w0 < $file
done
