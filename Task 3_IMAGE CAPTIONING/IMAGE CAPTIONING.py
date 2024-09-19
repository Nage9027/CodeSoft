"Install the Required Libraries""
"pip install tensorflow pillow numpy matplotlib"

"2. Import the Necessary Libraries"
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Add
from tensorflow.keras.models import Model

"3. Load Pre-trained CNN Model (ResNet)"
# Load the ResNet50 model pre-trained on ImageNet
base_model = ResNet50(weights="imagenet")
model = Model(inputs=base_model.input, outputs=base_model.layers[-2].output)

def extract_image_features(img_path):
    img = Image.open(img_path)
    img = img.resize((224, 224))
    img = np.array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    
    # Extract features
    features = model.predict(img)
    return features

"4. Build the Caption Generation Model (RNN + LSTM)"

def build_captioning_model(vocab_size, max_length):
    # Image feature input
    image_input = Input(shape=(2048,))
    image_layer = Dense(256, activation='relu')(image_input)
    
    # Text input (captions)
    caption_input = Input(shape=(max_length,))
    text_layer = Embedding(vocab_size, 256, mask_zero=True)(caption_input)
    text_layer = LSTM(256)(text_layer)
    
    # Combine the outputs of the image and text models
    combined = Add()([image_layer, text_layer])
    combined = Dense(256, activation='relu')(combined)
    
    # Final output layer to predict the next word in the sequence
    output = Dense(vocab_size, activation='softmax')(combined)
    
    model = Model(inputs=[image_input, caption_input], outputs=output)
    return model
"5. Prepare the Data"
from tensorflow.keras.preprocessing.text import Tokenizer

# Suppose we have a list of captions for the training data
captions = ["A dog running", "A cat sleeping", "A man riding a bike"]
tokenizer = Tokenizer()
tokenizer.fit_on_texts(captions)

# Convert captions to sequences of tokens
sequences = tokenizer.texts_to_sequences(captions)

# Pad the sequences to make them all the same length
max_length = max([len(seq) for seq in sequences])
sequences = pad_sequences(sequences, maxlen=max_length, padding='post')
"6. Train the Model"
# Assuming vocab_size and max_length are already defined
vocab_size = len(tokenizer.word_index) + 1

# Build the captioning model
captioning_model = build_captioning_model(vocab_size, max_length)

# Compile the model
captioning_model.compile(optimizer='adam', loss='categorical_crossentropy')

# Train the model (simplified example)
# You would need image features, caption sequences, and target words for actual training
# history = captioning_model.fit([image_features, input_sequences], target_words, epochs=20)

"7. Generate Captions for New Images"
def generate_caption(model, tokenizer, image_features, max_length):
    # Start the caption generation process
    input_text = 'startseq'
    for i in range(max_length):
        # Tokenize the input sequence
        sequence = tokenizer.texts_to_sequences([input_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        
        # Predict the next word
        y_pred = model.predict([image_features, sequence])
        y_pred = np.argmax(y_pred)
        
        # Get the corresponding word
        word = tokenizer.index_word[y_pred]
        input_text += ' ' + word
        
        # Stop if we reach the end
        if word == 'endseq':
            break
    
    return input_text

"8. Example Usage"
# Load an example image
image_path = 'Dog.jpg'
features = extract_image_features(image_path)

# Generate a caption
caption = generate_caption(captioning_model, tokenizer, features, max_length)
print("Generated Caption:", caption)
