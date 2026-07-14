"""
Data models for ReviewRadar.

The shapes of our data live here -- and ONlY here.
Every other file import these shapes instead of guessing dict keys.
"""

from dataclasses import dataclass, field

@dataclass(frozen=True)
class Review:
    review_id:str
    text:str
    rating:int
    verified:bool = False


    def is_negative(self)->bool:
        return self.rating <= 2 
    
    def is_positve(self)->bool:
        return self.rating >= 4
    
    def word_count(self)->int:
        return len(self.text.split()) 