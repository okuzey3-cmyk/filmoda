# Tur 15 - Gemini cevabi (model: gemini-3-flash-preview)

Selam Oğuzhan, Claude'un erişilebilirlik endişeleri yerinde ancak çözümü Filmoda'nın şık görüntüsünü bozmadan, "görünmez" dokunuşlarla halletmeliyiz.

**1. Dokunma Alanlarını Görünmez Büyütme:** Android ve Apple standartları 44-48px alan ister; 34px olan "Değiştir" ve "Kapat" düğmeleri 45+ kullanıcı için gerçek bir derttir. Görsel boyutu değiştirmeden, CSS `::after` ile dokunma alanını görünmez şekilde 44px'e çıkarmalıyız; böylece estetik bozulmaz ama ıskalama biter. Rakipler (JustWatch) bu gizli genişletmeyi yaygın kullanır. Kazanç: Memnuniyet; ekrana yeni öğe eklemez, karmaşıklık yaratmaz. (Zorluk: Kolay, Risk: Yok).

**2. Kritik Küçük Yazıları Düzeltme:** 11px ve 12px olan süre/puan altı metinleri 14px'e çekilmeli; bunlar film seçimini doğrudan etkileyen kritik verilerdir. "Hakkında" gibi ikincil metinler 13px kalabilir, böylece görsel hiyerarşi ve Steve Jobs vari sadelik korunur. Rakiplerde okunabilirlik şikayeti genelde bu "karınca duası" yazılardan çıkar. Kazanç: Belirsiz; sadece 2-3 satır CSS değişir, akış aynı kalır. (Zorluk: Kolay, Risk: Çok düşük).

**3. Yazı Birimi ve Sistem Uyumu:** Android sistem yazı boyutu büyütüldüğünde `px` birimi genelde sabit kalır ve büyümez; bu da erişilebilirlik uyarısı almamıza neden olur (Kaynaksız: Genel TWA tecrübesi). Ancak 4 Aralık'a kadar tüm yapıyı `rem` birimine çevirmek tasarımı "çamura" döndürebilir ve yerleşimleri kaydırabilir. Bu yüzden şimdilik sadece en küçük fontları 14px yaparak tasarımı riske atmadan güvenli bölgede kalmalıyız. Kazanç: Teknik sağlamlık. (Zorluk: Orta, Risk: Tasarımın kayması).

**4. Google Play Botlarını İkna Etme:** Google'ın "Lansman Öncesi Raporu" 48px altındaki her düğmeye uyarı verecektir; bu uyarılar mağaza görünürlüğünü etkileyebilir. Görünmez dokunma alanlarını (hitbox) büyüterek hem botları susturur hem de yaşlı kullanıcıyı mutlu ederiz. Rakipler bu teknikle hem "temiz" görünüp hem de tam puan alıyor. Kazanç: Mağaza prestiji; 0 tık karmaşası. (Zorluk: Kolay, Risk: Yok).

**5. Claude'a İtiraz ve Karar:** Claude'un "bekleyelim" önerisine katılmıyorum; dokunma alanı hatası "olsa güzel olur" değil, kullanıcıyı uygulamadan kovan bir hatadır. 45+ kullanıcı "yanlış yere bastım" diye uygulamayı silebilir; bu gerçek bir kullanıcı kaybıdır. Sadece görünmez hitbox ve 11-12px font düzeltmesini yapıp 4 Aralık başvurusuna girmeliyiz. Kazanç: Kullanıcı tutma; estetikten ödün vermez. (Zorluk: Kolay, Risk: Yok).
