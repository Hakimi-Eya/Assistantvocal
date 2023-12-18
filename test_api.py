import openai

# Configurer une clé d'API valide
openai.api_key = "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"


# Demander à l'utilisateur de saisir une recherche
prompt = input("Tape ta question : ")

# Envoyer une requête à l'API de GPT
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "c'est qui cristiano ronaldo ?"}
    ]
)

# Afficher la réponse
print(response)

