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
    private static final FastScanner in = new FastScanner();
    private static final PrintWriter  out = new PrintWriter(System.out);

    record State(int sum,int min){}

    public static void main(String[] args) throws Exception {
        int q = in.nextInt();
        Stack<State> S = new Stack<>();
        
        for(int i=0;i<q;i++){
            int n = in.nextInt();
            String s = "";
            if(n==1){
                s = in.next();    
                int add = (s.equals("(")) ? 1 : -1 ;
                int prevSum = S.isEmpty() ? 0 : S.peek().sum;
                int prevMin = S.isEmpty() ? 0 : S.peek().min;     
                int curSum = prevSum+ add;
                int curMin = Math.min(prevMin,curSum);
                S.push(new State(curSum,curMin));
            }else{
                S.pop();
            }
            if(S.isEmpty()){
                out.println("Yes");
            }else{
                if(S.peek().sum==0 && S.peek().min==0){
                    out.println("Yes");
                }else{
                    out.println("No");
                }
            }

        }
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
            for (int i = 0; i < n; i++) a[i] = in.nextInt();
            return a;
        }

    }
}
