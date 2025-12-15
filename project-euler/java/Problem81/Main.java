import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Objects;
import java.util.Queue;
import java.util.StringTokenizer;
import java.util.function.BiFunction;
import java.util.function.Function;

public class Main {

    static BiFunction<Integer, Integer, Integer> ADD = (x, y) -> (x + y);
    static BiFunction<ArrayList<Integer>, ArrayList<Integer>, ArrayList<Integer>> ADD_ARRAY_LIST = (x, y) -> {
        x.addAll(y);
        return x;
    };

    static Function<Pair<Integer, Integer>, Integer> GET_FIRST = (x) -> (x.first);
    static Function<Pair<Integer, Integer>, Integer> GET_SECOND = (x) -> (x.second);
    static Comparator<Pair<Integer, Integer>> C = Comparator.comparing(x -> x.first + x.second);
    static long MOD = 1_000_000_000 + 7;


    public static void main(String[] args) throws Exception {
        long startTime = System.nanoTime();
        int t = 1;
        while (t-- > 0) {
            solve();
        }
        long endTime = System.nanoTime();
        err.println("Execution Time : +" + (endTime - startTime) / 1000000 + " ms");
        exit(0);
    }

    static void solve() {
        int[][] vert = new int[80][80];
        int[][] id = new int[80][80];
        int[] weight = new int[6410];
        for (int i = 0; i < 80; i++) {
            String s = in.next();
            vert[i] = Arrays.stream(s.split(",")).mapToInt(Integer::parseInt).toArray();
        }
        for (int i = 0, k = 1; i < 80; i++) {
            for (int j = 0; j < 80; j++, k++) {
                id[i][j] = k;
                weight[k] = vert[i][j];
            }
        }
        ArrayList<Integer>[] adj = new ArrayList[6410];
        for (int i = 0; i < 80; i++) {
            for (int j = 0; j < 80; j++) {
                adj[id[i][j]] = new ArrayList<>();
                addEdge(i, j, id, adj);
            }
        }
        ArrayList<String> d = new ArrayList<>();
        for (int i = 1; i <= 10; i++) {
            d.addAll(toString(i, adj, weight));
        }
        genGraph(d);
    }

    static ArrayList<String> toString(int i, ArrayList<Integer>[] adj, int[] weight) {
        ArrayList<String> res = new ArrayList<>();
        for (int a : adj[i]) {
            res.add("(" + i + "," + a + "," + (weight[i] + weight[a]) + ")");
        }
        return res;
    }

    static void genGraph(ArrayList<String> g) {
        out.println("curGraph=Graph([");
        for (int i = 0; i < g.size(); i++) {
            out.print(g.get(i));
            if (i != g.size() - 1) {
                out.print(",");
            }
        }
        out.println("])");
    }

    class Vertex {
        int id;
        int distance;
    }

    static void addEdge(int i, int j, int[][] id, ArrayList[] adj) {
        int[] dx = {0, 1};
        int[] dy = {1, 0};
        for (int x = 0; x < dx.length; x++) {
            if (i + dx[x] < 80 && j + dy[x] < 80) {
                adj[id[i][j]].add(id[i + dx[x]][j + dy[x]]);
            }
        }
    }

    static void debug(Object... args) {
        for (Object a : args) {
            out.println(a);
        }
    }

    static int dist(Pair<Integer, Integer> a, Pair<Integer, Integer> b) {
        return Math.abs(a.first - b.first) + Math.abs(a.second - b.second);
    }

    static void y() {
        out.println("YES");
    }

    static void n() {
        out.println("NO");
    }

    static int[] stringToArray(String s) {
        return s.chars().map(x -> Character.getNumericValue(x)).toArray();
    }

    static <T> T min(T a, T b, Comparator<T> C) {
        if (C.compare(a, b) <= 0) {
            return a;
        }
        return b;
    }

    static <T> T max(T a, T b, Comparator<T> C) {
        if (C.compare(a, b) >= 0) {
            return a;
        }
        return b;
    }

    static void fail() {
        out.println("-1");
    }

    static class Pair<T, R> {
        public T first;
        public R second;

        public Pair(T first, R second) {
            this.first = first;
            this.second = second;
        }

        @Override
        public boolean equals(final Object o) {
            if (this == o) {
                return true;
            }
            if (o == null || getClass() != o.getClass()) {
                return false;
            }
            final Pair<?, ?> pair = (Pair<?, ?>) o;
            return Objects.equals(first, pair.first) && Objects.equals(second, pair.second);
        }

        @Override
        public int hashCode() {
            return Objects.hash(first, second);
        }

        @Override
        public String toString() {
            return "Pair{" + "a=" + first + ", b=" + second + '}';
        }

        public T getFirst() {
            return first;
        }

        public R getSecond() {
            return second;
        }
    }

    static <T, R> Pair<T, R> make_pair(T a, R b) {
        return new Pair<>(a, b);
    }

    static long mod_inverse(long a, long m) {
        Number x = new Number(0);
        Number y = new Number(0);
        extended_gcd(a, m, x, y);
        return (m + x.v % m) % m;
    }

    static long extended_gcd(long a, long b, Number x, Number y) {
        long d = a;
        if (b != 0) {
            d = extended_gcd(b, a % b, y, x);
            y.v -= (a / b) * x.v;
        } else {
            x.v = 1;
            y.v = 0;
        }
        return d;
    }

    static class Number {
        long v = 0;

        public Number(long v) {
            this.v = v;
        }
    }

    static long lcm(long a, long b, long c) {
        return lcm(a, lcm(b, c));
    }

    static long lcm(long a, long b) {
        long p = 1L * a * b;
        return p / gcd(a, b);
    }

    static long gcd(long a, long b) {
        while (b != 0) {
            long t = b;
            b = a % b;
            a = t;
        }
        return a;
    }

    static long gcd(long a, long b, long c) {
        return gcd(a, gcd(b, c));
    }

    static class ArrayUtils {

        static void swap(int[] a, int i, int j) {
            int temp = a[i];
            a[i] = a[j];
            a[j] = temp;
        }

        static void swap(char[] a, int i, int j) {
            char temp = a[i];
            a[i] = a[j];
            a[j] = temp;
        }

        static void print(char[] a) {
            for (char c : a) {
                out.print(c);
            }
            out.println("");
        }

        static int[] reverse(int[] data) {
            int[] p = new int[data.length];
            for (int i = 0, j = data.length - 1; i < data.length; i++, j--) {
                p[i] = data[j];
            }
            return p;
        }

        static void prefixSum(long[] data) {
            for (int i = 1; i < data.length; i++) {
                data[i] += data[i - 1];
            }
        }

        static void prefixSum(int[] data) {
            for (int i = 1; i < data.length; i++) {
                data[i] += data[i - 1];
            }
        }

        static long[] reverse(long[] data) {
            long[] p = new long[data.length];
            for (int i = 0, j = data.length - 1; i < data.length; i++, j--) {
                p[i] = data[j];
            }
            return p;
        }

        static char[] reverse(char[] data) {
            char[] p = new char[data.length];
            for (int i = 0, j = data.length - 1; i < data.length; i++, j--) {
                p[i] = data[j];
            }
            return p;
        }

        static int[] MergeSort(int[] A) {
            if (A.length > 1) {
                int q = A.length / 2;
                int[] left = new int[q];
                int[] right = new int[A.length - q];
                System.arraycopy(A, 0, left, 0, q);
                System.arraycopy(A, q, right, 0, A.length - q);
                int[] left_sorted = MergeSort(left);
                int[] right_sorted = MergeSort(right);
                return Merge(left_sorted, right_sorted);
            } else {
                return A;
            }
        }

        static int[] Merge(int[] left, int[] right) {
            int[] A = new int[left.length + right.length];
            int i = 0;
            int j = 0;
            for (int k = 0; k < A.length; k++) {
                // To handle left becoming empty
                if (i == left.length && j < right.length) {
                    A[k] = right[j];
                    j++;
                    continue;
                }
                // To handle right becoming empty
                if (j == right.length && i < left.length) {
                    A[k] = left[i];
                    i++;
                    continue;
                }
                if (left[i] <= right[j]) {
                    A[k] = left[i];
                    i++;
                } else {
                    A[k] = right[j];
                    j++;
                }
            }
            return A;
        }

        static long[] MergeSort(long[] A) {
            if (A.length > 1) {
                int q = A.length / 2;
                long[] left = new long[q];
                long[] right = new long[A.length - q];
                System.arraycopy(A, 0, left, 0, q);
                System.arraycopy(A, q, right, 0, A.length - q);
                long[] left_sorted = MergeSort(left);
                long[] right_sorted = MergeSort(right);
                return Merge(left_sorted, right_sorted);
            } else {
                return A;
            }
        }

        static long[] Merge(long[] left, long[] right) {
            long[] A = new long[left.length + right.length];
            int i = 0;
            int j = 0;
            for (int k = 0; k < A.length; k++) {
                // To handle left becoming empty
                if (i == left.length && j < right.length) {
                    A[k] = right[j];
                    j++;
                    continue;
                }
                // To handle right becoming empty
                if (j == right.length && i < left.length) {
                    A[k] = left[i];
                    i++;
                    continue;
                }
                if (left[i] <= right[j]) {
                    A[k] = left[i];
                    i++;
                } else {
                    A[k] = right[j];
                    j++;
                }
            }
            return A;
        }

        static int upper_bound(int[] data, int num, int start) {
            int low = start;
            int high = data.length - 1;
            int mid = 0;
            int ans = -1;
            while (low <= high) {
                mid = (low + high) / 2;
                if (data[mid] < num) {
                    low = mid + 1;
                } else if (data[mid] >= num) {
                    high = mid - 1;
                    ans = mid;
                }
            }
            if (ans == -1) {
                return 100000000;
            }
            return data[ans];
        }

        static int lower_bound(int[] data, int num, int start) {
            int low = start;
            int high = data.length - 1;
            int mid = 0;
            int ans = -1;
            while (low <= high) {
                mid = (low + high) / 2;
                if (data[mid] <= num) {
                    low = mid + 1;
                    ans = mid;
                } else if (data[mid] > num) {
                    high = mid - 1;
                }
            }
            if (ans == -1) {
                return 100000000;
            }
            return data[ans];
        }
    }

    static boolean[] primeSieve(int n) {
        boolean[] primes = new boolean[n + 1];
        Arrays.fill(primes, true);
        primes[0] = false;
        primes[1] = false;
        for (int i = 2; i <= Math.sqrt(n); i++) {
            if (primes[i]) {
                for (int j = i * i; j <= n; j += i) {
                    primes[j] = false;
                }
            }
        }
        return primes;
    }

    // Iterative Version
    static HashMap<Integer, Boolean> subsets_sum_iter(int[] data) {
        HashMap<Integer, Boolean> temp = new HashMap<Integer, Boolean>();
        temp.put(data[0], true);
        for (int i = 1; i < data.length; i++) {
            HashMap<Integer, Boolean> t1 = new HashMap<Integer, Boolean>(temp);
            t1.put(data[i], true);
            for (int j : temp.keySet()) {
                t1.put(j + data[i], true);
            }
            temp = t1;
        }
        return temp;
    }

    static HashMap<Integer, Integer> subsets_sum_count(int[] data) {
        HashMap<Integer, Integer> temp = new HashMap<>();
        temp.put(data[0], 1);
        for (int i = 1; i < data.length; i++) {
            HashMap<Integer, Integer> t1 = new HashMap<>(temp);
            t1.merge(data[i], 1, ADD);
            for (int j : temp.keySet()) {
                t1.merge(j + data[i], temp.get(j) + 1, ADD);
            }
            temp = t1;
        }
        return temp;
    }

    static class Graph {
        ArrayList<Integer>[] g;

        boolean[] visited;

        ArrayList<Integer>[] graph(int n) {
            g = new ArrayList[n];
            visited = new boolean[n];
            for (int i = 0; i < n; i++) {
                g[i] = new ArrayList<>();
            }
            return g;
        }

        void BFS(int s) {
            Queue<Integer> Q = new ArrayDeque<>();
            visited[s] = true;
            Q.add(s);
            while (!Q.isEmpty()) {
                int v = Q.poll();
                for (int a : g[v]) {
                    if (!visited[a]) {
                        visited[a] = true;
                        Q.add(a);
                    }
                }
            }
        }
    }

    static class SparseTable {
        int[] log;
        int[][] st;

        public SparseTable(int n, int k, int[] data, BiFunction<Integer, Integer, Integer> f) {
            log = new int[n + 1];
            st = new int[n][k + 1];
            log[1] = 0;
            for (int i = 2; i <= n; i++) {
                log[i] = log[i / 2] + 1;
            }
            for (int i = 0; i < data.length; i++) {
                st[i][0] = data[i];
            }
            for (int j = 1; j <= k; j++)
                for (int i = 0; i + (1 << j) <= data.length; i++)
                    st[i][j] = f.apply(st[i][j - 1], st[i + (1 << (j - 1))][j - 1]);
        }

        public int query(int L, int R, BiFunction<Integer, Integer, Integer> f) {
            int j = log[R - L + 1];
            return f.apply(st[L][j], st[R - (1 << j) + 1][j]);
        }
    }

    static class InputReader {
        public BufferedReader reader;
        public StringTokenizer tokenizer;

        public InputReader(InputStream stream) {
            reader = new BufferedReader(new InputStreamReader(stream), 2048);
            tokenizer = null;
        }

        public String next() {
            while (tokenizer == null || !tokenizer.hasMoreTokens()) {
                try {
                    tokenizer = new StringTokenizer(reader.readLine());
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
            return tokenizer.nextToken();
        }

        public long nextLong() {
            return Long.parseLong(next());
        }

        public int nextInt() {
            return Integer.parseInt(next());
        }

        public int[] readAllInts(int n) {
            int[] p = new int[n];
            for (int i = 0; i < n; i++) {
                p[i] = in.nextInt();
            }
            return p;
        }

        public int[] readAllInts(int n, int s) {
            int[] p = new int[n + s];
            for (int i = s; i < n + s; i++) {
                p[i] = in.nextInt();
            }
            return p;
        }

        public long[] readAllLongs(int n) {
            long[] p = new long[n];
            for (int i = 0; i < n; i++) {
                p[i] = in.nextLong();
            }
            return p;
        }

        public long[] readAllLongs(int n, int s) {
            long[] p = new long[n + s];
            for (int i = s; i < n + s; i++) {
                p[i] = in.nextLong();
            }
            return p;
        }

        public double nextDouble() {
            return Double.parseDouble(next());
        }
    }

    static void exit(int a) {
        out.close();
        err.close();
        System.exit(a);
    }

    static InputStream inputStream = System.in;
    static OutputStream outputStream = System.out;
    static OutputStream errStream = System.err;
    static InputReader in = new InputReader(inputStream);
    static PrintWriter out = new PrintWriter(outputStream);
    static PrintWriter err = new PrintWriter(errStream);
    static BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

}
