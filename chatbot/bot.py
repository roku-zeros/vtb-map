import tensorflow as tf
from tensorflow import keras

credit = []
card = []
invest = []

a = "Нужен кредит на ремонт квартиры и обновление интерьера"
def get_answers(input_message):
    if input_message in credit:
        category = 'credit'
    elif input_message in card:
        category = 'card'
    elif input_message in invest:
        category = 'invest'
    else:
        category = 'unknown'
    return(category)

def run():
    with open('credit.txt', 'r', encoding='utf-8') as file:

        for line in file:

            cleaned_line = line.strip('. \n')

            credit.append(cleaned_line)


    with open('card.txt', 'r', encoding='utf-8') as file:

        for line in file:

            cleaned_line = line.strip('. \n')

            card.append(cleaned_line)

    with open('investm.txt', 'r', encoding='utf-8') as file:

        for line in file:

            cleaned_line = line.strip('. \n')

            invest.append(cleaned_line)





    texts = ["Хочу взять кредит.", "Завожу бизнес в Москве.", "Снял наличные в банкомате.", "Обменяю доллары на евро.", "Принимаем оплату.", "Заказал новую карту.", "Обмен валюты в банке."]

    labels = ['Кредиты', 'Регистрация бизнеса', 'Cнятие наличных', 'Обмен валют', 'Приём платежей', 'Получение карты', 'Обмен валюты']

    """
    tokenizer = Tokenizer(num_words=10000, oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)
    sequences = tokenizer.texts_to_sequences(texts)
    padded_sequences = pad_sequences(sequences, maxlen=50, padding='post', truncating='post')
    
    model = keras.Sequential([
        keras.layers.Embedding(input_dim=10000, output_dim=16, input_length=50),
        keras.layers.GlobalAveragePooling1D(),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dense(len(labels), activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    
    
    labels_ids = [labels.index(label) for label in labels]
    #model.fit(padded_sequences, labels_ids, epochs=10)
    
    '''new_text = ["Обмен долларов на рубли."]
    new_sequence = tokenizer.texts_to_sequences(new_text)
    new_padded_sequence = pad_sequences(new_sequence, maxlen=50, padding='post', truncating='post')
    predicted_class = model.predict(new_padded_sequence)
    predicted_label = labels[predicted_class.argmax()]
    
    print(f"The text is classified as: {predicted_label}")'''
    
    
    print(f(a))
    """
    #%%
