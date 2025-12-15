import java.io.*;
import java.util.*;

public final class Main {
    private static final StringBuilder out = new StringBuilder();

    private static void y() { out.append("YES\n"); }
    private static void n() { out.append("NO\n"); }
    private static void yn(boolean ok) { out.append(ok ? "YES\n" : "NO\n"); }

    private static void pc(char[] a) { out.append(a); }
    private static void pcl(char[] a) { out.append(a).append('\n'); }
    private static void pc(char[] a, int off, int len) { out.append(a, off, len); }
    private static void pcl(char[] a, int off, int len) { out.append(a, off, len).append('\n'); }

    private static final class FastScanner {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0;
        private int len = 0;

        FastScanner(InputStream in) {
            this.in = in;
        }

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
            do {
                c = read();
                if (c == -1) return null;
            } while (c <= 32);
            while (c > 32) {
                sb.append((char) c);
                c = read();
            }
            return sb.toString();
        }

        int nextInt() throws IOException {
            String s = next();
            return s == null ? Integer.MIN_VALUE : Integer.parseInt(s);
        }
    }

    private static void solve(FastScanner fs) throws Exception {
        int t = fs.nextInt();
        for (int tc = 0; tc < t; tc++) {
            char [] s = fs.next().toCharArray();
            char [] tStr = fs.next().toCharArray();
            int start = 0; 
            for(int i=0;i<s.length;i++){
                if(start < tStr.length && (tStr[start]==s[i] || s[i]=='?')){
                    if(s[i] == '?'){
                        s[i] = tStr[start];
                    }
                    start++; 
                }
            }
            for(int i=0;i<s.length;i++){
                if(s[i]=='?') s[i] = 'a';
            }
            if(start == tStr.length){
                y();
                pcl(s);
            }else{
                n();
            }
        }
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        solve(fs);
        System.out.print(out);
    }
}
