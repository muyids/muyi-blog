修改 ingress nginx 请求头大小即可解决

```
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/proxy-body-size: 20m
    nginx.ingress.kubernetes.io/server-snippet: client_header_buffer_size 2046k;
```
