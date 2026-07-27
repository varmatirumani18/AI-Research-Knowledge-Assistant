import os
import numpy as np

try:
    import tensorflow as tf
    from tensorflow.keras import layers, models

    print("Building and training TensorFlow classifier according to reference guide...")

    # Dataset Parameters
    vocab_size = 10000
    max_len = 200
    num_classes = 6

    # Synthetic Dataset (Simulating tokenized sequences for domain classification)
    # Categories: [Artificial Intelligence, Machine Learning, Computer Vision, NLP, Cyber Security, Cloud Computing]
    np.random.seed(42)
    X_train = np.random.randint(1, vocab_size, size=(300, max_len))
    y_train = np.random.randint(0, num_classes, size=(300,))

    # Neural Network Architecture matching Guide Section 5.2
    model = models.Sequential([
        layers.Embedding(input_dim=vocab_size, output_dim=64, mask_zero=True),
        layers.GlobalAveragePooling1D(),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])

    # Compilation
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # Training
    model.fit(
        X_train, 
        y_train, 
        epochs=10, 
        batch_size=32, 
        validation_split=0.2,
        verbose=1
    )

    # Model Persistence
    model_dir = os.path.dirname(__file__)
    model_path = os.path.join(model_dir, "classifier.h5")
    model.save(model_path)
    print(f"\n✅ Model trained and saved successfully to: {model_path}")

except ModuleNotFoundError:
    print("❌ TensorFlow is not installed in the current environment. Skipping model training.")