# Tur 17 - Gemini cevabi (model: gemini-3-flash-preview)

Selam Oğuzhan, Claude'un teknik risk analizi çok kritik bir noktada. 4 Aralık'taki "ilk gerçek yayın" için şu somut adımları atmalıyız:

**1. En Büyük Risk: 14 Günlük Test Süreci:** En büyük risk, Google'ın 12 testçinin etkileşimini "yetersiz" bulup süreci uzatmasıdır. Formda "testten sonra ne değişti" sorusuna; "45+ yaş kullanıcılar için dokunma alanları büyütüldü ve erişilebilirlik artırıldı" (Tur 15'te yaptığımız) yazılmalı. Bu, gerçek bir iyileştirmedir ve Google bunu sever. (Yarar: Onay hızlanır, Zorluk: Kolay, Risk: Yüksek).

**2. İmza Anahtarı (Keystore) Felaketi:** Claude haklı; her derlemede yeni anahtar oluşuyorsa mevcut uygulamayı güncelleyemezsin. GitHub Artifacts kısmındaki `.keystore` dosyasını ve şifresini hemen indirip Google Drive gibi güvenli bir yere yedeklemelisin. Eğer kaybolursa Google Destek ile "Yükleme Anahtarı Sıfırlama" işlemi yapman gerekir ki bu süreci 1 hafta geciktirir. (Yarar: Uygulama ömrü, Zorluk: Orta, Risk: Kritik).

**3. Testçilere "Görev" Ver:** Kalan 8 günde 12 testçiden şu iki şeyi iste: "Arama kısmına en sevdiğin oyuncuyu yaz" ve "Bir filmi izleme listesine ekle". Bu hareketler Play Console panelinde "etkileşim" olarak görünür ve botların onayı vermesini sağlar. Rakipler bu süreci profesyonel test gruplarıyla geçer, biz samimi etkileşimle geçmeliyiz. (Yarar: Bot onayı, Zorluk: Kolay, Risk: Düşük).

**4. 2 Dakikalık "Adres Çubuğu" Kontrolü:** Uygulamayı telefonunda açtığında üstte tarayıcı adres çubuğu (URL bar) görüyorsan `assetlinks.json` hatalıdır. Eğer görünmüyorsa "estetik" tamdır ve Google Play ile web siten başarıyla mühürlenmiş demektir. Play Console'da "Hesap Ayrıntıları" kısmında kırmızı bir uyarı yoksa doğrulama tamamdır. (Yarar: Estetik bütünlük, Zorluk: Çok Kolay, Risk: Düşük).

**5. TMDB Atfı ve Dil:** TMDB atfının Türkçe olması bir ret sebebi değildir; JustWatch ve TMDB logolarının "Hakkında" kısmında olması yeterlidir. Bu bir "olsa güzel olur" değil, yasal zorunluluktur ve şu anki haliyle temizdir. Uygulamaya yeni bir "İngilizce metin" ekleyip sadeliği bozmaya gerek yok. (Yarar: Yasal uyum, Zorluk: Kolay, Risk: Yok).

**Ürün İlkesi Notu:** Bu maddelerin hiçbiri kod karmaşası yaratmaz, aksine "camura dönmeden" güvenli bir çıkış yapmanı sağlar. Kazanç: Uygulamanın markette kalıcı olması. Ekrana yeni bir "tık" eklenmiyor.
