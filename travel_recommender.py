import pandas as pd
from tabulate import tabulate


df = pd.read_csv("travel_dataset.csv")


df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

df = df.rename(columns={
    "city": "city",
    "state": "state",
    "name": "place_name",
    "google_review_rating": "rating",
    "number_of_google_review_in_lakhs": "popularity",
    "time_needed_to_visit_in_hrs": "time_needed"
})


df = df[
    ["city", "state", "place_name", "rating", "popularity", "time_needed"]
]


df.dropna(inplace=True)
df = df[df["time_needed"] > 0]

pd.set_option("display.float_format", "{:.2f}".format)



def recommend_places(source_city, top_n=5):
    source_rows = df[df["city"].str.lower() == source_city.lower()]

    if source_rows.empty:
        return f"❌ Source city '{source_city}' not found in dataset."

    source_state = source_rows.iloc[0]["state"]

   
    candidates = df[df["city"].str.lower() == source_city.lower()].copy()

    
    if len(candidates) < top_n:
        state_df = df[
            (df["state"] == source_state) &
            (df["city"].str.lower() != source_city.lower())
        ]
        candidates = pd.concat([candidates, state_df])


    if len(candidates) < top_n:
        all_df = df[df["city"].str.lower() != source_city.lower()]
        candidates = pd.concat([candidates, all_df])

   
    candidates = candidates.drop_duplicates(subset=["city", "place_name"])

   
   
    candidates["rating_score"] = candidates["rating"] / 5
    candidates["popularity_score"] = (
        candidates["popularity"] / candidates["popularity"].max()
    )
    candidates["time_score"] = 1 / candidates["time_needed"]

    candidates["final_score"] = (
        0.4 * candidates["rating_score"] +
        0.4 * candidates["popularity_score"] +
        0.2 * candidates["time_score"]
    )

  
    candidates = candidates.sort_values("final_score", ascending=False)
    candidates["rank"] = range(1, len(candidates) + 1)

  
    candidates["city"] = candidates["city"].str.title()
    candidates["place_name"] = candidates["place_name"].str.title()

    
    result = candidates.head(top_n)[
        ["rank", "city", "place_name", "rating", "popularity", "final_score"]
    ].round(2)

    return result


if __name__ == "__main__":
    source_city = input("Enter Source City: ")
    top_n = int(input("Enter number of destinations: "))

    result = recommend_places(source_city, top_n)

    print(f"\n🌍 Top Weekend Destinations from {source_city.title()} (Ranked)\n")

    if isinstance(result, str):
        print(result)
    else:
        print(tabulate(
            result,
            headers="keys",
            tablefmt="fancy_grid",
            showindex=False
        ))
