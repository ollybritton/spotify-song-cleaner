# `spotify-song-cleaner`
`spotify-song-cleaner` is a small program I wrote to clean up my liked songs on Spotify.

Ages ago I downloaded a bunch of albums on Spotify, but instead of pressing 'download' I pressed 'like'. It got downloaded, but it meant that about 100 albums were added to my liked songs which is too many to remove by hand.

![Let's ignore the fact that I probably spent more time programming this than I would have done just manually removing them.](https://imgs.xkcd.com/comics/automation.png)

It wouldn't be a problem except I like shuffling my liked songs but having all the albums in there means that occasionally I'll get a song that I don't know very well and don't listen too that often. Not a huge problem, but an inconvenience.

So I wrote this program to fix that. It:

* Uses `spotipy` to access the Spotify API
* Searches your liked songs and finds chunks where they all share the same album
* Gives you the option to remove them

Confused? It solves a very specific problem so I'm probably the only one who will ever use this but I still want to put it up on GitHub.

## Usage

To install:

```sh
git clone https://github.com/ollybritton/spotify-song-cleaner
cd spotify-song-cleaner
```

Then copy `example.config.toml` to a file called `config.toml`. Edit the values in there, you will likely have to create an app and give it the redirect URI of "http://localhost:8000".

Then you should just be able to:

```sh
pipenv run python main.py # Assumes pipenv is installed
```

The `spotipy` library will create a file called `.cache-your-username` which contains an access token so you might want to delete it once you're done, though the token is only short lived so it's not a huge issue.