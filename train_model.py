import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from utils import simulateBattle, getDualTypeMultiplier

# load in the dataset
pokemon_df = pd.read_csv("Pokemon.csv")

data = []

for _ in range(10000):
    # pick two random pokemon to use to train the dataset
    pokemon1 = pokemon_df.sample(1).iloc[0]
    pokemon2 = pokemon_df.sample(1).iloc[0]

    # calculate the type advantage multiplier
    m1 = getDualTypeMultiplier(pokemon1['Type 1'], pokemon2['Type 1'], pokemon2['Type 2'])
    m2 = getDualTypeMultiplier(pokemon2['Type 1'], pokemon1['Type 1'], pokemon1['Type 2'])

    # decide on the winner after simulating the battle
    winner = simulateBattle(pokemon1, pokemon2)

    # add the pokemon and battle results to the new dataset
    data.append([
        pokemon1['HP'], pokemon1['Attack'], pokemon1['Defense'], pokemon1['Sp. Atk'], pokemon1['Sp. Def'], pokemon1['Speed'],
        pokemon2['HP'], pokemon2['Attack'], pokemon2['Defense'], pokemon2['Sp. Atk'], pokemon2['Sp. Def'], pokemon2['Speed'],
        m1, m2,
        winner
    ])

# name the columns of the new dataset
battle_df = pd.DataFrame(data, columns=[
    'pokemon1_hp', 'pokemon1_attack', 'pokemon1_defense', 'pokemon1_spatk', 'pokemon1_spdef', 'pokemon1_speed',
    'pokemon2_hp', 'pokemon2_attack', 'pokemon2_defense', 'pokemon2_spatk', 'pokemon2_spdef', 'pokemon2_speed',
    'pokemon1_type_adv', 'pokemon2_type_adv',
    'winner'
])

# drop target
X = battle_df.drop('winner', axis=1)
y = battle_df['winner']

# make a random forest classifier model based off the new battle dataset
model = RandomForestClassifier()
model.fit(X, y)

# save the model
pickle.dump(model, open("pokemon_model.pkl", "wb"))