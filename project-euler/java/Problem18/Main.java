import lombok.Builder;

import java.io.*;
import java.util.*;
import java.util.function.BiFunction;
import java.util.function.Function;

public class Main {

  static BiFunction<Integer, Integer, Integer> ADD = (x, y) -> (x + y);
  static BiFunction<ArrayList<Integer>, ArrayList<Integer>, ArrayList<Integer>> ADD_ARRAY_LIST =
      (x, y) -> {
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
    ArrayList<Integer>[] data = new ArrayList[15];
    ArrayList<Node>[] listOfNodes = new ArrayList[15];
    int[][] weights = new int[15][15];
    List<Node> nodes = new ArrayList<>();
    List<Edge> edges = new ArrayList<>();
    for (int i = 0, k = 1; i < 15; i++) {
      data[i] = new ArrayList<>();
      listOfNodes[i] = new ArrayList<>();
      for (int j = 0; j <= i; j++, k++) {
        int v = in.nextInt();
        data[i].add(v);
        Node cur =
            Node.builder()
                .color("\"#6495ED\"")
                .label(Integer.toString(k))
                .weight(-v)
                .adj(new ArrayList<>())
                .build();
        listOfNodes[i].add(cur);
        nodes.add(cur);
      }
    }

    for (int i = 0; i < 14; i++) {
      for (int j = 0; j <= i; j++) {
        listOfNodes[i].get(j).adj.add(listOfNodes[i + 1].get(j));
        listOfNodes[i].get(j).adj.add(listOfNodes[i + 1].get(j + 1));
      }
    }
    for (int i = 0; i < 14; i++) {
      for (int j = 0; j <= i; j++) {
        edges.add(
            Edge.builder()
                .from(listOfNodes[i].get(j))
                .to(listOfNodes[i + 1].get(j))
                .color("blue")
                .penwidth(2)
                .label((listOfNodes[i].get(j).weight + listOfNodes[i + 1].get(j).weight) + "")
                .build());
        edges.add(
            Edge.builder()
                .from(listOfNodes[i].get(j))
                .to(listOfNodes[i + 1].get(j + 1))
                .color("blue")
                .penwidth(2)
                .label((listOfNodes[i].get(j).weight + listOfNodes[i + 1].get(j + 1).weight) + "")
                .build());
      }
    }
    DiGraph diGraph = new DiGraph(nodes, edges);
    PriorityQueue<Node> Q = new PriorityQueue<>(Comparator.comparing(Node::getDist).reversed());
    int count = 0;
    for (Node n : nodes) {
      n.dist = Integer.MAX_VALUE;
      Q.add(n);
    }
    nodes.get(0).dist = 0;
    Q.remove(nodes.get(0));
    Q.add(nodes.get(0));
    while (!Q.isEmpty()) {
      Node u = Q.poll();

      for (Node v : u.adj) {
        int temp = u.dist + u.weight + v.weight;
        if (temp < v.dist) {
          v.dist = temp;
          v.prev = u;
          Q.remove(v);
          Q.add(v);
          //          update(u, v, diGraph, "red", 5);
          //          update(v, u, diGraph, "red", 5);
          //          writeToFile(diGraph, count++);
        }
      }
    }
    for (Node x : listOfNodes[14]) {
      if (x.prev != null) {
        out.println(x + " " + x.dist);
      }
    }
  }

  static void writeToFile(DiGraph diGraph, int count) {
    try {
      String file = "/Users/serialcoder/Projects/Dijkstra/" + count;
      String img = "/Users/serialcoder/Projects/Dijkstra/" + count + ".png";
      BufferedWriter bf = new BufferedWriter(new FileWriter(file));
      bf.write(diGraph.toString());
      bf.close();
      String cmd = "/usr/local/bin/dot -Tpng " + file + " -o " + img;
      Runtime run = Runtime.getRuntime();
      Process pr = run.exec(cmd);
    } catch (Exception e) {

    }
  }

  static void update(Node from, Node to, DiGraph diGraph, String color, int pen) {
    for (Edge e : diGraph.edges) {
      if (e.from == from && e.to == to) {
        e.color = color;
        e.penwidth = pen;
      }
    }
  }

  @Builder
  static class Edge {
    Node from;
    Node to;
    String color;
    int penwidth;
    String label;

    @Override
    public String toString() {
      return String.format(
          "%s -> %s [label=%s,weight=%d,color=%s,penwidth=%d];\n",
          this.from.label,
          this.to.label,
          this.label,
          Integer.parseInt(this.label),
          this.color,
          this.penwidth);
    }
  }

  @Builder
  static class Node {
    String label;
    String color;
    int weight;
    int dist;
    ArrayList<Node> adj;
    Node prev;

    public int getDist() {
      return dist;
    }

    @Override
    public boolean equals(Object o) {
      if (this == o) return true;
      if (o == null || getClass() != o.getClass()) return false;
      Node node = (Node) o;
      return Objects.equals(label, node.label);
    }

    @Override
    public int hashCode() {
      return Objects.hash(label);
    }

    @Override
    public String toString() {
      return String.format("%s [fillcolor=%s];\n", this.label, this.color);
    }
  }

  static class DiGraph {
    List<Node> vertices;
    List<Edge> edges;

    public DiGraph(List<Node> vertices, List<Edge> edges) {
      this.vertices = vertices;
      this.edges = edges;
    }

    @Override
    public String toString() {
      StringBuilder res = new StringBuilder();
      res.append("digraph{\n");
      res.append(" node [style=filled];\n");
      for (Node n : vertices) {
        res.append(n.toString());
      }
      for (Edge n : edges) {
        res.append(n.toString());
      }
      res.append("}");
      return res.toString();
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

  static InputStream inputStream;

  static {
    try {
      inputStream = new FileInputStream("input");
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    }
  }

  static OutputStream outputStream;

  static {
    try {
      outputStream = new FileOutputStream("output");
    } catch (FileNotFoundException e) {
      e.printStackTrace();
    }
  }

  static OutputStream errStream = System.err;
  static InputReader in = new InputReader(inputStream);
  static PrintWriter out = new PrintWriter(outputStream);
  static PrintWriter err = new PrintWriter(errStream);
  static BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
}
