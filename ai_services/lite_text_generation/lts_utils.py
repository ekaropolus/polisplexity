from textgenrnn import textgenrnn

def train_text():
    # Load your dataset
    BASE_PATH = '/home/Admingania/portal_gain/ai_services/lite_text_generation/static/'
    with open(BASE_PATH + "text/dataset.txt", "r") as f:
        dataset = f.read()

    # Train the model
    textgen = textgenrnn()
    textgen.train_on_texts(dataset, num_epochs=5)

    # Save the model
    textgen.save(BASE_PATH + "models/model.h5")