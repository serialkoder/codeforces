import java.io.BufferedReader;
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
        var ans = "";
        var total = 0L;
        for(int i= 0;i <n;i++){
            var c = fs.next();
            var l = fs.nextLong();
            total += l;
            if(total <= 100){
                int rep = (int) l;
                ans = ans + c.repeat(rep);
            }
            else{
                ans = "Too Long";
                break;
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
        char nextChar() {return next().charAt(0);};
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