---
title: "面試心得 - MaiCoin"
description: "特別為了 MaiCoin 分出來的面試心得"
slug: "graduate-interview-maicoin"
date: 2022-02-22T23:18:57+08:00
categories:
-   Sharing
draft: false
image: "spark.jpg"
author: "謝宗晅"
---

把 MaiCoin 分出一篇的原因是，以整個面試流程來說，還有給的 package，甚至是超友善的 VP，都讓這間公司給我留下非常非常好的印象，真的是打從心底會想要工作看看的公司之一，也使得我最後在決定 offer 的時候痛苦萬分。

### 投遞方式（Backend Engineer）

* 之前聽過獵人頭說過的一家，也有看同學在玩 crypto 用的是他們的 app
* 寄信到他們信箱，隔天就回信約 google meet 線上面試了，頂級效率

#### 一面（Google Meet）

一面只約了一個小時，本來以為會考比較知識面的問題，結果什麼都沒有考，一般來說似乎是要考寫程式的，不過面試官說因為我是 new grad，所以就沒有考程式，整個過程都是在聊天，問一些可能跟 behavior 會擦到邊的問題。最一開始的時候他問了我怎麼會去準備 GRE，還有關於台灣碩班的一些事情，後來他也問到我有修 Ric 的網路服務程式設計和李宏毅 ML，當下我其實有點遲疑，想說我應該沒有給他成績單，怎麼會看到我修什麼課，直到晚上的時候才想到我有寫學期心得，看來面試官（我忘記了但一面好像就是 VP 了...）把我的某些文章讀了一遍，真的很用心（部落格總算是有點用了）。面試官說這個職位很少有 new grad 來面試，我覺得一方面應該是因為他們沒有在大力宣傳（有在宣傳的話就會寄到系上信箱了），二方面可能是他們想要蠻強的人？...而我會知道這家公司其實是因為獵人頭，不過當時聽的時候還不知道原來他說的這家這麼厲害，算是台灣在做交易所的前幾名了。雖說如此，但是他們負責做交易所的團隊其實相較起來算蠻小的，不到 10 人在負責這個台灣前幾大的 crypto 交易所，感覺還是蠻不可思議的。

中間也有問到我選工作的幾個要素，他發現我把薪水往後排了之後（我把成長性之類的排在前面），有提到說他們公司其實是有在賺錢的，所以薪水可以算是蠻不錯的（在他們的招募頁面也有寫保證百萬年薪，不過不知道 100+ 是+到哪）。中間也聊了很多關於做 crypto 交易的一些難處，例如：有些幣值太小，大家就會一次買個幾百萬顆甚至更多（數字可能會 overflow），或是有某個幣暴跌或暴漲的話，他們的流量也會跟著暴增等等的。最後就是說了接下來會有的流程，會是一個「一整個下午」的面試，聽起來像是我第一次面群暉實習生的那種情況，不過又更難了：面試官說會考白板題之外，還會考 system design，這應該就會是我人生第一次有 system design 的面試了吧。如果還有下一關的話應該會排久一點之後，就還可以看影片惡補一下...。（後記：把時間安排在後面一點好像也只多看了一兩部 system design 的影片）

隔天就寄信來約下一次的面試了！

#### 二面（Onsite）

<!-- 第一題：爬樓梯，一次能爬一階或兩階，問爬到 n 階有幾種爬法，我先給了一個 n 的解，之後面試官說有 log n 的解，我就猜說是不是二分搜，結果他馬上送我一個提示，就是把狀態的轉移換成矩陣乘法，這樣就可以快速冪了 -->
<!-- 第二題：一棵樹，要輸出從右邊看到的第一個 node 的 value 陣列，follow up：怎麼樣能不走完所有 node 就得到解答 -->
<!-- 第三題：sliding window 裡面的最大值，我一開始給了 nlog k 的解法，可是面試官要我給 n 的解法，之後卡了一下，總算是有吃到面試官的提示然後順利回想起應該要怎麼做那題 -->
從進去並找到公司就很有挑戰性的一次面試，首先進去大樓之後，要找到對的入口，可是找到入口還不夠，要先有訪客證，然而他們的訪客證也不是一般的訪客證，他們的訪客證超級酷，是有一台機台可以打電話到樓上的公司，跟他說我是要來面試之後，機器就會吐訪客證出來。

整個下午都在面試的經驗還真的是很少，大概只有群暉跟這家吧。第一關先是演算法的問題，大概考了三題（忘了有幾題，只記得三題的內容），每一題雖然題幹都沒有很難（如同信件寫的 medium），但延伸出來的 follow-up 都有讓我眼睛為之一亮，都是一些經典題可是卻有蠻多是我沒想過的東西，不是每個 follow up 都是叫我壓空間時間，有些是請我換個作法，再看看換作法之後時間複雜度會不會降低。過程中大概卡了一兩次，卡最久的是最後一題，明明是有寫過的題目但就是想不起來怎麼做，算是憑藉著不少面試官的引導才做出來。第二關是 system design，整個過程沒有我想像中那麼順利，看 yt 影片都覺得他講一講就很有道理，但我講出來的就沒有什麼道理，幾乎都是我提出一個作法，然後面試官說這樣可能有的問題，雖然在卡了一下之後我應該還是有提出一些合理的作法，各種使用 cache 等等的，感覺上我應該也不算是表現太好，至少不可能比演算法還要好。System design 回答完之後，同一批面試官也有問一些關於我履歷的問題，就也算是蠻閒聊的吧，不算是有壓力的問答。

下一關是 culture feed（？是這樣拼嗎），算是比較輕鬆的一關，主要是聊一些 behavior 的問題，履歷相關的只有帶過一些，在這關聊到蠻多關於福利的部分，以及他們覺得公司如何，其實都蠻一致的覺得很讚，同事很強，假很多放不完（不扣薪事病假），錢多不多我不確定（但應該也不少），在這關也知道了他們會有算是輪班的機制，每個人都會輪到一個禮拜的時間，那個禮拜就不用做本來的工作，只要負責接受客戶的需求，以及系統壞掉要負責修等等的，聽起來應該不算壓力很大的那種排班（他們說其實系統越做越好，已經很少有那種緊急情況需要修的了）。結束了這關聊天之後，最後一關也是聊天，是換成工程師 VP 還有 HR 來跟我聊天，一開始只有 HR 近來，因為 VP 在另一場面試那邊，HR 大致上說了一下基本的福利之後 VP 就進來了，問了 VP 幾個關於公司的問題，聊了一下 crypto 之後就結束了從下午兩點開始一直到六點的面試，進公司的時候天還是亮的，出去公司天就已經黑了。

面試到中間的時候其實就已經會開始隨機發呆了，講話講到一半有時候會突然當機，兩三秒之後才想到要繼續講什麼，HR 一開始就說如果想要休息的話可以說，但我還真的想不到要怎麼說自己想休息...，反正就那樣走完了，還真的是很累，獲得的資訊量也很大，不管是對公司的資訊或是技術方面的資訊都很大，很累可是感覺起來真的蠻充實的，異常的非常充實。

在面試過程中意外發現 MaiCoin 裡面有一些待過 HTC 的工程師，總共三輪每輪三個人的面試官裡面就有兩個是之前待過 HTC 的，這比例應該算高吧。HR 說大概要一個禮拜到兩個禮拜之後才能決定給不給我 offer，還真的是希望不要那麼久耶，一個禮拜過後都快要跨年了，也希望我能拿到他們的 offer（被面試這樣操下來蠻好奇他們會給到多高，感覺是有在賺錢的公司應該給的很不錯才對）。

結果隔天就說他們決定要給我 offer 了，超開心，可惜的是我在聊聊天階段不小心透露太多了，直接跟他們講群暉給的大概範圍，他們開的基本上就是以群暉為基底再往上加一點（後來想想應該是往上加蠻多的，如果包含謎樣的年終獎金的話，而且第一年開始就有得領了）。

### Offer Compete + 心得 + 特別感謝

最後我手頭上剩下兩個 offer，MixerBox 的和 MaiCoin 的，因為 MixerBox 給的比較多（後來想一想也不一定，因為 VP 一直沒有透露年終大概會有多少），所以我就拿他的去 compete，最後沒有 compete 成功，原因是我給的數字應該是他們 senior 的薪水，但我是 new grad，直接給我這種沒工作經驗 senior 的 offer 不太可行，雖說如此 VP 還是有提供一個特別方案，讓我只要績效有到就有機會達到那個數字（嚴格來講應該是超過那個數字，如果含年終的話）。那時候真的第一次覺得自己原來這麼有用嗎？完全把我之前遭拒絕被打擊的信心全部都補回來了，雖然這種依靠 feedback 來評斷自己價值的心態不怎麼健康，但受到這樣的對待還是讓人非常開心。

在 MaiCoin 的招募頁面那邊似乎沒有特別寫找 junior 或是 senior，我猜可能是因為要依照能力以及經歷來決定進去的等級，然而好像很少有聽說學長姐一畢業就去 MaiCoin 的，明明待遇福利都很不錯，也是有賺錢的公司，我猜可能是在校園徵才的部份他們沒有特別投入心力，或是說他們比較傾向於找多少有一點經驗的人，誰知道呢。總之整個面下來之後是真心覺得以後有機會轉職的話會想嘗試看看這家，也可以試試看他們做 Quant 的職位（他們叫作 Algorithmic Trading Software Engineer），這樣就可以不用寫 Ruby 了（那時候在考慮 offer 的時候也是有考慮到這點，進去是要寫完全沒寫過的 ruby，不過必須說讓我做出選擇最主要原因真的不是這個）。

最後要特別感謝 VP Yu-Te，在整個面試過程中都很友善，也聊了很多關於公司以及最初 crypto 產業的光景；給 package 的態度也讓人覺得是真的有在為公司找人才（這樣講好像也怪怪的，好像說自己是人才一樣，殊不知只是演算法剛好都被考到會寫的）。推薦有能力的人去面看看 MaiCoin，能拿到的待遇絕對不會讓你失望。