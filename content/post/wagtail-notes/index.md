---
title: "基礎 Wagtail 筆記"
slug: "wagtail-notes"
date: 2021-06-11T15:27:03+08:00
categories:
-   Sharing
draft: false
author: "謝宗晅"
---

（以下的 code 都是參考自[Wagtail Docs](https://docs.wagtail.io/en/stable/)）

### Wagtail 簡介

[Wagtail](https://wagtail.io/) 是一個基於 Python Django 的框架，提供了一個比較好用的 Content Manage System（CMS），比起預設的 Django 後台管理系統好用非常非常多，那用途的話，我目前看起來比較適合用在寫部落格或是官方網站，作為一個編輯網頁內容的後台，使用體驗真的非常不錯。這次學這個是因為實習會用到（部份的官方網站是用 Wagtail 作為 CMS），剛好以前也有因緣際會接觸過 Django，所以就順便複習一下 Django 的基本用法。這篇文章是最基礎的 tutorial 的筆記，涵蓋以下幾個基礎用法：
* Models
* Models
* Templates
* Images
* Tags
* Snippets

希望之後能有更多篇這類的文章，紀錄一下實習到底都學了些什麼。

### Models

```python
# appname/models.py

from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index

class PageName(Page):
    # database fields
    body = RichTextField(blank=True)
    intro = RichTextField(blank=True)
    date = models.DateField('Post date')

    # search fields
    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    # editor panel
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context
```

* `Page`
    * 頁面繼承的基本 class
* `RichTextField`
    * 用來儲存 rich text 的 field
    * rich text 能存的內容非常廣泛，除了單純的文字之外，還可以為文字加上各種效果（粗體、斜體等等），或是加上超連結、插入圖片
    * `blank=True`：optional field（`blank=False` 就是必填）
    * `StreamField`：
        * 概念像是能讓使用 CMS 的編輯者在單一的一個區塊整合一種以上的 block，以任意的順序安排事先被定義好的 block
        * 例如一個文章可能可以有好幾個 paragraph，使用 `StreamField` 就可以讓編輯者將不同 paragraph 分開（當然這只是很簡單的例子），並且因為編輯者能夠自由的安排順序以及某一個 block 出現的次數，所以有很大的自由度
* `FieldPanel`
    * 定義在 CMS 上面編輯者可以編輯的 block
    * 直接傳上面定義好的 class property 名稱的**字串**進去
    * `classname`：用來規定編輯頁面的 CSS，`'full'` 代表編輯欄位會橫向延伸滿編輯頁面，`'title'` 代表會把字體變大，適合用在標題的欄位
* `search_fields`
    * 用來定義這個頁面能搜尋的內容以及搜尋的方式
    * 一樣是傳 class property 名稱的字串進去
    * `index.SearchField`：full-text search
    * `index.FilterField`：在搜尋的時候可以 filter 這個欄位
* `content_panels`
    * 定義這個頁面在 CMS 裡面能夠編輯的 field
    * 在 CMS 裡面，編輯一個頁面有三種 attributes
        * content（`content_panels`）：管理主要內容的區塊
        * promote（`promote_panels`）：管理一些 tag、title 或是 slug 的地方
        * settings（`settings_panels`）：管理其他設定（例如：publish schedule）的地方
* `get_context`
    * `get_context` 這個 method 是用來加上額外想要給 template render 資訊的
    * `Page` 這個 class 本來就有一個了，所以我們要覆蓋它
    * 因為原先 `Page` 要拿的 `context` 也要一併傳進去 template，所以要先 `super().get_context(request)`（如果有接觸過 Django 的話應該不會太陌生）
    * 上面的範例是示範了如何過濾掉還沒有 published 的（published 的文章會是 `live` 狀態）
    * `order_by()` 傳入的是想要拿來排序的 property 名稱，範例裡面傳入的是 `Page` 的預設 property，前面加上負號的話就可以做逆序排序
    * Django 的 `context` 是 dictionary 的型態，所以要加東西進續的話就直接 `dict_name['some'] = something` 就好了

### Templates

```html
{% comment %}app_index.html{% endcomment %}

{% extends "base.html" %}

{% load wagtailcore_tags %}

{% block body_class %}template-homepage{% endblock %}

{% block content %}
    <h1>{{ page.title }}</h1>

    <div>{{ page.intro|richtext }}</div>

    {% for post in page.get_children %}
        {% with post=post.specific %}
            <h2><a href="{% pageurl post %}">{{ post.title }}</a></h2>
            {{ post.intro }}
            {{ post.body|richtext }}
        {% endwith %}
    {% endfor %}

    {{ page.body|richtext }}
{% endblock %}
```

其實基本上就是 Django 的 template 語法，只是多了一點點不一樣的東西。原則上在 Django 可以使用的東西這邊都可以使用。

* `{% comment %}{% endcomment %}`
    * 註解
* `{% extends "something.html" %}`
    * 把指定的 template 展開，就可以用這個檔案當作頁面的基底，通常這種基底都會挖一些空格來讓我們修改或是填入，要填入空格的話就是用 `{% block ... %}{% endblock %}` 的語法
* `{% load wagtailcore_tags %}`
    * 載入 wagtail 的一些 tag（`richtext` 就是其中之一）
* `{% block blockname %}{% endblock %}`
    * 在展開的 template 裡面填入我們的東西
* `{{ page.property }}`
    * 存取變數是直接用 `{{}}`，`page` 是這個頁面的 model（寫在 `appname/models.py` 裡面的），可以直接存取預先設定好的 field
    * 使用保留字是用 `{% ... %}` 的格式
* `{{ page.property|richtext }}`
    * 用 richtext render 頁面的內容，如果拿掉的話就會出現該 field 的 raw HTML
* `{% for e in some_list %}{% endfor %}`
    * 就是 for 迴圈，沒什麼特別的
* `{% with post=post.specific %}`
    * 可以一次 assign 一個以上的變數
    * 用法就跟 python 的 `with` 有點像但又不太一樣，Django 的 `with` 比較是用來簡寫的，如果在一個 block 裡面 call 一個東西很多次但又很長的話可以使用
    * 也可以寫成 `with ... as ...`（這個範例的話就是 `with post.specific as post`）
    * 如果用等號寫法的話，等號左右邊**不能空格**

### Images

圖片的 `model.py` 有兩個地方要處理，一個是要先在裡面加上「圖片本身」的 model，再把那個 model 放到我們的 page class 裡面。

```python
# appname/models.py

from django.db import models
from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

class PageName(Page):
    # database fields
    # ...
    # search fields
    # ...

    # editor panel
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
        InlinePanel('gallery_images', label='Gallery Images'),
    ]

    def get_context(self, request):
        # ...
        return context

class ImageGalleryClassName(Orderable):
    page = ParentalKey(PageName, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption')
    ]
```

* `InlinePanel`
    * 是用來新增其他 model 的內容，例如想在一個頁面裡面新增很多張圖片，就可以使用 `InlinePanel`
    * 傳入的字串一樣是 property 的名字，而且作為 subclass 的那個 class 需要用 `ParentalKey` 來綁定 parent class
        * 被傳入的必須是繼承 `Orderable` 的 class
    * 如果要限制能加入的 model 數量的話，可以傳入 `min_num=...` 和 `max_num=...`，例如限制一篇文章只能有一個作者的話，就可以設為 `max_num=1`（作者被定義在另外的 model）
* `Orderable`
    * 這個 class 用來編輯的 panel 是存在 `panels` 變數，和 `Page` 不一樣
* `ParentalKey`
    * 和指定的頁面綁定，使得指定頁面的 class 可以使用自己這個 class 的 property
    * 在 parent page 裡面就是直接 call `related_name` 的值就可以取得這個 class 的內容
    * （是繼承 Django 的 `models.ForeignKey`）
    * `on_delete` 和 `related_name` 放在 `models.ForeignKey` 說明
* `models.ForeignKey`
    * 這邊因為概念上是「先將圖片上傳」，再從 database 裡面的圖庫來選擇，因此要使用 `ForeignKey`
    * `on_delete` 規定的是「如果放在這邊的物件不在 database 了，那要怎麼辦」
        * `models.CASCADE` 是直接把 entry 刪掉，也就是說不會留下圖片曾經存在過的痕跡（一般來說比較常用這個）
        * `models.SET_NULL` 是讓被刪掉的痕跡存在，並將這個 entry 設成 `null`（要搭配著 `null=True` 一起傳進去）
        * `models.PROTECT` 設成這個的話，就會避免掉 database 把該 object 刪除的動作
        * （其他還有一些，可以參考 [Django Docs: ForeignKey.on_delete](https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.ForeignKey.on_delete)）
    * `related_name`
        * 規定 foreign 的 table 要用什麼名稱存取這個 property
        * 如果設成 `'+'` 的話是 disable 存取的功能，也就是無法從 foreign 的地方使用這個 property（設成 `'+'` 或是以 `'+'` 結尾的字串都可以達成這個效果）
        * 如果沒有給值的話，預設是 `[ClassName (lower case)]_set`
* `ImageChooserPanel`
    * 用來選擇圖片的 edit panel

```html
{% comment %}some_page.html{% endcomment %}

{% extends "base.html" %}

{% load wagtailcore_tags wagtailimages_tags %}

{% block body_class %}template-homepage{% endblock %}

{% block content %}
    <h1>{{ page.title }}</h1>

    <div>{{ page.intro|richtext }}</div>

    {% for item in page.gallery_images.all %}
        {% image item.image %}
        <p>{{ item.caption }}</p>
    {% endfor %}

    {{ page.body|richtext }}
{% endblock %}
```

* `wagtailimages_tags`
    * 包含了 image 相關的 tag
* `page.gallery_images.all`
    * 存取變數的方式和一般的一樣，只是要在後面加一個 `all`，因為這是 ForeignKey，所以使用這個 property 的時候會回傳一個 set
* `image`
    * 這個 tag 可以用於顯示圖片，以及規定顯示出的樣式（有很多種用法，參考：[Wagtail Docs: Use images in templates](https://docs.wagtail.io/en/stable/topics/images.html)）


### Tags


```python
# appname/models.py

from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

class TagClassName(TaggedItemBase):
    content_object = ParentalKey(
        'PageName',
        related_name=='tagged_items'.
        on_delete=models.CASCADE
    )

class PageName(Page):
    # database fields
    # ...
    # search fields
    # ...

    tags = ClusterTaggableManager(through=TagClassName, blank=True)

    # editor panel
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
        ], heading='Blog information'),
        FieldPanel('intro'),
        FieldPanel('body', classname='full'),
        InlinePanel('gallery_images', label='Gallery Images'),
    ]

    def get_context(self, request):
        # ...
        return context

class TagIndexPage(Page):

    def get_context(self, request):
        tag = request.GET.get('tag')
        blogpages = PageName.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context
```

* `TagClassName(TaggedItemBase)`
    * 首先要先建立一個拿來當作 tag 的 class
    * 也要使用 `ParentalKey` 來和 page model 綁定
    * `content_object`
        * 在 Django 裡面是寫成 ForeignKey，但在這邊就用 `ParentalKey` 取代
* `ClusterTaggableManager`
    * 用來管理每一個 page 的 tags
    * `through` 要傳入我們定義的 tag class
* `MultiFieldPanel`
    * 把幾個 field 整合在一個區塊的工具
    * 應該只有 CMS editor 感覺的出差別，其他部份都和一般的 `FieldPanel` 一樣
* `TagIndexPage`
    * 用來 filter tag 的頁面
    * `request.GET.get('tag')` 是用於等一下 template 的部份，在點擊 tag 之後會跑到這一個 filter 頁面，同時以 GET 傳入 tag 名稱，所以我們可以利用在 GET 裡面的參數來 filter 各個頁面
    * `tags__name`
        * 這個是從 Django 繼承的語法，語法是 `property__` 後面接 subproperty 名稱或是其他的 filter 規則，參考：[Django Docs: Field Lookups](https://docs.djangoproject.com/en/3.2/topics/db/queries/#field-lookups)
        * 因為在 `PageName` 裡面我們的 tag property 是叫作 `tags`，所以要搜尋 `PageName` 裡面的 `tags`
        * `name` 是因為 `TaggedItemBase` 裡面有一個 ForeignKey `Tag`，而 `Tag` 有 property 叫做 `name`，因此要包一個 `ClusterTaggableManager` 並且對 `name` 搜尋，參考：[Django-taggit github](https://github.com/jazzband/django-taggit/blob/master/taggit/models.py)

在本來的 page model 裡面加上這些，就能在 page 裡面顯示 tag：
```html
{% if page.tags.all.count %}
    <div>
        <h3>Tags</h3>
        {% for tag in page.tags.all %}
            <a href="{% slugurl 'tags' %}?tag={{ tag|urlencode }}">{{ tag }}</a>
        {% endfor %}
    </div>
{% endif %}
```

* `slugurl`
    * 和 `pageurl` 不同的地方在於傳入的是字串（`pageurl` 傳入的是 `Page` object）
    * 如果傳入 `slugurl` 的字串所指到的網址存在的話，就會回傳 `None`
    * 這邊還用了一個直接用 GET query 的技巧：在網址後面加上要 query 的字串就可以直接傳入 model 裡面的 request
    * `urlencode` 是為了要針對特殊的字元而把 query 的字串轉義才加的（官方的教學沒有加上這個，所以如果 tag 裡面出現特殊字元的話功能就會失效，例如 `&=` 之類的字串）


```html
{% comment %}tag_index_page.html{% endcomment %}

{% extends "base.html" %}

{% load wagtailcore_tags %}

{% block content %}
    {% if request.GET.tag|length %}
        <h4>Showing pages tagged "{{ request.GET.tag }}"</h4>
    {% endif %}

    {% for blogpage in blogpages %}
        <p>
            <strong><a href="{% pageurl blogpage %}">{{ blogpage.title }}</a></strong>
            <small>Revised: {{ blogpage.latest_revision_created_at }}</small>
        </p>
    {% empty %}
        No page found with this tag.
    {% endfor %}
{% endblock %}
```

* `request.GET.tag`
    * 一樣是存取 GET 的參數
* `{% empty %}`
    * 只能使用在 `{% for %}` 裡面，如果 for 迴圈裡面的東西是空的話就會顯示 `{% empty %}` 下面的東西

### Snippets

Snippets 概念上我覺得像是自訂一個 model，來讓其他 class 可以取這個物件當作 ForeignKey，就像 tag 或是圖片一樣，都是把物件先存在 database 裡面，再用 ForeignKey 去指向它。

```python
# appname/models.py

from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index

@register_snippet
class SnippetClassName(models.Model):
    name = models.CharField(max_length=250)
    profile = models.CharField(max_length=250)

    panels = [
        FieldPanel('name'),
        FieldPanel('profile'),
    ]

    def __str__(self):
        return self.name

class PageName(Page):
    # ... other informations
    my_snippet = models.ForeignKey(
        'SnippetClassName',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        SnippetChooserPanel('my_snippet'),
        # other panels
    ]
```

以上就算是完成了一個 snippet 的註冊，和直接使用 `MultiFieldPanel` 不一樣的地方是使用 snippet 會在 database 建立一個 object，而 `MultiFieldPanel` 並不會建立 object。

* `@register_snippet`
    * 用來註冊 snippet 的 decorator
    * class 一樣是使用 `panels` 來規定要有什麼樣的 field
* `__str__(self)`
    * 規定當 template 只存取最上層的 property 的話，要回傳怎樣的字串
    * 在這個例子裡面就是在 template 裡面使用 `page.my_snippet` 的時候會回傳的字串
* `SnippetChooserPanel`
    * 用來選擇 snippet 的 panel

還有可以將 snippet 設為 template tag 的語法（讓它可以直接用 tag 的方式存取），參考：[Wagtail Docs: Snippets](https://docs.wagtail.io/en/stable/topics/snippets.html)，這個參考裡面也有介紹如何在 `InlinePanel` 裡面使用 snippet。要在 `Page` 裡面存取就和其他 property 一樣，直接用 `page.property` 存取就好了。
