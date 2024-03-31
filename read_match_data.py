import psycopg2
import pandas as pd
from fantasy_op import solve_for_best_formation

# Your database connection details
db_params = {
    "dbname": "gpl",
    "user": "gpl_reader",
    "host": "13.232.119.181",
    "port":"5432",
    "password": "pa55w0rd!@#"
}

# SQL query with a placeholder for `match_id`
sql = """
SELECT 
    Name,
    team_id AS team,
    (Match_stats -> 'games' ->> 'position') AS position,
    CAST(Match_stats ->> 'fantasy_score' AS FLOAT) AS points
FROM 
    football_match_players
WHERE 
    match_id = %s
ORDER BY 
    points DESC;
"""

# Connect to the database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# The `match_id` you wish to query for
match_id = '1035467'

# Execute the query, passing the `match_id` as a parameter
cursor.execute(sql, (match_id,))

# Fetch the results
rows = cursor.fetchall()

# Optionally, convert to a pandas DataFrame
df = pd.DataFrame(rows, columns=['name', 'team', 'position', 'points'])

# Close the connection
cursor.close()
conn.close()


players = df.to_dict('records')
teams = df['team'].unique().tolist()


best_formation, max_points, grand_Points, selected_players = solve_for_best_formation(players, teams)
print(f"Best Formation: {best_formation}, Max Points: {max_points}, Grand Points: {grand_Points}")
print("Selected Players:", selected_players)




# pd.set_option('display.max_rows', None) 
# Do something with the DataFrame
# print(df)
