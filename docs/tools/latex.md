数学公式编辑可以使用 Latex

<!--more-->

## 四则运算

- `$a+b$` 显示效果 $ a+b $
- `$a-b$` 显示效果 $ a−b $
- `$a*b$` 显示效果 $a*b$
- `$\frac{a}{b}$` 显示效果 $\frac{a}{b}$

## 幂指对

- `$x^n$` 显示效果 $x^n$
- `$a^x$` 显示效果 $a^x$
- `$\log_a^b$` 显示效果 $\log_a^b$
- `$\ln x$` 显示效果 $\ln x$
  **注意：**

- 上标用`^`，下标用`_`;
- 如果上标或者下表不止一个符号，请用`{}`括起来；

## 根号，省略号，向量，特殊符号

- `$\sqrt x$` 显示效果 $\sqrt x$
- `$\sqrt[n]{x}$` 显示效果 $\sqrt[n]{x}$
- `$\dots$` 显示效果 $\dots$
- `$\vec x$` 显示效果 $\vec x$
- `$\to $` 显示效果 $\to $
- `$\alpha $` 显示效果 $\alpha $
- `$\theta_i $` 显示效果 $\theta_i $
- `$a \geq b $` 显示效果 $a \geq b $
- `$a \leq b $` 显示效果 $a \leq b $

**注意：**键盘不能直接输入的符号，用`\英文单词`

## 累加，累乘

- `$\sum_{i=1}^{n} a_i^2x_i$` 显示效果 $\sum_{i=1}^{n} a_i^2x_i$
- `$\displaystyle\sum_{i=1}^{n} a_i^2x_i$` 显示效果 $\displaystyle\sum_{i=1}^{n} a_i^2x_i$
- `$\prod_{i=1}^{n} a_i^2x_i$` 显示效果 $\prod_{i=1}^{n} a_i^2x_i$
- `$\displaystyle\prod_{i=1}^{n} a_i^2x_i$` 显示效果 $\displaystyle\prod_{i=1}^{n} a_i^2x_i$

## 表格

在 MathJax 中插入表格需要`$$\begin{array}{列格式}…\end{array}$$`，在`\begin{array}`后需要表明每列的格式：c 表示居中；l 表示左对齐；r 表示右对齐；|表示列分割线。每一行末用`\\`结束，用&分隔矩阵元素。用`\hline`表示行分割线。

```
$$
\begin{array}{c|lcr}
n & \text{Left} & \text{Center} & \text{Right} \\
\hline
1 & 0.24 & 1 & 125 \\
2 & -1 & 189 & -8 \\
3 & -20 & 2000 & 1+10i
\end{array}
$$
```

<div class='hasJax'>
$$
\begin{array}{c|lcr}
n & \text{Left} & \text{Center} & \text{Right} \\
\hline
1 & 0.24 & 1 & 125 \\
2 & -1 & 189 & -8 \\
3 & -20 & 2000 & 1+10i
\end{array}
$$
</div>

## 矩阵

- `$\begin{matrix} 1&2&3\\ 4&5&6\end{matrix}$` 显示效果 $\begin{matrix} 1&2&3\\\\  4&5&6\end{matrix}$
- `$\begin{bmatrix} 1&2&3\\ 4&5&6\end{bmatrix}$` 显示效果 $\begin{bmatrix} 1&2&3\\\\  4&5&6\end{bmatrix}$
- `$\begin{pmatrix} 1&2&3\\ 4&5&6\end{pmatrix}$` 显示效果 $\begin{pmatrix} 1&2&3\\\\  4&5&6\end{pmatrix}$
- `$\begin{bmatrix} 1&&\\ &1&\\&&1\end{bmatrix}$` 显示效果 $\begin{bmatrix} 1&&\\\\  &1&\\\\ &&1\end{bmatrix}$

### 矩阵带省略项

```
$$
  \begin{pmatrix}
  1 & a_1 & a_1^2 & \cdots & a_1^n\\
  1 & a_2 & a_2^2 & \cdots & a_2^n \\
  \vdots & \vdots & \ddots & \vdots \\
  1 & a_n & a_n^2 & \cdots & a_n^n  \\
  \end{pmatrix}
$$
```

<div class='hasJax'>
$$
  \begin{pmatrix}
  1 & a_1 & a_1^2 & \cdots & a_1^n\\
  1 & a_2 & a_2^2 & \cdots & a_2^n \\
  \vdots & \vdots & \ddots & \vdots \\
  1 & a_n & a_n^2 & \cdots & a_n^n  \\
  \end{pmatrix}
$$
</div>
### 增广矩阵

```
$$ \left[
    \begin{array}{cc|c}
      1&2&3\\
      4&5&6
    \end{array}
\right] $$
```

<div class='hasJax'>
$$ \left[
    \begin{array}{cc|c}
      1&2&3\\
      4&5&6
    \end{array}
\right] $$
</div>
## 公式中更改颜色

- `$\displaystyle\sum_{i=1}^{n}\color{red}{a_i^2}x_i$` 显示效果 $\displaystyle\sum_{i=1}^{n}\color{red}{a_i^2}x_i$

## 希腊字母

- `$\alpha$` 显示 $\alpha$
- `$A$` 显示 $A$
  其余类推 $\dots$

## 多行公式

### 分情况表达式

```
$$
f(n) =
\begin{cases}
n/2,  & \text{if $n$ is even} \\
3n+1, & \text{if $n$ is odd}
\end{cases}
$$
```

<div class='hasJax'>
$$
f(n) =
\begin{cases}
n/2,  & \text{if $n$ is even} \\[2ex]
3n+1, & \text{if $n$ is odd}
\end{cases}
$$
</div>

### 递推公式

```
$$
\begin {split}
y &= (a + b)^2 \\
  &= a^2 + b^2 + 2ab \\
  &= 0
\end {split}
$$
```

<div class='hasJax'>
$$
\begin {split}
y &= (a + b)^2 \\
  &= a^2 + b^2 + 2ab \\
  &= 0
\end {split}
$$
