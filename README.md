

FunkDL integrates SpotDL music gathering from spotify links and automatically reupload content to funkwhale creating/updating a playlist.

To use it, you need spotdl installed in PATH and an account on a Funkwhale pod (instance) with upload rights.

## Installation

- Clone this repository.
- Install SpotDL (look at their github README)
- Install python dependencies from `requirements.txt` in a virtualenv. For example:
    - `python3 -m venv`
    - `source venv/bin/activate`
    - `pip install -r requirements.txt`
- Create an application authentication token by visiting your account settings on the funkwhale instance.
- Also get the library identifier of the funkwhale library you want to upload to (for example by visiting the library page on instance looking for uuid like `a2114f40-aef6-4d1b-926d-d9fy5c928388` in the web url)
- FIRST DUPLICATE `cli_env.dist` into `cli_env` THEN (to avoid leaking your token through git) complete `cli_env` with preceding token, library id and funkwale base url (`https://your.funkwhale.io/`)
- Create environment parameters by sourcing `cli_env`: `source cli_env`.
- Use then `./funkdl '<spotify_url>'`.

Hopefully I'll find time soon to package this properly (to avoid this long dev installation).

## Usage

```
FunkDL. Funkwhale SpotDL integration to ease music gathering.

Usage:
  funkdl '<spotify_url>'  [--no-delete] [--no-playlist] [--no-upload] [--funkwhale-url=<funkwhale_url>] [--funkwhale-token=<funkwhale_token>] [--library-id=<library_id>] [--playlist-name=<playlist_name>]

Options:
  -h --help                             Show this screen.
  --funkwhale-url=<funkwhale_url>       Specify funkwhale instance url to upload to [default: FUNKWHALE_URL].
  --funkwhale-token=<funkwhale_token>   Authentication token (you need to create an app see funkwhale doc) [default: FUNKWHALE_TOKEN].
  --library-id=<library_id>             The funkwhale library to upload music into. [default: FUNKWHALE_LIBRARY_ID].
  --playlist-name=<playlist_name>       Override playlist name from spotify by your own.
  --no-playlist                         Don't create playlist for the uploaded content. 
  --no-delete                           Avoid final deletion of downloaded audio files.
  --no-upload                           Only add locally listed (m3u) files to playlist avoiding download and upload of files.

```