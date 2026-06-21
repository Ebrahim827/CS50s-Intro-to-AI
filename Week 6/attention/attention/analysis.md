# Attention Analysis

## Layer 3, Head 10
This attention head appears to pay attention to the token that immediately 
follows each word. For example, in "We turned down a narrow lane", the word 
"we" attends strongly to "turned", and "turned" attends strongly to "down".
This pattern was consistent across multiple sentences tested.

Example sentences:
- "We turned down a narrow lane and passed through a small [MASK]."
- "Then I picked up a [MASK] from the table."

## Layer 6, Head 3
This attention head appears to pay attention to the relationship between 
determiners and the nouns they modify. The word "a" and "the" consistently 
attend strongly to the noun that follows them.

Example sentences:
- "We turned down a narrow lane and passed through a small [MASK]."
- "Then I picked up a [MASK] from the table."