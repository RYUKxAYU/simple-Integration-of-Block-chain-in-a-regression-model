!pip install sklearn numpy

import hashlib
import json
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

def create_dataset():
    X = np.array([[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]])
    y = np.array([2, 4, 5, 4, 5, 6, 7, 8, 8, 9])
    return X, y

def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model

def make_prediction(model, X):
    return model.predict(X)

X, y = create_dataset()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = train_model(X_train, y_train)

blockchain = Blockchain()

predictions = []
for i in range(len(X_test)):
    prediction = make_prediction(model, X_test[i].reshape(1, -1))[0]
    data = {
        "input": float(X_test[i][0]),
        "actual": float(y_test[i]),
        "prediction": float(prediction)
    }
    new_block = Block(len(blockchain.chain), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), data, blockchain.get_latest_block().hash)
    blockchain.add_block(new_block)
    predictions.append(prediction)

for block in blockchain.chain:
    print(f"Block #{block.index}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Data: {block.data}")
    print(f"Hash: {block.hash}")
    print(f"Previous Hash: {block.previous_hash}")
    print("\n")

# Visualize the results
plt.figure(figsize=(10, 6))
plt.scatter(X, y, color='blue', label='Data points')
plt.plot(X, model.predict(X), color='red', label='Regression line')
plt.scatter(X_test, predictions, color='green', label='Predictions')
plt.xlabel('X')
plt.ylabel('y')
plt.title('Linear Regression with Blockchain-stored Predictions')
plt.legend()
plt.show()
