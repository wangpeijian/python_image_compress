# python_image_compress
python脚本实现批量图片压缩

### 运行项目
`$path`为需要压缩文件的根目录，脚本自动遍历目录扫描要压缩的文件。小于10K的文件不压缩
输出目录为`$path`同级目录，添加`_compress`后缀。

```
python src -d $path 
```

### 注册账号
使用项目需要注册`https://tinypng.com`账号配置 API key, 配置文件在`/src/config/system`下