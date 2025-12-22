import java.io.*;
import java.util.*;

public final class Main {
    private static final FastScanner in = new FastScanner(System.in);
    private static final PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));

    private static void y() { out.println("YES"); }
    private static void n() { out.println("NO"); }
    private static void yn(boolean ok) { out.println(ok ? "YES" : "NO"); }
    private static void fail() { out.println(-1); }

    private static void reverse(int[] a) {
        for (int i = 0, j = a.length - 1; i < j; i++, j--) {
            int t = a[i];
            a[i] = a[j];
            a[j] = t;
        }
    }

    private static void reverse(long[] a) {
        for (int i = 0, j = a.length - 1; i < j; i++, j--) {
            long t = a[i];
            a[i] = a[j];
            a[j] = t;
        }
    }

    public static void main(String[] args) throws Exception {
        solve();
        out.flush();
    }

    private static void solve() throws Exception {
        // int n = in.nextInt();
        // long x = in.nextLong();
        // String s = in.next();
        //
        // TODO: solve
        // out.println(answer);
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
