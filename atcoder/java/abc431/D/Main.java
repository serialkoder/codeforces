import java.io.*;
import java.util.*;

public final class Main {
    private static final FastScanner in = new FastScanner(System.in);
    private static final PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));

    private static void y() { out.println("YES"); }
    private static void n() { out.println("NO"); }
    private static void yn(boolean ok) { out.println(ok ? "YES" : "NO"); }
    private static void fail() { out.println(-1); }

    public static void main(String[] args) throws Exception {
        solve();
        out.flush();
    }

    private static void solve() throws Exception {
        int n = in.nextInt();
        int [] w = new int[n];
        int [] h = new int[n];
        int [] b = new int[n];
        int total = 0;
        long baseHappiness = 0;
        for(int i = 0;i <n;i++){
            w[i] = in.nextInt();
            h[i] = in.nextInt();
            b[i] = in.nextInt();
            total += w[i];
            baseHappiness += b[i];
        }        
        int threshold = total/2;
        long [] dp = new long[threshold+1];
        for(int i=0;i<n;i++){
            int wi = w[i];
            long vi = h[i]-b[i];
            for(int c= threshold;c>=wi;c--){
                dp[c] = Math.max(dp[c],dp[c-wi] + vi);
            }
        }
        out.println(dp[threshold]+baseHappiness);
    }

    private static final class FastScanner {
        private final InputStream inputStream;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;

        FastScanner(InputStream inputStream) {
            this.inputStream = inputStream;
        }

        private int readByte() throws IOException {
            if (ptr >= len) {
                len = inputStream.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }

        String next() throws IOException {
            StringBuilder sb = new StringBuilder();
            int c;
            while ((c = readByte()) <= 32 && c != -1) {}
            while (c > 32) {
                sb.append((char) c);
                c = readByte();
            }
            return sb.toString();
        }

        int nextInt() throws IOException { return Integer.parseInt(next()); }
        long nextLong() throws IOException { return Long.parseLong(next()); }
        double nextDouble() throws IOException { return Double.parseDouble(next()); }

        int[] readIntArray(int n) throws IOException {
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = nextInt();
            return a;
        }

        long[] readLongArray(int n) throws IOException {
            long[] a = new long[n];
            for (int i = 0; i < n; i++) a[i] = nextLong();
            return a;
        }
    }
}
