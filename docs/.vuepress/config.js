module.exports = {
  title: "木易", // HTML的title
  description: "闻道有先后，术业有专攻", // 描述
  // tagline: 青春年少正当时，努力莫负好韶华
  keywords: "算法，跑步，编程", // 关键字
  head: [
    // 配置头部
    [
      [
        "link",
        {
          rel: "icon",
          href: "https://muyids.oss-cn-beijing.aliyuncs.com/run.jpeg",
        },
      ],
      [
        "meta",
        {
          name: "viewport",
          content:
            "width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0;",
        },
      ],
    ],
  ],
  markdown: {
    lineNumbers: true, // 代码显示行号
    externalLinks: {
      target: "_blank",
    },
    extendMarkdown: (md) => {
      md.set({
        html: true,
      });
      md.use(require("markdown-it-katex"));
    },
  },
  head: [
    [
      "link",
      {
        rel: "stylesheet",
        href: "https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.7.1/katex.min.css",
      },
    ],
    [
      "link",
      {
        rel: "stylesheet",
        href: "https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/2.10.0/github-markdown.min.css",
      },
    ],
  ],
  dest: "./public", // 设置打包路径
  lastUpdated: "Last Updated", // 显示更新时间
  themeConfig: {
    smoothScroll: true,
    logo: "https://muyids.oss-cn-beijing.aliyuncs.com/run.jpeg", // 导航栏左边logo,不写就不显示
    nav: require("./nav"),
    // 为以下路由添加侧边栏
    sidebarDepth: 2, // 侧边栏显示2级
    sidebar: require("./sidebar"),
  },
  plugins: [
    // 'axios'  // 配置插件
    [
      "@vuepress/search",
      {
        searchMaxSuggestions: 10,
      },
    ],
  ],
};
