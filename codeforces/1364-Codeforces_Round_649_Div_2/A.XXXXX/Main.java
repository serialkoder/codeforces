// Contest: 1364  Problem: A - XXXXX
// URL: https://codeforces.com/contest/1364/problem/A
import java.io.*;
import java.util.*;

public final class Main {
    private static final PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(System.out)));

    private static void y() { out.println("YES"); }
    private static void n() { out.println("NO"); }
    private static void yn(boolean ok) { out.println(ok ? "YES" : "NO"); }

    private static void pc(char[] a) { out.print(a); }
    private static void pcl(char[] a) { out.print(a); out.println(); }
    private static void pc(char[] a, int off, int len) { out.write(a, off, len); }
    private static void pcl(char[] a, int off, int len) { out.write(a, off, len); out.println(); }

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
        int[] readInts(int n) throws IOException {
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = nextInt();
            return a;
        }
    }

    public static void main(String[] args) throws Exception {
        FS in = new FS(System.in);
        int t = in.nextInt(); // uncomment for multi-case
        while (t-- > 0) {
            int n = in.nextInt();
            int x = in.nextInt();
            int [] data = in.readInts(n);
            long [] pref = new long [n+1];
            long sum = 0;
            int best = -1;
            for (int i = 0; i < n; i++){
              pref[i+1] = pref[i] + data[i];
              sum += data[i];
            } 
            if (sum % x != 0) {
                best = n;
            }
            else{
                for(int i = 0; i< n;i++){
                        long prefixSum = pref[i];
                        long suffixSum = sum - pref[i+1];
                        if (prefixSum%x != 0 ) best = Math.max(best,i);
                        if (suffixSum%x != 0 ) best = Math.max(best,n-i-1);
                }
            }
            out.println(best);
        }
        out.flush();
    }
}
