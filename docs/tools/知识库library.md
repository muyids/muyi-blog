## Calibre-web ebook on k8s

https://github.com/janeczku/calibre-web

## 本地搭建

conda create -n py-calibre

conda activate py-calibre

conda install python=3.9

pip install calibreweb

cps

Point your browser to http://localhost:8083

Default admin login:
Username: admin
Password: admin123

选择 DB

报错： DB location is not valid, please enter correct path · Issue #30 · linuxserver/docker-calibre-web

因为 没有生成 metadata.db

下载 或 创建 metadata.db ，选择即可

拷贝主机文件到 pods
k cp metadata.db -n project-calibre -c release-name-calibre-web release-name-calibre-web-755f464458-mlbjv:/books/metadata.db
开启上传 books 功能

配置 LDAP Login

https://github.com/janeczku/calibre-web/wiki/LDAP-Login

https://github-wiki-see.page/m/janeczku/calibre-web/wiki/LDAP-Login

配置参考：Calibre Web

K8S Helm Charts

搜索 Charts

helm search hub -o json calibre | jq '.'

选择 Charts

{
"url": "https://artifacthub.io/packages/helm/truecharts/calibre",
"version": "7.0.10",
"app_version": "5.44.0",
"description": "Calibre is a powerful and easy to use e-book manager.",
"repository": {
"url": "https://charts.truecharts.org/",
"name": "truecharts"
}
}
helm repo add truecharts https://charts.truecharts.org/

helm install my-calibre truecharts/calibre --version 7.0.10

拉取到本地

helm pull truecharts/calibre-web --untar

Storage Class 选择 performance

权限控制

Allow&Deny Tag 机制

使用 Tags 的 Allow 和 Deny 机制 实现权限控制。

场景举例：

数据价值团队 要上传一份内部资料，部门外部人员无权限访问；

我们对数据价值团队以外的所有 members 增加 Deny Tag : 数据价值内部资料；

当我们要标识一份 资料为 数据价值团队内部资料时，将这份资料打上标签 ”数据价值团队内部资料“ 就可以实现 只有 数据价值团队成员可以访问的效果。

增加 tag
#!/bin/bash
set -ex
for i in {92..99}
do # 增加 tag
curl 'https://library.data-exchange.aibee.cn/ajax/addrestriction/2/'$i \
 -H 'authority: library.data-exchange.aibee.cn' \
 -H 'accept: _/_' \
 -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8' \
 -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \
 -H 'cookie: \_ga=GA1.2.1959650803.1654586228; ajs_user_id=83c0c771-4d14-59ce-8967-d1e9caac708c; ajs_anonymous_id=19615aed-8525-4e33-96b9-e119c2c22ffd; rl_page_init_referrer=RudderEncrypt%3AU2FsdGVkX1%2FFwnfPnPwpR3Rqxj2SSRZJgEdLwPKt7l8%3D; rl_page_init_referring_domain=RudderEncrypt%3AU2FsdGVkX1%2BhKADQV3s3Z8J%2BiI7uhjzcTGb0lkb14bU%3D; rl_anonymous_id=RudderEncrypt%3AU2FsdGVkX19wI93kk51zl4hwhtlKgP3tzY792UiSs3P3xhi9zEPSJ89uGXU%2BpEXiQdcSO4%2FvOW2QmD504n1XTw%3D%3D; rl_user_id=RudderEncrypt%3AU2FsdGVkX1%2BVZjfZuL6VEShdGe4ibj0brIiLt%2F6rNNMUsNqz6KtZ39IuIKJt7BC9wS8LgFr8AmmwWIfon8ICVHwpnGgNAj7SJbkYjW5rm4LWJaIFYyZ9U5YgZGsE%2Fv51; remember_token=1|06b87c491948fb937f77c4d9dd83a32922a1ac206cb40f3f093328b0e489e0a638fe67d3a636d06c54e31c46d4d386c4598a1c1ad0edc792ec6531221a055cf8; session=.eJwljklqA0EMAP_SZx-kXqSWPzO0NhIMCczYJ-O_pyHHqkNR73LkGddXuT_PV9zK8e3lXii9AlukrSBsqDyCvbFBAELnHEwCodCqi9WhC21glRa2kLpEw-gJ1BLRQIYsZlVvtiiZ0FHqTmgGGtfOxkt1ESf1yZNjlj3yuuL8v8GNdp15PH8f8bPF7EBTCOsu9ll9BQ-akCE-SDmz-hBoUT5_9m0_Ng.YrsDPA.SEey-VPqgSYz9FfP7IMZKuiqZkA' \
 -H 'origin: https://library.data-exchange.aibee.cn' \
 -H 'referer: https://library.data-exchange.aibee.cn/admin/user/'$i \
 -H 'sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"' \
 -H 'sec-ch-ua-mobile: ?0' \
 -H 'sec-ch-ua-platform: "macOS"' \
 -H 'sec-fetch-dest: empty' \
 -H 'sec-fetch-mode: cors' \
 -H 'sec-fetch-site: same-origin' \
 -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36' \
 -H 'x-csrftoken: Ijg0MDY4OTYxMmQzYzQ4MmRhZTc1NjgwZmU5ZDU2YjdmZjJkNTkwM2Ui.YrsDNg.gE8Su9Z2Q3Nd-Dbe0KHACdDqZA8' \
 -H 'x-requested-with: XMLHttpRequest' \
 --data-raw 'add_element=%E7%A7%81%E6%9C%89&submit_deny=' \
 --compressed
done

删除 tag

#!/bin/bash

set -ex
for i in {2..565}
do # 删除 Tag
curl 'https://library.data-exchange.aibee.cn/ajax/deleterestriction/2/'$i \
 -H 'authority: library.data-exchange.aibee.cn' \
 -H 'accept: _/_' \
 -H 'accept-language: zh-CN,zh;q=0.9' \
 -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \
 -H 'cookie: remember_token=1|06b87c491948fb937f77c4d9dd83a32922a1ac206cb40f3f093328b0e489e0a638fe67d3a636d06c54e31c46d4d386c4598a1c1ad0edc792ec6531221a055cf8; session=.eJwljsGqAjEMAP-lZw9J2ySNP7M0aYIiKOzqSfz3t_COM4dhvmXLPY5bub73T1zKdl_lWjhXBfFIn8HY0IRCVhOHAIQuScIKYdDqUq9kE52wagufyF2jYfQEbonooKRTxGw1n5zCuFDrmbAMdKldXKbZZEnuQ4bEKOfI54j9_wZP9GPP7f16xPMUNqlzp4HMw0V741HVadVBS3CkBziBUfn9AfDBPtE.YrsKtQ.fgwr0PFsWcDTmrqg4u0sH1wnkBs' \
 -H 'origin: https://library.data-exchange.aibee.cn' \
 -H 'referer: https://library.data-exchange.aibee.cn/admin/user/'$i \
 -H 'sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"' \
 -H 'sec-ch-ua-mobile: ?0' \
 -H 'sec-ch-ua-platform: "macOS"' \
 -H 'sec-fetch-dest: empty' \
 -H 'sec-fetch-mode: cors' \
 -H 'sec-fetch-site: same-origin' \
 -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36' \
 -H 'x-csrftoken: ImJhNTQ2NDU4MTY2OGM3OTQzNjgyOWM1ZDI4NWQ3MThmY2UwYzUwYjUi.YrsKsg.bvK9w6GLv8Owl0IRurapXAwQTLU' \
 -H 'x-requested-with: XMLHttpRequest' \
 --data-raw 'id=d0&type=Deny&Element=%E7%A7%81%E6%9C%89' \
 --compressed
done

标签维护

成员维护

需要动态维护 公司所有成员 标签

原则：

1. 以数据安全为优先原则，保证 Deny 优先于 Allow
2. 不确定的情况，一律使用 Deny
   多种情况：

3. 公司入职新人
4. 增加所有 Deny 标签
5. 成员加入团队
6. 首先，按新人入职处理，添加所有 Deny
7. 将 所在团队内部标签从 Deny Set 移除
8. 成员离开团队
