import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pms.settings')
django.setup()

from intern_portal.models import Intern, Project

# Project assignments - you can modify this list
# Format: {'intern_email': 'email@oneeyespace.com', 'project_names': ['Project 1', 'Project 2']}
assignments = [
    {
        'intern_email': 'berfininan@oneeyespace.com',  # Stajyer e-posta adresi
        'project_names': ['OptiLocus', 'LAWOES']  # Atanacak proje adları
    },
    {
        'intern_email': 'bernacakir@oneeyespace.com',
        'project_names': ['OptiLocus', 'LAWOES']
    },
    {
        'intern_email': 'erfanfarhangkia@oneeyespace.com',
        'project_names': ['OptiLocus', 'LAWOES']
    },
    {
        'intern_email': 'esmasivri@oneeyespace.com',
        'project_names': ['OptiLocus', '']
    },
    {
        'intern_email': 'rumeysasen@oneeyespace.com',
        'project_names': ['OptiLocus', 'VoC Intelligence']
    },
    {
        'intern_email': 'serifeocak@oneeyespace.com',
        'project_names': ['OptiLocus', 'VoC Intelligence']
    },
    {
        'intern_email': 'esmaaydin@oneeyespace.com',
        'project_names': ['VoC Intelligence', '']
    },
    {
        'intern_email': 'mehmetdedeoglu@oneeyespace.com',
        'project_names': ['VoC Intelligence', 'OneEyeTrack']
    },
    {
        'intern_email': 'tahaoktar@oneeyespace.com',
        'project_names': ['VoC Intelligence', 'LAWOES']
    },
    {
        'intern_email': 'alituysuz@oneeyespace.com',
        'project_names': ['tyreX', 'OneEyeTrack']
    },
    {
        'intern_email': 'beyzadogan@oneeyespace.com',
        'project_names': ['tyreX', 'OneEyeTrack']
    },
    {
        'intern_email': 'suleymankarayel@oneeyespace.com',
        'project_names': ['tyreX', 'OneEyeTrack']
    },
    # Daha fazla atama eklemek için yukarıdaki formatı kopyalayın
]

print("Proje atamaları yapılıyor...")
print("=" * 60)

for assignment in assignments:
    # Skip empty entries
    if not assignment['intern_email'] or not assignment['project_names']:
        continue
    
    try:
        # Find intern
        intern = Intern.objects.filter(email=assignment['intern_email']).first()
        if not intern:
            print(f"❌ Stajyer bulunamadı: {assignment['intern_email']}")
            continue
        
        print(f"👤 Stajyer: {intern.get_full_name()} ({intern.email})")
        
        # Clear existing assignments (optional)
        # intern.assigned_projects.clear()
        
        # Assign projects
        assigned_count = 0
        for project_name in assignment['project_names']:
            if not project_name:  # Skip empty project names
                continue
                
            project = Project.objects.filter(name=project_name).first()
            if project:
                intern.assigned_projects.add(project)
                print(f"   ✅ '{project.name}' projesi atandı")
                assigned_count += 1
            else:
                print(f"   ❌ Proje bulunamadı: '{project_name}'")
        
        if assigned_count > 0:
            print(f"   📋 Toplam {assigned_count} proje atandı")
        
        print("-" * 60)
        
    except Exception as e:
        print(f"❌ Hata: {assignment['intern_email']} için atama yapılırken hata: {e}")
        print("-" * 60)

print("✨ Proje atama işlemi tamamlandı!")

# Show summary
print("\n📊 Atama Özeti:")
for intern in Intern.objects.filter(assigned_projects__isnull=False).distinct():
    projects = intern.assigned_projects.all()
    print(f"   {intern.get_full_name()}: {', '.join([p.name for p in projects])}")

print(f"\n🎯 Toplam {Intern.objects.filter(assigned_projects__isnull=False).distinct().count()} stajyere proje atandı")