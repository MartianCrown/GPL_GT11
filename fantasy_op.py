import pandas as pd
import pulp

def setup_problem(players, formation, formation_name, teams):
    problem = pulp.LpProblem(f"Fantasy_Team_Selection_{formation_name}", pulp.LpMaximize)
    player_vars = {p['name']: pulp.LpVariable(f"player_{p['name']}", cat='Binary') for p in players}
    problem += pulp.lpSum([p['points'] * player_vars[p['name']] for p in players]), "Total_Fantasy_Points"
    
    positions = ['G', 'D', 'M', 'F']
    for pos, req in zip(positions, formation):
        problem += pulp.lpSum(player_vars[p['name']] for p in players if p['position'] == pos) == req, f"{pos}_Requirement"
    
    for team in teams:
        problem += pulp.lpSum(player_vars[p['name']] for p in players if p['team'] == team) <= 7, f"Max_7_from_{team}"
    
    return problem, player_vars

def solve_for_best_formation(players, teams):
    formations = {
        '4-4-2': (1, 4, 4, 2),
        '4-3-3': (1, 4, 3, 3),
        '4-5-1': (1, 4, 5, 1),
        '3-4-3': (1, 3, 4, 3),
        '3-5-2': (1, 3, 5, 2),
        '5-3-2': (1, 5, 3, 2),
        '5-4-1': (1, 5, 4, 1),
    }
    best_score = 0
    best_formation = None
    best_team = []
    
    for formation_name, formation in formations.items():
        problem, player_vars = setup_problem(players, formation, formation_name, teams)
        status = problem.solve()
        
        if status == pulp.LpStatusOptimal:
            score = pulp.value(problem.objective)
            if score > best_score:
                best_score = score
                best_formation = formation_name
                selected_players = [p for p in players if player_vars[p['name']].varValue > 0.5]
                best_team = [p['name'] for p in players if player_vars[p['name']].varValue > 0.5]
                grandPoints = best_score + 0.5 * selected_players[0]['points'] + 0.25 * selected_players[1]['points']

    return best_formation, best_score, grandPoints, best_team

# def read_players_from_csv(file_path):
#     # Reading the CSV into a DataFrame
#     df = pd.read_csv(file_path)
    
#     # Convert DataFrame to list of dictionaries
#     players = df.to_dict('records')
#     teams = df['team'].unique().tolist()
#     return players, teams

# # Replace 'your_file_path_here.csv' with your actual file path
# file_path = 'match_data.csv'
# players,teams = read_players_from_csv(file_path)
# best_formation, max_points, selected_players = solve_for_best_formation(players, teams)
# print(f"Best Formation: {best_formation}, Max Points: {max_points}")
# print("Selected Players:", selected_players)
