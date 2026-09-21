# Lab2

## Bug Fix

原始程式在切換圖片時直接對 `current_index` 加 1 或減 1，
當 index 超出 `images` 的範圍時會發生 `IndexError`。

修正方式：
使用 modulo (`%`) 將 index 限制在圖片數量範圍內。

```python
current_index = (current_index + 1) % len(images)
current_index = (current_index - 1) % len(images)
