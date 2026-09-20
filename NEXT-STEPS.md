# tpematsfactory.com — 本轮进展与剩余事项（2026-09-20）

> **站点已上线**：https://tpematsfactory.com（GitHub Pages，仓库 `vb57j427kd-alt/tpematsfactory`）
> 本轮完成：代建分析工具、打开速度优化、搜索引擎收录、内容建设、排名优化。
> 详细运维记录见 [DEPLOY.md](DEPLOY.md)。

---

## 1. 站点现状

| 项目 | 数量 / 状态 |
|---|---|
| 页面总数 | **99**（首页 1 + 品类 4 + 产品 51 + 车型 37 + 车型索引 1 + 站点地图 1 + 博客 4） |
| 产品 / 车型 | 51 款 / 37 个 `/shop-by-vehicle/{make}/{model}/` |
| 图片 | 51 张 × 4 变体（800px JPG/WebP + 400px 卡片 JPG/WebP），站点内零重复 |
| 内链 | 站内地图页全量索引；博客内链经程序校验 0 断链 |
| 结构化数据 | Organization / CollectionPage / Product+additionalProperty / BreadcrumbList / **FAQPage** |
| 分析 | GA4 `G-QH57L3C2J0` + Clarity `yl2mwy2l99`（均已上线注入，实测确认） |

---

## 2. 打开速度：首页 884 KB → 143 KB（−84%）

| 页面 | 前 | 后 | 降幅 |
|---|---|---|---|
| 首页 | 884 KB | 143 KB | −84% |
| 车型页 | 126 KB | 39 KB | −69% |
| 产品页 | 388 KB | 101 KB | −74% |

关键动作是图片：卡片图从 85 KB 降到 18 KB，并用 `<picture>` 让浏览器自动选 WebP。

---

## 3. 收录情况

| 渠道 | 状态 |
|---|---|
| Google Search Console | ✅ 域名资源验证通过（DNS TXT）+ sitemap 已提交，**99 URL 已发现** |
| Bing Webmaster | ✅ CNAME 验证通过 + sitemap 已提交（Processing，0 错误） |
| IndexNow | ✅ Bing 端点返回 202（已受理） |
| robots.txt / sitemap.xml | ✅ 均在线，robots 指向 sitemap |

---

## 4. 内容与排名

- 3 篇博客（1280 / 1031 / 1153 词）：TPE vs PVC vs 橡胶选材、定制脚垫下单前的核对清单、OEM 从开模到装柜
- 4 个品类页导购正文（242–269 词）：直接回答「这个品类适合什么、下单前要确认什么、和隔壁品类的区别」
- 车型页 / 产品页 FAQ 区块 + FAQPage 结构化数据，**与可见文案同源生成**
- HTML 站点地图 `/site-map/`：99 页全索引，方便爬虫与内链

**主要页面盯的词**（供你后续投放参考）

| 落地页 | 主攻意图 |
|---|---|
| 车型页 `/shop-by-vehicle/{make}/{model}/` | `{make} {model} floor liners` / `tpe floor mats for {model}`（最高价值，买家意图最明确） |
| 品类页 `/floor-liners/` | `3d tpe car floor liners` / `custom fit car mats wholesale` |
| 产品页 | 长尾 + 车型组合，承接车型页分配的内部权重 |
| 博客 | 上游信息型检索（选材、验货、OEM 流程），把流量导向车型页与询盘 |

---

## 5. ⚠️ 待处理事项（第 3 项已完成）

| # | 事项 | 说明 |
|---|---|---|
| 1 | **模具清单**（Make / Model / 年款区间 / 左右舵） | 目前 33/37 个车型没有年款（标题里本来就没写），**留空未推测**。这是车型索引最大的短板 |
| 2 | **Formspree 表单后端** | 两次受阻：① Formspree 注册页**没有任何 SSO**（只有邮箱+密码），② 第二次尝试时 **Chrome 的 Accio Browser Relay 断连**，表单填到一半中断。**不影响接询盘**（WhatsApp 按钮 + 邮件都已可用）。恢复中继后我可以重试；或你自己注册 2 分钟搞定 |
| 3 | ~~站内邮箱~~ **已完成** | ✅ 阿里云企业邮箱免费版（¥0，51 账号，到期 2027-09-21），站点邮箱 **`yale@tpematsfactory.com`**。MX / SPF / **DKIM** 三项在控制台均为「通过」。DKIM 记录 `default._domainkey`（2048 位 RSA）已发布，与控制台取值逐字符比对一致、公网解析实测生效。**外发被判垃圾邮件的风险已消除** |
| 4 | **Enforce HTTPS** | 证书仍在签发（GitHub 处理中），已排一次性定时任务：签发后自动帮你勾上 |

---

## 6. 验证记录

| 校验 | 结果 |
|---|---|
| `python _verify_generate.py`（合成回归 + `node --check`） | 全绿 |
| `python ../tools/audit_build.py`（真实构建 25 项） | 全绿 |
| `python ../tools/check_claims.py`（适配/年款来源追溯 + 图片 md5 + 认证词扫描） | 通过：年款全部可回溯标题原文、102 张图零重复组、认证类词零命中 |
| `python ../tools/perf_report.py`（首屏重量，按浏览器实际选择计） | 见上表 |
| 上线前真机渲染（1440 / 375） | 定位并修复 3 个 P0（见 DEPLOY.md 与提交历史） |
| 独立验证子代理 | 确认 boilerplate 适配结论、零编造价格/MOQ；指出并已修 8 类问题 |

---

## 7. 已知遗留（不影响上线）

- 多车型合并的车型名（如 `Ranger / Escape / Mustang`、`H5 / H6 / H7 / H9`）未拆成独立页面——按 listing 原文如实呈现，用 `/` 区分
- 8 个未解析出车型的产品只挂在品类页，没有车型页
- `api.indexnow.org` 从本机网络不可达（Bing 端点正常）
- 未做 GSC/Bing 之外的中文搜索引擎提交（百度需单独账号与主动推送 token）
