package maldonado.recommender;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;

class Utils {

    HashMap<Long, String> ReadCsv(String _pathname) throws IOException {
        HashMap<Long, String> _values = new HashMap<Long, String> ();

        BufferedReader br = new BufferedReader(new FileReader((_pathname)));

        String line;

        while ((line = br.readLine()) != null){
            String cols[] = line.split(",", -1);
            _values.put(Long.parseLong(cols[0]), cols[1]);
        }

        br.close();

        return _values;
    }

}
