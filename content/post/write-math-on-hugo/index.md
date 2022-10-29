---
title: "如何在 Hugo 內嵌 Latex 數學式"
description: ""
date: 2021-01-17T21:55:43+08:00
categories:
-   Hugo
draft: false
image: "cubes.jpg"
author: "謝宗晅"
---

這篇文章要分享如何在 Hugo 的網頁裡面內嵌 Latex 數學式，以及如何解決 Hugo 內建的 Markdown renderer 會無差別的將 `\` 轉義掉的問題。

### 使用 Katex 來 render Latex 數學式

這個部份是參考我使用的 Hugo 模板的[說明](https://theme-stack.jimmycai.com/p/math-typesetting/)，如果你的模板有自己的方式，那就請參考你的模板的方式。

我先在模板的 header 中能加上關於數學 parameter 的模板，下面這段的意思是如果這篇文章的 front matter 有將 `math` 的參數設為 `true`，或是在 `config.toml` 裡面的 `params.math` 是 `true` 的話，就會將 `partial/math.html` 放到 header 裡面。（`.Params.math` 是 front matter 的部份，`.Site.Params.math` 是 `config.toml` 裡面的變數）
```HTML
<!-- layouts/partials/head/custom.html -->
{{ if or .Params.math .Site.Params.math }}
{{ partial "math.html" . }}
{{ end }}
```
所以我們必須建立一個新的檔案，`layouts/partials/math.html`，並且裡面必須包含 Latex renderer，在這邊我是使用 Katex 來作為我的 Latex renderer，可以參考 [Katex 官網](https://katex.org/docs/autorender.html) 的詳細說明：
```HTML
<!-- layouts/partials/math.html -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css" integrity="sha384-AfEj0r4/OFrOo5t7NnNe46zW/tFgW6x/bCJG8FqQCEo3+Aro6EYUG4+cU+KJWu/X" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js" integrity="sha384-g7c+Jr9ZivxKLnZTDUhnkOnsh30B4H0rpLUpJ4jAIKs4fnJI+sEnkvrMWph2EDg4" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/contrib/auto-render.min.js" integrity="sha384-mll67QQFJfxn0IYznZYonOWZ644AWYC+Pt2cHqMaRhXVrursRwvLnLaebdGIlYNa" crossorigin="anonymous"
    onload="renderMathInElement(document.body);"></script>
```
但依照上面這個語法，是沒有辦法 render 以單一個 `$` 括起來的 inline 數學式，因此必須調整成下列的樣子才能有這樣的功能（以下的也是參考 [Katex 官網](https://katex.org/docs/autorender.html)）：
```HTML
<!-- layouts/partials/math.html -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.css" integrity="sha384-AfEj0r4/OFrOo5t7NnNe46zW/tFgW6x/bCJG8FqQCEo3+Aro6EYUG4+cU+KJWu/X" crossorigin="anonymous">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/katex.min.js" integrity="sha384-g7c+Jr9ZivxKLnZTDUhnkOnsh30B4H0rpLUpJ4jAIKs4fnJI+sEnkvrMWph2EDg4" crossorigin="anonymous"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.12.0/dist/contrib/auto-render.min.js" integrity="sha384-mll67QQFJfxn0IYznZYonOWZ644AWYC+Pt2cHqMaRhXVrursRwvLnLaebdGIlYNa" crossorigin="anonymous"></script>
<script>
    document.addEventListener("DOMContentLoaded", function() {
        renderMathInElement(document.body, {
            delimiters: [
                {left: "$$", right: "$$", display: true},
                {left: "$", right: "$", display: false},
                {left: "\\(", right: "\\)", display: false},
                {left: "\\[", right: "\\]", display: true}
            ]
        });
    });
</script>
```
可以看到我們傳入了特殊的 delimiters 來達成我們的目標。最後，可以依照個人的需求，直接在 `config.toml` 加入以下的設定（這樣就能使得每一篇文章都有 Katex 的 renderer）：
```toml
...
[params]
    math = true
...
```
或是如果不想要讓每一篇文章都有 Latex renderer 的話，就必須在有數學式的文章的 front matter 中（front matter 就是設定 title 等等的區塊），加入 `math = true` 的設定，就可以在 Markdown 中內嵌 Latex 數學式了！

### 解決反斜線的轉義問題

因為 Hugo 官方所採用的 Markdown renderer 會將 `\` 後面不是接字母的東西全部轉義（例如後面如果是換行的話就是強制換行），如果想要打出真正的反斜線的話，就必須打在程式區塊裡面（像是我這一句話一樣），不然就要用兩個反斜線 `\\` 才能做出一個真正的反斜線。但是問題在於，Latex 裡面所需的東西就會使用到 `\` 後面不是接字母的，例如 Norm {{< math >}}$\|\cdot\|${{< /math >}} 就是由 `\|` 變成的，以及換行 `\\`，只打兩個反斜線就不會換行（因為被轉義成只有一個反斜線了），這對寫文章來說是非常麻煩的一件事，會造成我在 Markdown 編輯器裡面看到的東西跟網頁上面的東西完全不一樣，由於如果要打出 `\\` 的話就必須要用雙倍的反斜線，`\\\\` 來表示。而且還不止於此，連用 `_` 的東西都會被當作是斜體的功能（Markdown 中使用 `_` 將一段文字括起來的話就是斜體），`*` 也是和 `_` 有一樣的功能，所以必須使用特殊的方法來避免掉他們的轉義。

#### 第一步：建立 Shortcode

在 Hugo 中，有一個 Shortcode 的功能，是讓我們在 Markdown 中，使用特殊的模板語法就可以為我們達到非常便利的事情。如果想要直接看官網的詳細說明的話可以點[這裡](https://gohugo.io/content-management/shortcodes/)，我使用的是方法是自己新增一個 Shortcode 來避免掉 Markdown renderer 的轉義，因為在 Markdown 的 render 之前，會先將所有 Shortcode 都處理過之後才去 render。

建立一個新的 Shortcode 要在 `layouts/shortcodes` 裡面新增檔案，我將我的 Shortcode 命名為 `math`，所以我必須建立一個叫作 `layouts/shortcodes/math.html` 的檔案，和上方的 `math.html` 的位置不一樣哦：
```HTML
<!-- layouts/shortcodes/math.html -->
{{ .Inner }}
```
這個 Shortcode 做的事情就是將被「括起來的內容」原封不動的輸出，有幾個反斜線就輸出幾個反斜線，不用擔心被 render 掉。做到這裡其實就已經可以算是解決了一半的問題了，因為只要在每一個 `$$` 的前後都加上 Shortcode 的語法，就能避免掉被括起來的內容慘遭 render 這件事：
```
{{< math >}}$anything you want\${{< /math >}}
```
以上的這個 block 其實是這樣寫的
```
{{</* math */>}}$anything you want\${{</* /math */>}}
```
可以發現到只要打一個反斜線就能實際製造出一個反斜線。

但是這樣每次寫一個數學式就要打那麼長的東西有有點麻煩，所以就有了第二步。

#### 第二步：寫一個 Python 腳本

我寫了一個很簡陋的版本，但應該比原本那樣要每一個數學式都加上前後括號還要好一點。我寫的 Python 腳本邏輯沒有很複雜，最麻煩的主要是將本來的資料夾結構改成新的資料夾結構，所幸目前的文章數還沒有很多，所以可以很快的就改好了（雖然如果文章數很多的話也是可以寫個腳本來做就是了）：
```
// old structure
content
└── post
    └── post_name
        ├── index.md
        └── other_things

// new structure
content
└── post
    └── post_name
        ├── raw
        │   ├── other_things
        │   └── index.md
        ├── index.md
        └── other_things
```
這樣一來就能不被當作是一個頁面，也能存放在同一個資料夾裡面。在編輯的時候就在 raw 資料夾裡面編輯，寫完了再用這個腳本在 `$` 前後都加上 Shortcode 的語法。

還剩下最後一個問題就是在文章裡面所引用的其他資料，例如圖片等等的，也需要同步被搬移，因此就需要再寫另一個腳本來做這件事。

最後附上我寫的腳本們，因為有點長所以就不貼在這裡了：

（我使用文字檔，避免直接下載檔案造成的驚悚不安感，歡迎複製使用以及回報 bug 甚至改進空間，我自以為使用方法應該寫的算...清楚了）

* [preprocessing_markdown.py](/codes/write-math-on-hugo/preprocessing_markdown.txt)
* [preprocessing_copy_files](/codes/write-math-on-hugo/preprocessing_copy_files.txt)
