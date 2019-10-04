package maldonado.recommender;


import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.ThresholdUserNeighborhood;
import org.apache.mahout.cf.taste.impl.recommender.GenericUserBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.PearsonCorrelationSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.recommender.UserBasedRecommender;
import org.apache.mahout.cf.taste.similarity.UserSimilarity;

import java.io.File;
import java.io.IOException;
import java.util.List;

public class TUserRecommended {
    public static void main(String[] args) throws IOException, TasteException {
        String pathname = "/home/maldonado/Cloud/data/mahout/data.csv";
        //String movies = "/home/maldonado/Cloud/data/mahout/movies.csv";

        //Utils utils = new Utils();
        //HashMap<Long, String> movieList = utils.ReadCsv(movies);

        // Load historical data about user preferences
        DataModel model = new FileDataModel(new File(pathname));

        // Compute the similarity between users, according to their preferences
        UserSimilarity similarity = new PearsonCorrelationSimilarity(model);

        // Group the users with similar preferences
        UserNeighborhood neighborhood = new ThresholdUserNeighborhood(0.1,
                similarity, model);

        // Create a recommended
        UserBasedRecommender recommended = new GenericUserBasedRecommender(
                model, neighborhood, similarity);

        // For the user with the id t get n recommendations
        long userID = 1L;
        int rNumber = 5;

        List<RecommendedItem> recommendations = recommended.recommend(userID, rNumber);
        // String name;

        for (RecommendedItem recommendation : recommendations) {
            //name = movieList.get(recommendation.getItemID());
            System.out.println("User " + userID + " might like movie with ID " + recommendation.getItemID()  + " (preference :"
                    + recommendation.getValue() + ")");
        }
    }
}
