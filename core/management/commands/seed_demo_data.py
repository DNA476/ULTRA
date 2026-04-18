from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

from clients.models import Client
from employees.models import EmployeeProfile
from models_app.models import ModelCard
from projects.models import Participation, Project


DEFAULT_PASSWORD = 'Ultra12345!'


class Command(BaseCommand):
    help = 'Create demo users, employees, model cards, clients, projects and participations.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            default=DEFAULT_PASSWORD,
            help='Password for created demo users.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        password = options['password']
        User = get_user_model()

        groups = self.create_groups()
        users = self.create_users(User, groups, password)
        employees = self.create_employees(users)
        models = self.create_models(users['scout'])
        clients = self.create_clients()
        projects = self.create_projects(clients, employees)
        participations_count = self.create_participations(projects, models)

        self.stdout.write(self.style.SUCCESS('Demo data is ready.'))
        self.stdout.write(f'Users password: {password}')
        self.stdout.write(f'Employees: {len(employees)}')
        self.stdout.write(f'Model cards: {len(models)}')
        self.stdout.write(f'Clients: {len(clients)}')
        self.stdout.write(f'Projects: {len(projects)}')
        self.stdout.write(f'Participations created or updated: {participations_count}')

    def create_groups(self):
        role_names = {
            EmployeeProfile.Role.DIRECTOR: 'Director',
            EmployeeProfile.Role.BOOKER: 'Booker',
            EmployeeProfile.Role.SCOUT: 'Scout',
            EmployeeProfile.Role.ADMIN: 'System administrator',
        }
        groups = {}
        for role, name in role_names.items():
            group, _ = Group.objects.get_or_create(name=name)
            groups[role] = group
        return groups

    def create_users(self, User, groups, password):
        user_specs = {
            'admin': {
                'username': 'admin',
                'email': 'admin@ultra.local',
                'first_name': 'System',
                'last_name': 'Admin',
                'role': EmployeeProfile.Role.ADMIN,
                'is_staff': True,
                'is_superuser': True,
            },
            'director': {
                'username': 'director',
                'email': 'director@ultra.local',
                'first_name': 'Maria',
                'last_name': 'Director',
                'role': EmployeeProfile.Role.DIRECTOR,
                'is_staff': True,
                'is_superuser': False,
            },
            'booker': {
                'username': 'booker',
                'email': 'booker@ultra.local',
                'first_name': 'Elena',
                'last_name': 'Booker',
                'role': EmployeeProfile.Role.BOOKER,
                'is_staff': True,
                'is_superuser': False,
            },
            'scout': {
                'username': 'scout',
                'email': 'scout@ultra.local',
                'first_name': 'Nika',
                'last_name': 'Scout',
                'role': EmployeeProfile.Role.SCOUT,
                'is_staff': False,
                'is_superuser': False,
            },
        }

        users = {}
        for key, data in user_specs.items():
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'is_staff': data['is_staff'],
                    'is_superuser': data['is_superuser'],
                    'is_active': True,
                },
            )
            user.email = data['email']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.is_staff = data['is_staff']
            user.is_superuser = data['is_superuser']
            user.is_active = True
            if created:
                user.set_password(password)
            user.save()
            user.groups.set([groups[data['role']]])
            users[key] = user
        return users

    def create_employees(self, users):
        today = date.today()
        specs = {
            'admin': {
                'role': EmployeeProfile.Role.ADMIN,
                'phone': '+971500000001',
                'hire_date': today - timedelta(days=730),
                'notes': 'Maintains local system settings and user accounts.',
            },
            'director': {
                'role': EmployeeProfile.Role.DIRECTOR,
                'phone': '+971500000002',
                'hire_date': today - timedelta(days=900),
                'notes': 'Responsible for agency management and financial reports.',
            },
            'booker': {
                'role': EmployeeProfile.Role.BOOKER,
                'phone': '+971500000003',
                'hire_date': today - timedelta(days=420),
                'notes': 'Manages clients, castings and project bookings.',
            },
            'scout': {
                'role': EmployeeProfile.Role.SCOUT,
                'phone': '+971500000004',
                'hire_date': today - timedelta(days=180),
                'notes': 'Adds new faces and supports model database updates.',
            },
        }

        employees = {}
        for key, data in specs.items():
            employee, _ = EmployeeProfile.objects.update_or_create(
                user=users[key],
                defaults={
                    'role': data['role'],
                    'phone': data['phone'],
                    'hire_date': data['hire_date'],
                    'is_active': True,
                    'notes': data['notes'],
                },
            )
            employees[key] = employee
        return employees

    def create_models(self, added_by):
        model_specs = [
            ('Anna', 'Volkova', 'Dubai', 176, 84, 60, 88, 'top', 'active'),
            ('Sofia', 'Morozova', 'Abu Dhabi', 174, 82, 59, 87, 'new_face', 'active'),
            ('Mila', 'Sokolova', 'Dubai', 179, 86, 61, 90, 'commercial', 'on_contract'),
            ('Daria', 'Petrova', 'Sharjah', 172, 83, 62, 89, 'new_face', 'active'),
            ('Alina', 'Smirnova', 'Dubai', 181, 87, 60, 91, 'top', 'on_contract'),
            ('Eva', 'Kuznetsova', 'Ajman', 170, 81, 58, 86, 'commercial', 'active'),
            ('Polina', 'Lebedeva', 'Dubai', 177, 85, 61, 89, 'top', 'active'),
            ('Kira', 'Orlova', 'Abu Dhabi', 173, 82, 60, 88, 'new_face', 'archived'),
            ('Vera', 'Fedorova', 'Dubai', 175, 84, 59, 87, 'commercial', 'active'),
            ('Nina', 'Makarova', 'Sharjah', 178, 86, 62, 90, 'new_face', 'active'),
        ]

        models = []
        for index, spec in enumerate(model_specs, start=1):
            first_name, last_name, city, height, bust, waist, hips, category, status = spec
            model, _ = ModelCard.objects.update_or_create(
                email=f'{first_name.lower()}.{last_name.lower()}@models.local',
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'birth_date': date(1998 + index % 6, index % 12 + 1, min(index + 8, 28)),
                    'phone': f'+971551000{index:03d}',
                    'city': city,
                    'height': height,
                    'bust': bust,
                    'waist': waist,
                    'hips': hips,
                    'shoe_size': Decimal('38.0') + Decimal(index % 4) / Decimal('2'),
                    'hair_color': ['brown', 'blonde', 'black', 'dark blonde'][index % 4],
                    'eye_color': ['brown', 'blue', 'green', 'gray'][index % 4],
                    'experience': 'Commercial shoots, castings and showroom work.' if index % 3 else '',
                    'category': category,
                    'status': status,
                    'added_by': added_by,
                },
            )
            models.append(model)
        return models

    def create_clients(self):
        client_specs = [
            ('Aurora Fashion', 'Olivia Stone', '+97144000101', 'booking@aurora.local', 'Dubai'),
            ('Palm Events', 'Adam Grant', '+97144000102', 'events@palm.local', 'Dubai'),
            ('Desert Media', 'Sara Bloom', '+97144000103', 'hello@desertmedia.local', 'Abu Dhabi'),
            ('Marina Studio', 'Liam Fox', '+97144000104', 'studio@marina.local', 'Dubai'),
            ('Gulf Retail Group', 'Mona Reed', '+97144000105', 'retail@gulf.local', 'Sharjah'),
        ]

        clients = []
        for name, contact, phone, email, city in client_specs:
            client, _ = Client.objects.update_or_create(
                name=name,
                defaults={
                    'contact_person': contact,
                    'phone': phone,
                    'email': email,
                    'city': city,
                    'notes': 'Demo client for local testing.',
                },
            )
            clients.append(client)
        return clients

    def create_projects(self, clients, employees):
        today = date.today()
        project_specs = [
            ('Spring Lookbook', 0, 'photosession', -35, -33, 'completed', '18000.00', 'booker'),
            ('Mall Casting', 4, 'casting', -18, None, 'in_progress', '6000.00', 'booker'),
            ('Luxury Brand Show', 0, 'show', 10, 11, 'new', '35000.00', 'director'),
            ('Summer Campaign', 2, 'advertising', -8, 2, 'in_progress', '42000.00', 'booker'),
            ('Editorial Shoot', 3, 'photosession', -60, -59, 'completed', '12000.00', 'booker'),
            ('Retail Casting', 4, 'casting', 5, None, 'new', '5000.00', 'scout'),
            ('Evening Wear Show', 1, 'show', -75, -74, 'completed', '26000.00', 'director'),
            ('Beauty Product Ad', 2, 'advertising', -3, 12, 'in_progress', '30000.00', 'booker'),
        ]

        projects = []
        for title, client_index, project_type, start_delta, end_delta, status, budget, employee_key in project_specs:
            start_date = today + timedelta(days=start_delta)
            end_date = today + timedelta(days=end_delta) if end_delta is not None else None
            project, _ = Project.objects.update_or_create(
                title=title,
                defaults={
                    'client': clients[client_index],
                    'project_type': project_type,
                    'description': f'Demo project: {title}.',
                    'start_date': start_date,
                    'end_date': end_date,
                    'status': status,
                    'budget': Decimal(budget),
                    'responsible_employee': employees[employee_key],
                    'notes': 'Created by seed_demo_data command.',
                },
            )
            projects.append(project)
        return projects

    def create_participations(self, projects, models):
        statuses = [
            Participation.Status.INVITED,
            Participation.Status.UNDER_REVIEW,
            Participation.Status.APPROVED,
            Participation.Status.REJECTED,
            Participation.Status.COMPLETED,
        ]
        count = 0
        for project_index, project in enumerate(projects):
            selected_models = [
                models[project_index % len(models)],
                models[(project_index + 2) % len(models)],
                models[(project_index + 4) % len(models)],
            ]
            for model_index, model in enumerate(selected_models):
                status = statuses[(project_index + model_index) % len(statuses)]
                Participation.objects.update_or_create(
                    project=project,
                    model=model,
                    defaults={
                        'status': status,
                        'comment': 'Demo participation created for reports and project cards.',
                    },
                )
                count += 1
        return count
