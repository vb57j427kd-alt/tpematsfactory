# tpematsfactory.com — 建站状态交接（2026-09-20）

> **当前状态：本地站点已完整生成并通过两套校验，尚未部署上线。**
> 数据来源：`https://lywalter.en.alibaba.com`（Linyi Walt 店铺）抓取，2026-09-20。
> 站点主体：**Linyi Strawberry International Trade Co., Ltd.**

---

## 1. 已交付的站点

| 项目 | 数量 |
|---|---|
| 页面总数 | **94**（首页 1 + 品类 4 + 产品 51 + 车型 37 + 车型索引 1） |
| 产品 | 51 款（floor-liners 42 / all-weather 5 / trunk 3 / double-layer 1） |
| 车型适配页 | 37 个 `/shop-by-vehicle/{make}/{model}/` |
| 产品图 | 51 张，全部落盘 `images/`，**零重复**（md5 校验） |
| `sitemap.xml` | 94 条 URL，车型页 priority 0.9 > 产品页 0.8 |
| 首页筛选器 | Year → Make → Model 三级联动，数据源 `vehicles.json` |

架构要点（相对 BHT 的 5 处改造）：全站目录化输出、车型落地页、车型索引、`vehicles.json`、sitemap 优先级；另加 B2B 询价弹窗（Country / Company / Vehicle model / Quantity）、产品页 Fitment + Material 区块、按页型区分 JSON-LD。

本地预览（**必须用 http 服务**，筛选器要 fetch `vehicles.json`，双击打开会被浏览器本地策略拦住）：

```powershell
cd <本目录>
python generate.py          # 重新生成
python -m http.server 8000  # 浏览器打开 http://localhost:8000/
```

---

## 2. ⚠️ 抓取过程中发现的四个数据质量问题（都已做处理，但你需要知道）

### 2.1 阿里详情页的「车型适配」属性是店铺级模板，**不可用**
抓取时发现详情页有结构化的 `Car Fitment / Model / Year` 属性，本以为是最好的数据源。实测：**96 个 listing 只有 8 种适配签名，其中 1 种被 86 个 listing 共用**（都写着 Ford Ranger / Honda Civic / Tesla Model 3/Y / Toyota Hilux）。

如果直接采用，会出现「长安 UNI-T 的脚垫页面写着适配福特 Ranger」——这正是车垫品类最致命的错误。

**处理：车型只从各 listing 自己的标题解析**（标题是卖家为每个产品单独写的，产品级）。已逐条核对：4 条年款全部能在各自标题中找到原文，品牌仅是 `Benz→Mercedes-Benz`、`VW→Volkswagen` 的别名归一，无编造。

### 2.2 96 个 listing 只有 55 张不重复的图片
**59 个 listing 在复用别的 listing 的同一张图**（最大一组 9 个 listing 共用一张）。产品站上多个不同车型显示同一张照片会显得像模板站。

**处理：按图片 md5 去重，保留 51 款（41 个重复图 listing 被丢弃，记录在 `../tools/dropped.json`）。** 如果你希望这些车型也上架，需要补拍对应的产品图。

### 2.3 只有 4 个 listing 的标题写了年款 → **33/37 个车型没有年款**
标题里普遍是「for Honda CR-V」这种写法，不带年款。年款是车垫退换货的第一大原因，**所以宁可留空也没推测**。

**这需要你的模具清单来补**：哪些车型、哪些年款区间、左右舵。填好发我，我批量补进 `VEHICLES`。

### 2.4 皮革类产品被排除
店铺有独立的 Leather Car Mats 分类（4 款）。因为站点定位是 **TPE 车垫工厂**（域名即 `tpematsfactory`），纳入皮革会稀释定位。需要的话我可以加第 5 个品类。

---

## 3. 需要你补齐的输入

| # | 事项 | 影响 |
|---|---|---|
| 1 | **模具清单**（Make / Model / 年款区间 / 左右舵 / 可做位置） | 补全 33 个车型的年款；确认 37 个车型的适配成立与否 |
| 2 | **新建 GA4 property** | 生成器当前跳过注入；复用 BHT 的会混三站流量 |
| 3 | **新建 Microsoft Clarity 项目** | 同上 |
| 4 | **新建 Formspree 表单** | 复用 BHT 的会撞免费版 50 封/月上限，询盘直接丢 |
| 5 | **本站收件邮箱** | 建议独立邮箱，便于分站统计询盘 |
| 6 | **认证情况** | 有 FMVSS 302 / REACH / RoHS 报告就填 `SITE["certificates"]`，信任区才会出现；没有就先别放，留空比放占位图安全 |
| 7 | **银行信息复核** | 已从 BHT 沿用（Linyi Strawberry 主体），上线前请自己过一遍 |
| 8 | ❓「**图片改为中英双语**」 | 本站是英文 B2B 站，按既有红线默认**纯英文、无第三方品牌**。这条是本站需求还是别的项目？ |
| 9 | ❓模板服务承诺 | 首页写了「24h 回复」。这是模板文案，你确认能兑现就保留 |

另有 8 个产品的车型没能从标题解析出来（品牌级/未解析），目前只挂在品类页、没有车型页，文案写成「按你的车型定制」。需要的话把对应 SKU 的车型告诉我，我升级成车型页。

---

## 4. 上线步骤（数据齐了之后）

1. 建 GitHub 仓库 `tpematsfactory`，SSH over 443 推送
2. 仓库 Settings → Pages：`main` / `root`，Custom domain `tpematsfactory.com`，勾 Enforce HTTPS
3. 阿里云 DNS：4 条 A 记录（185.199.108–111.153）+ `www` CNAME → `<账号>.github.io`
4. `nslookup tpematsfactory.com` 验证 → GSC / Bing 提交 sitemap
5. 建 6 个 cron（isolated 会话）：站点存活 / sitemap 刷新 / 图片完整性 / meta 审计 / DNS+SSL / 趋势注入

---

## 5. 验证记录

| 校验 | 结果 |
|---|---|
| `python _verify_generate.py`（合成数据回归，含 `node --check` 内联 JS） | 全绿 |
| `python ../tools/audit_build.py`（真实构建审计：图片存在性、og 图、title/desc 唯一性、车型页与产品页双向链接、sitemap 完整性、占位 ID 泄漏） | 全绿 |
| `python ../tools/check_claims.py`（适配与年款的来源追溯、图片 md5 去重、认证类词扫描） | 全部通过 |
| 独立验证子代理对抗性复核 | 见下方遗留说明 |

**已知遗留**
- 40 个车型名是多车型合并（如 `Ranger / Escape / Mustang`、`H5 / H6 / H7 / H9`）——这是 listing 原文写法，已用 `/` 分隔表达「覆盖多个车型」，但每个车型没拆成独立页面。要拆的话告诉我。
- 未做真机 375px 渲染实测（响应式是按 CSS 规则断言的，非实测像素）。
- 8 个未解析车型的产品没有车型页。
