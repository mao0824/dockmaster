# dockmaster — 手搓群晖 NAS 导航页

一个**单文件手搓**的 NAS 服务导航页:Docker 一键部署,自适应内网/公网,实时服务状态灯,零第三方依赖(python 标准库即可运行)。

## 特性

- 🌗 **内网/公网自适应**——按访问域名自动切换服务地址;没有公网转发的服务自动置灰标记「仅内网」
- 🟢 **实时状态灯**——服务端(容器内)对每个服务端口做 TCP 探测,每 20 秒刷新,内外网结果都准确
- 📱 手机自适应,深色主题,零外部资源(无 CDN/字体/图标请求)
- 🐳 compose 一键部署,自带 healthcheck 与日志轮转,内存占用 ~15MB

## 快速开始

```bash
git clone https://github.com/mao0824/dockmaster.git
cp config.example.json config.json   # 生成你自己的配置(更新不会覆盖)
cd dockmaster
cd dockmaster
docker compose up -d --build
```

浏览器访问 `http://NAS_IP:13002`。

## 配置

一切都在 **`config.json`**,改完刷新页面即生效(热加载),无需重启容器:

| 字段/文件 | 作用 |
|---|---|
| `title` | 页面标题 |
| `port` | 服务监听端口(默认 13002;改后需重启一次容器) |
| `services[]` | 服务卡片:`icon` 图标、`name` 名称、`port` 状态探测端口、`lan` 内网地址、`wan` 公网地址(**留空或不填 = 仅内网**) |
| `links[]` | 常用站快捷链接 |

内网/公网判定逻辑:访问域名是 `192.168.*`、`localhost`、`*.local` 时走内网地址,其余(公网域名)走公网地址。

## 群晖部署注意

## 群晖部署注意

- 使用 `network_mode: host`:容器内的 `127.0.0.1` 才能探测到宿主机上各服务的端口(桥接网络探测全部失联,这是踩过的坑)
- 适合在 Container Manager 里登记为项目,方便 UI 管理
- 建议在路由器将 13002 端口转发,即可在外网使用公网模式

## License

MIT
