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
        int a = fs.nextInt();
        int b = fs.nextInt();   
        int c = fs.nextInt();        
        int [] counts = new int[11];
        counts[a]++;

        counts[b]++;
        counts[c]++;

        if(counts[5]==2 && counts[7]==1){
            out.println("YES");
        }else{
            out.println("NO");
        }
        out.flush();                   // remember to flush!
    }

    static class SimpleHashSet{
        int size = 0 ;
        int P = 31;
        long MOD = 0x7FFFFFFFL;
        int buckets = 1000;
        @SuppressWarnings("unchecked")
        ArrayList<String>[] values = (ArrayList<String>[]) new ArrayList[1000];
        void put(String s){
            int code = hashCode(s);
            int index = Math.floorMod(code,buckets);
            if(values[index] == null ){
                values[index] = new ArrayList<String>();
                values[index].add(s);
                size++;
            }else{
                for(String ss:values[index]){
                    if(ss.equals(s)){
                        return;
                    }
                }
                values[index].add(s);
                size++;
            }
        }
        int hashCode(String s){
            long code = 0;
            long pow = 1;
            for(int i=0;i<s.length();i++){
                code = (code + (s.charAt(i)*pow))%MOD;
                pow = (pow*P)%MOD;
            }
            return (int) code;
        }
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
