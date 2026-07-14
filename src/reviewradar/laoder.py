"""
loading and validating review data from files.
"""

import csv
from pathlib import Path

from .models import Review

def validate_review(row:dict)->Review | None:

    text = row.get("text","").strip()  


    if not text:
        return None   

    try:
        rating = int(row.get("rating","")) 
    except ValueError: # in case of failed conversion like "rating":"five". Instead of '5'
        return None
    
    if not 1 <= rating <= 5:
          return None
    

    return Review(
        review_id=row.get("review_id",""),
        text=text,
        rating=rating,
        verified= row.get("verified", "").lower()=="true",  
    )

def load_reviews(filepath:str)->list[Review]:

    path = Path(filepath)

    if not path.exists():   

        raise FileNotFoundError(f"Review file not found: {path}")
    
    reviews:list[Review] = []

    skipped = 0

    with open(path, mode='r', encoding="utf-8") as file:
        reader = csv.DictReader(file, skipinitialspace=True)



        for row in reader:
            review  = validate_review(row) 

            if review is None:
                skipped += 1
                continue
            reviews.append(review)

        if skipped:
            print(f"skipped {skipped} invalid review(s)")     
    
    return reviews




    

