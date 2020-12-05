---
title: "設定 Hugo 網頁的 Favicon"
date: 2020-10-28T19:52:29+08:00
categories:
-   "Hugo"
draft: false
---

### 如何在 Hugo 網頁上面設定 Favicon

在不同的 theme 上要達成這個目標都有不同的作法，而我使用的 theme 是 [hugo-theme-stack](https://themes.gohugo.io/hugo-theme-stack/)，在我使用的時候的版本是沒有提供直接的 favicon 支援的（在舊的版本好像有支援，但是新的版本拿掉了[^1]），所以如果你的 theme 是有支援的（我說的有支援是指能在 `config.toml` 裡面直接設定），就可以直接跳到這篇文章的最後了；如果沒有的話，我的這篇文章可能可以幫助到你，不過還是要看每一個 theme 它不同的設定。這篇文章分享的是最簡單的設定方法，並且能在 `config.toml` 裡面加上 entry 使得以後更改 favicon 能夠更方便，但沒有保證能跟每一個瀏覽器功能（例如顯示於手機桌面的網頁捷徑）都有最好的相容性。如果需要能支援瀏覽器擴充功能的話，請參考 [Favicon Generator](https://realfavicongenerator.net/)，但是這樣可能就要做更多額外的設定，以後如果有機會使用的話再分享。

<!-- https://gohugo.io/variables/site/ -->
[^1]: [Add favicon in config.toml - Issue #42](https://github.com/CaiJimmy/hugo-theme-stack/issues/42)

### 正文

#### 第一步：理解 theme 的 layout 架構

因為我使用的 theme 是 [hugo-theme-stack](https://themes.gohugo.io/hugo-theme-stack/)，所以以下的程式碼可能會跟你的 theme 有所不同，但是架構跟觀念是一樣的。

還有一點是，如果你已經把 `themes` 裡面的 `layouts` 放到自己的 `layouts` 裡面的話（`/layouts/...`），也沒關係，因為 Hugo 會優先使用 root 資料夾的東西，找不到的話才會使用 `themes` 裡面的東西。而如果還沒放到自己的 `layouts` 裡面的話，可能要先把原本的 theme file 備份，或是直接把會改到的檔案依照一樣的資料夾名稱放到自己的 root `layouts` 裡面（如果在 `themes` 裡面的是 `/themes/[theme_name]/layouts/_default/...`，那就要把它放在 `/layouts/_default/...`），不然之後如果 theme 有更新的話可能會有點麻煩哦。

先看看 theme 資料夾裡面的 layouts 資料夾（`/themes/[theme_name]/layouts`），應該會看到很多個資料夾，以我的為例：
```
.
├── 404.html
├── _default
├── index.html
├── partials
├── post
├── rss.xml
└── shortcodes
```

如果還不知道 `layouts` 資料夾的功能的話，可以理解成規範每一個頁面的架構所需的檔案，比如說我的 sidebar 要放哪裡、我的 menu 要長怎樣等等的，除了每篇文章的 `.md` 檔的文字內容之外，要顯示成一個網頁所需的所有規定的架構就是放在 `layout` 資料夾裡面，以後如果有機會的話再分享有關 `layouts` 的東西。

#### 第二步：改 `layouts` 裡的檔案

我們需要用到的東西是 `_default/` 裡面的 `baseof.html`，`baseof.html` 是定義每一個網頁的基本架構，像是每一個網頁裡面最基本的積木，要做出網頁的其他頁面就是把更多積木疊上來而已，所以你的 theme 應該也會有一樣的東西，如果沒有的話可以參考 [Hugo's Lookup Order](https://gohugo.io/templates/lookup-order/)，應該可以找到相對應的檔案。我的 `baseof.html` 如下：
```html
<!-- baseof.html -->
<!DOCTYPE html>
<html lang="{{ .Site.LanguageCode }}">
    {{- partial "head/head.html" . -}}
    <body class="{{ block `body-class` . }}{{ end }}">
        <div class="container flex on-phone--column align-items--flex-start {{ if .Site.Params.widgets.enabled }}extended{{ else }}compact{{ end }} {{ block `container-class` . }}{{end}}">
            {{ partial "sidebar/left.html" . }}
            <main class="main full-width">
                {{- block "main" . }}{{- end }}
            </main>
            {{- block "right-sidebar" . -}}{{ end }}
        </div>
        {{ partial "footer/include.html" . }}
    </body>
</html>
```
那些 `class` 裡面內容可以先不管它，只要看用 `{{ }}` 括起來的東西就好了：我們看到有 `{{- partial "head/head.html" . -}}`，這個語法的意思就是把 `layouts/partials/head/head.html` 在該處展開。而且因為它的命名以及位置，看起來就是要定義 header 的檔案（一個網頁的 favicon 是定義在 `<head></head>` 裡面），所以就再把 `layouts/partial/head/head.html` 打開來看：
```html
<!-- layouts/partial/head/head.html -->
<head>
    <meta charset='utf-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1'>

    {{- $description := partialCached "data/description" . .RelPermalink -}}
    <meta name='description' content='{{ $description }}'>

    {{- $title := partialCached "data/title" . .RelPermalink -}}
    <title>{{ $title }}</title>

    <link rel='canonical' href='{{ .Permalink }}'>

    {{- partial "head/style.html" . -}}
    {{- partial "head/script.html" . -}}
    {{- partial "head/opengraph/include.html" . -}}

    {{- range .AlternativeOutputFormats -}}
        <link rel="{{ .Rel }}" type="{{ .MediaType.Type }}" href="{{ .Permalink | safeURL }}">
    {{- end -}}

    {{- partial "head/custom.html" . -}}
</head>
```
就發現到了有一個 `head/custom.html`，因為作者說可以加在 `custom.html` [^1]，因此我就把以下的東西加到 `layouts/head/custom.html`（當然如果不想要加在 `custom.html` 的話，直接加在 `head.html` 也是可行的做法）：
```html
<!-- layouts/head/custom.html -->
<link rel="icon" type="image/png" href="{{ .Site.Params.favicon }}">
```
上面這個意思是從 `config.toml` 取一個變數，而那個變數的名稱是 `favicon`：為了要讓 Hugo 執行程式的片段，我們必須用兩個大括號括起來；而 `.Site.Params` 來取得 `config.toml` 裡面 `[params]` 存放的變數，更多資訊可以參考 [Site Variables | Hugo](https://gohugo.io/variables/site/)。

在做完以上的這些事情之後，有需要更改的檔案們應該長的像是這樣：
```
layouts
└── partials
    └── head
        ├── custom.html
        └── head.html
```

#### 第三步：更改 `config.toml`

只要在 `[params]` 的區塊裡面加上檔案的位置就可以了：
```toml
# /config.toml
...
[params]
    ...
    favicon = "/img/favicon.png"
...
```
因為在 `custom/html` 裡面我們取的變數名稱是 `favicon`，所以在這邊就也要用一樣的名稱（也是可以把名字都換掉）。

**小提醒**：圖片的路徑必須使用絕對路徑（"`/img/favicon.png`"），
因為網頁在存取圖片的時候，那個 `href` 如果不是給絕對路徑的話，
就可能會跑掉，舉例來說，如果現在在 `aaa.com/about/`，
而我們不是使用絕對路徑的話（"`img/favicon.png`"），
就會跑到 `aaa.com/about/img/favicon.png`，而不是 `aaa.com/img/favicon.png`
那樣就會找不到你的圖片，因為靜態檔案（static files：圖片、文件等等的）所存放的地方是有規定的，下一個區塊會說明。

#### 第四步：把圖片檔案放進去

最後就把圖片的檔案放在 `/static/` 資料夾，就是 Hugo 預設存放靜態檔案的地方，通常會分類一下，像是以下的樣子：
```
static
└── img
    └── favicon.png
```
把檔案放好了之後，你就可以在 `your-website/img/favicon.png` 看到你的圖片了！

本次的分享就到這邊結束囉。

### Q&A
* favicon 有限定只能使用 `.png` 檔案嗎？
    * 應該是也可以用 `.jpg` 檔案，不過不建議，其實使用 `.ico` 會有最好的相容性（[參考](https://favicon.io/favicon-converter/)），但是可能要之後才會試試看，也超過這篇文章的範圍了。
