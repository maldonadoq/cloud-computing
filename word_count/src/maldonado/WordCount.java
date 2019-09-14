package maldonado;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class WordCount {
    public static void main(String[] args) throws Exception{
        long startTime = System.currentTimeMillis();

        if (args.length == 0) {
            // System.out.println("Hello World");
            args = new String[1];
            args[0] = "/home/maldonado/Cloud/data/data3kkk.txt";
        }
        if (args.length > 0){
            File file = new File(args[0]);
            int nChunks = 16;
            int sizeBuffer = 1024*1024 * 10;

            // We create readers depending on each piece of the giant file
            List<ReadWords> readers = IntStream
                    .range(0, nChunks)
                    .mapToObj(position -> new ReadWords(file, nChunks, position, sizeBuffer))
                    .collect(Collectors.toList());

            // We set the end of reading for each reader
            for(int index=1; index<readers.size() ;index++) {
                readers.get(index-1).setEnd(readers.get(index).getRealPosition());
            }
            readers.get(readers.size()-1).setEnd(file.length()-1);

            // We create "nChunks" threads to launch and read in parallel
            ExecutorService service = Executors.newFixedThreadPool(nChunks);

            // We invoke the threads
            List<Future<Map<String, Count>>> results = service.invokeAll(readers);

            // We hope the threads finish their work
            service.shutdown();

            Map<String, Count> total = new TreeMap<>();

            results.forEach(words -> {
                try {
                    words.get().forEach((word, Count) -> {
                        Count CountTotal = total.get(word);
                        if (CountTotal == null) {
                            total.put(word, new Count(Count.getCount()));
                        } else {
                            CountTotal.add(Count.getCount());
                        }
                    });
                } catch (InterruptedException | ExecutionException ex) {
                    Logger.getLogger(WordCount.class.getName()).log(Level.SEVERE, null, ex);
                }
            });

            total.forEach((word, Count) -> {
                System.out.println(word + " => " + Count.getCount());
            } );
        }

        long endTime = System.currentTimeMillis();
        long timeElapsed = endTime - startTime;
        System.out.println("\nExecution time in milliseconds: " + timeElapsed);
        System.out.println("Execution time in seconds: " + (double)timeElapsed/1000);
        System.out.println("Execution time in minutes: " + (double)timeElapsed/(1000*60));
    }
}