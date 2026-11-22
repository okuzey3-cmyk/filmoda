# Tur 13 - Gemini cevabi (model: gemini-3-flash-preview)

Selam Oğuzhan, Claude'un teknik titizliği değerli ancak Filmoda'nın "saf" kalması için bazı konularda netleşmeliyiz:

**1. Veri Güvenliği Beyanı (Claude'un A itirazına):** Google Play'de "Veri toplanmıyor" beyan edilmeli; çünkü veriyi biz (geliştirici) almıyoruz, TMDB ve YouTube "Hizmet Sağlayıcı" (Service Provider) istisnasına giriyor (Kaynak: Google Play Data Safety - "Ephemereal processing" ve "Service Provider" maddeleri). Rakipler (JustWatch, Letterboxd) veri toplar ve kullanıcılar izlenmekten şikayetçidir; bizim "sıfır veri" duruşumuz gerçek bir dert çözer. Kazanç: Kullanıcı güveni. Ekrana veya koda hiçbir karmaşıklık eklemez, gizlilik metnindeki belirsizliği çıkarır. (Zorluk: Kolay, Risk: Yok).

**2. Mağaza Metni ve Çevrimdışı Vaadi (Claude'un B itirazına):** Claude haklı, "internetsiz liste erişimi" vaadi afişler gözükmediği için zayıf kalır ve yanıltıcı algılanabilir. Bunun yerine "Hafiflik ve Hız" (sadece 1-2 MB yer kaplar) vurgulanmalı; rakiplerin hantallığından yorulan kullanıcıların derdine hitap eder. Kazanç: Belirsiz. Akışı bozmaz, sadece mağaza açıklamasını sadeleştirir. (Zorluk: Kolay, Risk: Yanlış beyan riski kalkar).

**3. Uygulama İçi Puan İsteği (EKLEME):** Kesinlikle eklenmemeli; rakipler bunu yapıyor ve kullanıcılar tam film seçerken çıkan pop-up'lardan nefret ediyor. Kullanıcının "hızlıca film seçme" akışını bozar ve Jobs-vari sadeliğe aykırıdır. Kazanç: Belirsiz (puan artabilir ama deneyim düşer). Akışı 1 tam ekran öğe kadar karmaşıklaştırır. (Zorluk: Kolay, Risk: Kullanıcıyı uygulamadan soğutma).

**4. Üretim Sonrası Takip (Play Console):** Kod eklemeden sadece Play Console üzerinden "Android Vitals" (çökme oranı) ve "Yorumlar" takip edilmeli. Rakipler karmaşık analiz araçları kullanır, biz ise kod eklemeden sadece uygulamanın çalışıp çalışmadığını (hata oranını) izleriz. Kazanç: Teknik sağlamlık. Karmaşıklık eklemez, aksine analiz kütüphanesi yükünü uygulamadan çıkarır. (Zorluk: Kolay, Risk: Yok).

**5. Yorum Yanıtlama Stratejisi:** Olumsuz yorumlara (Örn: "Film yok") "Filmoda bir izleme platformu değil, sadece rehberdir; veriler TMDB'den gelir" şeklinde dürüst ve kısa cevaplar verilmeli. Rakipler genelde robotik cevaplar verir, biz ise samimi ve şeffaf kalarak marka kimliğini koruruz. Kazanç: Belirsiz. Kod dışı bir süreçtir, uygulama akışını etkilemez. (Zorluk: Kolay, Risk: Yok).
