# youdaoDictation

有道听写

依赖有道词典web实现英语单词的听写

依赖库：

+ requests
+ bs4
+ mp3play(需修改以适应python3.x)

## mp3play for python3.x

```python
class _mci:
    def __init__(self):
        self.w32mci = windll.winmm.mciSendStringA
        self.w32mcierror = windll.winmm.mciGetErrorStringA

    def send(self, command):
        buffer = c_buffer(255)
        command=command.encode(encoding="utf-8")  # add this line
        
        errorcode = self.w32mci(command, buffer, 254, 0)  # remove str()
        if errorcode:
            
            return errorcode, self.get_error(errorcode)
        else:
            return errorcode, buffer.value

    def get_error(self, error):
        error = int(error)
        buffer = c_buffer(255)
        self.w32mcierror(error, buffer, 254)
        return buffer.value

    def directsend(self, txt):
        (err, buf) = self.send(txt)
        if err != 0:
            print ('Error %s for "%s": %s' % (str(err), txt, buf)) # print -> print()
        return (err, buf)
```

reference in this section

> https://www.cnblogs.com/XingzhiDai/p/11654484.html

