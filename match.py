import pandas as pd
from rapidfuzz import fuzz, process

# Fuzzy matching function
def fuzzy_match(df1, df2, col1, col2, threshold=60):
    results = []
    
    for idx, title1 in df1[col1].items():
        # Compare title1 with all titles in df2[col2]
        match = process.extractOne(title1, df2[col2], scorer=fuzz.ratio)
        
        # Append to results if similarity score exceeds the threshold
        if match[1] >= threshold:
            results.append((idx, title1, match[0], match[1]))
    
    # Convert results to DataFrame
    return pd.DataFrame(results, columns=['df1_index',f'{col1}_DF1', f'{col2}_DF2', 'Similarity'])

# Fuzzy match and get results

def check_against_db(df):
    df_scan = df.copy()
    db_df = pd.read_csv('book_db/books.csv')
    db_df['Zprice'] = db_df['Zprice'].astype(float)
    df_scan['combined'] = df_scan.apply(lambda row: str(row['Book Title'])+" " + str(row['Author']), axis=1)
    
    matched_df2 = fuzzy_match(db_df, df_scan, 'title', 'Book Title', threshold=90)
    matched_df1 = fuzzy_match(db_df, df_scan, 'combined', 'combined', threshold=85)

    out1 = db_df.loc[matched_df1['df1_index']]
    out1['match'] = "Title only"
    out2 = db_df.loc[matched_df2['df1_index']]
    out2['match'] = "Both"
    out = pd.concat([out1, out2], ignore_index=True) 
    out = out[['title','authors','Zprice','isbn','match']] #,'publication_date'

    # Find the row with the max Zprice per title
    out = out.loc[out.groupby('title')['Zprice'].idxmax()]
    
    out = out[out['Zprice']>=0.0].reset_index()
    out['Zprice'] = out['Zprice'].apply(lambda x: "£"+str(x) + ' - ' + str(x * 2))
    out = out.rename(columns={'Zprice': 'Price Est.'})
    out = out.drop(columns=['index'])

    return out 
