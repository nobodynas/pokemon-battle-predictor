import streamlit as st
import pandas as pd
import pickle
from utils import getDualTypeMultiplier

pokemon_df = pd.read_csv("Pokemon.csv")
pokemon_df['id'] = pokemon_df['#']

# load in the model
pokemon_model = pickle.load(open("pokemon_model.pkl", "rb"))

st.title("Pokémon Battle Predictor")

names = pokemon_df['Name'].tolist()

feature_names = [
        'pokemon1_hp', 'pokemon1_attack', 'pokemon1_defense', 'pokemon1_spatk', 'pokemon1_spdef', 'pokemon1_speed',
        'pokemon2_hp', 'pokemon2_attack', 'pokemon2_defense', 'pokemon2_spatk', 'pokemon2_spdef', 'pokemon2_speed',
        'pokemon1_type_adv', 'pokemon2_type_adv'
    ]

# create a dropdown with all the pokemon names
pokemon1_name = st.selectbox("Pokémon 1", names)
pokemon2_name = st.selectbox("Pokémon 2", names)

pokemon1 = pokemon_df[pokemon_df['Name'] == pokemon1_name].iloc[0]
pokemon2 = pokemon_df[pokemon_df['Name'] == pokemon2_name].iloc[0]

# load in sprites from PokeAPI
pokemon1_img = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon1['id']}.png"
pokemon2_img = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon2['id']}.png"

# set up sprites for each pokemon
col1, col2 = st.columns(2)

with col1:
    st.image(pokemon1_img, caption=pokemon1_name)
    with st.expander("View Stats"):
        st.write(f"Type 1: {pokemon1['Type 1']}")
        st.write(f"Type 2: {pokemon1['Type 2']}")
        st.write(f"HP: {pokemon1['HP']}")
        st.write(f"Attack: {pokemon1['Attack']}")
        st.write(f"Defense: {pokemon1['Defense']}")
        st.write(f"Sp. Atk: {pokemon1['Sp. Atk']}")
        st.write(f"Sp. Def: {pokemon1['Sp. Def']}")
        st.write(f"Speed: {pokemon1['Speed']}")
with col2:
    st.image(pokemon2_img, caption=pokemon2_name)
    with st.expander("View Stats"):
        st.write(f"Type 1: {pokemon2['Type 1']}")
        st.write(f"Type 2: {pokemon2['Type 2']}")
        st.write(f"HP: {pokemon2['HP']}")
        st.write(f"Attack: {pokemon2['Attack']}")
        st.write(f"Defense: {pokemon2['Defense']}")
        st.write(f"Sp. Atk: {pokemon2['Sp. Atk']}")
        st.write(f"Sp. Def: {pokemon2['Sp. Def']}")
        st.write(f"Speed: {pokemon2['Speed']}")

# create button that shows the predicted winner after pressing
if st.button("Predict Winner"):
    m1 = getDualTypeMultiplier(pokemon1['Type 1'], pokemon2['Type 1'], pokemon2['Type 2'])
    m2 = getDualTypeMultiplier(pokemon2['Type 1'], pokemon1['Type 1'], pokemon1['Type 2'])

    features = pd.DataFrame([[
        pokemon1['HP'], pokemon1['Attack'], pokemon1['Defense'], pokemon1['Sp. Atk'], pokemon1['Sp. Def'], pokemon1['Speed'],
        pokemon2['HP'], pokemon2['Attack'], pokemon2['Defense'], pokemon2['Sp. Atk'], pokemon2['Sp. Def'], pokemon2['Speed'],
        m1, m2
    ]], columns=feature_names)

    probability = pokemon_model.predict_proba(features)[0]

    pokemon1_win = probability[1] * 100
    pokemon2_win = probability[0] * 100

    if pokemon1_win > pokemon2_win:
        st.success(f"{pokemon1_name} wins!")
    else:
        st.success(f"{pokemon2_name} wins!")

    st.write(f"{pokemon1_name}: {pokemon1_win:.2f}%")
    st.write(f"{pokemon2_name}: {pokemon2_win:.2f}%")