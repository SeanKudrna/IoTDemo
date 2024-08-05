import asyncio
import json
import ssl
import os
import random
from datetime import datetime
from gmqtt import Client as MQTTClient
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Define the MQTT topic
topic = "iot/topic"

class MyMQTTClient(MQTTClient):
    """
    Custom MQTT Client class inheriting from gmqtt.Client.
    Handles connection and disconnection events.
    """
    
    async def on_connect(self, flags, rc, properties):
        """
        Handles the event when the client connects to the broker.
        
        Parameters:
        - flags: connection flags
        - rc: return code of the connection
        - properties: connection properties
        """
        if rc == 0:
            print("Connected successfully.")
            await self.subscribe(topic, qos=1)
        else:
            print(f"Failed to connect, return code {rc}")

    async def on_disconnect(self, exc):
        """
        Handles the event when the client disconnects from the broker.
        
        Parameters:
        - exc: exception if the disconnection was due to an error
        """
        print("Disconnected")

async def main():
    """
    Main coroutine to initialize the MQTT client, set up SSL, and publish messages in a loop.
    """
    client = MyMQTTClient("unique_client_id_1108")
    
    # Create an SSL context for a secure connection
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.load_verify_locations(os.getenv('ROOT_CA_FILE'))
    ssl_context.load_cert_chain(os.getenv('CERT_FILE'), os.getenv('KEY_FILE'))
    
    # Connect to the MQTT broker
    await client.connect(os.getenv('AWS_ENDPOINT'), 8883, ssl=ssl_context)
    
    try:
        while True:
            now = datetime.utcnow().isoformat() + 'Z'  # Current UTC time in ISO format

            # Possible error codes for the payload
            possible_errors = ["E001", "E002", "E003", "E004", "E005"]
            include_errors = random.choice([True, False])  # Randomly decide whether to include errors
            error_list = random.sample(possible_errors, random.randint(1, len(possible_errors))) if include_errors else []

            # Create the payload as a JSON string
            payload = json.dumps({
                "timestamp": now,
                "temperature": random.uniform(20.0, 25.0),
                "voltage": random.uniform(23.0, 25.0),
                "device_id": "1108",
                "location": {"lat": random.uniform(-90, 90), "lon": random.uniform(-180, 180)},
                "PWM": random.randint(100, 200),
                "battery_health": "Good",
                "battery_charge": random.randint(50, 100),
                "speed": random.uniform(0.0, 10.0),
                "load_weight": random.uniform(0.0, 100.0),
                "cart_status": random.choice(["Operating", "Idle", "Maintenance"]),
                "error_codes": error_list
            })

            # Publish the payload to the MQTT topic
            client.publish("iot/topic", payload, qos=1)
            print(f"Published: {payload}")
            await asyncio.sleep(10)  # Wait for 10 seconds before publishing the next message
    except KeyboardInterrupt:
        print("Exiting")
    finally:
        # Disconnect the client
        await client.disconnect()

if __name__ == '__main__':
    # Run the main coroutine
    asyncio.run(main())
