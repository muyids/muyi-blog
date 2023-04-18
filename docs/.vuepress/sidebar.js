//  docs/.vuepress/sidebar.js
// module.exports = {
//   '/api/front/2019/': require('../.vuepress/frontbar/2019'),  // 继续分类
//   '/api/front/2020/': require('../.vuepress/frontbar/2020'),
//   '/api/end/2019/': require('../.vuepress/endbar/2019'),
//   '/api/learn/koa/': require('../.vuepress/learnbar/koabar'),
//   '/api/learn/express/': require('../.vuepress/learnbar/expressbar'),
//   '/api/learn/java/': require('../.vuepress/learnbar/javabar'),
//   '/api/learn/es6/': require('../.vuepress/learnbar/es6bar'),
//   '/api/learn/vue/': require('../.vuepress/learnbar/vuebar'),
// }

module.exports = {
  // '/middleware/': require('./toc/middleware'),
  // '/java/': require('./toc/java'),
  // '/javascript/': require('./toc/javascript'),
  // '/blogs/': require('./toc/blogs'),
  // '/system/': [
  //   [ '/system/0.前言.md', '前言' ],
  //   [ '/system/1.用户系统设计.md', '用户系统设计' ],
  //   [ '/system/2.设计一个短网址系统.md', '短网址系统设计' ]
  // ],
  "/算法/": require("./toc/alg"),
  "/run/": require("./toc/run"),
};
