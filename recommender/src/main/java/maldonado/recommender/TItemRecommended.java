package maldonado.recommender;

import javafx.util.Pair;
import org.apache.mahout.cf.taste.common.TasteException;
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.recommender.GenericItemBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.PearsonCorrelationSimilarity;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.recommender.ItemBasedRecommender;
import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.similarity.ItemSimilarity;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;

public class TItemRecommended {
    public static void main(String[] args) throws IOException, TasteException {
        String pathname = "/home/maldonado/Cloud/data/mahout/data.csv";
        String movies = "/home/maldonado/Cloud/data/mahout/movies.csv";

        Utils utils = new Utils();
        HashMap<Long, String> movieList = utils.ReadCsv(movies);

        // Load historical data about user preferences
        DataModel model = new FileDataModel(new File(pathname));

        // Compute the similarity between items, according to their preferences
        ItemSimilarity similarity = new PearsonCorrelationSimilarity(model);

        // Create a recommended
        ItemBasedRecommender recommended = new GenericItemBasedRecommender(model, similarity);

        // For the user with the id t get n recommendations
        long userID = 1L;
        int rNumber = 5;

        List<RecommendedItem> recommendations = recommended.recommend(userID, rNumber);
        String name;

        for (RecommendedItem recommendation : recommendations) {
            name = movieList.get(recommendation.getItemID());
            System.out.println("User " + userID + " might like " + name  + " (preference :"
                    + recommendation.getValue() + ")");
        }
    }
}
