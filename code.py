from solana.publickey import PublicKey
from solana.transaction import Transaction
from solana.system_program import SYS_PROGRAM_ID
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solana.rpc.async_api import AsyncClient
from solana.keypair import Keypair
from borsh_construct import CStruct, U8, U64, F64, Vec
import tensorflow as tf
import numpy as np

# Solana client setup
client = Client("https://api.devnet.solana.com")

# Define the structure matching the smart contract
RegressionData = CStruct(
    "input_data" / Vec(F64),  # List of floats
    "prediction" / F64,       # Single float prediction
)

# Load keypair and create account
payer = Keypair.from_secret_key(...)
account = Keypair()

# Define your regression model in TensorFlow
model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[len(input_features)])
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(training_inputs, training_outputs, epochs=10)

# Predict using the model
input_data = np.array([...])  # Replace with actual input data
prediction = model.predict(input_data)[0][0]

# Prepare data for blockchain
regression_data = RegressionData.build({
    "input_data": input_data.tolist(),
    "prediction": prediction,
})

# Create the transaction
transaction = Transaction()
transaction.add(
    client.program_instruction(
        program_id=PublicKey("Your_Program_Id_Here"),
        data=regression_data,
        keys=[
            {"pubkey": account.public_key, "is_signer": True, "is_writable": True},
            {"pubkey": SYS_PROGRAM_ID, "is_signer": False, "is_writable": False},
        ],
    )
)

# Send the transaction
response = client.send_transaction(transaction, payer, account, opts=TxOpts(skip_preflight=True))
print(f"Transaction ID: {response['result']}")
