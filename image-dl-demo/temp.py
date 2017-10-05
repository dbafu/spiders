from urllib import request 
import re
import zlib
from io import BytesIO

img_urls = ['https://a1.jikexueyuan.com/home/201604/28/3f10/57216b7d1ac79.jpg','https://a1.jikexueyuan.com/home/201604/20/7883/5717574c478e6.jpg','https://a1.jikexueyuan.com/home/201604/18/afbb/57144fb5d7336.jpg','https://a1.jikexueyuan.com/home/201604/14/99ca/570f03bc14c9e.jpg','https://a1.jikexueyuan.com/home/201604/12/545c/570c5c6d6707c.jpg','https://a1.jikexueyuan.com/home/201603/24/c8c9/56f35c7525600.jpg','https://a1.jikexueyuan.com/home/201605/13/62a0/57357fa98c62c.png','https://a1.jikexueyuan.com/home/201603/15/1367/56e76cf3a0c86.jpg','https://a1.jikexueyuan.com/home/201603/03/aa32/56d7a48f1e972.jpg','https://a1.jikexueyuan.com/home/201602/22/6fb0/56ca71ff9d11c.jpg','https://a1.jikexueyuan.com/home/201602/15/6740/56c17789aee50.jpg','https://a1.jikexueyuan.com/home/201602/03/3f64/56b10922cf909.jpg','https://a1.jikexueyuan.com/home/201601/28/b014/56a9793756358.jpg','https://a1.jikexueyuan.com/home/201601/20/03bc/569eea58d14af.jpg','https://a1.jikexueyuan.com/home/201601/14/4d2b/569708c8cdfe3.jpg','https://a1.jikexueyuan.com/home/201512/21/524f/5677591a95318.jpg','https://a1.jikexueyuan.com/home/201512/18/eb0f/56736e50049bb.jpg','https://a1.jikexueyuan.com/home/201512/04/6f16/56610abc695b5.jpg','https://a1.jikexueyuan.com/home/201512/03/a06d/565faa8e7b4ca.jpg','https://a1.jikexueyuan.com/home/201511/24/fc70/5653c629976bf.jpg','https://a1.jikexueyuan.com/home/201511/19/d7a3/564d2b9a132b3.jpg','https://a1.jikexueyuan.com/home/201509/23/dd7b/56020a66eef96.jpg','https://a1.jikexueyuan.com/home/201509/15/898b/55f7775a6044d.jpg','https://a1.jikexueyuan.com/home/201509/11/4f8f/55f2354f0d63b.jpg']

i=0

for each in img_urls:
    print(''+each)
    req = request.urlopen(each)
    buf = req.read()
    bio = BytesIO(buf)
    bufstr = zlib.decompress(buf, zlib.MAX_WBITS|32)
    with open('pic/%s.jpg'%str(i), 'wb') as f:
        f.write(bufstr)
    i+=1