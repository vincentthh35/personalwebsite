---
title: "[Paper Notes] Deep Learning for Understanding Faces"
slug: "Deep Learning for Understanding Faces"
date: 2021-03-08T13:22:30+08:00
categories:
-   Paper-Notes
-   aMMAI
draft: false
author: "謝宗晅"
---

論文網址：\
[Deep Learning for Understanding Faces](https://ieeexplore.ieee.org/document/8253595)

### 概述

這篇論文介紹了從過去一直到現在的臉部辨識技術的演進。不過這篇論文涵蓋的範圍大部份是在 deep learning based 的方法，涵蓋到傳統方法的篇幅比較少。在臉部辨識的範疇中，要改進的方向大致上會分為三種：
* face detector
    * 用於框出圖片中的臉
* fiducial point detector
    * 用於標示臉部的 landmark（例如眼睛、鼻子、嘴巴的位置）
* face identification/verification
    * 用於萃取出臉部所隱藏的資訊，例如年齡、種族，也可以用於分辨兩張圖片中的臉是不是同一個人

### Face Detector

Deep learning based 的方法主要可以分為兩種：
* region based
* sliding-window based

---

Region based 的方法是先找出所有可能含有臉的區域（proposal），再用一個 classifier 來判斷那些 proposal 框出來的地方是不是一張臉。

比較常見的是使用 [Faster-RCNN](https://arxiv.org/abs/1506.01497) 裡面的 Region Proposal Network（RPN）來提出 proposal。

這類方法的弱點在於比較困難的臉比較難被框出來，並且因為架構中要提出 proposal 的部份（RPN 等等的）會使得 model 的速度比較慢。

---

Sliding-window based 的本質是用一個 bounding box 滑過圖片的每一個 pixel，再判斷那個 pixel 附近有沒有臉出現。在這個前提之下，還分為兩種方：一種是使用 pyramid 的方法來做出不同解析度的 feature map，另一種是使用 [single-shot detector（SSD）](https://arxiv.org/abs/1512.02325)。

SSD based 與 pyramid based 的不同之處在於 SSD based 不需要一個特別的金字塔架構，而是在 convolution 的過程中 pool 所有 feature。並且 SSD based 的方法因為只需要一個 forward pass 就能得到結果，因此會比 faster RCNN based 的方法還要來的快一些。

### Fiducial Detection

前面有提過了 fiducial detection 的目的是找出臉上的 landmark，也就是眼睛、臉、鼻子、嘴巴等等的位置，有了那些 landmark 之後，就可以做其他的 task，例如計算出臉面向的方向等等的。而 fiducial detection 的 approach 有以下兩種：
* model based
* cascaded regression based

---

Model based 的方法是直接訓練出一個能 fit 出那些 landmark 的地方。這種 model based 的方法對於不同角度、不同表情的臉的表現比較不穩定。

---

Cascaded regression based 的方法的核心概念是讓 model 學出一組 feature，再用 regression 來得到實際上的 landmark 位置。因此這種方法的 performance 會取決於 model 學到的 feature 強度。

而也有另一個作法是同時訓練 face detector 和 fiducial detection 的 model（ multi task learning，MTL）。

### Face Identification/Verification

* face identification
    * 決定兩張輸入的臉是不是一樣的臉
* face verification
    * 要在一個 gallery 裡面找出輸入的臉是不是在裡面

這個部份的 approach 有兩種，一種是試著學出最有代表性的 feature，再使用一般常見的 metric（L1、L2）來判斷相似度；而另一種是學出一個好的「比較 feature 的方法」，其實基本上就是 metric learning，就是學出一個好的評分標準來比較學出來的 feature。

在實務上的作法大多都是學出一組好的 feature，再把那些 feature 兩兩比較來計算出相似度來決定兩張臉是不是一樣的。

### Challenges

* face detection
    * 人臉的變化因素太多了，包含表情、角度、光線明暗，甚至化妝等等
    * 找出高/低解析度的臉相對困難
* fiducial detection
    * dataset 的數量比較少（因為要人工標註那些點需要大量的成本）
* face identification/verification
    * 記憶體的限制使得在效能上面必須有所犧牲
    * 在影片中的辨識

### Contributions

* 整理了到 2018 年以前的 deep learning based 的各種方法
