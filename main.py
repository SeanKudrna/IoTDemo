import asyncio
import json
import ssl
import os
from gmqtt import Client as MQTTClient
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# This topic matches the one listed in the resource section of the Publish, Subscribe, and Receive permissions in the AWS Policy attached to our Thing.
topic = "iot/topic"

# Define a custom MQTT client with specific callback methods
class MyMQTTClient(MQTTClient):
    async def on_connect(self, flags, rc, properties):
        """
        Callback for when the client receives a CONNACK response from the server.
        Subscribes to the specified topic if the connection is successful.
        
        Parameters:
        - flags: dict, connection flags.
        - rc: int, connection result code.
        - properties: dict, additional properties.
        """
        if rc == 0:
            print("Connected successfully.")
            await self.subscribe(topic, qos=1)
        else:
            print(f"Failed to connect, return code {rc}")

    async def on_disconnect(self, exc):
        """
        Callback for when the client disconnects from the server.
        
        Parameters:
        - exc: Exception, the exception causing the disconnection, if any.
        """
        print("Disconnected")

async def main():
    """
    Main function to establish an MQTT connection, publish messages periodically,
    and handle graceful shutdown on interrupt.
    """
    # Initialize the MQTT client with a unique client ID. This client ID matches the one listed in the Resource section of the Connect permission in the AWS Policy attached to our Thing.
    client = MyMQTTClient("unique_client_id_1108")
    
    # Set up SSL context for secure communication
    ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ssl_context.load_verify_locations(os.getenv('ROOT_CA_FILE'))
    ssl_context.load_cert_chain(os.getenv('CERT_FILE'), os.getenv('KEY_FILE'))

    # Connect to the MQTT broker
    await client.connect(os.getenv('AWS_ENDPOINT'), 8883, ssl=ssl_context)
    
    try:
        while True:
            # Prepare and publish a JSON payload with sensor data
            payload = json.dumps({"temperature": 22.5, "voltage": 24.8, "device_id": 1108})
            client.publish("iot/topic", payload, qos=1)
            print(f"Published: {payload}")
            await asyncio.sleep(10)
    except KeyboardInterrupt:
        # Handle graceful shutdown on user interrupt
        print("Exiting")
    finally:
        # Disconnect the MQTT client
        await client.disconnect()

if __name__ == '__main__':
    # Run the main function asynchronously
    asyncio.run(main())
