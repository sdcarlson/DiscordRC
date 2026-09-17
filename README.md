# DiscordRC

DiscordRC is a Discord **server configuration** project: a React webapp for designing a server (roles, channels, permissions), a FastAPI API that stores users and configs in MongoDB, and a Python Discord bot that can create a guild from that JSON and return an invite.

The FastAPI app is titled `DiscordRC`. The webapp package describes itself as a "Discord Webapp to Configure Servers." The bot in `DiscordBot/` applies a guild config and returns an invite; the API drives it via `POST /bot/create` (`DiscordBot.DiscordInterface`).

**Status:** Public snapshot of a 2024 academic/side project (this tree's last commits are from March 2024). Not a production service.

## Stack

- **Bot** (`DiscordBot/`): Python, discord.py
- **API** (`api/`): FastAPI, Uvicorn, Motor/PyMongo, MongoDB (Docker in the API setup script)
- **Webapp** (`webapp/`): React 18, Webpack, Express, MUI

API CI uses Python 3.11. The webpack workflow uses Node 21.x.

## Run locally

### API

From [`api/README.md`](api/README.md):

```bash
cd api
python3 -m venv venv
. venv/bin/activate   # bash
pip3 install -r requirements.txt
./mongo_setup.sh      # Docker MongoDB
sh -c 'cd .. && uvicorn api.main:app --reload'
```

Then open http://localhost:8000/docs.

Tests: start the database, make sure the API is not running, then `tests/run_tests.sh` from `api/`.

### Webapp

```bash
cd webapp
npm install
npm start
```

Express listens on port 8001. The UI calls the API at `http://localhost:8000`. To emit the Webpack bundle into `webapp/public`: `npm run build`.

### Bot

The bot is not a separately documented service. The API starts it through `DiscordBot.DiscordInterface`, which reads **`DISCORD_TOKEN` from the process environment**. There is no in-repo sample secret file; do not commit a token.

`DiscordBot/guild_creator_main.py` is a manual loop for creating guilds from JSON. `example_config.json` at the repo root shows the config shape.

## CI

GitHub Actions live in [`.github/workflows/`](.github/workflows/):

- [`webpack.yml`](.github/workflows/webpack.yml) — on push, `npm install` and `npm run build` in `webapp/` (commits the bundle if it changed)
- [`api_tests.yml`](.github/workflows/api_tests.yml) — on pull requests to `main`, API tests against MongoDB
- [`epics.yml`](.github/workflows/epics.yml) — keeps epic issue task lists in sync

## License

[Apache License 2.0](LICENSE)
