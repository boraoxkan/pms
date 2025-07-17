import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pms.settings')
django.setup()

from intern_portal.models import Project

projects = [
    {
        'name': 'Lastik',
        'short_description': 'Lastik aşınma durumunu yapay zeka ile tespit eden proje.',
        'full_description': '''
<h2>Lastik Projesi</h2>
<p>Lastik projesi, araçların lastik durumunu yapay zeka teknolojisi kullanarak analiz eden yenilikçi bir çözümdür.</p>

<h3>Özellikler:</h3>
<ul>
<li>Derin öğrenme modelleri ile lastik aşınma tespiti</li>
<li>Gerçek zamanlı görüntü işleme</li>
<li>Mobil uygulama entegrasyonu</li>
<li>Kullanıcı dostu arayüz</li>
<li>Detaylı raporlama sistemi</li>
</ul>

<h3>Bu projede çalışacak stajyerler:</h3>
<ul>
<li>Yapay zeka ve görüntü işleme konularında deneyim kazanacak</li>
<li>Modern yazılım geliştirme pratiklerini öğrenecek</li>
<li>Gerçek dünya problemlerine çözüm üretecek</li>
</ul>
''',
        'team_size': '2-3',
        'work_type': 'hybrid',
        'duration': '3'
    },
    {
        'name': 'OptiLocus',
        'short_description': 'Depo içi optimizasyon ve lokasyon yönetimi projesi.',
        'full_description': '''
<h2>OptiLocus Projesi</h2>
<p>OptiLocus, depo yönetimini optimize eden ve lokasyon bazlı çözümler sunan kapsamlı bir projedir.</p>

<h3>Özellikler:</h3>
<ul>
<li>Akıllı depo yerleşim planlaması</li>
<li>Gerçek zamanlı stok takibi</li>
<li>Rota optimizasyonu</li>
<li>İş gücü planlama</li>
<li>Performans analizi</li>
</ul>

<h3>Bu projede çalışacak stajyerler:</h3>
<ul>
<li>Optimizasyon algoritmaları geliştirecek</li>
<li>Veritabanı yönetimi konusunda deneyim kazanacak</li>
<li>Web teknolojileri ile çalışacak</li>
</ul>
''',
        'team_size': '3-4',
        'work_type': 'office',
        'duration': '4'
    },
    {
        'name': 'OneEyeTrack',
        'short_description': 'Çalışan takip ve performans analizi sistemi.',
        'full_description': '''
<h2>OneEyeTrack Projesi</h2>
<p>OneEyeTrack, çalışanların performansını ve verimliliğini ölçen modern bir izleme sistemidir.</p>

<h3>Özellikler:</h3>
<ul>
<li>Gerçek zamanlı performans takibi</li>
<li>Otomatik raporlama</li>
<li>Hedef bazlı değerlendirme</li>
<li>Dashboard ve analitik araçlar</li>
<li>Mobil uygulama desteği</li>
</ul>

<h3>Bu projede çalışacak stajyerler:</h3>
<ul>
<li>Full-stack web geliştirme deneyimi kazanacak</li>
<li>Veri analizi ve görselleştirme yapacak</li>
<li>Kullanıcı deneyimi tasarımı konusunda çalışacak</li>
</ul>
''',
        'team_size': '2-3',
        'work_type': 'remote',
        'duration': '3'
    },
    {
        'name': 'LAWOES',
        'short_description': 'Hukuki süreç otomasyonu ve yapay zeka destekli analiz sistemi.',
        'full_description': '''
<h2>LAWOES Projesi</h2>
<p>LAWOES, hukuki süreçleri otomatikleştiren ve yapay zeka ile analiz eden yenilikçi bir platformdur.</p>

<h3>Özellikler:</h3>
<ul>
<li>Doğal dil işleme ile belge analizi</li>
<li>Otomatik dava takibi</li>
<li>Karar destek sistemi</li>
<li>Yasal süreç otomasyonu</li>
<li>Gelişmiş arama ve filtreleme</li>
</ul>

<h3>Bu projede çalışacak stajyerler:</h3>
<ul>
<li>NLP ve makine öğrenmesi konularında çalışacak</li>
<li>Hukuki süreç otomasyonu geliştirecek</li>
<li>Backend sistemleri tasarlayacak</li>
</ul>
''',
        'team_size': '3-4',
        'work_type': 'hybrid',
        'duration': '4'
    },
    {
        'name': 'VOC Intelligence',
        'short_description': 'Müşteri geri bildirimlerini analiz eden yapay zeka sistemi.',
        'full_description': '''
<h2>VOC Intelligence Projesi</h2>
<p>VOC Intelligence, müşteri sesini (Voice of Customer) yapay zeka ile analiz eden gelişmiş bir sistemdir.</p>

<h3>Özellikler:</h3>
<ul>
<li>Duygu analizi</li>
<li>Otomatik kategorizasyon</li>
<li>Trend analizi</li>
<li>Gerçek zamanlı raporlama</li>
<li>Çok dilli destek</li>
</ul>

<h3>Bu projede çalışacak stajyerler:</h3>
<ul>
<li>Doğal dil işleme modelleri geliştirecek</li>
<li>Veri madenciliği yapacak</li>
<li>API geliştirme konusunda deneyim kazanacak</li>
</ul>
''',
        'team_size': '2-3',
        'work_type': 'remote',
        'duration': '3'
    }
]

# Önce var olan projeleri sil
Project.objects.all().delete()

# Yeni projeleri ekle
for project_data in projects:
    Project.objects.create(**project_data)

print("Projeler başarıyla eklendi!") 