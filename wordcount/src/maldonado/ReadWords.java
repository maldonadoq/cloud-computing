package maldonado;

import java.io.File;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.Callable;
import java.util.logging.Level;
import java.util.logging.Logger;

public class ReadWords implements Callable<Map<String, Count>> {
    private final Map<String, Count> words;
    private RandomAccessFile fileInput;
    private long realPosition;
    private final long nChunks;
    private long end;
    private final byte[] buffer;

    public ReadWords(File file, int nChunks, int position, int sizeBuffer){
        words = new HashMap<>();
        try {
            createAccess(file, nChunks, position);
        } catch (IOException e) {
            e.printStackTrace();
        }
        this.nChunks = nChunks;
        this.end = 0;
        buffer = new byte[sizeBuffer];
    }

    private void createAccess(File file, int nChunks, int position) throws IOException {
        try {
            realPosition = (file.length() / nChunks) * position;
            fileInput = new RandomAccessFile(file, "r");
            fileInput.seek(getRealPosition());
            movePositionInitialRight();
        } catch (Exception ex) {
            Logger.getLogger(ReadWords.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    private void movePositionInitialRight() throws IOException {
        final byte EOF = -1;

        if(fileInput.getFilePointer() == 0)
            return;

        char c = (char)fileInput.readByte();

        while (c != EOF && Character.isAlphabetic(c)){
            realPosition++;
            c = (char)fileInput.readByte();
        }
    }

    @Override
    public Map<String, Count> call() throws Exception {
        try {
            StringBuilder builder = new StringBuilder();
            char c;
            Count count;
            String word;
            int bufferIndex = 0;

            while(this.realPosition <= end) {
                bufferIndex = bufferIndex%buffer.length;
                if (bufferIndex == 0) {
                    fileInput.read(buffer);
                }
                c = (char)buffer[bufferIndex];
                if ( Character.isAlphabetic(c) ) {
                    builder.append(c);
                } else {
                    word = builder.toString();
                    if(word.length()>0) {
                        count = words.get(word);
                        if (count == null) {
                            words.put(word, new Count(1));
                        } else {
                            count.add(1);
                        }

                        builder.setLength(0);
                    }
                }
                bufferIndex++;
                realPosition++;
            }
        } catch (IOException ex) {
            Logger.getLogger(ReadWords.class.getName()).log(Level.SEVERE, null, ex);
        }
        return this.words;
    }

    public long getRealPosition() {
        return realPosition;
    }

    public void setEnd(long end) {
        this.end = end;
    }
}
