# Tur 8 - Gemini cevabi (model: gemini-3-flash-preview)

Selam Oğuzhan, Claude'un teknik çıkmazına ilke odaklı ve estetik bir çözümle yanıt veriyorum:

**1. Karar: B Seçeneği (Kopyala + Kart Paylaş):** Rakipler (Letterboxd) genelde sadece metin paylaşır; biz ise kart estetiğinden vazgeçmiyoruz. Paylaş butonuna basıldığında link otomatik panoya kopyalanır, ardından görsel paylaşım menüsü açılır ve kullanıcıya "Bağlantı kopyalandı, yapıştırabilirsin" uyarısı verilir. Bu yöntem ekrana yeni bir buton eklemez, akışı bozmaz ve "gerçek bir dert" olan link kaybını çözer. (Zorluk: Kolay, Kazanç: Belirsiz).

**2. iOS ve Kullanıcı Deneyimi:** iOS Safari'de pano işlemi paylaşım menüsünden *önce* bitmelidir, aksi halde güvenlik nedeniyle engellenir. Kullanıcının yapıştırmayı unutma riski olsa da, kartın üzerindeki URL'yi elle yazmasından çok daha kolaydır. Bu çözüm sunucu gerektirmez, uygulamanın ücretsiz ve hesapsız kimliğini korur. (Risk: Kullanıcının ikinci adımı (yapıştır) yapmaması).

**3. Neden A (Sadece Metin) Değil?:** Sadece metin paylaşmak işlevseldir ama senin estetik vizyonunu ve uygulamanın "hediye kartı" hissini öldürür. Sunucusuz olduğumuz için her film için ayrı link önizlemesi (OG Tag) oluşturamayız; bu yüzden metin linki WhatsApp'ta sönük kalır. Kart tasarımı Filmoda'nın imzasıdır, korunmalıdır. (Fark: Estetik vs. İşlevsellik).

**4. Android TWA Link Davranışı:** Android tarafında linkin tarayıcıyı değil direkt uygulamayı (TWA) açması için `assetlinks.json` yapılandırması şarttır. Eğer bu dosya doğru yerleştirilirse, paylaşılan linke dokunan arkadaşı uygulamayı hiç yüklememişse tarayıcıda, yüklüyse direkt Filmoda içinde filmi görür. Bu, kullanıcıyı uygulama içinde tutmak için en kritik "teknik ciladır". (Zorluk: Orta).

**5. Sadelik Uyarısı:** Paylaşım için ikinci bir buton (Örn: "Sadece Link Gönder") eklemeyi kesinlikle reddediyorum. Mevcut "Arkadaşına gönder" butonu hem kopyalama hem paylaşma işini aynı anda, kullanıcıyı yormadan yapmalıdır. Daha fazla özellik eklemek yerine, mevcut butonun arkasındaki mantığı bu şekilde "akıllandırmak" en sade yoldur. (Kural: Çamura dönmemeli).
