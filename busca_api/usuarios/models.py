from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Manager customizado
class UsuarioManager(BaseUserManager):
    # Cria usuário solicitante
    def create_user(self, email, nome, tipo='solicitante', setor=None, cargo=None, password=None, **extra_fields):
        if not email:
            raise ValueError('O usuário deve ter um email')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, tipo=tipo, setor=setor, cargo=cargo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    # Cria usuário administrador
    def create_superuser(self, email, nome, password=None, **extra_fields):
        user = self.create_user(email, nome, tipo='administrador', password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Modelo de usuário
class Usuario(AbstractBaseUser, PermissionsMixin):
    TIPOS = (
        ('solicitante', 'Solicitante'),
        ('administrador', 'Administrador'),
    )

    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    setor = models.CharField(max_length=100, blank=True, null=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # usado pelo Django admin

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'tipo']

    def __str__(self):
        return f"{self.nome} ({self.tipo})"
