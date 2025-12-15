// File: SumOfUniqueSubsetSums.java
// Compile:  javac --release 21 SumOfUniqueSubsetSums.java
// Run:      java  SumOfUniqueSubsetSums
//
//  n  ≤ 100,  a[i] ≤ 10 000  ⇒  Σ ≤ 338 350
//  Time   O(n · k · Σ)
//  Memory O((k+1) · (Σ+1))  bytes   (≈ 51 MB for k = 50)

import java.util.*;
import java.math.BigInteger;
import static java.lang.System.out;

public final class UniqueSquaresSubsetSums {

    /*───────────────────────────────────────────────────────────────────────*/
    /** Returns a boolean/tri-state table dp[k][sum] clipped at 2.
     *  dp[k][s] == 0 → no k-subset hits s
     *  dp[k][s] == 1 → exactly one k-subset hits s
     *  dp[k][s] == 2 → two + k-subsets hit s
     */
    private static byte[][] buildClippedDP(int[] nums, int k, int sigma) {
        byte[][] dp = new byte[k + 1][sigma + 1];
        dp[0][0] = 1;                                        // empty subset

        for (int x : nums) {
            for (int size = Math.min(k - 1, nums.length); size >= 0; --size) {
                for (int s = sigma - x; s >= 0; --s) {
                    byte ways = dp[size][s];
                    if (ways == 0) continue;
                    int newSize = size + 1, newSum = s + x;
                    int merged = dp[newSize][newSum] + ways;
                    dp[newSize][newSum] = (byte) (merged >= 2 ? 2 : merged);
                }
            }
        }
        return dp;
    }

    /*───────────────────────────────────────────────────────────────────────*/
    public static void main(String[] args) {
        /* 1.  Build the squares array  */
        final int n = 100, k = 50;
        int[] squares = new int[n];
        for (int i = 1; i <= n; ++i) squares[i - 1] = i * i;
        final int sigma = Arrays.stream(squares).sum();      // 338 350

        /* 2.  DP to classify counts  */
        byte[][] dp = buildClippedDP(squares, k, sigma);

        /* 3.  Aggregate the unique sums  */
        BigInteger total = BigInteger.ZERO;
        long uniqueCount = 0;
        for (int s = 0; s <= sigma; ++s) {
            if (dp[k][s] == 1) {
                total = total.add(BigInteger.valueOf(s));
                ++uniqueCount;
            }
        }
        System.out.println(total);
    }
}
