# 年款数据说明（tpematsfactory.com）

> 2026-09-20 记录。**这份文件解释为什么站上有 22 个车型的年款是空的**，以及填了的那些数据从哪来。

---

## 1. 结论先说

| 来源 | 车型数 | 说明 |
|---|---|---|
| 供应商自己的 listing 标题 | **4** | 最强证据：店铺自己写的年款 |
| 公开车型世代资料 | **11** | 有出处，**页面上标注「仅供参考，下单前确认」** |
| 留空（未推测） | **22** | 查不到可支撑的证据，宁可为空 |

全站 37 个车型，15 个有年款。

---

## 2. 为什么供应商数据里挖不出年款（三重验证，全部失败）

1. **标题**：96 条 listing 只有 4 条写了年款。
2. **详情页产品描述**：0 / 96 条提到任何年款（脚本扫全部缓存详情页）。
3. **详情页整页扫描**：95/96 页确实有「车型 + 年款」表格，但**两张不同产品的表格内容完全相同**——标题写着「Toyota Hilux Revo」的产品，表里列的是 Ford Ranger / VW Teramont / Volvo S60L / Mitsubishi PAJERO。这是**店铺级模板**，不是产品级数据，采用会造成「长安 UNI-T 适配福特 Ranger」这种致命错误。
4. **扩大抓取**：扫了店铺 30 页、约 480 条 listing，按车型聚合年款 —— 对我们的 33 个车型 **0 条新证据**（带年款的都是另一批车型：Tesla Cybertruck、Toyota 4Runner、Voxy Noah 等）。

**所以「根据车型有的年款补充」这件事，靠供应商数据是做不到的**——数据里根本没有。

---

## 3. 填进去的 11 个，出处与置信度

| 车型 | 年款 | 置信度 | 出处 |
|---|---|---|---|
| BYD Atto | 2022-present | high | [BYD Atto 3](https://en.wikipedia.org/wiki/BYD_Atto_3) |
| Toyota Fortuner Prado | 2015-present | high | [Toyota Fortuner](https://en.wikipedia.org/wiki/Toyota_Fortuner) |
| Toyota Prius | 2022-present | high | [Toyota Prius](https://en.wikipedia.org/wiki/Toyota_Prius) |
| Honda CR-V | 2022-present | medium | [CR-V 6th gen](https://en.wikipedia.org/wiki/Honda_CR-V_(sixth_generation)) |
| Toyota Corolla | 2018-present | medium | [Corolla E210](https://en.wikipedia.org/wiki/Toyota_Corolla_(E210)) |
| Toyota Crown | 2022-present | medium | [Toyota Crown](https://en.wikipedia.org/wiki/Toyota_Crown) |
| Toyota Hilux (Vigo Dual Cab) | 2015-present | medium | [Toyota Hilux](https://en.wikipedia.org/wiki/Toyota_Hilux) |
| Nissan Navara NP300 | 2014-present | medium | [Nissan Navara](https://en.wikipedia.org/wiki/Nissan_Navara) |
| Nissan X-Trail | 2021-present | medium | [Nissan X-Trail](https://en.wikipedia.org/wiki/Nissan_X-Trail) |
| Buick Excelle | 2018-2023 | medium | [Buick Excelle](https://en.wikipedia.org/wiki/Buick_Excelle) |
| Toyota RAV4 | 2019-2025 | **low** | [CarBuzz generations](https://carbuzz.com/cars/toyota/rav4/generations/) |

**刻意没填的**：Audi A6 A8（两个车型混在一个字段，无法择一）、Fiat Palio（已停产）、以及 20 个查不到可靠世代资料的（Mercedes E300L/C260L、Ford Ranger/Raptor/F150、VW Polo、Land Cruiser LC200/LC300/Prado、现代 Elantra、以及全部中国品牌车型）。

> RAV4 那条置信度是 **low**（有资料声称 2026 年换代，与主流口径冲突）。**如果你只想保留高置信度的，把 `tools/model_years.json` 里 RAV4 的 `years` 改成空串再跑一次 `emit_site_data.py` 即可。**

---

## 4. 页面上的诚实处理

年款来自公开资料的车型，页面上会多出一行小字：

> Year range shown is the model generation, for reference only. Fitment changes between generations - send us your exact year and we confirm against our tooling before you order.

数据层里每个车型都带 `years_source` 字段（`listing_title` / `model_generation` / 空），所以**供应商真实数据的年款和参考年款在代码层面就是分开的**，不会被混淆。

---

## 5. 真正的解法

年款唯一可靠的来源是**模具清单**（Make / Model / 年款区间 / 左右舵）。
给我这份清单，我可以把所有 `model_generation` 的年款替换成实锤数据，页面上那行「仅供参考」的提示也会消失。
