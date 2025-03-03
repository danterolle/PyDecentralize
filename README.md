# PyDecentralize

A lightweight, educational client for the Nostr decentralized social network protocol, developed as a project for the **Internet of Things Based Smart Systems** course.

## Features

- Connect to Nostr relays via WebSockets
- Subscribe to and display text notes (kind 1 events)
- Publish simple text notes to the network
- Command-line interface for basic interaction

## Installation

```bash
git clone https://github.com/danterolle/pydecentralize.git
cd pydecentralize
```

### Dependencies:

```bash
python -m venv env
source env/bin/activate
pip install websocket-client
```

## Usage

```bash
python main.py
```

After starting the client:
1. The application will connect to a default relay (wss://relay.damus.io)
2. Recent messages will be displayed
3. You can type any text messages to publish to the network
4. Type 'exit' to close the application

## Troubleshooting 

You may get the error that the `websocket` module has not been imported even though it is installed. Use `sudo` to run the script.

## Resources

- [Nostr Protocol](https://github.com/nostr-protocol/nostr)
- [NIP-01: Basic Protocol](https://github.com/nostr-protocol/nips/blob/master/01.md)
