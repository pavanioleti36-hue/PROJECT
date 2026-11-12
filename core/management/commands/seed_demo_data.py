"""
Demo data seed command for Forest Fire Detection System.
All created data is clearly marked as SIMULATED.

Usage:
    python manage.py seed_demo_data
"""

import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
import datetime


class Command(BaseCommand):
    help = ('Seed the database with demo data for demonstration purposes. '
            'All created data is clearly marked as SIMULATED.')

    def handle(self, *args, **options):
        self.stdout.write(
            '\n' + '='*60 + '\n'
            'FOREST FIRE DETECTION SYSTEM - DEMO DATA SEEDER\n'
            'All created data is SIMULATED and for demo only.\n'
            + '='*60
        )

        from sensors.models import SensorNode
        if SensorNode.objects.filter(is_simulated=True).exists():
            self.stdout.write(
                '\nDemo data already exists. Skipping.\n'
                'To re-seed, delete existing simulated records first.'
            )
            return

        self._create_users()
        forests, areas = self._create_forests_and_areas()
        nodes = self._create_sensor_nodes(areas)
        self._create_sensor_readings(nodes)
        self._create_weather(areas)
        self._create_incidents(forests, areas)
        self._create_alerts(areas, nodes)
        self._print_summary()

    def _create_users(self):
        from accounts.models import CustomUser
        self.stdout.write('\n[1/7] Creating demo users...')

        if not CustomUser.objects.filter(username='admin').exists():
            CustomUser.objects.create_superuser(
                username='admin',
                email='admin@forestfire.example.com',
                password='admin123',
                first_name='System',
                last_name='Administrator',
                role='administrator',
                department='IT Administration',
            )
            self.stdout.write(self.style.SUCCESS('  [OK] Superuser: admin / admin123'))
        else:
            self.stdout.write('  admin already exists')

        demo_users = [
            ('forest_officer', 'officer', 'Ravi', 'Kumar', 'Forest Range', 'FO-001'),
            ('fire_department', 'fireofficer', 'Priya', 'Sharma', 'Fire Dept', 'FD-001'),
            ('local_authority', 'localadmin', 'Suresh', 'Patel', 'Local Admin', 'LA-001'),
            ('administrator', 'sysadmin', 'Anjali', 'Singh', 'IT Admin', 'SA-001'),
        ]
        for role, username, first, last, dept, emp_id in demo_users:
            if not CustomUser.objects.filter(username=username).exists():
                CustomUser.objects.create_user(
                    username=username, password='demo1234',
                    first_name=first, last_name=last,
                    email=username + '@forestfire.example.com',
                    role=role, department=dept, employee_id=emp_id,
                )
                self.stdout.write(self.style.SUCCESS(
                    '  [OK] ' + role + ': ' + username + ' / demo1234'))

    def _create_forests_and_areas(self):
        from forest_env.models import Forest, ForestArea, Vegetation, Wildlife
        self.stdout.write('\n[2/7] Creating forests and areas...')

        forest_data = [
            {'name': 'Sariska Tiger Reserve', 'state': 'Rajasthan', 'district': 'Alwar',
             'forest_type': 'Tropical Dry Deciduous', 'total_area_hectares': Decimal('87300'),
             'is_protected': True, 'established_year': 1958,
             'description': 'Famous tiger reserve in Rajasthan.'},
            {'name': 'Bandipur National Park', 'state': 'Karnataka', 'district': 'Chamarajanagar',
             'forest_type': 'Southern Tropical Moist Deciduous', 'total_area_hectares': Decimal('87400'),
             'is_protected': True, 'established_year': 1974,
             'description': 'Part of the Nilgiris Biosphere Reserve.'},
            {'name': 'Simlipal Biosphere Reserve', 'state': 'Odisha', 'district': 'Mayurbhanj',
             'forest_type': 'Tropical Moist Semi-Evergreen', 'total_area_hectares': Decimal('284500'),
             'is_protected': True, 'established_year': 1973,
             'description': 'One of the largest national parks in India.'},
        ]
        forests = []
        for fd in forest_data:
            f, _ = Forest.objects.get_or_create(name=fd['name'], defaults=fd)
            forests.append(f)
            self.stdout.write('  Forest: ' + f.name)

        area_configs = [
            (forests[0], 'North Zone', 'core', Decimal('12500'), 27.3516, 76.3421, True),
            (forests[0], 'South Buffer Zone', 'buffer', Decimal('8200'), 27.2890, 76.3891, False),
            (forests[1], 'Moyar River Zone', 'core', Decimal('15000'), 11.6765, 76.6342, True),
            (forests[1], 'Eastern Grasslands', 'peripheral', Decimal('6500'), 11.7123, 76.7045, False),
            (forests[2], 'Chahala Core', 'core', Decimal('25000'), 21.8451, 86.3123, True),
            (forests[2], 'Nawana Buffer', 'buffer', Decimal('18000'), 21.9234, 86.4567, False),
        ]
        areas = []
        for forest, name, zone, area_ha, lat, lng, high_risk in area_configs:
            area, _ = ForestArea.objects.get_or_create(
                name=name, forest=forest,
                defaults={'zone_type': zone, 'area_hectares': area_ha,
                          'latitude': Decimal(str(lat)), 'longitude': Decimal(str(lng)),
                          'is_high_risk': high_risk})
            areas.append(area)
            self.stdout.write('  Area: ' + area.name)

        veg_types = ['Sal', 'Teak', 'Bamboo', 'Acacia', 'Dry Grassland', 'Shrubland']
        for i, area in enumerate(areas):
            Vegetation.objects.get_or_create(
                forest_area=area, vegetation_type=veg_types[i],
                defaults={'density': random.choice(['moderate', 'dense', 'very_dense']),
                          'moisture_content': Decimal(str(random.randint(15, 65))),
                          'fire_susceptibility': 'high' if area.is_high_risk else 'medium'})

        species = [
            ('Bengal Tiger', 'Panthera tigris tigris', 'endangered'),
            ('Indian Leopard', 'Panthera pardus fusca', 'rare'),
            ('Asian Elephant', 'Elephas maximus indicus', 'endangered'),
            ('Sloth Bear', 'Melursus ursinus', 'rare'),
            ('Indian Gaur', 'Bos gaurus', 'common'),
            ('Spotted Deer', 'Axis axis', 'abundant'),
        ]
        for i, area in enumerate(areas):
            sname, sciname, status = species[i]
            Wildlife.objects.get_or_create(
                forest_area=area, species_name=sname,
                defaults={'scientific_name': sciname, 'conservation_status': status,
                          'population_estimate': random.randint(5, 200)})
        return forests, areas

    def _create_sensor_nodes(self, areas):
        from sensors.models import (SensorNode, TemperatureSensor, SmokeSensor,
                                     FlameSensor, HumiditySensor, GasSensor)
        self.stdout.write('\n[3/7] Creating sensor nodes...')
        nodes = []
        node_configs = [
            (areas[0], 'SN-001', 'North Zone Alpha Node'),
            (areas[1], 'SN-002', 'South Buffer Node'),
            (areas[2], 'SN-003', 'Moyar River Sensor'),
            (areas[3], 'SN-004', 'Eastern Grassland Monitor'),
            (areas[4], 'SN-005', 'Chahala Core Detector'),
            (areas[5], 'SN-006', 'Nawana Boundary Node'),
        ]
        for area, node_id, name in node_configs:
            node, created = SensorNode.objects.get_or_create(
                node_id=node_id,
                defaults={'name': name, 'forest_area': area,
                          'latitude': area.latitude, 'longitude': area.longitude,
                          'status': 'active', 'is_simulated': True,
                          'battery_level': random.randint(60, 100),
                          'last_seen': timezone.now()})
            if created:
                TemperatureSensor.objects.create(node=node)
                SmokeSensor.objects.create(node=node)
                FlameSensor.objects.create(node=node)
                HumiditySensor.objects.create(node=node)
                GasSensor.objects.create(node=node)
            nodes.append(node)
            self.stdout.write('  Node: ' + node.node_id + ' - ' + node.name)
        return nodes

    def _create_sensor_readings(self, nodes):
        from sensors.models import SensorData
        self.stdout.write('\n[4/7] Creating sensor readings (20 per node)...')
        scenarios = [('normal', 15), ('warning', 3), ('fire_suspected', 1), ('fire_detected', 1)]
        now = timezone.now()
        for node in nodes:
            count = 0
            for scenario, num in scenarios:
                for _ in range(num):
                    offset = random.randint(0, 168)
                    ts = now - datetime.timedelta(hours=offset, minutes=random.randint(0, 59))
                    SensorData.objects.create(**self._build_reading(node, scenario, ts))
                    count += 1
            self.stdout.write('  Node ' + node.node_id + ': ' + str(count) + ' readings')

    def _build_reading(self, node, scenario, ts):
        cfg = {
            'normal': (20, 36, 50, 82, 5, 80, 5, 60, False, 0),
            'warning': (38, 52, 25, 45, 100, 220, 70, 130, False, 0),
            'fire_suspected': (55, 72, 12, 28, 250, 420, 150, 250,
                               random.random() > 0.5, random.uniform(15, 55)),
            'fire_detected': (75, 110, 5, 18, 450, 700, 250, 450,
                              True, random.uniform(60, 100)),
        }[scenario]
        tlo, thi, hlo, hhi, slo, shi, glo, ghi, flame, fi = cfg
        return {
            'node': node, 'timestamp': ts,
            'temperature': Decimal(str(round(random.uniform(tlo, thi), 2))),
            'humidity': Decimal(str(round(random.uniform(hlo, hhi), 2))),
            'smoke_level': Decimal(str(round(random.uniform(slo, shi), 2))),
            'gas_concentration': Decimal(str(round(random.uniform(glo, ghi), 2))),
            'flame_detected': flame,
            'flame_intensity': Decimal(str(round(fi, 2))) if flame and fi > 0 else None,
            'is_simulated': True,
            'notes': '[SIMULATED] Scenario: ' + scenario,
        }

    def _create_weather(self, areas):
        from forest_env.models import WeatherCondition
        self.stdout.write('\n[5/7] Creating weather records...')
        now = timezone.now()
        conds = ['Clear', 'Partly Cloudy', 'Hot & Dry', 'Windy', 'Overcast']
        for i, area in enumerate(areas):
            WeatherCondition.objects.get_or_create(
                forest_area=area, recorded_at=now - datetime.timedelta(hours=i),
                defaults={
                    'temperature': Decimal(str(round(random.uniform(28, 42), 1))),
                    'humidity': Decimal(str(round(random.uniform(18, 65), 1))),
                    'wind_speed': Decimal(str(round(random.uniform(5, 35), 1))),
                    'wind_direction': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
                    'rainfall': Decimal('0.00'), 'condition': conds[i % len(conds)]})
            self.stdout.write('  Weather for: ' + area.name)

    def _create_incidents(self, forests, areas):
        from incidents.models import FireIncident
        self.stdout.write('\n[6/7] Creating fire incidents...')
        data_list = [
            {'forest': forests[0], 'forest_area': areas[0],
             'title': 'North Zone Fire Incident 2024',
             'description': '[SIMULATED] Wildfire in north zone.',
             'severity': 'major', 'status': 'extinguished',
             'latitude': areas[0].latitude, 'longitude': areas[0].longitude,
             'fire_start_time': timezone.now() - datetime.timedelta(days=30),
             'fire_end_time': timezone.now() - datetime.timedelta(days=28),
             'area_burned_hectares': Decimal('450.00'), 'is_simulated': True},
            {'forest': forests[1], 'forest_area': areas[2],
             'title': 'Moyar River Smoke Detection',
             'description': '[SIMULATED] Smoke near river zone.',
             'severity': 'minor', 'status': 'false_alarm',
             'latitude': areas[2].latitude, 'longitude': areas[2].longitude,
             'fire_start_time': timezone.now() - datetime.timedelta(days=15),
             'fire_end_time': timezone.now() - datetime.timedelta(days=15),
             'area_burned_hectares': Decimal('0.00'), 'is_simulated': True},
            {'forest': forests[2], 'forest_area': areas[4],
             'title': 'Chahala Core - Active Fire Alert',
             'description': '[SIMULATED] Active fire in sal forest.',
             'severity': 'catastrophic', 'status': 'under_control',
             'latitude': areas[4].latitude, 'longitude': areas[4].longitude,
             'fire_start_time': timezone.now() - datetime.timedelta(hours=6),
             'area_burned_hectares': Decimal('1200.00'), 'is_simulated': True},
        ]
        for data in data_list:
            inc = FireIncident.objects.create(**data)
            self.stdout.write('  Incident: ' + inc.incident_id + ' - ' + inc.title)

    def _create_alerts(self, areas, nodes):
        from alerts.models import Alert
        self.stdout.write('\n[7/7] Creating demo alerts...')
        alert_list = [
            (areas[0], nodes[0], 'critical', 'FIRE DETECTED - North Zone Alpha',
             '[SIMULATED] Temp 87C, Smoke 520ppm, Flame confirmed.',
             'fire_detected', Decimal('85.50'), 'active'),
            (areas[2], nodes[2], 'critical', 'Fire Suspected - Moyar River Zone',
             '[SIMULATED] Temp 65C, Smoke 380ppm.',
             'fire_suspected', Decimal('68.20'), 'active'),
            (areas[4], nodes[4], 'critical', 'EMERGENCY - Chahala Core Fire',
             '[SIMULATED] All sensors indicate active fire.',
             'fire_detected', Decimal('92.10'), 'acknowledged'),
            (areas[1], nodes[1], 'warning', 'High Temperature Warning',
             '[SIMULATED] Temp exceeds 45C threshold.',
             'warning', Decimal('42.00'), 'resolved'),
            (areas[3], nodes[3], 'info', 'Smoke Level Elevated',
             '[SIMULATED] Smoke above 150ppm.',
             'warning', Decimal('28.50'), 'resolved'),
        ]
        for area, node, severity, title, msg, cond, score, status in alert_list:
            Alert.objects.create(
                forest_area=area, sensor_node=node, severity=severity,
                title=title, message=msg, condition=cond,
                fire_risk_score=score, status=status, is_simulated=True)
            self.stdout.write('  Alert [' + severity.upper() + ']: ' + title[:50])

    def _print_summary(self):
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('DEMO DATA SEEDED SUCCESSFULLY!'))
        self.stdout.write('='*60)
        self.stdout.write('\nLOGIN CREDENTIALS:')
        self.stdout.write('  Admin         : admin / admin123')
        self.stdout.write('  Forest Officer: officer / demo1234')
        self.stdout.write('  Fire Dept     : fireofficer / demo1234')
        self.stdout.write('  Local Auth    : localadmin / demo1234')
        self.stdout.write('  Sys Admin     : sysadmin / demo1234')
        self.stdout.write('\nNOTE: All data is SIMULATED. Not real sensor data.\n')
