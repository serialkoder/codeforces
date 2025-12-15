/*  File:  sum_unique_squares.c
    Build & run (mac / Linux):
        gcc -std=c17 -O2 -Wall -Wextra -o sum_unique_squares sum_unique_squares.c
        ./sum_unique_squares
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define N 100          /* array size              */
#define K 50           /* subset size             */
#define SIGMA 338350   /* sum(1^2 … 100^2)        */

/* handy macro to map 2-D (size,sum) -> flat index */
#define IDX(size, sum) ((size) * (SIGMA + 1) + (sum))

int main(void)
{
    /* 1. Build squares 1² … 100² */
    int nums[N];
    for (int i = 1; i <= N; ++i) nums[i - 1] = i * i;

    /* 2. Allocate DP table: (K+1) × (SIGMA+1) bytes, init-zero */
    size_t rows = K + 1, cols = SIGMA + 1;
    uint8_t *dp = calloc(rows * cols, sizeof(uint8_t));
    if (!dp) { perror("calloc"); return 1; }
    dp[IDX(0, 0)] = 1;                 /* empty subset */

    /* 3. Dynamic-programming update (0/1/2 clipped counts) */
    for (int idx = 0; idx < N; ++idx) {
        int x = nums[idx];
        for (int size = K - 1; size >= 0; --size) {
            for (int s = SIGMA - x; s >= 0; --s) {
                uint8_t ways = dp[IDX(size, s)];
                if (!ways) continue;
                int newSize = size + 1;
                int newSum  = s + x;
                uint8_t merged = dp[IDX(newSize, newSum)] + ways;
                dp[IDX(newSize, newSum)] = merged >= 2 ? 2 : merged;
            }
        }
    }

    /* 4. Aggregate unique sums */
    uint64_t uniqueCount = 0;
    uint64_t total       = 0;          /* fits in 64-bit: 338 350² ≈ 1.15e11 */
    for (int s = 0; s <= SIGMA; ++s) {
        if (dp[IDX(K, s)] == 1) {
            ++uniqueCount;
            total += (uint64_t)s;
        }
    }

    printf("Unique %u-subset sums: %llu\n", K, (unsigned long long)uniqueCount);
    printf("Sum of those unique sums: %llu\n", (unsigned long long)total);

    free(dp);
    return 0;
}
