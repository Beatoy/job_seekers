from db import get_db
from bson.objectid import ObjectId
import datetime

def seed_vacancies():
    db = get_db()
    
    # 1. Create or Get a Demo Company
    company = db.companies.find_one({'email': 'demo@computrabajo.com'})
    if not company:
        print("Creating Demo Company...")
        company_id = db.companies.insert_one({
            'email': 'demo@computrabajo.com',
            'password': 'encrypted_password_placeholder', # In a real app, encrypt this
            'company_name': 'Empresas Líderes (Demo)',
            'location': 'Ciudad de México'
        }).inserted_id
    else:
        print("Using existing Demo Company...")
        company_id = company['_id']

    company_name = 'Empresas Líderes (Demo)'

    # 2. Define 26 Vacancies
    vacancies_data = [
        # Tech / Dev
        {"title": "Desarrollador Full Stack Python", "salary": "$35,000 - $45,000", "degree": "Ingeniería en Sistemas", "hours": "Lunes a Viernes 9-6", "requirements": "Experiencia en Flask, React, MongoDB. Inglés intermedio."},
        {"title": "Frontend Developer React", "salary": "$30,000 - $40,000", "degree": "Ingeniería en Software", "hours": "Remoto", "requirements": "React.js, CSS avanzado, Redux. Portafolio requerido."},
        {"title": "Backend Developer Node.js", "salary": "$32,000 - $42,000", "degree": "Ciencias de la Computación", "hours": "Híbrido", "requirements": "Node.js, Express, SQL. Conocimiento de AWS."},
        {"title": "Data Scientist Jr", "salary": "$25,000 - $35,000", "degree": "Matemáticas o Afín", "hours": "Lunes a Viernes 8-5", "requirements": "Python, Pandas, Scikit-learn. Gusto por las estadísticas."},
        {"title": "DevOps Engineer", "salary": "$45,000 - $60,000", "degree": "Ingeniería en Sistemas", "hours": "Remoto", "requirements": "Docker, Kubernetes, CI/CD pipelines, Linux."},
        {"title": "QA Automation Engineer", "salary": "$28,000 - $38,000", "degree": "Ingeniería en Computación", "hours": "Lunes a Viernes 9-6", "requirements": "Selenium, Python o Java, pruebas automatizadas."},
        {"title": "Mobile Developer iOS", "salary": "$40,000 - $50,000", "degree": "Ingeniería de Software", "hours": "Híbrido", "requirements": "Swift, Xcode, publicación en App Store."},
        {"title": "Mobile Developer Android", "salary": "$38,000 - $48,000", "degree": "Ingeniería en Sistemas", "hours": "Híbrido", "requirements": "Kotlin, Android Studio, APIs REST."},
        
        # Design / Creative
        {"title": "Diseñador UX/UI", "salary": "$25,000 - $35,000", "degree": "Diseño Gráfico", "hours": "Lunes a Viernes 9-6", "requirements": "Figma, Adobe XD, prototipado, investigación de usuarios."},
        {"title": "Diseñador Gráfico Senior", "salary": "$22,000 - $30,000", "degree": "Diseño Gráfico", "hours": "Presencial", "requirements": "Suite Adobe, Branding, diseño editorial."},
        {"title": "Editor de Video", "salary": "$18,000 - $25,000", "degree": "Comunicación Visual", "hours": "Freelance / Proyecto", "requirements": "Premiere Pro, After Effects, narrativa visual."},
        
        # Marketing / Sales
        {"title": "Gerente de Marketing Digital", "salary": "$35,000 - $50,000", "degree": "Mercadotecnia", "hours": "Lunes a Viernes 9-6", "requirements": "Google Ads, Facebook Ads, SEO/SEM, liderazgo de equipos."},
        {"title": "Community Manager", "salary": "$12,000 - $18,000", "degree": "Comunicación", "hours": "Híbrido", "requirements": "Gestión de redes, copy creativo, atención al cliente."},
        {"title": "Ejecutivo de Ventas B2B", "salary": "$15,000 + Comisiones", "degree": "Administración", "hours": "Lunes a Viernes 8-5", "requirements": "Experiencia en ventas corporativas, CRM, negociación."},
        {"title": "Analista de SEO", "salary": "$20,000 - $28,000", "degree": "Mercadotecnia o Sistemas", "hours": "Remoto", "requirements": "Google Analytics, Search Console, optimización on-page."},
        
        # Admin / HR
        {"title": "Gerente de Recursos Humanos", "salary": "$40,000 - $55,000", "degree": "Psicología o Administración", "hours": "Presencial", "requirements": "Reclutamiento, nómina, clima laboral, LFT."},
        {"title": "Reclutador IT", "salary": "$20,000 - $30,000", "degree": "Psicología", "hours": "Híbrido", "requirements": "Experiencia reclutando perfiles tech, LinkedIn Recruiter."},
        {"title": "Asistente Administrativo", "salary": "$10,000 - $14,000", "degree": "Bachillerato / Trunca", "hours": "Lunes a Viernes 9-6", "requirements": "Manejo de Office, organización, atención a llamadas."},
        {"title": "Contador General", "salary": "$25,000 - $35,000", "degree": "Contaduría Pública", "hours": "Presencial", "requirements": "Cálculo de impuestos, estados financieros, SAT."},
        
        # Other
        {"title": "Ingeniero Civil de Obra", "salary": "$30,000 - $40,000", "degree": "Ingeniería Civil", "hours": "Lunes a Sábado", "requirements": "Supervisión de obra, estimaciones, manejo de personal."},
        {"title": "Arquitecto Proyectista", "salary": "$25,000 - $35,000", "degree": "Arquitectura", "hours": "Lunes a Viernes 9-6", "requirements": "AutoCAD, Revit, renderizado, normatividad."},
        {"title": "Médico General Laboral", "salary": "$22,000 - $28,000", "degree": "Medicina", "hours": "Lunes a Viernes 7-3", "requirements": "Título y cédula, experiencia en salud ocupacional."},
        {"title": "Abogado Corporativo", "salary": "$30,000 - $45,000", "degree": "Derecho", "hours": "Presencial", "requirements": "Contratos, derecho mercantil, propiedad intelectual."},
        {"title": "Chef Ejecutivo", "salary": "$35,000 - $50,000", "degree": "Gastronomía", "hours": "Rotativo", "requirements": "Manejo de cocina, costos, creación de menús."},
        {"title": "Gerente de Operaciones", "salary": "$45,000 - $60,000", "degree": "Ingeniería Industrial", "hours": "Presencial", "requirements": "Optimización de procesos, logística, KPIs."},
        {"title": "Soporte Técnico Bilingüe", "salary": "$16,000 - $22,000", "degree": "Sistemas o Afín", "hours": "Turnos rotativos", "requirements": "Inglés avanzado, troubleshooting, atención a tickets."}
    ]

    # 3. Insert Vacancies
    print(f"Inserting {len(vacancies_data)} vacancies...")
    count = 0
    for v in vacancies_data:
        # Check if exists to avoid duplicates if run multiple times
        if not db.vacancies.find_one({'title': v['title'], 'company_id': company_id}):
            vacancy_doc = {
                'company_id': company_id,
                'company_name': company_name,
                'title': v['title'],
                'requirements': v['requirements'],
                'degree': v['degree'],
                'salary': v['salary'],
                'hours': v['hours'],
                'created_at': datetime.datetime.now(),
                'views': 0,
                'status': 'active'
            }
            db.vacancies.insert_one(vacancy_doc)
            count += 1
            print(f"Inserted: {v['title']}")
        else:
            print(f"Skipped (exists): {v['title']}")

    print(f"Done! Inserted {count} new vacancies.")

if __name__ == '__main__':
    seed_vacancies()
