package maldonado.recommender;

import java.io.*;

public class TConvert {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader(("/home/maldonado/Cloud/data/mahout/ratings.csv")));
        BufferedWriter bw = new BufferedWriter(new FileWriter("/home/maldonado/Cloud/data/mahout/data.csv"));

        String line;

        while ((line = br.readLine()) != null){
            String values[] = line.split(",", -1);
            bw.write(values[0] + "," + values[1] + "," + values[2] + "\n");
        }

        br.close();
        bw.close();
    }
}
