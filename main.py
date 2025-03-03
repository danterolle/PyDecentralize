"""
PyDecentralize - Desktop Client

This code implements a basic client for connecting to the decentralized Nostr network.

Key features:
- WebSocket connection to Nostr relays (relay.damus.io)
- Receiving and displaying messages (type 1 events)
- Sending simple text messages
- Command-line interface

The client uses threading to keep the interface responsive while managing
the WebSocket connection in the background, allowing users to send messages
without blocking I/O operations.
"""

import json
import time
import websocket
import secrets
import threading

class PyDecentralize:
    def __init__(self, relay_url="wss://relay.damus.io"):
        self.relay_url = relay_url
        self.ws = None
        # Using a fictitious ID to simplify; a real app would use cryptography
        # For demonstration purposes only - proper authentication is essential in production
        self.pubkey = "simply_client_" + secrets.token_hex(4)
        self.subscription_id = "sub_" + secrets.token_hex(4)
        
    def connect(self):
        self.ws = websocket.WebSocketApp(
            self.relay_url,
            on_open=lambda ws: self.subscribe_to_feed(),
            on_message=self.on_message,
            on_error=lambda ws, error: print(f"Error: {error}"),
            on_close=lambda ws, code, msg: print("Closed connection")
        )
        # Using run_forever to maintain persistent connection with the relay
        # This ensures we don't miss any events and can respond in real time
        self.ws.run_forever()
        
    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            if data[0] == "EVENT":
                event = data[2]
                # Truncating public keys for readability in the UI
                # Full keys are too long for comfortable display
                author = event.get("pubkey", "anonymous")[:8]
                content = event.get("content", "")
                created_at = event.get("created_at", 0)
                time_str = time.strftime('%H:%M:%S', time.localtime(created_at))
                
                print(f"\n[{time_str}] {author}: {content}")
            elif data[0] == "EOSE":
                # EOSE (End Of Stored Events) marks the boundary between historical and real-time events
                # This helps users understand when they've seen all past messages
                print("\n--- End Of stored events ---")
        except Exception as e:
            print(f"Error: {e}")
        
    def subscribe_to_feed(self):
        print(f"Connected to {self.relay_url} as {self.pubkey}")
        
        subscription = [
            "REQ", 
            self.subscription_id,
            {"limit": 5, "kinds": [1]}  # Limiting to 5 posts to prevent overwhelming the user
            # Kind 1 specifically targets text notes, filtering out other event types
        ]
        self.ws.send(json.dumps(subscription))
        print("Listening for new messages...")
        
    def publish_note(self, content):
        # In a real implementation, we would cryptographically sign the event
        # This simplified version skips proper authentication for educational purposes
        event = {
            "id": secrets.token_hex(8),  # Simplified ID generation
            "pubkey": self.pubkey,
            "created_at": int(time.time()),
            "kind": 1,  # Type 1 = text post in the Nostr protocol
            "tags": [],
            "content": content,
            "sig": "simplified"  # A real implementation would require ECDSA signature for security
        }
        
        publish_message = ["EVENT", event]
        self.ws.send(json.dumps(publish_message))
        print(f"Message sent: {content}")

if __name__ == "__main__":
    client = PyDecentralize()
    
    print("=== PyDecentralize - Desktop Client ===")
    
    # Starting connection in background to keep the UI responsive
    # This prevents WebSocket operations from blocking user input
    ws_thread = threading.Thread(target=client.connect)
    ws_thread.daemon = True  # Making thread daemon so it terminates with main program
    ws_thread.start()
    
    # Brief pause to establish connection before accepting input
    # Ensures the WebSocket is ready before user interaction begins
    time.sleep(1)
    
    # Main loop for user interaction
    try:
        while True:
            msg = input("\nWrite some text (or just type 'exit'): ")
            if msg.lower() == 'exit':
                break
            client.publish_note(msg)
    except KeyboardInterrupt:
        print("\nClosing the client...")
