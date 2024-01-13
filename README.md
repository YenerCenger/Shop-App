# Dukkan Uygulaması

Bu, Flask ve SQLAlchemy kullanılarak oluşturulmuş basit bir alışveriş uygulamasıdır. Kullanıcılar, ürünleri görüntüleyebilir, satın alabilir ve yönetebilir.

## Başlarken

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları takip edin.

### Gereksinimler

- Python yüklü olmalıdır.

### Kurulum

1. Projeyi klonlayın:

    ```bash
    git clone https://github.com/kullanici/DukkanUygulamasi.git
    ```

2. Proje dizinine gidin:

    ```bash
    cd DukkanUygulamasi
    ```

3. Gerekli bağımlılıkları yükleyin:

    ```bash
    pip install -r requirements.txt
    ```

4. Uygulamayı başlatın:

    ```bash
    python app.py
    ```

## Kullanım

1. **Uygulamayı Çalıştırma:**

    - Bir terminal veya komut istemcisini açın ve `app.py` dosyasının bulunduğu dizine gidin.
    - Aşağıdaki komutu çalıştırın:

        ```bash
        python app.py
        ```

    - Uygulama `http://127.0.0.1:5000/` adresinden erişilebilir.

2. **Ana Sayfa:**

    - Tarayıcınızdan `http://127.0.0.1:5000/` adresine gidin.
    - Ürünleri görüntüleyin ve alışveriş yapın.

3. **Ürün Ekleme:**

    - Ürün eklemek için uygun formu doldurun ve "Ekle" düğmesine tıklayın.

4. **Ürünleri Yönetme:**

    - Ürünleri düzenlemek veya silmek için ilgili bağlantılara tıklayın.

## Katkıda Bulunma

1. Bu depoyu fork edin.
2. Yeni bir özellik dalı oluşturun: `git checkout -b yeni_özellik`
3. Değişikliklerinizi kaydedin: `git commit -am 'Yeni özellik ekle'`
4. Dalınızı itin: `git push origin yeni_özellik`
5. Bir Pull Request (Çekme İsteği) gönderin.

## Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
