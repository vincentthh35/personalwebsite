---
title: "在 Hugo 中使用翻譯功能"
description: ""
slug: "use-translation-in-hugo"
date: 2022-10-29T17:08:10+08:00
categories:
-   Hugo
draft: false
image: "translation.jpg"
author: "謝宗晅"
---

### 消失的字

在架設這個 blog 的時候一直有一個困擾我的地方，是在 theme 某一次更新之後我發現 theme 裡面某些字會不見（例如左下角的 Dark Mode），然後找了一下我自己 theme 的 code 才發現那些消失的字都是被以下的 template 語法包起來：
```
{{ T "disappearing_words" }}
```

這件事是在某一次更新 theme 之後才發生的，於是我就去找了一下 github 看看有沒有人有一樣的 issue，結果沒有，我想應該是我做了什麼不對的事情，但我又一直找不出原因，所以最後的 work-around 是直接把字硬寫在 template 裡面。一直到前陣子我下定決心要來好好整理一下這個部落格，更新了 theme 之後發現問題還是存在，別人都沒有這種 issue，只有我有問題，那肯定是我在耍白痴才會這樣。果不其然，這次就讓我找到那個 template 的用處了，原來那個 template 是拿來翻譯用的，`T` 代表的就是 translation，把我們丟進去的 key 變成我們預先寫好的翻譯文字。

### Hugo 的翻譯功能

我用的 [theme](https://github.com/CaiJimmy/hugo-theme-stack) 在這方面做的蠻好的，有超多語言：
```
hugo-theme-stack/
└── i18n
    ├── ar.yaml
    ├── bn.yaml
    ├── ca.yaml
    ├── de.yaml
    ├── el.yaml
    ├── en.yaml
    ├── es.yaml
    ├── fa.yaml
    ├── fr.yaml
    ├── hu.yaml
    ├── id.yaml
    ├── it.yaml
    ├── ja.yaml
    ├── ko.yaml
    ├── nl.yaml
    ├── pl.yaml
    ├── pt-br.yaml
    ├── ru.yaml
    ├── th.yaml
    ├── tr.yaml
    ├── uk.yaml
    ├── zh-cn.yaml
    ├── zh-hk.yaml
    └── zh-tw.yaml
```
那這麼多語言要怎麼用呢，其實只要在你的 `config.toml`（或 `config.yaml`）裡面加入以下的變數：
```toml
# config.toml
defaultContentLanguage = "en"  # theme i18n support
```
像這樣打的話就是預設我們 `T` 模板會去找 `i18n` 資料夾底下的 `en.yaml`，找到我們傳進去的 key，再把他翻譯成我們想要的東西。以 `en.yaml` 為例：
```yaml
# en.yaml
darkMode:
    other: Dark Mode

list:
    page:
        one: "{{ .Count }} page"
        other: "{{ .Count }} pages"

    subsection:
        one: Subsection
        other: Subsections
```
當在 template 裡面出現 `{{ T "darkMode" }}` 時，他就會自動找到 `darkMode` 並取代成 Dark Mode，就像我 blog 左下角的那個開關一樣（只有電腦版看得到）。這裡還有一個很貼心的設計，當我們遇到翻譯可能會因為數量而不一樣時，Hugo 也有對應的機制。當我們沒有指定數字時就會自動去拿 `other` 的值，如果有指定數字的話就會把數字存在 `.Count` 裡面，並且去取得跟該數字對應的值，拿上面的 `en.yaml` 當例子的話，就會像是以下這樣：
```
# without number -> fallback to "other"
{{ T "darkMode" }}
=> Dark Mode

# with number "one" -> use "one", page with no "s"
{{ T "page" 1 }}
=> 1 page

# with number other than one -> use other
{{ T "page" 5 }}
=> 5 pages
```
當然你可能會想說如果我沒給他數字，但翻譯還是不小心使用了 `{{ .Count }}` 的話會怎麼樣，他會在 `.Count` 的地方顯示 `<no-value>`：
```
{{ T "page" }}
=> <no-value> pages
```

### 結論

關於翻譯還有很多功能，可以參考官網 [Multilingual Mode | Hugo](https://gohugo.io/content-management/multilingual/)，不過因為我沒有想要翻譯文章的意思，所以大概是不會用到那些 fancy 的翻譯文章功能。經過這次之後學到的教訓是抄 code 的時候還是要注意一下，不然有可能會卡超久（大概卡了一年之類的）...。

### References

* [Multilingual Mode | Hugo](https://gohugo.io/content-management/multilingual/)
* [i18n Tutorial: How To Go Multilingual in Hugo](https://phrase.com/blog/posts/i18n-tutorial-how-to-go-multilingual-with-hugo/)
