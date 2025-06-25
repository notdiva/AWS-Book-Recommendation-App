import pandas as pd
import random

# Load your datasets
users_df = pd.read_csv('user_data.csv')      # Should have: user_id
books_df = pd.read_csv('book_data.csv')      # Should have: book_id (or item_id) and title

# Rename for consistency
books_df.rename(columns={'book_id': 'item_id'}, inplace=True)

# Create a new list to hold generated interactions
interactions = []

# Set number of interactions to generate
num_interactions = 1000  # You can modify this

# Generate interactions
for _ in range(num_interactions):
    user = random.choice(users_df['user_id'].tolist())
    random_book = books_df.sample(1).iloc[0]
    book_id = random_book['item_id']
    book_title = random_book['book_title']
    timestamp = random.randint(10000, 50000)  # Smaller timestamp
    
    interactions.append([user, book_id, book_title, timestamp])

# Convert to DataFrame
interactions_df = pd.DataFrame(interactions, columns=['user_id', 'item_id', 'book_title', 'timestamp'])

# Save to CSV
interactions_df.to_csv('interactions.csv', index=False)
print("Generated interactions.csv successfully!")
