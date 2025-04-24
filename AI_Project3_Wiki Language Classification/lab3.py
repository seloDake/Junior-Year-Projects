""" Lab 3 """
import sys
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
import re

# Function to extract features based on substrings
def extract_features(segment):
    """
    Extracts features based on common words in English and Dutch for language classification.
    """
    features = {
        "contains_the": "the" in segment.lower(),  # Common in English
        "contains_and": "and" in segment.lower(),  # Common in English
        "contains_is": "is" in segment.lower(),    # Common in English
        "contains_van": "van" in segment.lower(),  # Common in Dutch
        "contains_het": "het" in segment.lower()   # Common in Dutch
    }
    return features

# Function to process data (train or test)
def process_data(file_path, features):
    X = []  # Feature matrix
    y = []  # Labels (en/nl)
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            label, segment = line.strip().split(" | ")  # Split the line into label and segment
            feature_values = [extract_features(segment).get(feature, False) for feature in features]
            X.append(feature_values)
            y.append(label)  # Add the label (en/nl)
    
    return X, y

# Function to train a Decision Tree
def train_decision_tree(X_train, y_train, max_depth=None):
    clf = DecisionTreeClassifier(max_depth=max_depth)
    clf.fit(X_train, y_train)
    return clf

# Function to train Adaboost with decision stumps
def train_adaboost(X_train, y_train, n_estimators=50):
    stump = DecisionTreeClassifier(max_depth=1)  # Decision stump (depth = 1)
    clf = AdaBoostClassifier(base_estimator=stump, n_estimators=n_estimators)
    clf.fit(X_train, y_train)
    return clf

# Function to predict using a trained model
def predict(model, X_test):
    return model.predict(X_test)

# Function to save the trained model to a file
def save_model(model, filename):
    joblib.dump(model, filename)

# Function to load the model from a file
def load_model(filename):
    return joblib.load(filename)

# Main program for training or prediction based on command-line arguments
if __name__ == "__main__":
    # Parse the command-line arguments
    if sys.argv[1] == 'train':
        # Read the feature names from features.txt
        with open("features.txt", 'r', encoding='utf-8') as file:
            features = [line.strip() for line in file.readlines()]
        
        # Process the training data
        X_train, y_train = process_data(sys.argv[2], features)  # sys.argv[2] is the path to train.dat
        
        # Train the model based on the chosen learning type
        if sys.argv[4] == 'dt':
            model = train_decision_tree(X_train, y_train, max_depth=5)
        elif sys.argv[4] == 'ada':
            model = train_adaboost(X_train, y_train, n_estimators=50)
        
        # Save the trained model to a file
        save_model(model, sys.argv[3])  # sys.argv[3] is the output model file name (e.g., 'best.model')
        print(f"Model saved to {sys.argv[3]}")
    
    elif sys.argv[1] == 'predict':
        # Load the trained model
        model = load_model(sys.argv[3])  # sys.argv[3] is the model file name (e.g., 'best.model')
        
        # Read the feature names from features.txt
        with open("features.txt", 'r', encoding='utf-8') as file:
            features = [line.strip() for line in file.readlines()]
        
        # Process the test data
        X_test, _ = process_data(sys.argv[2], features)  # sys.argv[2] is the path to test.dat
        
        # Make predictions
        predictions = predict(model, X_test)
        
        # Print the predictions (each prediction on a new line)
        for prediction in predictions:
            print(prediction)

