# Weekend-Getaway-Ranker
Python-based weekend travel recommendation system that ranks nearby destinations using distance, user ratings, and popularity, enabling data-driven local getaway planning from a chosen source city.


## 🧠 Recommendation Logic

The dataset does not contain explicit city-to-city distance values.  
To address this, the system uses the following **well-justified approach**:

| Factor | Usage |
|------|------|
| Rating | Higher rating → higher recommendation |
| Popularity | More Google reviews → more popular |
| Time Needed | Less time → more suitable for a weekend trip |

### 🔢 Final Score Formula

