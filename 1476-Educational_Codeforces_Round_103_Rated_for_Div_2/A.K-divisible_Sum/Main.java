// Contest: 1476  Problem: A - K-divisible Sum
// URL: https://codeforces.com/contest/1476/problem/A
import java.io.*;
import java.util.*;

public final class Main {
    private static final class FS {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;
        FS(InputStream is) { in = is; }
        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }
        String next() throws IOException {
            StringBuilder sb = new StringBuilder();
            int c;
            while ((c = read()) <= 32 && c != -1) {}
            while (c > 32) { sb.append((char)c); c = read(); }
            return sb.toString();
        }
        int nextInt() throws IOException { return Integer.parseInt(next()); }
        long nextLong() throws IOException { return Long.parseLong(next()); }
    }

    public static void main(String[] args) throws Exception {
        FS fs = new FS(System.in);
        PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));
        // int t = Integer.parseInt(fs.next()); // uncomment for multi-case
        // while (t-- > 0) {
        //     int n = fs.nextInt();
        //     // long[] a = new long[n];
        //     // for (int i = 0; i < n; i++) a[i] = fs.nextLong();
        //     // TODO: solve
        //     // out.println(ans);
        // }
        out.flush();
    }
}
