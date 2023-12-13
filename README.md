# spotipie-bot

A fork of [Neel's Spotipie-bot](https://github.com/k-neel/spotipie-bot).

## Environment variables and their descriptions

| Variable                  | Description                                | Notes                                                                                           |
| ------------------------- | ------------------------------------------ | ----------------------------------------------------------------------------------------------- |
| `MONGO_ROOT_PASSWORD`     | MongoDB root password                      |                                                                                                 |
| `MONGO_SPOTIPIE_USER`     | MongoDB user for Spotipie                  |                                                                                                 |
| `MONGO_SPOTIPIE_PASSWORD` | MongoDB password for Spotipie              |                                                                                                 |
| `MONGO_SPOTIPIE_DB`       | MongoDB database for Spotipie              |                                                                                                 |
| `API_KEY`                 | Telegram bot API key                       | Get one from [BotFather](https://t.me/BotFather)                                                |
| `SPOTIFY_CLIENT_ID`       | Spotify client ID                          | Get one from [Spotify Developers Dashboard](https://developer.spotify.com/dashboard)            |
| `SPOTIFY_CLIENT_SECRET`   | Spotify client secret                      | Get one from [Spotify Developers Dashboard](https://developer.spotify.com/dashboard)            |
| `TEMP_CHANNEL`            | Telegram channel ID for temporary messages |                                                                                                 |
| `REDIRECT_URI`            | Spotify redirect URI                       | This should contain the link to your authserver, which is defined below                         |
| `BOT_URL`                 | Telegram bot URL                           | Currently accepts links in `t.me/BOTUSERNAME?start` format (to be replaced with `BOT_USERNAME`) |
| `PORT`                    | Express server port                        |                                                                                                 |

TODO:

-   Round album cover, user profile picture
-   Make mongo less verbose
-   Change Telegram bot messages
-   Authserver: change BOT_URL to expect bot's username, not t.me/BOTNAME?start=
-   Documentation
-   Specify image versions in docker-compose.yml
-   Authserver: maybe upgrade to Express 5? Express 4 works just fine though
