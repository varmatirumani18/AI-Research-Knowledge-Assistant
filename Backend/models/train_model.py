import os
import numpy as np

try:
    import tensorflow as tf
    from tensorflow.keras import layers, models

    print("Training TensorFlow Document Classifier...")

    # Generate synthetic feature vectors representing TF-IDF/embeddings
    X_train = np.random.rand(200, 100)
    y_train = np.random.randint(0, 6, size=(200,))

    model = models.Sequential([
        layers.Dense(64, activation='relu', input_shape=(100,)),
        layers.Dropout(0.3),
        layers.Dense(32, activation='relu'),
        layers.Dense(6, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=10, batch_size=16, verbose=1)

    model_dir = os.path.dirname(__file__)
    model_path = os.path.join(model_dir, "classifier.h5")
    model.save(model_path)
    print(f"Model successfully saved to: {model_path}")

except ModuleNotFoundError:
    print("TensorFlow not installed. Skipping offline training script.")