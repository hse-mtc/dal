from django.db import models


class Person(models.Model):
    surname = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32, blank=True)
    

    @property
    def full_name(self):
        return " ".join([self.surname, self.name, self.patronymic])

    class Meta:
        abstract = True
        verbose_name = "Person"
        verbose_name_plural = "Persons"

    def __str__(self):
        return self.full_name

    
class Relative(Person):
    relative_list = [('father', 'отец'),
                    ('mother', 'мать'),
                    ('sister', 'сестра'),
                    ('brother', 'брат')]
    rel_status = models.CharField(max_length=32, choices=relative_list)
    birthdate = models.DateField()
    citizenship = models.CharField(max_length=32)
    pers_mobile = models.CharField(max_length=15, blank=True)
    permanent_address = models.CharField(max_length=64)
    place_birth = models.CharField(max_length=64)

    class Meta:
        abstract = False
        verbose_name = "Person"
        verbose_name_plural = "Persons"

    def __str__(self):
        return self.full_name

    
class Personnel(Person):
    birthdate = models.DateField()
    photo = models.ImageField(upload_to = '', max_length=128)
    place_birth = models.CharField(max_length=32)
    region_birth = models.CharField(max_length=64)
    citizenship = models.CharField(max_length=32)
    pers_mobile = models.CharField(max_length=15)
    corp_email = models.EmailField()
    pers_email = models.EmailField(blank=True)
    permanent_address = models.CharField(max_length=64)

    class Meta:
        abstract = True
        verbose_name = "Personnel"
        verbose_name_plural = "Personnel"

    def __str__(self):
        return self.full_name
