
from file_to_titles import read_image
from match import check_against_db
import concurrent.futures 
import os
import random
from rapidfuzz import process, fuzz

def common_df(dfA,dfB):
    dfA['Match'] = dfA['Book Title'].apply(find_matches, candidates=dfB['Book Title'].tolist())
    df = dfA[dfA['Match'].notnull()]
    df = df.drop(columns='Match')
    df = df.dropna(subset=["Book Title"])
    return df

# Create a function to find matches
def find_matches(row, candidates, scorer=fuzz.ratio):

    # Define a threshold for similarity
    threshold = 90

    # Use process.extractOne for fuzzy matching
    result = process.extractOne(row, candidates, scorer=scorer)
    if result:
        match, score, _ = result
        return match if score >= threshold else None
    return None



def analyse_image(cropped, name, side=None):
    
     
    file_loc = f"store/{name}_shelf_" + str(random.randint(1, 10000)) + ".jpg"
    cropped.save(file_loc)

    # Get 3 different readings of the image
    params = [0.2, 0.25, 0.3]    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda p: read_image(file_loc, p), params))
    
    df1, df2, df3 = results 

    # Check different attempts against each other
    pairs = [(df1, df2), (df1, df3), (df2, df3)]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda p: common_df(*p), pairs))

    df_v1, df_v2, df_v3 = results  # Unpack results

    # Select the iteration with the most matches
    all_df = max([df_v1, df_v2, df_v3], key=len)

    db_match = check_against_db(all_df)

    all_df = all_df[['Book Title', 'Author']]
    if side != None:
        all_df['side'] = side
        db_match['side'] = side

    return db_match, all_df


def clear_temp_files():
    folder_path =  "store"
    
    # List all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # Check if it's a file and delete it
        if os.path.isfile(file_path):
            os.remove(file_path)
            #print(f"Deleted: {file_path}")
