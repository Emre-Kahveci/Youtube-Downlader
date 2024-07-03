<h1 align="center" id="title">Youtube Downloader</h1>

![Youtube-Downlader](https://socialify.git.ci/Emre-Kahveci/Youtube-Downlader/image?font=Jost&language=1&name=1&pattern=Charlie%20Brown&theme=Dark)
<div align="center">

  <a href="">![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)</a>
  <a href="">![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)</a>
</div>

## Youtube Downloader

**Youtube Downloader**, YouTube'dan video veya shorts indirmenizi sağlayan bir araçtır. Kullanıcıların videoları veya ses dosyalarını istenilen format ve çözünürlükte indirmesine olanak tanır.

## Özellikler

- **Video İndirme**: MP4 ve WEBM formatlarında video indirme.
- **Ses İndirme**: MP3, MP4 ve WEBM formatlarında ses dosyası indirme.
- **Çözünürlük ve Kalite Seçimi**: Videoları ve ses dosyalarını farklı çözünürlük ve bit rate (ABR) seçenekleriyle indirme.

## Kullanılan Kütüphaneler/Modüller

Bu projede aşağıdaki Python kütüphaneleri kullanılmıştır:

- `pytube`
- `customtkinter`
- `ffmpeg`

## Kurulum

Projeyi kullanabilmeniz için bilgisayarınızda `ffmpeg` yüklü ve PATH'e eklenmiş olmalıdır. Kurulumun doğru yapıldığını kontrol etmek için komut istemcisine `ffmpeg` yazarak test edebilirsiniz.

### Adımlar

1. **Depoyu Klonla**:
    ```sh
    git clone https://github.com/kullanici-adi/youtube-downloader.git
    cd youtube-downloader
    ```

2. **Gereksinimleri Yükle**:
    ```sh
    pip install -r requirements.txt
    ```

## Kullanım

1. Programı başlatın.
2. İndirmek istediğiniz YouTube video veya shorts linkini giriş (entry) kısmına yapıştırın.
3. Video veya ses türünden birini seçin.
4. Kalite veya bit rate (ABR) seçimini kalite combobox'ından yapın.
5. "İndir" butonuna tıklayın.

