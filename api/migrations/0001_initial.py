# Generated by Django 4.0.5 on 2022-10-10 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorRegister',
            fields=[
                ('doctor_id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=50)),
                ('specialization', models.CharField(max_length=150)),
                ('hospital_id', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('password1', models.CharField(max_length=20)),
                ('password2', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'doctor_reg',
            },
        ),
        migrations.CreateModel(
            name='PainAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'pain_answers',
            },
        ),
        migrations.CreateModel(
            name='PainQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'pain_questions',
            },
        ),
        migrations.CreateModel(
            name='PatientRegister',
            fields=[
                ('patient_id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=15)),
                ('username', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=50)),
                ('password1', models.CharField(max_length=10)),
                ('password2', models.CharField(max_length=10)),
                ('hospital_number', models.CharField(blank=True, default='', max_length=20)),
                ('dateofbirth', models.CharField(default='', max_length=10)),
                ('address', models.TextField(blank=True, default='')),
                ('postcode', models.CharField(default='', max_length=10)),
                ('is_verified', models.BooleanField(default=False)),
                ('auth_token', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'db_table': 'patient_reg',
            },
        ),
        migrations.CreateModel(
            name='TechRegister',
            fields=[
                ('tech_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('phone_number', models.BigIntegerField()),
                ('address', models.TextField()),
                ('password1', models.CharField(max_length=10)),
                ('password2', models.CharField(max_length=10)),
                ('doctor_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.doctorregister')),
                ('patient_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.patientregister')),
            ],
            options={
                'db_table': 'tech_reg',
            },
        ),
        migrations.CreateModel(
            name='PainSelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.BooleanField(default=False)),
                ('comments', models.TextField(blank=True, null=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('answer_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.painanswers')),
                ('patient_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.patientregister')),
                ('question_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.painquestions')),
            ],
            options={
                'db_table': 'pain_selection',
            },
        ),
        migrations.CreateModel(
            name='PainDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_pain_began', models.CharField(blank=True, max_length=20)),
                ('onset_of_pain', models.CharField(blank=True, max_length=20)),
                ('gender', models.CharField(max_length=20)),
                ('comments', models.TextField(blank=True)),
                ('patient_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.patientregister')),
            ],
            options={
                'db_table': 'pain_details',
            },
        ),
    ]
