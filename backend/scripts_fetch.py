import os
import pandas as pd
import random


def script_fetcher()->list:
        
        script_list = []

        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path  = os.path.join(script_dir,  "clean_transcripts.csv")

        df = pd.read_csv(csv_path, header=None)

        col0 = df[0].dropna()                     
        col0 = col0.astype(str)                    
        col0 = col0[col0.str.strip() != ""]         

        if len(col0) < 5:
            raise ValueError(f"Only found {len(col0)} non‑empty rows; need at least 5.")

        choices = random.sample(col0.tolist(), 5)
        for i, val in enumerate(choices, 1):
              script_list.append(f"{i}. {val}")

        return script_list
        
