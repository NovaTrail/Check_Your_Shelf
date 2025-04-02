from io import StringIO
import pandas as pd

from huggingface_hub import InferenceClient 

client = 0 # Replace with Auth Client

import base64

def read_image(file_path,temp):
    try:
        with open(file_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        messages = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
                        You are a vision request to text AI assistant. Make a table of the visible books on this shelf, do not imagine extra books.
                        List only what is visible in the image. If the book's author is not clear leave the author entry blank. Do not repeat books.
                        
                        Table format:
                        | Book Title | Author |
                        | --- | --- |
                        | Left-most book | Author |

                        example (do not return these): 
                        | Book Title | Author |
                        | --- | --- |
                        | The Di Vinci Code | Dan Brown |
                        | Of Adam |  |
                        | Mr Jekyll and Dr Hyde |  |

                        """

                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                ]
            }
        ]

        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct", 
            messages=messages,
            temperature=temp,
            #frequency_penalty = 0.01,
            top_p = 0.96,  # Optional: Control randomness
            max_tokens=400  # Limit response length

        )

        content = completion.choices[0].message.content
        if "|" in content:
            content = content.rsplit(" | ", 1)[0]
        else:
            raise ValueError("Content has no table")
        
        # Remove markdown table formatting and read the table into a pandas DataFrame
        data = StringIO(content)  # Simulate a file object
        df = pd.read_table(data, sep='|', header=0, engine='python').iloc[:, 1:-1]  # Remove extra spaces and columns

        # Rename columns for better readability (optional)
        df.columns = ['Book Title', 'Author']
        
        return df
    except Exception as e:
        columns = ['Book Title', 'Author']
        df = pd.DataFrame([['Could not', 'read']], columns=columns)
        return df