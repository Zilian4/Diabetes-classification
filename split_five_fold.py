import numpy as np
import json



# Write to a JSON file
for i in range(10):
    # Example list with 139 numbers
    data = list(range(1, 140))  # Example dataset (1 to 139)

    # Shuffle the data
    np.random.seed(42)  # Set seed for reproducibility
    np.random.shuffle(data)

    # Split into train and test
    test_size = len(data) // 10  # 10% for testing
    test_set = data[:test_size]
    train_set = data[test_size:]

    # Save train and test sets to a JSON file
    output = {
        "train": [str(id)+'.nii.gz' for id in train_set],
        "test": [str(id)+'.nii.gz' for id in test_set]
    }
    with open(f"/Users/zilianghong/Documents/GitHub/Diabetes-classification/Trial_{i+1}.json", "w") as json_file:
        json.dump(output, json_file, indent=4)

    print("Training and testing sets saved as 'train_test_split.json'")
