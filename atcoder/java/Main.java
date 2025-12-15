import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.*;

/**
 * Skeleton for most competitive-programming problems.
 *   • Fast input via BufferedReader + StringTokenizer
 *   • Fast output via PrintWriter (auto-flush off)
 *
 * Usage:
 *   int n   = fs.nextInt();
 *   long x  = fs.nextLong();
 *   String s= fs.next();
 */
public class Main {
    private static final FastScanner fs = new FastScanner();
    private static final PrintWriter  out = new PrintWriter(System.out);

    public static void main(String[] args) throws Exception {
        int n = fs.nextInt();          // sample read
        int l = fs.nextInt();
        int r = fs.nextInt();
        int ans = 0 ;
        for(int i=0;i<n;i++){
            int x = fs.nextInt();
            int y = fs.nextInt();
            if (x>=l && y<=r){
                ans++; 
            }
        }
        out.println(ans);     
        out.flush();                   // remember to flush!
    }




    // ---------- fast I/O ----------
    private static final class FastScanner {
        private final BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        private StringTokenizer st = new StringTokenizer("");

        /** Returns next token (word/number). */
        String next() {
            try {
                while (!st.hasMoreTokens()) st = new StringTokenizer(br.readLine());
            } catch (Exception e) {
                return null;           // EOF
            }
            return st.nextToken();
        }
        int    nextInt()    { return Integer.parseInt(next()); }
        long   nextLong()   { return Long.parseLong(next()); }
        double nextDouble() { return Double.parseDouble(next()); }
        /* Reads n integers and returns them as an int[] */
        static int[] readIntArray(int n) {
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = fs.nextInt();
            return a;
        }

    }
}
