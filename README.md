# IoTDemo

Creating a software-only demo that showcases connectivity with AWS for an IoT project. This proof of concept demonstrates how to connect to AWS IoT, publish sensor data, and manage the required security credentials before incorporating hardware like a GPS/GSM chip.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Project Setup](#project-setup)
4. [Setting Up AWS IoT](#setting-up-aws-iot)
5. [Managing Sensitive Files](#managing-sensitive-files)
6. [Running the Project](#running-the-project)
7. [Security Considerations](#security-considerations)

## Overview

This demo connects a simulated IoT device to AWS IoT Core, publishes sensor data, and subscribes to an MQTT topic. The project uses Python with the `gmqtt` library and handles sensitive security credentials using environment variables.

## Prerequisites

- Python 3.6 or later
- AWS account
- Basic understanding of IoT concepts and AWS services

## Project Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/IoTDemo.git
   cd IoTDemo
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**

   Create a `.env` file in the root directory to store the paths to your sensitive files. Example:

   ```bash
    CERT_FILE=aws/device-certificate/your-certificate.pem.crt
    KEY_FILE=aws/private-key/your-private.pem.key
    ROOT_CA_FILE=aws/root-ca/AmazonRootCA1.pem
    AWS_ENDPOINT=your-endpoint.iot.region.amazonaws.com
   ```

   (Information on how to get these files is detailed below in the [Setting Up AWS IoT](#setting-up-aws-iot) section.)

4. **Update `.gitignore`**

   Ensure the `.env` file and sensitive directories are listed in `.gitignore` to prevent accidental commits.

   ```bash
   .env
   aws/root-ca/*
   aws/device-certificate/*
   aws/private-key/*
   ```

## Setting Up AWS IoT

1. **Create an AWS IoT Thing**

   - Go to the AWS IoT Core console.
   - Create a new Thing and download the security credentials (certificate and private key).

2. **Create and Attach a Policy**

   - Create an IoT policy with the necessary permissions for connecting, publishing, subscribing, and receiving messages.
   - Attach the policy to your Thing's certificate.

   - Example policy:

     ```bash
     {
         "Version": "2012-10-17",
         "Statement": [
             {
             "Effect": "Allow",
             "Action": "iot:Connect",
             "Resource": "arn:aws:iot:<yourRegion>:<yourAccountId>:client/<yourClientID>"
             },
             {
             "Effect": "Allow",
             "Action": "iot:Publish",
             "Resource": "arn:aws:iot:<yourRegion>:<yourAccountId>:topic/<yourTopic>"
             },
             {
             "Effect": "Allow",
             "Action": "iot:Subscribe",
             "Resource": "arn:aws:iot:<yourRegion>:<yourAccountId>:topic/<yourTopic>"
             },
             {
             "Effect": "Allow",
             "Action": "iot:Receive",
             "Resource": "arn:aws:<yourRegion>:<yourAccountId>:topic/<yourTopic>"
             }
         ]
     }
     ```

   - `<region>` is the AWS region code you are using associated with your AWS account. i.e.)

     ```bash
     N. Virginia -> us-east-1
     ```

   - `<yourAccountID>` is the 12 digit number (without hyphens) associated with your AWS account. i.e.)

     ```bash
     Account ID: 1234-5678-9999 -> 123456789999
     ```

   - `<yourClientID>` will be some unique id that you connect to your MQTT client with in your code. i.e.)

     ```bash
     client = MyMQTTClient("<yourClientID>")
     ```

   - `<yourTopic>` is the name of the MQTT topic you will be publishing to in your code. i.e.)

     ```bash
     client.publish("<yourTopic>", payload, qos=1)
     ```

3. **Download the Root CA**

   - Obtain the Amazon Root CA file from the [AWS IoT documentation](https://docs.aws.amazon.com/iot/latest/developerguide/managing-device-certs.html#server-authentication) and save it to `aws/root-ca/`. Add the file path to your `.env` file like so:

     ```bash
     ROOT_CA_FILE=aws/root-ca/AmazonRootCA1.pem
     ```

4. **Prepare Your Certificates and Keys**

   - Place the downloaded certificate and private key in the `aws/device-certificate/` and `aws/private-key/` directories, respectively. Add the file paths to your `.env` file like so:

     ```bash
     CERT_FILE=aws/device-certificate/your-certificate.pem.crt
     KEY_FILE=aws/private-key/your-private.pem.key
     ```

5. **Get your Device data endpoint**

   - In your AWS IoT Core dashboard, find `settings` on the bottom of the left sidebar. Clicking on this will display your `Device data endpoint`. Copy this, and add it to your `.env` file like so:

     ```bash
     AWS_ENDPOINT=your-endpoint.iot.region.amazonaws.com
     ```

## Managing Sensitive Files

For security, do not commit sensitive files to your repository. Use environment variables and `.gitignore` to manage these files securely. The `.env` file should contain paths to these files:

```bash
.env
CERT_FILE=aws/device-certificate/your-certificate.pem.crt
KEY_FILE=aws/private-key/your-private.pem.key
ROOT_CA_FILE=aws/root-ca/AmazonRootCA1.pem
```

## Running the Project

1. **Run the Application**

   ```bash
   python main.py
   ```

   This script will simulate sensor data, publish it to the specified MQTT topic, and print received messages.

## Security Considerations

- **Never commit sensitive files** like certificates or private keys to your Git repository.
- **Use environment variables** to manage paths and credentials securely.
- **Regularly rotate** your AWS IoT credentials to mitigate security risks.

By following these instructions, you can set up and run the IoT demo project, demonstrating basic connectivity and data handling with AWS IoT Core. For further development, consider integrating hardware components like GPS/GSM modules.
