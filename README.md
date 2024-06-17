# Papara Ödeme Doğrulama Telegram Botu

Bu, Papara API kullanarak yapılan ödemeleri doğrulayan ve hesap bakiyesini kontrol eden bir Telegram botudur. Bot, kullanıcılara ödeme yaparken kullanmaları için benzersiz bir açıklama sağlar ve bu açıklamayı Papara API üzerinden kontrol ederek ödemeyi doğrular.

## Özellikler

- Her ödeme isteği için benzersiz bir açıklama oluşturur.
- Papara API kullanarak ödemeleri doğrular.
- Kullanıcılara Telegram üzerinden gerçek zamanlı ödeme onayı sağlar.
- Papara hesap bakiyesini kontrol eder.
- Kullanıcılara QR Kod, POS ve Uygulama ile ödeme seçenekleri sunar.
- Kullanıcıların istediği tutarda ödeme yapabilmelerine olanak tanır.
- Ödeme ve bakiye bilgilerini SQLite veritabanında saklar.

## Gereksinimler

- Python 3.7+
- BotFather'dan alınmış bir Telegram bot tokeni.
- Papara API anahtarları.

## Kurulum

1. Depoyu klonlayın:

    ```sh
    git clone https://github.com/yaaniyakup/kurumsalpapara.git
    cd kurumsalpapara
    ```

2. Gerekli Python paketlerini yükleyin:

    ```sh
    pip install -r requirements.txt
    ```

3. `config.py` dosyasını oluşturun ve aşağıdaki yapılandırma bilgilerini ekleyin:

    ```python
    # config.py
    PAPARA_API_KEY = 'your_papara_api_key'
    PAPARA_API_URL = 'https://merchant-api.papara.com'
    ```

## Kullanım

1. Botu çalıştırın:

    ```sh
    python papara_payment_bot.py
    ```

2. Bot ile Telegram üzerinden etkileşime geçin:

    - `/start` komutunu kullanarak botu başlatın.
    - `/pay` komutunu kullanarak ödeme bilgisi isteyin ve tutarı girin.
    - `/payment` komutunu kullanarak ödeme yöntemini seçin (QR Kod, POS, Uygulama).
    - `/confirm` komutunu kullanarak ödemeyi onaylayın.
    - `/balance` komutunu kullanarak bakiyenizi öğrenin.

## Dosya Açıklamaları

- `papara_payment_bot.py`: Telegram komutlarını ve ödeme doğrulamasını yöneten ana bot betiği.
- `papara_api.py`: Papara API'sini kullanarak ödeme doğrulaması ve bakiye kontrolü yapan betik.
- `database.py`: Kullanıcı bakiyelerini ve ödeme bilgilerini yönetmek için SQLite veritabanını yöneten betik.
- `config.py`: API anahtarları ve yapılandırma bilgilerini içeren dosya.

## Telegram Komutları

- `/start`: Botu başlatır ve hoş geldiniz mesajı gönderir.
- `/pay`: Benzersiz bir ödeme açıklaması oluşturur ve ödeme talimatlarını gönderir.
- `/payment`: Kullanıcının seçtiği ödeme yöntemine göre ödeme işlemini başlatır (QR Kod, POS, Uygulama).
- `/confirm`: Ödeme doğrulamasını kontrol eder ve kullanıcıyı bilgilendirir.
- `/balance`: Kullanıcının bakiyesini gösterir.

## Notlar

- API anahtarlarınızı ve diğer hassas bilgileri güvende tuttuğunuzdan emin olun.
- Bu bot, Papara API'si kullanılarak ödemeleri doğrular ve bakiyenizi kontrol eder.

## Katkıda Bulunma

1. Depoyu forklayın.
2. Yeni bir dal oluşturun (`git checkout -b feature-branch`).
3. Değişikliklerinizi yapın.
4. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik ekle'`).
5. Dala push edin (`git push origin feature-branch`).
6. Yeni bir Pull Request oluşturun.

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için [LICENSE](LICENSE) dosyasına bakın.
