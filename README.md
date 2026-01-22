# How to run: 
## Prerequisites
- Docker
- https://ollama.com/download

## Install uv
https://docs.astral.sh/uv/getting-started/installation/

## Virtual Environemnt
- Setup the virtual environemnt with `uv venv` 
- Activate the virtual environment with `source .venv/bin/activate`
- Install all necessary python packages to run the project with `uv sync`
- Start the docker container in `data/conversations/docker-compose.yml` with `docker-compose up`
- Pull the model with `ollama pull qwen2.5-coder:7b` (or any other model)


## The different components
### llm
- Start the API with `python llm/main.py`

### database
- Start the docker container in `data/conversations/example/docker-compose.yml` with `docker-compose up`
- Start the API with `data/api/example_api.py`

### cli 
- Start the CLI tool with `python cli/main.py`
- Follow the instructions