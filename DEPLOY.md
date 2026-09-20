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

## 6. 回滚

站点是纯静态 + Git 管理，回滚就是 `git revert` 或 `git reset --hard <commit>` 后强推。
DNS 回滚：删掉 5 条记录即可（域名本身就注册在阿里云，不存在赎回风险）。
