# Washington Trails Recommender
## Description
Trails were scraped from the [Washington Trails Association](https://www.wta.org/go-outside/hikes) website and clustered based on their physical features, e.g. having meadows, mountain views, rivers, etc. The cluster labels were then used to build a recommender system which was then used as the foundation for a microservice hosted on Heroku, [here](https://watrailsrecommender.herokuapp.com/). 

The way the recommender system works is that users input 3 trails and the reccomender returns 3 similar type trails.
