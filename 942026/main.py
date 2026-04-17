import json
import jmespath

from page.first import FinalOutput
from page.second import seeAllAmenitiesGroups
from page.third import FinalReviews
from page.forth import ProfileDetails

FinalOutput["amenities"] = seeAllAmenitiesGroups
FinalOutput["reviews"] = FinalReviews
FinalOutput["ProfileDetails"] = ProfileDetails

with open("output.json","w",encoding="utf-8") as f:
     json.dump(FinalOutput,f,indent=2)
