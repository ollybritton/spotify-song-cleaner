import spotipy
import toml
import questionary

from spotipy.oauth2 import SpotifyOAuth

def load_spotify_from_config():
    with open("config.toml", "r") as f:
        parsed = toml.loads(f.read())

    scopes = "user-library-read user-library-modify"

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scopes,
            username=parsed["username"],
            client_id=parsed["client_id"],
            client_secret=parsed["client_secret"],
            redirect_uri=parsed["redirect_uri"],
        )
    )

    return sp

def get_all_liked_songs(sp):
    songs = []
    offset = 0
    
    while True:
        results = sp.current_user_saved_tracks(20, offset)['items']

        for _, item in enumerate(results):
            songs.append(item['track'])

        offset += 20
        
        if len(results) != 20:
            break

    return songs

def backup_liked_songs(sp, filename):
    with open(filename, "w") as f:
        f.write("\n".join([ x['uri'] for x in get_all_liked_songs(sp) ]))

def load_backup(sp, filename):
    with open(filename, "r") as f:
        lines = [x for x in f.readlines().reverse() if x != ""] # reversed so they're added back in the original order
        sp.current_user_saved_tracks_add(tracks=lines)

def group_liked_songs(songs):
    groups = []

    for song in songs:
        if len(groups) == 0 or groups[len(groups)-1][0]['album']['uri'] != song['album']['uri']:
            groups.append([song])
        else:
            groups[len(groups)-1].append(song)

    return groups

def main():
    sp = load_spotify_from_config()
    print("Successfully authenticated to the Spotify API.")
    print("")

    answer = questionary.select(
        "What would you like to do?",
        choices=[
            "Make a backup (recommended)",
            "Load a backup",
            "Clean spotify library",
        ]
    ).ask()

    print("")

    if answer == "Make a backup (recommended)":
        filename = questionary.text("What should the filename be?", default="spotify.backup").ask()
        backup_liked_songs(sp, filename)

    if answer == "Load a backup":
        filename =  questionary.text("What is the name of the backup?", default="spotify.backup").ask()
        load_backup(sp, filename)

    if answer == "Clean spotify library":
        songs = get_all_liked_songs(sp)
        groups = group_liked_songs(songs)
        groups = [ g for g in groups if len(g) > 2 ]

        for i, g in enumerate(groups):
            print(f"({i+1}/{len(groups)}) Found multiple songs next to each other sharing '{g[0]['album']['name']}'.")
            remove = questionary.confirm("Remove them?").ask()

            if remove:
                sp.current_user_saved_tracks_delete([t['uri'] for t in g])

if __name__ == "__main__":
    main()