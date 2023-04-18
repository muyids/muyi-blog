**背景**

最近遇到一个需求，需要将纸质文件用扫描仪扫描后，得到一组图片，然后将图片上的内容解析并生成一整张 pdf 文件，进行存档，要求图片上的文本格式基本不变，并且输出的 pdf 文件是可编辑的

**需求分析**

我们从技术方面进行剖析：

首先，图片上的文字要提取出来，这时候我们需要 OCR 识别技术解析得到图片上的文本内容；

然后，我们需要把文本尽量按照原图片格式输出到 pdf 文件中

最后，将 pdf 文件进行拼接，形成一整张归档 pdf 文件

**技术调研和选型**

关于 OCR 技术的方案，我们大致有两种选择：

1. 依赖百度等大型互联网公司提供的三方服务
2. 借助开源软件
   前者的优势在于专业的人做专业的事情，大厂的技术积淀胜过我们瞎折腾，而且开发起来更快捷，缺点在于需要付费；后者优势是不需要额外费用，缺点需要我们去搭建一些环境，去折腾一番，需要一定的开发资源

关于 pdf 的操作：这里开发可以根据自己使用的编程语言选择 pdf 操作库，我们使用了 java 语言实现，选择了社区较为活跃成熟的`itextpdf`库

**开发阶段**

**1.OCR 实现**

购买三方服务根据对应的服务提供商的开发文档和提供的 SDK 进行操作即可，这里我们不再赘述；

下面，我们简单介绍一下[`tesseract-ocr`](https://github.com/tesseract-ocr/tesseract/)环境的搭建和使用，参考[文档地址](https://github.com/tesseract-ocr/tessdoc)

这里，我们在`mac os`系统上使用`homebrew`安装，执行命令`brew install tesseract`，安装完成后，使用

`tesseract --version` 查看是否成功安装，其他操作系统环境或者安装失败请参考网上教程安装

安装成功后，我们先截取一张英文图片进行测试：

![image-20210913090033002](https://muyids.oss-cn-beijing.aliyuncs.com/image-20210913090033002.png)

可以看到英文的识别成功率几乎 100%。

下面我们进行中文识别，tesseract 默认安装了英文训练数据包，中文识别需要我们额外配置我们的训练数据包。这里我们从官方开源的 github 仓库下载数据集，地址为：https://github.com/tesseract-ocr/tessdata；

下载完成后，将我们的数据包复制到指定位置，我的数据包安装位置在`/usr/local/Cellar/tesseract/4.1.1/share/tessdata`，复制完成后，使用命令`tesseract --list-langs`来检测安装了哪些语言包，可以看到官方提供了非常多语言的数据集，其中 chi_sim 表示中文简体，eng 表示英文。

下面我们来测试一下中文的识别情况吧！

![2021-09-13 am9.08.41](https://muyids.oss-cn-beijing.aliyuncs.com/2021-09-13 am9.08.41.png)

可以看到，识别情况并不是很理想，我们还需要进行训练优化我们的数据集。有兴趣的朋友可以参考文档[数据训练](https://github.com/tesseract-ocr/tessdoc/blob/main/tess4/TrainingTesseract-4.00.md)尝试优化。

**2.写入 pdf 文档**

首先**引入 jar 包**

```xml
<!-- https://mvnrepository.com/artifact/com.itextpdf/itextpdf -->
<dependency>
  <groupId>com.itextpdf</groupId>
  <artifactId>itextpdf</artifactId>
  <version>5.5.13.2</version>
</dependency>
```

itextpdf 工具包提供了使用 ocr 接口引擎创建 pdf 文件的 API：OcrPdfCreator，构造方法如下：

```java

    /**
     * Creates a new {@link OcrPdfCreator} instance.
     *
     * @param ocrEngine selected OCR Reader {@link IOcrEngine}
     * @param ocrPdfCreatorProperties set of properties for {@link OcrPdfCreator}
     */
    public OcrPdfCreator(final IOcrEngine ocrEngine,
            final OcrPdfCreatorProperties ocrPdfCreatorProperties) {
        setOcrEngine(ocrEngine);
        setOcrPdfCreatorProperties(ocrPdfCreatorProperties);
    }

```

我们的 ocr 引擎使用的是`tesseract`，引入 pdfocr 操作 tesseract 的依赖

```xml
<!-- https://mvnrepository.com/artifact/com.itextpdf/pdfocr-tesseract4 -->
<dependency>
  <groupId>com.itextpdf</groupId>
  <artifactId>pdfocr-tesseract4</artifactId>
  <version>1.0.3</version>
</dependency>
```

最终我们得到了如下代码：

```java
public class TestPdf {
    static final Tesseract4OcrEngineProperties tesseract4OcrEngineProperties = new Tesseract4OcrEngineProperties();
    private static final String TESS_DATA_FOLDER = "/usr/local/Cellar/tesseract/4.1.1/share/tessdata";
    private static List LIST_IMAGES_OCR = Arrays.asList(new File("en.png"));
    private static String OUTPUT_PDF = "en.pdf";
    public static void main(String[] args) throws IOException {
        final Tesseract4LibOcrEngine tesseractReader = new Tesseract4LibOcrEngine(tesseract4OcrEngineProperties);
        tesseract4OcrEngineProperties.setPathToTessData(new File(TESS_DATA_FOLDER));
//        tesseract4OcrEngineProperties.setLanguages(Arrays.asList("chi_sim"));
        OcrPdfCreatorProperties properties = new OcrPdfCreatorProperties();
//        properties.setPdfLang("zh");
        properties.setTextColor(DeviceRgb.RED);
        properties.setTextLayerName("text");
        properties.setImageLayerName("image");

        OcrPdfCreator ocrPdfCreator = new OcrPdfCreator(tesseractReader, properties);
        try (PdfWriter writer = new PdfWriter(OUTPUT_PDF)) {
            ocrPdfCreator.createPdf(LIST_IMAGES_OCR, writer).close();
        }
    }
}
```

参考文档：https://itextpdf.com/en/blog/technical-notes/how-use-itext-pdfocr-recognize-text-scanned-documents

最终实现效果如下（上层红色的文本层是我们进行 OCR 识别后写入到 pdf 文件中的，支持编辑）：

![2021-09-13 am9.27.44](https://muyids.oss-cn-beijing.aliyuncs.com/2021-09-13 am9.27.44.png)

**3.pdf 文件合并操作**

```java
/**
 * 合并pdf文件
 * @param files 要合并文件数组(如{ "1.pdf", "2.pdf", 3.pdf"}),合并的顺序按照数组中的先后顺序，如2.pdf合并在1.pdf后。
 * @param newfile 合并后新产生的文件路径，如 tempNew.pdf,
 * @return boolean 合并成功返回true；否则，返回false
 */
@Override
public boolean mergePdfFiles(String[] files, String newfile) {
  boolean retValue = false;
  Document document = null;
  try {
    document = new Document(new PdfReader(files[0]).getPageSize(1));
    PdfCopy copy = new PdfCopy(document, new FileOutputStream(newfile));
    document.open();
    for (int i = 0; i < files.length; i++) {
      PdfReader reader = new PdfReader(files[i]);
      int n = reader.getNumberOfPages();
      for (int j = 1; j <= n; j++) {
        document.newPage();
        PdfImportedPage page = copy.getImportedPage(reader, j);
        copy.addPage(page);
      }
    }
    retValue = true;
  } catch (Exception e) {
    System.out.println(e);
  } finally {
    System.out.println("执行结束");
    document.close();
  }
  return retValue;
}
```
