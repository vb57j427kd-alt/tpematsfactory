# tpematsfactory.com 上线手册

## ✅ 上线状态：已完成（2026-09-20）

| 项目 | 状态 |
|---|---|
| GitHub 仓库 | `vb57j427kd-alt/tpematsfactory`（Public） |
| 部署密钥 | `tpematsfactory-deploy`（Read/write）已添加 |
| 推送 | 已完成，`main` 分支，最新提交 `e6a795a` |
| GitHub Pages | 源 `main` / `/ (root)`；自定义域名 `tpematsfactory.com` 已保存 |
| 阿里云 DNS | 4 条 A + 1 条 www CNAME 已生效（原记录列表为空） |
| 线上实测 | `http://tpematsfactory.com/` → **200**，`Server: GitHub.com`；首页 / 车型索引 / 产品页 / `vehicles.json` / `sitemap.xml` 全部 200 |
| Enforce HTTPS | ⏳ 待证书签发后开启（已排一次性定时任务跟进） |

**线上验证用 DoH（不要用 nslookup）**

```
https://dns.google/resolve?name=tpematsfactory.com&type=A
→ 185.199.108.153 / .109.153 / .110.153 / .111.153
```

> ⚠️ **这台机器的局域网劫持了 UDP:53**：`nslookup`（哪怕指定 1.1.1.1 / 9.9.9.9 / 权威服务器）会被替换成同一个假 IP `59.82.113.122`，导致误判「DNS 没生效」。验证必须走 DoH，或直连真实 IP：
> ```
> curl.exe -sS -o NUL -w "%{http_code}" --resolve tpematsfactory.com:443:185.199.108.153 https://tpematsfactory.com/
> ```
> 你在自己电脑/手机上访问时如果打不开，先换个网络（比如手机流量）试。

---

## 0. 本地状态（已完成的）

```
仓库路径   C:\Users\sy911\AccioWork\2026-09-19-09-31-14-323-991e68d4\tpematsfactory-site
分支       main
提交       1224c32
作者身份   vb57j427kd-alt <vb57j427kd@privaterelay.appleid.com>   （沿用 BHT 仓库的身份）
```

**部署密钥（公钥，需要加到 GitHub 仓库的 Deploy keys）**

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMXCr1SgGCmDlT0n9RuvSMpk63IZvtUZHto8S76W7xMR tpematsfactory-deploy
```

私钥位置：`C:\Users\sy911\.ssh\id_ed25519_tpemats`（无密码短语）
指纹：`SHA256:mYfVvv4u8DnkmhgvwYeWIDCeeb5/LBMp3537bBi8W1g`

> 与既有密钥分开，便于按站点吊销。BHT 用 `id_ed25519_bht`，MJ 用 `id_ed25519_mahjongbest`。

---

## 1. 顺序很重要（官方明确警告）

**必须先在 GitHub 添加自定义域名，再去改 DNS。** 反过来做会有一段时间窗口，别人可以拿你的子域名去托管站点。

正确顺序：

1. 建仓库 → 2. 加部署密钥 → 3. 推送 → 4. 开 Pages + 填自定义域名 → 5. 配 DNS → 6. 开 Enforce HTTPS → 7. GSC/Bing 提交

---

## 2. GitHub

### 2.1 建仓库
- 账号：`vb57j427kd-alt`（与 BHT / MJ 同一账号）
- 仓库名：**`tpematsfactory`**
- 可见性：**必须 Public**（GitHub Free 计划下 Pages 只支持公开仓库；若账号是 Pro 可选私有）
- **不要**勾选自动生成 README / .gitignore / license（本地已有内容）

### 2.2 加部署密钥
仓库 → Settings → Deploy keys → Add deploy key
- Title：`tpematsfactory-deploy`
- Key：粘贴上面那串公钥
- ✅ **勾选 Allow write access**（否则无法 push）

### 2.3 推送

```powershell
cd C:\Users\sy911\AccioWork\2026-09-19-09-31-14-323-991e68d4\tpematsfactory-site
git remote add origin ssh://git@ssh.github.com:443/vb57j427kd-alt/tpematsfactory.git
git remote set-url --add --push origin ssh://git@ssh.github.com:443/vb57j427kd-alt/tpematsfactory.git
$env:GIT_SSH_COMMAND = 'ssh -i C:\Users\sy911\.ssh\id_ed25519_tpemats -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new'
git push -u origin main
```

> 首次推送建议先单独验证密钥：`ssh -i $env:USERPROFILE\.ssh\id_ed25519_tpemats -T git@ssh.github.com -p 443`
> 返回 `Hi vb57j427kd-alt/tpematsfactory! You've successfully authenticated...` 即通。

### 2.4 开 Pages
Settings → Pages
- Source：`Deploy from a branch`
- Branch：`main` / `/ (root)`
- Custom domain：`tpematsfactory.com` → Save
  （`CNAME` 文件仓库里已有，内容就是 `tpematsfactory.com`，GitHub 会直接认）
- 等 DNS 生效后勾 **Enforce HTTPS**（证书签发最长 24h）

---

## 3. 阿里云 DNS（NS 为 `dns7.hichina.com` / `dns8.hichina.com`）

域名当前**没有任何 A 记录**，属于干净状态，直接加以下记录即可：

| 记录类型 | 主机记录 | 记录值 | TTL |
|---|---|---|---|
| A | `@` | `185.199.108.153` | 10 分钟 |
| A | `@` | `185.199.109.153` | 10 分钟 |
| A | `@` | `185.199.110.153` | 10 分钟 |
| A | `@` | `185.199.111.153` | 10 分钟 |
| CNAME | `www` | `vb57j427kd-alt.github.io` | 10 分钟 |

可选 IPv6（要加就 4 条一起加，只加 IPv6 全球普及率低会漏访客）：
`2606:50c0:8000::153`、`2606:50c0:8001::153`、`2606:50c0:8002::153`、`2606:50c0:8003::153`

**注意事项**
- `www` 的 CNAME 必须指向 `vb57j427kd-alt.github.io`，**不要**带仓库名，也不要指向 `*.pages.github.io`
- 若阿里云自动塞了默认解析记录，先删掉
- **不要**用通配符 `*` 记录（域名接管风险）

验证：

```powershell
nslookup -type=A tpematsfactory.com
nslookup -type=CNAME www.tpematsfactory.com
```

---

## 4. 搜索引擎收录

1. Google Search Console → 添加资源（域名型验证，阿里云加 TXT）
2. 提交 `https://tpematsfactory.com/sitemap.xml`（94 条 URL）
3. Bing Webmaster Tools → 从 GSC 导入

---

## 5. 上线后建议加的定时任务（与 BHT/MJ 同模式，isolated 会话）

| 频率 | 任务 |
|---|---|
| 每日 | 站点存活 + HTTP 状态 + 首页 H1/产品卡计数 |
| 每日 | `sitemap.xml` 与实际页面数一致性比对 |
| 每日 | `images/` 完整性（图片 404 = 直接掉转化） |
| 每周 | meta/title 唯一性审计（可复用 `_verify_generate.py`） |
| 每周 | DNS + SSL 证书到期检查 |
| 每月 | 车型索引与店铺 listing 的差异比对（新品/下架同步） |

---

## 6.5 收录与性能优化记录（2026-09-20 补做）

### 收录 / 分析

| 项目 | 状态 |
|---|---|
| GA4 | ✅ `G-QH57L3C2J0`（新建，专属本站，未复用 BHT） |
| Microsoft Clarity | ✅ `yl2mwy2l99`（新建，专属本站） |
| Formspree | ❌ 未建——Formspree 只提供邮箱+密码登录，没有 GitHub SSO，需你登录一次 |
| Google Search Console | ✅ 域名资源已验证（DNS TXT `google-site-verification=F0AI1mPJBAPa2DBL7xmeSqZAK6L4Yw2lYd07-YriIL0`），sitemap 已提交，**99 个 URL 已被发现** |
| Bing Webmaster | ✅ 站点已验证（CNAME `95e24c04f74772eda13ae62939fc108f` → `verify.bing.com`），sitemap 已提交（Processing，0 错误 0 警告） |
| IndexNow | ✅ Bing 端点已接受（HTTP 202）；`api.indexnow.org` 从本机网络被连续切断（3 次 RemoteDisconnected），不影响 Bing 收录 |
| 站内邮箱 | ✅ `yale@tpematsfactory.com`（阿里云企业邮箱免费版）。MX / SPF / DKIM 控制台均「通过」，详见 6.6 |

### 打开速度（实测，非估计）

| 页面 | 优化前首屏 | 优化后 | 降幅 |
|---|---|---|---|
| 首页 | 884 KB | **143 KB** | −84% |
| 车型页 Honda CR-V | 126 KB | **39 KB** | −69% |
| 产品页 | 388 KB | **101 KB** | −74% |

做法：每个产品图生成 4 个变体（800px 全尺寸 JPG/WebP + 400px 卡片 JPG/WebP），页面用 `<picture>` 让浏览器自动取 WebP（不支持时回落 JPG）；卡片图中位数 85 KB → 18 KB；标题字体字重从 7 个减到 5 个（Oswald 500 无人使用，已删）；加 `.nojekyll` 免 Jekyll 处理。
注意：仓库总体积反而涨了（4.3 MB → 5.9 MB），因为四种变体都要入库——**换来的是访客下载量降了 84%**，这个 trade-off 值得。

### SEO / 排名

- 车型页与产品页新增 FAQ 区块 + `FAQPage` JSON-LD（**与可见内容同源生成，不可能漂移**）
- 4 个品类页新增导购正文（242–269 词/页），补足内容深度
- 新增 HTML 站点地图 `/site-map/`：99 个页面全索引，改善抓取路径与内链权重分配
- 新增 3 篇博客（1280 / 1031 / 1153 词），内链经程序校验**全部指向真实存在的页面，断链 0**
- IndexNow 验证文件 `9f2c7a41d68b4e53a1c0f7e29d34b856.txt` 已随站点发布并实测可访问

---

## 6.6 站内邮箱与邮件认证（2026-09-20）

**邮箱**：`yale@tpematsfactory.com` —— 阿里云企业邮箱免费版（¥0，实例 `alimailhzbc655255e1f540bc8861daa56b53e777`，到期 2027-09-21）。站点首页与产品页均有 `mailto:` 链接。

**收信**：MX → `mx1/mx2/mx3.qiye.aliyun.com`（优先级 5 / 10 / 15）；SPF `v=spf1 include:spf.qiye.aliyun.com -all`。

**DKIM**：`default._domainkey` TXT 记录已发布，控制台验证状态 **通过**（原为未通过）。

```
记录类型  TXT
主机记录  default._domainkey
记录值    v=DKIM1; k=rsa; p=MIIBIjANBgkqh…（2048 位 RSA，共 411 字符）
TTL       600
```

发布前后的独立校验（`python ../tools/verify_dkim.py`，可重复运行）：

| 校验项 | 结果 |
|---|---|
| 公网解析（阿里云 DoH，绕开本机 UDP:53 劫持） | 记录存在 |
| 解析值 vs 控制台读到的值，逐字符比对 | **完全一致（411 / 411 字符）** |
| `p=` 部分 base64 解码 | 294 字节合法 SPKI |
| RSA 模数位长 | **2048 位**（这一步才能排除"看着正常但被静默截断"） |
| 邮箱控制台「立即验证」 | **通过** |
| MX / SPF / google-site-verification / 4 条 A 记录 | 全部未被扰动 |

> ⚠️ **本机可用的 DoH 端点只有一个**：`dns.google` 与 `cloudflare-dns.com` 从这台机器**直连不通**（curl exit 28 / Python WinError 10060）。
> 可用的是 **`https://dns.alidns.com/resolve?name=<域名>&type=<类型>`**（带 `accept: application/dns-json`）。
>
> ⚠️ **长 TXT 记录会分片返回**成 `"chunk1" "chunk2"` 两段。比对前必须把分片拼起来（去掉引号、**中间不插空格**），
> 否则 411 字符的 DKIM 值会被误判成"值不一致"。

---

## 7. 回滚

站点是纯静态 + Git 管理，回滚就是 `git revert` 或 `git reset --hard <commit>` 后强推。
DNS 回滚：删掉 5 条记录即可（域名本身就注册在阿里云，不存在赎回风险）。
