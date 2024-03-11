import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load data
books_dict = pickle.load(open("C:/Users/Asus/PycharmProjects/book_Recommendation/artifacts/books_dict.pkl", "rb"))
books = pd.DataFrame(books_dict)
similarity_scores = pickle.load(open("artifacts/similarity_scores.pkl", "rb"))
book_pivot = pickle.load(open("artifacts/book_pivot_df.pkl", "rb"))
book_pivot1 = book_pivot.reset_index()



def recommend(book_name):
    # Check if book_name exists in book_pivot.index
    if book_name in book_pivot.index:
        # index fetch
        index = np.where(book_pivot1['title'] == book_name)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:13]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['title'] == book_pivot.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('title')['title'].values))
            item.extend(list(temp_df.drop_duplicates('title')['author'].values))
            item.extend(list(temp_df.drop_duplicates('title')['image_url'].values))

            data.append(item)

        return data
    else:
        # Handle case when book_name is not found
        st.error(f"Book '{book_name}' not found in the recommendation list.")
        return []


st.title("Book Recommendation System")

selected_book_name = st.selectbox(
    'Select a book:',
    book_pivot1["title"].unique())  # Assuming 'books' is the correct DataFrame

if st.button('Recommend'):
    recommendation_data = recommend(selected_book_name)

    if recommendation_data:
        # Ensure there are only 12 recommendations for display
        recommendation_data = recommendation_data[:12]

        # Calculate the total number of recommendations
        total_recs = len(recommendation_data)

        # Calculate how many full rows of 4 we will have
        full_rows = total_recs // 4

        for i in range(full_rows):
            # Create a row of 4 columns for each set of 4 recommendations
            cols = st.columns(4)
            start_index = i * 4
            for col, book in zip(cols, recommendation_data[start_index:start_index+4]):
                with col:
                    st.image(book[2], width=150)  # Display book image
                    st.write(f"{book[0]}")  # Display book title
                    st.write(f"by {book[1]}")  # Display author name

        # Check if there are any remaining recommendations to display in a final row
        remaining_recs = total_recs % 4
        if remaining_recs:
            cols = st.columns(4)
            start_index = full_rows * 4
            for index in range(remaining_recs):
                with cols[index]:
                    book = recommendation_data[start_index + index]
                    st.image(book[2], width=150)
                    st.write(f"{book[0]}")
                    st.write(f"by {book[1]}")



