# dropbox-upload

## Dependencies

```
pip install dropbox python-dotenv
```

## Installation

```
git clone https://github.com/sunknudsen/dropbox-upload.git
cd dropbox-upload
cp .env.sample .env
```

## Configuration

Create a Dropbox app here: https://www.dropbox.com/developers/apps

Add the app key and secret to `.env`.

Run `python dropbox-auth.py`

Add the access token to `.env`.

## Usage

Run `python dropbox-upload.py path-to-file`
