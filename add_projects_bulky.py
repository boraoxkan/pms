import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pms.settings')
django.setup()

from intern_portal.models import Project

# Project data - you can modify this list
projects_data = [
    {
        'name': 'VoC Intelligence',  # Proje adı
        'short_description': 'İşletmelerin sosyal medya ve anketler gibi kanallardan gelen müşteri geri bildirimlerini (Müşteri Sesi) yapay zeka ile analiz ederek anlamlı içgörülere dönüştürmesini sağlar. Bu platform, müşteri memnuniyetini artırmak ve stratejik kararlar almak için kullanılır.',  # Kısa açıklama
        'full_description': '''
        <!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VoCIntelligence Projesi - Stajyer Bilgilendirme ve Keşif Dokümanı</title>
</head>
<body>

    <h1>VoCIntelligence Projesi - Stajyer Bilgilendirme ve Keşif Dokümanı</h1>

    <h2>Hoş Geldiniz, Geleceğin Veri Bilimcileri ve Yapay Zeka Uzmanları!</h2>
    <p>"VoCIntelligence" projemize hoş geldiniz! Bu proje, işletmelerin en değerli varlıklarından biri olan "müşteri sesi"ni (Voice of Customer - VoC) dijital çağın karmaşasından çıkarıp, anlamlı ve eyleme geçirilebilir içgörülere dönüştürmeyi hedefleyen yenilikçi bir yapay zeka girişimidir. Amacımız, müşterilerin sosyal medya, anketler ve diğer dijital kanallar üzerinden dile getirdiği her yorumu, şikayeti veya öneriyi derinlemesine analiz ederek, markaların stratejik kararlar almasına yardımcı olmaktır.</p>

    <h2>Projemizin Amacı: Müşterilerin Fısıltılarını Duymak ve Anlamak</h2>
    <p>Günümüz pazarında, işletmelerin başarısı büyük ölçüde müşteri memnuniyetine ve bağlılığına dayanmaktadır. Ancak, geleneksel yöntemlerle milyonlarca müşteri geri bildirimini anlamak ve bunlardan ders çıkarmak neredeyse imkansızdır. Müşteri yorumlarının çoğu, "olumlu", "olumsuz" gibi basit etiketlemelerin ötesinde, derin motivasyonlar, gizli beklentiler ve karşılanmayan ihtiyaçlar barındırır. "VoCIntelligence" ile, bu yüzeysel analizin ötesine geçiyoruz. Makinelerden gelen sinyaller gibi, müşterilerin yorumlarındaki her "fısıltıyı" duyuyor, yapay zeka destekli algoritmalarımızla bunları ana ve alt kategorilerde sınıflandırıyoruz. Ardından, Bayes ortalaması gibi ileri istatistiksel yöntemlerle bu yorumları skorluyor ve markalara, ürünlerine, şubelerine hatta rakiplerine kıyasla derinlemesine içgörüler sunuyoruz. Bu sayede işletmeler, sorunları büyümeden tespit edebilir, doğru stratejilerle müşteri deneyimini geliştirebilir ve rekabette öne geçebilir.</p>

    <h2>Ne Yapıyoruz?</h2>
    <h3>"Akıllı İçgörü Sistemi"</h3>
    <p>Bu projenin ilk aşamasında, temel işlevlere sahip bir "Minimum Uygulanabilir Ürün" (MVP) yani bir prototip geliştiriyoruz. Bu prototipin ana hatları şöyle:</p>
    <ul>
        <li><strong>Veri Toplama:</strong> Google, Instagram, LinkedIn, YouTube, Twitter (X), Şikayetvar, Ekşi Sözlük gibi sosyal medya ve web kanallarından, ayrıca müşteri anketlerinden sürekli ve otomatik veri akışı sağlıyoruz. Bu, sistemimizin "veri avcısı"dır.</li>
        <li><strong>Yapay Zeka Destekli Analiz:</strong> Topladığımız bu devasa metin verisini işlemek için OpenAI platformunun Chat-GPT altyapısı ve çeşitli görevler için özelleştirilmiş büyük dil modellerini kullanıyoruz. Bu modeller, yorumları ana ve alt kategorilerde işaretler, Bayes ortalaması ile skorlar ve %99.97 gibi yüksek bir doğruluk oranıyla duygu analizi ve derinlemesine içgörüler sunar. Burası sistemimizin "akıllı beyin"idir.</li>
        <li><strong>Örnek PoC Çalışması:</strong> Bir otomotiv firması için gerçekleştirdiğimiz PoC'de, 1.7 milyon yorum; satış, servis, ürün, uygulama ana kategorileri ve beklentiyi karşılama, aracı teslim süresi, araç temizliği, yedek parça bulunurluğu, fiyat gibi alt kategorilerde detaylıca incelendi.</li>
        <li><strong>Raporlama ve Görselleştirme:</strong> Elde ettiğimiz analiz sonuçlarını, kullanıcı dostu web panolarında ve entegre iş zekası araçları (Microsoft PowerBI, Qlik vb.) üzerinden sunuyoruz. Marka, bayi/şube ve rakip bazlı karşılaştırmalı raporlar, işletmelerin karar alma süreçlerini destekler. Bu da sistemimizin "içgörü ekranı" ve "rehberi"dir.</li>
    </ul>
    <p>Unutmayın, bu ilk aşama, projenin temel fikrinin ve teknik fizibilitesinin kanıtıdır. Tam teşekküllü bir ticari ürün değil, geleceğin "VoCIntelligence" platformunun ilk adımıdır.</p>

    <h2>Sizin Rolünüz: Keşif, Araştırma ve Geliştirme</h2>
    <p>Bu projede stajyer olarak sadece kod yazmakla kalmayacak, aynı zamanda projenin geleceğini şekillendirmeye de yardımcı olacaksınız. Sizden beklentimiz, meraklı olmanız, araştırmanız ve fikirlerinizi paylaşmanızdır.</p>
    
    <h3>Öğrenme ve Katkı Alanlarınız:</h3>
    <ul>
        <li><strong>Yapay Zeka ve Doğal Dil İşleme (NLP):</strong> Müşteri yorumlarını en doğru şekilde kategorize etmek, Bayes ortalaması ile skorlamak, gizli duygu ve beklentileri tespit etmek için OpenAI'ın Chat-GPT tabanlı modellerini nasıl daha etkin kullanabiliriz? Yeni alt kategoriler veya metrikler nasıl tanımlanabilir? Bu alanda araştırmalar yapacak, model performansını artırmak için fikirler geliştireceksiniz.</li>
        <li><strong>Büyük Veri Mimarileri ve Yönetimi:</strong> Milyonlarca metin verisini farklı kaynaklardan nasıl hızlı, güvenli ve verimli bir şekilde toplayabilir, işleyebilir ve depolayabiliriz? Zaman serisi verilerinin (yorum akışları) yönetimi ve veri güvenliği (KVKK uyumluluğu, uluslararası sertifikalı veri merkezleri) konularında araştırma yapacak, mimari tasarımlara katkıda bulunacaksınız.</li>
        <li><strong>Web Teknolojileri ve Veri Görselleştirme:</strong> Topladığımız verileri ve AI analiz sonuçlarını, markaların ve bayi/şubelerin kolayca anlayabileceği, etkileşimli ve görsel açıdan zengin web panolarında nasıl sunabiliriz? Kullanıcı deneyimini (UX) ve arayüz tasarımını (UI) geliştirmek için modern JavaScript kütüphaneleriyle (React/Vue.js) neler yapabiliriz? Bu konuda da fikirleriniz ve yeteneklerinizle destek olacaksınız.</li>
        <li><strong>Veri Entegrasyonu ve Otomasyon:</strong> Farklı sosyal medya platformları ve web sitelerinden (Şikayetvar, Ekşi Sözlük vb.) veri toplama süreçlerini nasıl daha sağlam ve ölçeklenebilir hale getirebiliriz? Anket sistemleriyle entegrasyon için en iyi yaklaşımlar nelerdir? Bu konularda mevcut çözümleri inceleyecek ve geliştirmelere destek olacaksınız.</li>
    </ul>

    <h2>Neden Araştırma ve Sorgulama Önemli?</h2>
    <p>Teknolojinin hızıyla birlikte, en uygun çözümler de sürekli değişiyor. Size direkt olarak "şunu kullanın" demek yerine, sizden bu alanda güncel kalmanızı, farklı seçenekleri araştırmanızı ve kendi argümanlarınızla çözümler önermenizi bekliyoruz. Belki de sizin bulacağınız bir algoritma veya teknoloji, projemizin geleceğini bambaşka bir noktaya taşıyacak! Bu süreçte, takım liderleriniz ve diğer mühendislerimiz size rehberlik edecek, sorularınızı yanıtlayacak ve fikirlerinizi tartışmak için her zaman hazır olacaklar. Hata yapmaktan korkmayın; her hata bir öğrenme fırsatıdır.</p>
    <p>"VoCIntelligence" projesi, hem teorik bilginizi pratiğe dönüştürmek hem de doğal dil işleme, yapay zeka ve büyük veri analizi alanında değerli bir deneyim kazanmak için eşsiz bir fırsat sunuyor. Bu heyecan verici yolculukta sizinle birlikte çalışmayı dört gözle bekliyoruz!</p>
    <p>Başarılar dileriz!</p>

</body>
</html>
        ''',
        'team_size': '3-4',  # Seçenekler: '1', '2-3', '3-4', '4+'
        'work_type': 'remote',  # Seçenekler: 'remote', 'hybrid', 'office'
        'duration': '4'  # Seçenekler: '2', '3', '4'
    },
    {
        'name': 'LAWOES',
        'short_description': 'Hukuk profesyonelleri için geliştirilen bu yapay zeka asistanı, milyonlarca emsal kararı ve UYAP verilerini kullanarak dilekçe hazırlama, emsal karar bulma ve evrak yönetimi gibi zaman alıcı görevleri otomatize eder.',
        'full_description': '''
        <!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LAWOES Projesi - Stajyer Bilgilendirme ve Keşif Dokümanı</title>
</head>
<body>

    <h1>LAWOES Projesi - Stajyer Bilgilendirme ve Keşif Dokümanı</h1>

    <h2>Hoş Geldiniz, Geleceğin Hukuk Teknologları ve Yapay Zeka Uzmanları!</h2>
    <p>"LAWOES" projemize hoş geldiniz! Bu proje, hukuk sektörünü yapay zeka ile dönüştürmeyi hedeflenen, One Eye Systems'in çığır açan bir girişimidir. Amacımız, hukukçuların günlük rutinlerindeki zaman alıcı ve tekrar eden iş yükünü otomatize ederek, onların daha stratejik ve yaratıcı hukuki çalışmalara odaklanmalarını sağlamaktır. Kısacası, avukatların sanal asistanı olup, hukuki süreçleri daha akıllı, hızlı ve hatasız hale getiriyoruz.</p>

    <h2>Projemizin Amacı: Hukukun Geleceğini Tek Tuşla Yanınızda Getirmek</h2>
    <p>Hukuk profesyonelleri, emsal karar araştırması, dilekçe yazımı, takvim ve evrak yönetimi gibi konularda yoğun bir iş yüküyle karşılaşmaktadır. Bu süreçler hem ciddi zaman kayıplarına yol açmakta hem de hata yapma potansiyelini barındırmaktadır. Geleneksel yaklaşımlar, bu karmaşıklığı tam olarak çözmekten uzaktır. "LAWOES" ile bu sorunlara kökten bir çözüm sunuyoruz. Türkiye'deki 17.5 milyondan fazla emsal kararı ve UYAP verilerini kullanarak, hukukçuların ihtiyaç duyduğu bilgiyi anında sunan ve rutin görevleri otomatize eden bir sistem geliştiriyoruz. Amacımız, bakımın ötesine geçip, planlı ve proaktif bir yaklaşımla hukuki süreçlerde verimliliği ve doğruluğu en üst seviyeye çıkarmaktır.</p>

    <h2>Ne Yapıyoruz?</h2>
    <h3>"Akıllı Hukukçu Asistanı"</h3>
    <p>Bu projenin ilk aşamasında, temel işlevlere sahip bir "Minimum Uygulanabilir Ürün" (MVP) yani bir prototip geliştiriyoruz. Bu prototipin ana hatları şöyle:</p>
    <ul>
        <li><strong>Veri Toplama:</strong> Türkiye'deki mahkeme kararları, yasal yayınlar ve içtihatlardan oluşan 17.5 milyonluk emsal karar veri setini topluyor ve sistemimize entegre ediyoruz. Ayrıca, UYAP entegrasyonu ile dava, duruşma, dilekçe ve görev atamaları gibi güncel süreç verilerini çekiyoruz. Büroların kendi iç evrak sistemlerinden de Optik Karakter Tanıma (OCR) teknolojileri ile veri alıyoruz.</li>
        <li><strong>Yapay Zeka Destekli Analiz:</strong> NVIDIA H200 çiplerini kullanarak, hukuki metinleri anlama, yorumlama ve üretme konusunda uzmanlaşmış, One Eye Systems'e ait özgün bir Büyük Dil Modeli (LLM) geliştiriyoruz. Bu LLM üzerinde emsal karar eşleştirme, dilekçe şablonlama ve üretimi, takvimleme ve görev atama, evrak sınıflandırma ve yönetimini otomatize eden özel NLP modülleri oluşturuyoruz. Hukuk Asistanı (Chatbot) ile de avukatların sorularına hukuki perspektifle cevaplar üretiyoruz.</li>
        <li><strong>Bildirim ve Görselleştirme:</strong> Avukatların kolayca navigasyon yapabileceği, dilekçe oluşturabileceği, emsal kararlara erişebileceği ve takvimlerini yönetebileceği kullanıcı dostu bir web panosu geliştiriyoruz. Sistemde sesli komut desteği de mevcut olacak.</li>
    </ul>
    <p>Unutmayın, bu ilk aşama, projenin temel fikrinin ve teknik fizibilitesinin kanıtıdır. Tam teşekküllü bir ticari ürün değil, geleceğin "LAWOES" platformunun ilk adımıdır.</p>

    <h2>Sizin Rolünüz: Keşif, Araştırma ve Geliştirme</h2>
    <p>Bu projede stajyer olarak sadece kod yazmakla kalmayacak, aynı zamanda projenin geleceğini şekillendirmeye de yardımcı olacaksınız. Sizden beklentimiz, meraklı olmanız, araştırmanız ve fikirlerinizi paylaşmanızdır.</p>
    
    <h3>Öğrenme ve Katkı Alanlarınız:</h3>
    <ul>
        <li><strong>Yapay Zeka ve Büyük Dil Modelleri (LLM/NLP):</strong> Hukuki metinleri anlamak, emsal kararları eşleştirmek, dilekçeler üretmek ve hukuki sorulara doğru cevaplar vermek için özgün LLM'imizi nasıl daha da geliştirebiliriz? Modelin doğruluğunu ve performansını artırmak için hangi yöntemler kullanılabilir? Bu alanda araştırmalar yapacak, model eğitimi ve fine-tuning süreçlerine katkıda bulunacaksınız.</li>
        <li><strong>Büyük Veri Mimarileri ve Hukuki Veri Yönetimi:</strong> 17.5 milyon emsal karar ve sürekli gelen UYAP verileri gibi büyük ve hassas hukuki veri setlerini nasıl en verimli şekilde toplayabilir, işleyebilir ve depolayabiliriz? Veri bütünlüğünü, gizliliğini ve güvenliğini (KVKK uyumluluğu dahil) sağlamak için hangi yaklaşımlar en iyisidir? Projeye özel veri merkezinin avantajlarını araştıracaksınız.</li>
        <li><strong>Web Teknolojileri ve Kullanıcı Deneyimi (UI/UX):</strong> Hukuk profesyonellerinin günlük iş akışlarına kusursuzca entegre olacak, sezgisel ve etkileşimli bir web arayüzünü nasıl tasarlarız? Takvimler, evrak akışları ve arama sonuçları gibi karmaşık hukuki verileri kullanıcılar için anlaşılır ve estetik bir şekilde nasıl görselleştirebiliriz? Sesli komutları nasıl daha doğal ve işlevsel hale getirebiliriz?</li>
        <li><strong>Entegrasyon ve Otomasyon:</strong> UYAP gibi kritik sistemlerle entegrasyonu daha sağlam ve otomatik hale getirmek için hangi teknikler kullanılabilir? Evrakların OCR ile metne dönüştürülmesi ve otomatik sınıflandırılması süreçlerini nasıl optimize edebiliriz?</li>
    </ul>

    <h2>Neden Araştırma ve Sorgulama Önemli?</h2>
    <p>Hukuk teknolojisi alanı hızla gelişiyor ve en uygun çözümler sürekli evrim geçiriyor. Size direkt olarak "şunu kullanın" demek yerine, sizden bu alanda güncel kalmanızı, farklı seçenekleri araştırmanızı ve kendi argümanlarınızla çözümler önermenizi bekliyoruz. Belki de sizin bulacağınız bir algoritma veya teknoloji, projemizin geleceğini bambaşka bir noktaya taşıyacak! Bu süreçte, takım liderleriniz ve diğer mühendislerimiz size rehberlik edecek, sorularınızı yanıtlayacak ve fikirlerinizi tartışmak için her zaman hazır olacaklar. Hata yapmaktan korkmayın; her hata bir öğrenme fırsatıdır.</p>
    <p>"LAWOES" projesi, hem teorik bilginizi pratiğe dönüştürmek hem de yapay zeka destekli hukuk teknolojileri alanında değerli bir deneyim kazanmak için eşsiz bir fırsat sunuyor. Bu heyecan verici yolculukta sizinle birlikte çalışmayı dört gözle bekliyoruz!</p>
    <p>Başarılar dileriz!</p>

</body>
</html>
        ''',
        'team_size': '2-3',
        'work_type': 'remote',
        'duration': '4'
    },
    {
        'name': 'OptiLocus',
        'short_description': 'Girişimcilerin doğru iş yeri lokasyonunu seçmelerine yardımcı olmak için nüfus, rakip ve gayrimenkul verilerini yapay zeka ile analiz eden bir platformdur. Bu sistem, belirli bir konum için en uygun işletme türünü önerir ve rekabet stratejileri sunar.',
        'full_description': '''
        <!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OptiLocus Projesi - Stajyer Bilgilendirme ve Keşif Dokümanı</title>
</head>
<body>

    <h1>OptiLocus Projesi - Stajyer Bilgilendirme ve Keşif Dokümanı</h1>

    <h2>Hoş Geldiniz, Geleceğin Veri Bilimcileri, Geliştiricileri ve Stratejistleri!</h2>
    <p>"OptiLocus" projemize hoş geldiniz! Bu proje, Türkiye'deki girişimcilik dünyasına yepyeni bir soluk getirmeyi hedefleyen, veri ve yapay zeka odaklı, heyecan verici bir platformdur. Amacımız, bir iş kurmak veya büyütmek isteyen herkesin, "Nerede açmalıyım?", "Bu dükkanın potansiyeli ne?", "Rakiplerimle nasıl başa çıkarım?" gibi kritik sorularına bilimsel ve objektif yanıtlar bulmalarına yardımcı olmak.</p>

    <h2>Projemizin Amacı: Girişimciliğin Pusulası Olmak</h2>
    <p>Türkiye'de pek çok yeni işletme, yanlış lokasyon seçimi veya pazar analizi eksikliği gibi nedenlerle kısa sürede kapanmak zorunda kalıyor. Girişimciler genellikle sezgilerine ya da kısıtlı bilgilere dayanarak büyük kararlar alıyorlar ki bu da yüksek risk anlamına geliyor. Bizim "OptiLocus" ile amacımız, bu belirsizliği ortadan kaldırmak.</p>

    <h2>Ne Yapıyoruz?</h2>
    <h3>"Akıllı Lokasyon ve İşletme Analiz Platformu"</h3>
    <p>OptiLocus, çok sayıda farklı veri kaynağını (gayrimenkul ilanları, nüfus bilgileri, rakip işletme verileri, yaya trafiği gibi) bir araya getirerek anlamlı içgörüler sunacak bir sistem. Platformumuzun temel yetenekleri şunlar olacak:</p>
    <ul>
        <li><strong>Lokasyon Puanlama:</strong> Belirli bir bölgenin iş potansiyelini onlarca farklı parametreye göre analiz edip bir puan vereceğiz.</li>
        <li><strong>İşletme Türü Tavsiyesi:</strong> Seçilen lokasyonda hangi tür işletmenin (kafe, restoran, butik vb.) daha başarılı olabileceğini tahmin edeceğiz.</li>
        <li><strong>Rekabet ve Optimizasyon Stratejileri:</strong> Rakipleri analiz ederek, menü ve fiyatlandırma konusunda girişimciye rekabette öne geçmesi için stratejiler sunacağız.</li>
    </ul>
    <p>Bu ilk aşamada, projemizin temel fikrinin teknik olarak mümkün olduğunu gösteren bir prototip (MVP) üzerinde çalışıyoruz. Amacımız, hızlıca çalışan, temel değer önerisini gösteren bir sistem ortaya koymak.</p>

    <h2>Sizin Rolünüz: Soru Soran, Araştıran ve Geliştiren Beyinler</h2>
    <p>Bu projede stajyer olarak sadece verilen görevleri yapmakla kalmayacak, aynı zamanda projenin geleceğini şekillendirmeye de aktif olarak katılacaksınız. Sizden beklentimiz, meraklı olmanız, yeni şeyler keşfetmeye istekli olmanız ve bulgularınızı, fikirlerinizi ekiple paylaşmaktan çekinmemenizdir.</p>
    
    <h3>Öğrenme ve Katkı Alanlarınız – Keşfedilecek Sorular:</h3>
    <ul>
        <li><strong>Veri Toplama Sanatı:</strong> Web sitelerinden büyük veri setlerini (gayrimenkul ilanları, işletme bilgileri) nasıl güvenli ve etik bir şekilde toplayabiliriz? Hangi araçlar (web scraping kütüphaneleri, API'ler) bu iş için en verimli olur? Topladığımız farklı yapıdaki verileri (HTML, JSON, resimler) nasıl düzenli bir hale getirebiliriz? Menü fotoğraflarından metin çıkarmak için hangi "Optik Karakter Tanıma (OCR)" teknikleri veya kütüphaneleri kullanılabilir?</li>
        <li><strong>Büyük Veriyi Yönetmek:</strong> Onlarca farklı kaynaktan gelen yüzbinlerce, hatta milyonlarca veri noktasını nasıl depolayacağız? Bu tür çok çeşitli ve büyük veri setleri için en uygun veritabanı çözümleri nelerdir (ilişkisel mi, NoSQL mi, belki de özel veri ambarları)? Verileri depolarken erişim hızını ve maliyeti nasıl optimize ederiz?</li>
        <li><strong>Yapay Zeka ile Karar Vermek:</strong> Bir lokasyonun potansiyelini tahmin etmek veya hangi işletme türünün daha başarılı olacağını öngörmek için hangi makine öğrenimi modelleri en iyi sonucu verir? "Hayatta kalma analizi" gibi daha karmaşık tahminler için ne tür yaklaşımlar (örneğin; regresyon, sınıflandırma, farklı ağaç tabanlı modeller) denemeliyiz? Kullanıcıların doğal dilde sorduğu soruları anlayıp cevaplamak için hangi "Doğal Dil İşleme (NLP)" modelleri kullanılabilir?</li>
        <li><strong>Akıllı Uygulamalar Geliştirmek:</strong> Tüm bu karmaşık veri analizi ve yapay zeka modellerini, kullanıcıların kolayca anlayabileceği, etkileşimli bir web panosuna nasıl dönüştürebiliriz? Kullanıcıların harita üzerinde lokasyonları seçebileceği, verileri görselleştirebileceği kullanıcı arayüzleri için hangi modern web teknolojileri (frontend ve backend) en uygun olur?</li>
    </ul>

    <h2>Neden Araştırma ve Sorgulama Önemli?</h2>
    <p>Teknoloji sürekli gelişiyor ve "en iyi" çözüm her zaman değişebiliyor. Biz size hazır yanıtlar vermek yerine, size bu soruları sorma, araştırma yapma ve kendi argümanlarınızla çözümler önerme fırsatı sunuyoruz. Belki de sizin keşfettiğiniz bir algoritma veya önerdiğiniz bir araç, OptiLocus'un başarısını doğrudan etkileyecek! Bu süreçte takım liderleriniz ve deneyimli mühendislerimiz size rehberlik edecek, sorularınızı yanıtlayacak ve fikirlerinizi tartışmaktan büyük keyif alacaklardır. Hata yapmak, öğrenme sürecinin doğal bir parçasıdır.</p>
    <p>OptiLocus projesi, gerçek dünya problemlerini veri bilimi ve yapay zeka ile çözmek, büyük veri ekosisteminde pratik deneyim kazanmak ve bir ürünün fikir aşamasından prototip aşamasına nasıl geldiğini görmek için eşsiz bir fırsat sunuyor.</p>
    <p>Bu heyecan verici yolculukta sizinle birlikte çalışmayı dört gözle bekliyoruz!</p>
    <p>Başarılar dileriz!</p>

</body>
</html>
        ''',
        'team_size': '2-3',
        'work_type': 'remote',
        'duration': '3'
    },
    {
        'name': 'OneEyeTrack',
        'short_description': 'Endüstriyel makinelerden gelen sensör verilerini (sıcaklık, titreşim vb.) sürekli analiz ederek, arızaları oluşmadan önce tespit etmeyi hedefleyen akıllı bir kestirimci bakım sistemidir.',
        'full_description': '''
        <!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OneEyeTrack Projesi - Stajyer Bilgilendirme ve Keşif Dokümanı</title>
</head>
<body>

    <h1>OneEyeTrack Projesi - Stajyer Bilgilendirme ve Keşif Dokümanı</h1>

    <h2>Hoş Geldiniz, Geleceğin Veri Bilimcileri ve Mühendisleri!</h2>
    <p>"OneEyeTrack" projemize hoş geldiniz! Bu proje, endüstriyel dünyada büyük bir fark yaratmayı hedefleyen, son teknoloji ürünü bir girişimdir. Amacımız, fabrikalardaki makinelerin arıza yapmadan önce "sinyal vermesini" sağlayarak, büyük üretim kayıplarını ve plansız duruşları engellemek. Kısacası, makinelerin gizli dertlerini önceden anlayıp, onlara zamanında "bakım" yapılmasına olanak tanıyan akıllı bir sistem geliştiriyoruz.</p>

    <h2>Projemizin Amacı: Makinelerin Fısıltılarını Duymak</h2>
    <p>Endüstriyel tesislerde, bir makinenin aniden bozulması büyük bir kaosa yol açabilir: üretim durur, maliyetler artar, zaman kaybedilir. Şu anki yaklaşımlar genellikle ya makine bozulduktan sonra tamir etmeye dayalı (reaktif) ya da belirli aralıklarla (ihtiyaç olmasa bile) bakım yapmaya (periyodik) dayalıdır. Bizim amacımız ise bu geleneksel döngüyü kırmak. "OneEyeTrack" ile, makinelerden gelen anlık verileri (sıcaklık, titreşim, basınç gibi "fısıltıları") sürekli dinleyeceğiz. Bu verilerdeki en ufak bir "anormalliği" tespit ederek, makine bozulmadan çok önce bakım ekiplerini uyaracağız. Böylece, bakım planlı hale gelecek, üretim kesintileri azalacak ve maliyetler düşecek.</p>

    <h2>Ne Yapıyoruz?</h2>
    <h3>"Akıllı Gözcü Sistemi"</h3>
    <p>Bu projenin ilk aşamasında, bir "Minimum Uygulanabilir Ürün" (MVP) yani temel işlevlere sahip bir prototip geliştiriyoruz. Bu prototipin ana hatları şöyle:</p>
    <ul>
        <li><strong>Veri Toplama:</strong> Fabrikadaki makinelerin sensörlerinden sürekli ve gerçek zamanlı veri akışı sağlayacağız.</li>
        <li><strong>Veri İşleme ve Analiz:</strong> Topladığımız bu büyük veri setini işleyecek ve içinde "anormallikler" olup olmadığını tespit edecek zekice yöntemler geliştireceğiz.</li>
        <li><strong>Bildirim ve Görselleştirme:</strong> Bir anormallik tespit edildiğinde, ilgili kişilere otomatik bildirimler gönderecek ve makinenin durumunu gösteren, kolay anlaşılır bir web panosu oluşturacağız.</li>
    </ul>
    <p>Unutmayın, bu ilk aşama, projenin temel fikrinin ve teknik fizibilitesinin kanıtıdır. Tam teşekküllü bir ticari ürün değil, geleceğin "OneEyeTrack" platformunun ilk adımıdır.</p>

    <h2>Sizin Rolünüz: Keşif, Araştırma ve Geliştirme</h2>
    <p>Bu projede stajyer olarak sadece kod yazmakla kalmayacak, aynı zamanda projenin geleceğini şekillendirmeye de yardımcı olacaksınız. Sizden beklentimiz, meraklı olmanız, araştırmanız ve fikirlerinizi paylaşmanızdır.</p>
    
    <h3>Öğrenme ve Katkı Alanlarınız:</h3>
    <ul>
        <li><strong>Veri Bilimi ve Makine Öğrenimi:</strong> Makine verilerindeki anormallikleri tespit etmek için hangi algoritmalar kullanılabilir? İstatistiksel yaklaşımlar mı daha iyi, yoksa makine öğrenimi modelleri mi? Eğer makine öğrenimi ise, hangi modeller (örneğin; karar ağaçları, kümeleme algoritmaları, sinir ağları) bu tür zaman serisi verileri için daha uygun olur? Bu konuda araştırmalar yapacak, farklı algoritmaları deneyerek performanslarını karşılaştıracaksınız.</li>
        <li><strong>Büyük Veri Mimarileri:</strong> Binlerce sensörden gelen milyonlarca veri noktasını nasıl hızlı ve verimli bir şekilde toplayabilir, işleyebilir ve depolayabiliriz? Hangi veritabanları bu tür "zaman serisi" verileri için idealdir? Veri akışını nasıl yönetmeli ve veri kaybını nasıl önlemeliyiz? Mesaj kuyrukları nedir ve neden önemlidirler? Bu soruların cevaplarını araştıracak ve mimari tasarımlara katkıda bulunacaksınız.</li>
        <li><strong>Web Teknolojileri:</strong> Topladığımız verileri ve anomali tespit sonuçlarını kullanıcıların kolayca anlayabileceği bir web panosunda nasıl görselleştirebiliriz? Kullanıcı dostu arayüzler tasarlarken hangi teknolojileri kullanmalıyız (örneğin; modern JavaScript kütüphaneleri)? Bu konuda da fikirleriniz ve yeteneklerinizle destek olacaksınız.</li>
        <li><strong>Uç Cihazlar ve Entegrasyon:</strong> Sensör verilerini makinelerden nasıl toplayacağız ve merkezi sistemimize nasıl göndereceğiz? IoT cihazları ve protokolleri hakkında temel araştırmalar yapacak, mevcut çözümleri inceleyeceksiniz.</li>
    </ul>

    <h2>Neden Araştırma ve Sorgulama Önemli?</h2>
    <p>Teknolojinin hızıyla birlikte, en uygun çözümler de sürekli değişiyor. Size direkt olarak "şunu kullanın" demek yerine, sizden bu alanda güncel kalmanızı, farklı seçenekleri araştırmanızı ve kendi argümanlarınızla çözümler önermenizi bekliyoruz. Belki de sizin bulacağınız bir algoritma veya teknoloji, projemizin geleceğini bambaşka bir noktaya taşıyacak!</p>
    <p>Bu süreçte, takım liderleriniz ve diğer mühendislerimiz size rehberlik edecek, sorularınızı yanıtlayacak ve fikirlerinizi tartışmak için her zaman hazır olacaklar. Hata yapmaktan korkmayın; her hata bir öğrenme fırsatıdır.</p>
    <p>"OneEyeTrack" projesi, hem teorik bilginizi pratiğe dönüştürmek hem de endüstriyel IoT ve Yapay Zeka alanında değerli bir deneyim kazanmak için eşsiz bir fırsat sunuyor. Bu heyecan verici yolculukta sizinle birlikte çalışmayı dört gözle bekliyoruz!</p>
    <p>Başarılar dileriz!</p>

</body>
</html>
        ''',
        'team_size': '2-3',
        'work_type': 'remote',
        'duration': '3'
    },
    {
        'name': 'tyreX',
        'short_description': 'Toptan lastik ticaretindeki geleneksel sipariş süreçlerini dijitalleştirmeyi amaçlayan bu proje, toptancıların ürünlerini listeleyebileceği ve perakendecilerin sipariş talebi oluşturabileceği bir dijital sipariş formu geliştirmektedir.',
        'full_description': '''
        <!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>tyreX Projesi - Stajyer Bilgilendirme Dokümanı</title>
</head>
<body>

    <h1>tyreX Projesi - Stajyer Bilgilendirme Dokümanı</h1>

    <h2>Hoş Geldiniz, Geleceğin Yazılımcıları!</h2>
    <p>"tyreX" projemize hoş geldiniz! Bu proje, toptan lastik
 ticareti sektöründeki geleneksel ve bazen verimsiz olan sipariş süreçlerini dijitalleştirmeyi hedefleyen heyecan verici bir girişimdir. Biz, bu projenin ilk ve en önemli adımını atarak, temel bir "Minimum Viable Product" (MVP) yani "Minimum Uygulanabilir Ürün" geliştiriyoruz. Bu MVP, ticari bir ürün olmaktan ziyade, projenin temel fikrinin ve işleyişinin teknik olarak mümkün olduğunu gösteren bir prototip olacak.</p>

    <h2>Projemizin Amacı ve Neden Önemli?</h2>
    <p>Amacımız, telefon ve e-posta gibi yöntemlerle yapılan lastik sipariş süreçlerini, basit ama etkili bir dijital platforma taşımak. Bu, toptancılar ve perakendeciler arasındaki iletişimi kolaylaştıracak ve siparişlerin daha hızlı ve hatasız bir şekilde kaydedilmesini sağlayacak. Sizin de katkılarınızla geliştireceğimiz bu prototip, potansiyel yatırımcılarımıza ve ilk kullanıcılarımıza projemizin değerini gösterecek bir kanıt niteliği taşıyor.</p>

    <h2>Ne Yapıyoruz?</h2>
    <h3>"Dijital Sipariş Formu"</h3>
    <p>MVP'mizin özü, "Dijital Sipariş Formu" adını verdiğimiz bir sistem. Bu sistem sayesinde:</p>
    <ul>
        <li><strong>Toptancılar:</strong> Ürünlerini (lastik markası, boyutu, fiyatı, stoğu gibi temel bilgileri) sisteme girebilecekler.</li>
        <li><strong>Perakendeciler:</strong> Platformdaki tüm lastikleri listeleyip görebilecek ve ilgilendikleri ürünler için kolayca sipariş talebi oluşturabilecekler.</li>
        <li><strong>Bildirimler:</strong> Bir perakendeci sipariş oluşturduğunda, ilgili toptancıya otomatik bir bildirim (örneğin e-posta ile) gidecek ve sipariş sistemde kayıt altına alınacak.</li>
    </ul>
    <p>Unutmayın, bu ilk aşamada ödeme işlemleri veya kargolama gibi lojistik süreçler platformumuz üzerinden yönetilmeyecek. Amacımız, temel sipariş akışını dijitalleştirmek.</p>

    <h2>Hangi Teknolojileri Kullanıyoruz?</h2>
    <p>Bu projede hızlı ve etkili bir şekilde ilerlemek için belirli teknoloji seçimleri yaptık:</p>
    <ul>
        <li><strong>Programlama Dili ve Çerçeve (Framework):</strong> Python dili ve onun güçlü web çerçevesi Django'yu kullanıyoruz. Django, hem arka uç (backend) kodlaması hem de basit arayüzler (frontend) oluşturmak için bize büyük kolaylıklar sağlıyor.</li>
        <li><strong>Veritabanı:</strong> Verilerimizi güvenli bir şekilde depolamak için PostgreSQL veya daha hafif bir seçenek olan SQLite kullanacağız.</li>
        <li><strong>Sunucu ve Dağıtım:</strong> Geliştirdiğimiz uygulamayı internet üzerinde canlı hale getirmek için Heroku veya Render gibi "Platform as a Service" (Hizmet Olarak Platform) araçlarını kullanacağız. Bu araçlar, karmaşık sunucu kurulumlarıyla uğraşmadan uygulamamızı hızla yayınlamamızı sağlar.</li>
    </ul>

    <h2>Sizin Rolünüz ve Öğrenme Deneyiminiz</h2>
    <p>Bu projede stajyer olarak aktif rol alacaksınız. Temel olarak şu alanlarda deneyim kazanacaksınız:</p>
    <ul>
        <li><strong>Web Geliştirme Temelleri:</strong> Django ile model, view, template gibi web geliştirmenin temel kavramlarını öğrenecek ve uygulayacaksınız.</li>
        <li><strong>Veritabanı Yönetimi:</strong> Veri modelleri oluşturma, veritabanı sorguları ve ilişkileri hakkında pratik bilgi edineceksiniz.</li>
        <li><strong>Kullanıcı Arayüzü (UI) Geliştirme:</strong> Temel HTML ve CSS kullanarak Django şablonları üzerinden kullanıcıların etkileşimde bulunacağı sayfaları oluşturmaya katkıda bulunacaksınız.</li>
        <li><strong>Problem Çözme ve Hızlı Geliştirme:</strong> Minimum kaynakla, belirli bir sürede çalışan bir ürün ortaya koymanın zorluklarını ve çözümlerini deneyimleyeceksiniz.</li>
    </ul>
    <p>Bu süreçte, hızlı ilerlemek ve temel işlevselliği sağlamak ana hedefimiz olacak. Kodun mükemmel olması yerine, çalışır durumda olması ve projenin amacına hizmet etmesi önceliğimizdir. Bu da size "hızlı prototipleme" ve "MVP geliştirme" konularında değerli bir bakış açısı kazandıracak.</p>

    <h2>Beklentilerimiz ve Destek</h2>
    <p>Sizden meraklı, öğrenmeye istekli ve takım çalışmasına yatkın olmanızı bekliyoruz. Takım liderleriniz ve diğer geliştiricilerimiz her adımda size rehberlik edecek ve karşılaşacağınız sorunlarda destek sağlayacaklardır. Sorular sormaktan çekinmeyin, her soru öğrenme sürecinizin bir parçasıdır.</p>
    <p>Bu proje, hem teknik becerilerinizi geliştirmek hem de gerçek bir iş projesinin dinamiklerini deneyimlemek için harika bir fırsat sunuyor. "tyreX" projesindeki katkılarınızla, dijitalleşen dünyaya adım atmanın heyecanını birlikte yaşayacağız!</p>
    <p>Başarılar dileriz!</p>

</body>
</html>
        ''',
        'team_size': '2-3',
        'work_type': 'remote',
        'duration': '2'
    },
    # Daha fazla proje eklemek için yukarıdaki formatı kopyalayın
]

print("Projeler ekleniyor...")
print("=" * 60)

# Clear existing projects (optional - comment out if you want to keep existing)
# Project.objects.all().delete()
# print("🗑️  Mevcut projeler temizlendi")

for project_data in projects_data:
    # Skip empty entries
    if not project_data['name'] or not project_data['short_description']:
        continue
    
    try:
        # Check if project already exists
        existing_project = Project.objects.filter(name=project_data['name']).first()
        if existing_project:
            print(f"⚠️  '{existing_project.name}' projesi zaten mevcut")
            continue
        
        # Create project
        project = Project.objects.create(
            name=project_data['name'],
            short_description=project_data['short_description'],
            full_description=project_data['full_description'],
            team_size=project_data['team_size'],
            work_type=project_data['work_type'],
            duration=project_data['duration']
        )
        
        print(f"✅ '{project.name}' projesi başarıyla eklendi")
        print(f"   👥 Ekip Büyüklüğü: {project.get_team_size_display()}")
        print(f"   🏢 Çalışma Şekli: {project.get_work_type_display()}")
        print(f"   ⏱️  Süre: {project.get_duration_display()}")
        print(f"   📝 Açıklama: {project.short_description[:50]}...")
        print("-" * 60)
        
    except Exception as e:
        print(f"❌ Hata: '{project_data['name']}' projesi eklenirken hata: {e}")
        print("-" * 60)

print("✨ Proje ekleme işlemi tamamlandı!")

# Show summary
total_projects = Project.objects.count()
print(f"📊 Toplam proje sayısı: {total_projects}")

print("\n🎯 Proje Seçenekleri:")
print("   Team Size: '1', '2-3', '3-4', '4+'")
print("   Work Type: 'remote', 'hybrid', 'office'")
print("   Duration: '2', '3', '4'")