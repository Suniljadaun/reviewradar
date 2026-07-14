""" 
Statistics  and summaries over collection of reviews. 
"""

from .models import Review


def summarize_reviews(reviews :list[Review])->dict:

    if not reviews:
        return {"count":0}
    
    ratings = [r.rating for r in reviews]
    
    return {
        "count":len(reviews),
        "avg_rating":round(sum(ratings)/len(ratings), 2),

        "five_star":sum(1 for r in reviews if r.is_positve() ),
        "one_star" : sum(1 for  r in reviews if r.is_negative()) ,

        "verified_pct": round(100 * sum(1 for r in reviews if r.verified)/ len(reviews), 1), 
        "avg_word_count": round(sum(r.word_count() for r in reviews)/len(reviews), 1), 
    }