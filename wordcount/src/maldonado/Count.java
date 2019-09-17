package maldonado;

public class Count {
    private int count;

    public Count(int _count) {
        this.count = _count;
    }

    public int getCount() {
        return count;
    }

    public void add(int _count) {
        count += _count;
    }
}
