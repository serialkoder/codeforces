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
        long n = fs.nextLong();          // sample read
        long ans = generate(n,a);
        out.println(ans);     
        out.flush();                   // remember to flush!
    }

    public static String toBase(long num, int base) {
            return Long.toString(num, base); // Uppercase for A-F in bases > 10
    }

    public static boolean isPalindrome(String s) {
        if (s == null || s.isEmpty()) {
            return false; // Handle null or empty strings
        }
        int left = 0;
        int right = s.length() - 1;
        while (left < right) {
            if (s.charAt(left) != s.charAt(right)) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }


/** Sum of all base-10 palindromes ≤ limit whose representation in the given radix is also a palindrome. */
    public static long generate(long limit, int base) {
        if (limit < 1) return 0;
        long sum = 0;
        int maxDigits = Long.toString(limit).length();

        outer:
        for (int len = 1; len <= maxDigits; len++) {
            boolean odd = (len & 1) == 1;
            int halfLen = (len + 1) / 2;
            long start = pow10(halfLen - 1);
            long end = pow10(halfLen) - 1;

            for (long half = start; half <= end; half++) {
                long pal = odd ? buildOddPalindrome(half)
                               : buildEvenPalindrome(half);
                if (pal > limit) break outer;
                if (isPalindrome(toBase(pal, base))) sum += pal;
            }
        }
        return sum;
    }

    private static long buildOddPalindrome(long half)  { return appendReverse(half, half / 10); }
    private static long buildEvenPalindrome(long half) { return appendReverse(half, half); }

    private static long appendReverse(long prefix, long number) {
        long pal = prefix;
        while (number != 0) {
            pal = pal * 10 + (number % 10);
            number /= 10;
        }
        return pal;
    }

    private static long pow10(int exp) { long p = 1; while (exp-- > 0) p *= 10; return p; }





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
