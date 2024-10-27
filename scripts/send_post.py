import requests

# Define the URL to which you want to send the POST request
url = 'http://127.0.0.1:5000'  # Replace with the actual endpoint

# Define the JSON payload
payload = {
  "mathml": "<math><mrow><mi>x</mi><mo>+</mo><mn>2</mn></mrow></math>"
}

# Send the POST request
response = requests.post(url, json=payload)

# Check the response status code
if response.status_code == 200:
    print("Success!")
    print("Response JSON:", response.json())  # Print the response JSON if applicable
else:
    print("Failed to send POST request.")
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
