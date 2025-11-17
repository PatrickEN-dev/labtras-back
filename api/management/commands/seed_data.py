from django.core.management.base import BaseCommand
from api.models.location import Location
from api.models.room import Room
from api.models.manager import Manager
from api.models.booking import Booking


class Command(BaseCommand):
    help = "Popula o banco de dados com dados iniciais baseados no mock do front-end"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Limpa todos os dados antes de criar novos",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Limpando dados existentes..."))
            Booking.objects.all().delete()
            Room.objects.all().delete()
            Manager.objects.all().delete()
            Location.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Dados limpos com sucesso!"))

        # Verificar se já existem dados
        if Location.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Dados já existem no banco. Use --clear para limpar antes de popular."
                )
            )
            return

        self.stdout.write("📍 Criando localizações...")

        # Criar localizações
        location1 = Location.objects.create(
            name="Prédio Principal",
            address="Rua das Empresas, 123 - Centro",
            description="Prédio principal da empresa",
        )

        location2 = Location.objects.create(
            name="Anexo Administrativo",
            address="Rua das Empresas, 125 - Centro",
            description="Prédio anexo com salas administrativas",
        )

        location3 = Location.objects.create(
            name="Centro de Treinamento",
            address="Av. do Conhecimento, 456 - Tech Park",
            description="Centro dedicado a treinamentos e workshops",
        )

        self.stdout.write("🏢 Criando salas...")

        # Criar salas - Prédio Principal
        Room.objects.create(
            name="Sala de Reunião A",
            capacity=10,
            location=location1,
            description="Sala com projetor e ar condicionado",
        )

        Room.objects.create(
            name="Sala de Reunião B",
            capacity=6,
            location=location1,
            description="Sala mais reservada para reuniões menores",
        )

        Room.objects.create(
            name="Auditório Principal",
            capacity=50,
            location=location1,
            description="Auditório para apresentações e eventos",
        )

        Room.objects.create(
            name="Sala Íntima",
            capacity=2,
            location=location1,
            description="Sala para 2 pessoas - perfeita para reuniões 1:1",
        )

        Room.objects.create(
            name="Sala Média",
            capacity=12,
            location=location1,
            description="Sala para 12 pessoas - boa para reuniões de equipe",
        )

        # Criar salas - Anexo Administrativo
        Room.objects.create(
            name="Sala de Conferência",
            capacity=15,
            location=location2,
            description="Sala de conferência com videoconferência",
        )

        Room.objects.create(
            name="Sala de Brainstorming",
            capacity=8,
            location=location2,
            description="Sala criativa com quadro branco",
        )

        Room.objects.create(
            name="Sala Pequena",
            capacity=4,
            location=location2,
            description="Sala para 4 pessoas - ideal para equipes pequenas",
        )

        Room.objects.create(
            name="Sala Executive",
            capacity=8,
            location=location2,
            description="Sala executiva para 8 pessoas - reuniões de diretoria",
        )

        # Criar salas - Centro de Treinamento
        Room.objects.create(
            name="Laboratório de Informática",
            capacity=20,
            location=location3,
            description="Laboratório com computadores para treinamento",
        )

        Room.objects.create(
            name="Sala de Workshop",
            capacity=25,
            location=location3,
            description="Sala flexível para workshops e dinâmicas",
        )

        Room.objects.create(
            name="Sala Grande",
            capacity=30,
            location=location3,
            description="Sala para 30 pessoas - ideal para treinamentos",
        )

        Room.objects.create(
            name="Sala de Apresentação",
            capacity=40,
            location=location3,
            description="Sala para 40 pessoas - apresentações e demos",
        )

        self.stdout.write("👥 Criando gerentes...")

        # Criar gerentes
        Manager.objects.create(
            name="João Silva", email="joao.silva@empresa.com", phone="(11) 9876-5432"
        )

        Manager.objects.create(
            name="Maria Santos",
            email="maria.santos@empresa.com",
            phone="(11) 9876-5433",
        )

        Manager.objects.create(
            name="Pedro Oliveira",
            email="pedro.oliveira@empresa.com",
            phone="(11) 9876-5434",
        )

        Manager.objects.create(
            name="Ana Costa", email="ana.costa@empresa.com", phone="(11) 9876-5435"
        )

        Manager.objects.create(
            name="Carlos Ferreira",
            email="carlos.ferreira@empresa.com",
            phone="(11) 9876-5436",
        )

        self.stdout.write(self.style.SUCCESS("✅ Seed concluído com sucesso!"))
        self.stdout.write(f"📍 {Location.objects.count()} localizações criadas")
        self.stdout.write(f"🏢 {Room.objects.count()} salas criadas")
        self.stdout.write(f"👥 {Manager.objects.count()} gerentes criados")
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("🎉 Agora você pode criar bookings facilmente!")
        )
