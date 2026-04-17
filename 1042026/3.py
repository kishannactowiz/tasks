import json
import jmespath

with open("airbnb_review.json","r",encoding="utf-8") as f:
    data = json.load(f)


start = jmespath.search("data.presentation.stayProductDetailPage.reviews",data)


reviewsName = jmespath.search("reviews[].reviewer.firstName",start)
reviewsDate = jmespath.search("reviews[].localizedDate",start)
reviewsRating = jmespath.search("reviews[].rating",start)
raviewsComment = jmespath.search("reviews[].commentV2",start)


FinalReviews = []

for i in range(len(reviewsName)):
    temp = {
        "name":reviewsName[i],
        "rating": reviewsRating[i],
        "date": reviewsRating[i],
        "comments": raviewsComment[i]
    }
    FinalReviews.append(temp)

print(FinalReviews)

with open("3output.json","w") as f: 
    json.dump(FinalReviews,f,indent=2)





print(raviewsComment)