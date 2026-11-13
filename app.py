
import os
from flask import Flask, jsonify
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

# Read Key Vault URL from environment configuration
KEY_VAULT_URL = os.environ["KEY_VAULT_URL"]

# Authenticate using the Web App's managed identity
credential = ManagedIdentityCredential()

# Create Key Vault client
client = SecretClient(
    vault_url=KEY_VAULT_URL,
    credential=credential
)

@app.route("/")
def home():
    return "Azure Web App is running successfully!"

@app.route("/get-secret")
def get_secret():
    try:
        # Retrieve secret from Azure Key Vault
        secret = client.get_secret("DBPassword")

        # Use the retrieved value inside the application
        db_password = secret.value

        if db_password:
            return jsonify({
                "status": "success",
                "message": "Secret retrieved successfully from Azure Key Vault"
            })

        return jsonify({
            "status": "failed",
            "message": "Secret value is empty"
        }), 500

    except Exception:
        app.logger.exception("Key Vault secret retrieval failed")
        return jsonify({
            "status": "failed",
            "message": "Unable to retrieve secret from Key Vault"
        }), 500

if __name__ == "__main__":
    app.run()
