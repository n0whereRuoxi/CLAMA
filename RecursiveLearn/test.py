file_path = "./domain.pddl"

with open(file_path, 'r') as file:
    content = file.read()

char_at_position_30 = (content[30:35])
line_2 = content.split('\n')[1]
column_3 = line_2[2]

print(f"Character at position 30: {char_at_position_30}")
print(f"Line 2: {line_2}")
print(f"Column 3: {column_3}")
