QUERIES = {
    "rooms_and_students_count": """
        SELECT r.name, COUNT(s.id) as students_count 
        FROM rooms r LEFT JOIN students s ON r.id = s.room_id 
        GROUP BY r.id, r.name;
    """,
    "top_5_youngest_rooms": """
        SELECT r.name, AVG(EXTRACT(YEAR FROM AGE(NOW(), s.birthday))) as avg_age 
        FROM rooms r JOIN students s ON r.id = s.room_id 
        GROUP BY r.id, r.name ORDER BY avg_age ASC LIMIT 5;
    """,
    "top_5_age_diff_rooms": """
        SELECT r.name, 
               MAX(EXTRACT(YEAR FROM AGE(NOW(), s.birthday))) - MIN(EXTRACT(YEAR FROM AGE(NOW(), s.birthday))) as age_diff
        FROM rooms r JOIN students s ON r.id = s.room_id 
        GROUP BY r.id, r.name ORDER BY age_diff DESC LIMIT 5;
    """,
    "mixed_rooms": """
        SELECT r.name 
        FROM rooms r JOIN students s ON r.id = s.room_id 
        GROUP BY r.id, r.name HAVING COUNT(DISTINCT s.sex) > 1;
    """
}