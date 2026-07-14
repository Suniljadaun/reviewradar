""" 
Entry point for ReviewRadar - 
"""


import sys

sys.path.insert(0, "src") 

from reviewradar import load_reviews, summarize_reviews


def main():
    reviews = load_reviews("data/reviews_sample.csv")

    stats = summarize_reviews(reviews) 

    print("\n Review radar - Data summary ")
    for key , value in stats.items():
        print(f"{key}:{value}")



    print("\n Sample negative reviews:")
    for review in reviews:
        if review.is_negative():
            print(f"[{review.rating}] {review.text[:50]}") 


if __name__ == "__main__":
    main()
