# 最长递增序列（LIS）

最长连续递增序列

# 最长公共子序列（LCS）

[LeetCode 1143. Longest Common Subsequence (medium)](https://github.com/muyids/leetcode/blob/master/algorithms/1101-1200/1143.longest-common-subsequence.md)

最长公共子序列

```cpp
class Solution {
public:
    int longestCommonSubsequence(string s, string t) {
        vector<vector<int>> dp(s.size()+1, vector<int>(t.size()+1, 0));
        int ans = 0;
        for (int i = 1; i< dp.size(); i++){
            for (int j = 1; j < dp[0].size(); j++){
                if (s[i-1] == t[j-1]) {
                    dp[i][j] = dp[i-1][j-1] + 1;
                    ans = max(ans, dp[i][j]);
                } else {
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
                }
            }
        }
        return ans;
    }
};
```

最长公共子串

```cpp
class Solution {
public:
    int findLength(string s, string t) {
        vector<vector<int>> dp(s.size()+1, vector<int>(t.size()+1, 0));
        int ans = 0;
        for (int i = 1; i < dp.size(); i++){
            for (int j = 1; j < dp[0].size(); j++){
                if (s[i-1] == t[j-1]) {
                    dp[i][j] = dp[i-1][j-1] + 1;
                    ans = max(ans, dp[i][j]);
                }
            }
        }
        return ans;
    }
};
```
