import pandas as pd

# a chart demonstrating all the type matchups between pokemon
# it provides multipliers depending on the matchup
type_chart = {
    "Normal": {"Fighting": 0.5, "Ghost": 0},
    "Fire": {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 2, "Bug": 2, "Rock": 0.5, "Dragon": 0.5, "Steel": 2},
    "Water": {"Fire": 2, "Water": 0.5, "Grass": 0.5, "Ground": 2, "Rock": 2, "Dragon": 0.5},
    "Electric": {"Water": 2, "Electric": 0.5, "Grass": 0.5, "Ground": 0, "Flying": 2, "Dragon": 0.5},
    "Grass": {"Fire": 0.5, "Water": 2, "Grass": 0.5, "Poison": 0.5, "Ground": 2, "Flying": 0.5, "Bug": 0.5, "Rock": 2, "Dragon": 0.5, "Steel": 0.5},
    "Ice": {"Fire": 0.5, "Water": 0.5, "Grass": 2, "Ice": 0.5, "Ground": 2, "Flying": 2, "Dragon": 2, "Steel": 0.5},
    "Fighting": {"Normal": 2, "Ice": 2, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2, "Ghost": 0, "Dark": 2, "Steel": 2, "Fairy": 0.5},
    "Poison": {"Grass": 2, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0, "Fairy": 2},
    "Ground": {"Fire": 2, "Electric": 2, "Grass": 0.5, "Poison": 2, "Flying": 0, "Bug": 0.5, "Rock": 2, "Steel": 2},
    "Flying": {"Electric": 0.5, "Grass": 2, "Fighting": 2, "Bug": 2, "Rock": 0.5, "Steel": 0.5},
    "Psychic": {"Fighting": 2, "Poison": 2, "Psychic": 0.5, "Dark": 0, "Steel": 0.5},
    "Bug": {"Fire": 0.5, "Grass": 2, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Ghost": 0.5, "Dark": 2, "Steel": 0.5, "Fairy": 0.5},
    "Rock": {"Fire": 2, "Rock": 2, "Fighting": 0.5, "Ground": 0.5, "Flying": 2, "Bug": 2, "Steel": 0.5},
    "Ghost": {"Normal": 0, "Psychic": 2, "Ghost": 2, "Dark": 0.5},
    "Dragon": {"Dragon": 2, "Steel": 0.5, "Fairy": 0},
    "Dark": {"Fighting": 0.5, "Psychic": 2, "Ghost": 2, "Dark": 0.5, "Fairy": 0.5},
    "Steel": {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2, "Rock": 2, "Steel": 0.5, "Fairy": 2},
    "Fairy": {"Fire": 0.5, "Fighting": 2, "Poison": 0.5, "Dragon": 2, "Dark": 2, "Steel": 0.5},
}

# function to get/calculate the multiplier between the attacker pokemon and the defending one depending on the type matchup
def getDualTypeMultiplier(attacker, def_type1, def_type2):
    multiplier = 1

    if attacker in type_chart:
        multiplier *= type_chart[attacker].get(def_type1, 1)

    if pd.notna(def_type2):
        if attacker in type_chart:
            multiplier *= type_chart[attacker].get(def_type2, 1)

    return multiplier

# pokemon battle simulation using pokemon stats and typings
def simulateBattle(pokemon1, pokemon2):
    m1 = getDualTypeMultiplier(pokemon1['Type 1'], pokemon2['Type 1'], pokemon2['Type 2'])
    m2 = getDualTypeMultiplier(pokemon2['Type 1'], pokemon1['Type 1'], pokemon1['Type 2'])

    pokemon1_damage = (pokemon1['Attack'] / pokemon2['Defense']) + (pokemon1['Sp. Atk'] / pokemon2['Sp. Def'])
    pokemon2_damage = (pokemon2['Attack'] / pokemon1['Defense']) + (pokemon2['Sp. Atk'] / pokemon1['Sp. Def'])

    # scale speed and hp stats down before adding so they don't dominate the results
    pokemon1_score = (pokemon1_damage * m1) + (pokemon1['Speed'] * 0.1) + (pokemon1['HP'] * 0.05)
    pokemon2_score = (pokemon2_damage * m2) + (pokemon2['Speed'] * 0.1) + (pokemon2['HP'] * 0.05)

    if pokemon1_score > pokemon2_score:
        return 1
    else:
        return 0