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
* [Python](https://python.org)

## How to use it?

Pour lancer la stack il faut éxecuter les commandes suivantes :
```bash
cd elk-demo
sudo docker compose up
```

Puis il faux éxecuter le script:
```bash
chmod +x scriptELK.sh
./scriptELK.sh
```

Puis il faut :
* http://127.0.0.1:9000 to manage the created index (just choose to connect to `http://elasticsearch:9200`)
* http://127.0.0.1:5601 to start to play with Kibana

