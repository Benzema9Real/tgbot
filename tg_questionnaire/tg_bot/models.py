from django.db import models

class RentSalePremises(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Собственник'),
        ('agent', 'Посредник'),
        ('agency', 'Агентство'),
    ]
    role = models.CharField('Собственник/Посредник/Агентство', max_length=20, choices=ROLE_CHOICES)
    whatsapp = models.CharField('Контакт (WhatsApp)', max_length=20)
    location = models.CharField('Локация, точный адрес', max_length=455)
    entrance_street = models.CharField('С какой улицы вход', max_length=255, blank=True)
    square_meters = models.PositiveIntegerField('Площадь (м²)')
    condition = models.CharField('Состояние помещения (ПСО и т.д.)', max_length=1000)
    kilowatt = models.DecimalField('Нагрузка (кВт)', max_digits=5, decimal_places=2)
    three_phases = models.BooleanField('Есть ли 3 фазы')
    sewerage = models.BooleanField('Канализация')
    water_supply = models.BooleanField('Водопровод')
    ventilation = models.BooleanField('Вентиляция')
    conditioning = models.BooleanField('Кондиционирование')

    ceiling_height = models.DecimalField('Высота потолка (м)', max_digits=4, decimal_places=2)
    entrances_count = models.PositiveIntegerField('Количество входов')
    summer_area = models.BooleanField('Летняя площадка/место под неё')

    parking_available = models.BooleanField('Парковка есть?')
    parking_capacity = models.PositiveIntegerField('На сколько машин', null=True, blank=True)
    parking_type = models.CharField('Тип парковки', max_length=50, choices=[
        ('private', 'Собственная'),
        ('municipal', 'Муниципальная'),
    ])

    documentation_purpose = models.CharField('Профильное предназначение по документам', max_length=100)
    rent_holidays = models.BooleanField('Предоставляются каникулы?')
    holidays_months = models.PositiveIntegerField('Сколько месяцев каникул', null=True, blank=True)

    price_per_m2_kgs = models.DecimalField('Цена за м² (сом)', max_digits=10, decimal_places=2, null=True, blank=True)
    price_per_m2_usd = models.DecimalField('Цена за м² (USD)', max_digits=10, decimal_places=2, null=True, blank=True)

    min_rent_duration_months = models.PositiveIntegerField('Мин. срок аренды (мес)')

    was_operated_before = models.BooleanField('Сдавалось ранее?')

    additional_features = models.TextField('Доп. преимущества (мангал, подвал и пр.)', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.role} - {self.location}'

    class Meta:
        verbose_name = 'Помещение под общепит'
        verbose_name_plural = 'Помещения под общепит'


class InteriorPhoto(models.Model):
    premises = models.ForeignKey(RentSalePremises, on_delete=models.CASCADE, related_name='interior_photos')
    photo = models.ImageField('Фото интерьера', upload_to='interior_photos/')

    def __str__(self):
        return f'Фото для: {self.premises.location}'


class BusinessForSale(models.Model):
    OWNERSHIP_CHOICES = [
        ('rent', 'Аренда'),
        ('owned', 'Собственность'),
    ]
    PARKING_TYPE_CHOICES = [
        ('private', 'Собственная'),
        ('municipal', 'Муниципальная'),
    ]

    ownership = models.CharField('Помещение в аренде или собственность', max_length=10, choices=OWNERSHIP_CHOICES)
    whatsapp = models.CharField('Контакт (WhatsApp)', max_length=20)
    location = models.CharField('Локация, точный адрес', max_length=455)
    entrance_street = models.CharField('С какой улицы вход', max_length=255, blank=True)
    square_meters = models.PositiveIntegerField('Площадь (м²)')
    condition = models.CharField('Состояние помещения (ПСО и т.д.)', max_length=1000)
    kilowatt = models.DecimalField('Нагрузка (кВт)', max_digits=5, decimal_places=2)
    three_phases = models.BooleanField('Есть ли 3 фазы')
    sewerage = models.BooleanField('Канализация')
    water_supply = models.BooleanField('Водопровод')
    ventilation = models.BooleanField('Вентиляция')
    conditioning = models.BooleanField('Кондиционирование')

    ceiling_height = models.DecimalField('Высота потолка (м)', max_digits=4, decimal_places=2)
    entrances_count = models.PositiveIntegerField('Количество входов')
    summer_area = models.BooleanField('Летняя площадка/место под неё')

    parking_available = models.BooleanField('Парковка есть?')
    parking_capacity = models.PositiveIntegerField('На сколько машин', null=True, blank=True)
    parking_type = models.CharField('Тип парковки', max_length=50, choices=PARKING_TYPE_CHOICES)

    documentation_purpose = models.CharField('Профильное предназначение по документам', max_length=100)

    business_price = models.DecimalField('Цена продажи бизнеса (сом)', max_digits=12, decimal_places=2)
    rent_price_per_month = models.DecimalField('Стоимость аренды в месяц (сом)', max_digits=10, decimal_places=2)
    rent_contract_duration = models.PositiveIntegerField('Срок договора аренды (мес)')

    business_name = models.CharField('Название бизнеса', max_length=255)

    additional_features = models.TextField('Доп. преимущества (мангал, подвал и пр.)', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.business_name} – {self.location}'

    class Meta:
        verbose_name = 'Готовый бизнес'
        verbose_name_plural = 'Готовые бизнесы'


class BusinessInteriorPhoto(models.Model):
    business = models.ForeignKey(BusinessForSale, on_delete=models.CASCADE, related_name='interior_photos')
    photo = models.ImageField('Фото интерьера', upload_to='business_interior_photos/')

    def __str__(self):
        return f'Фото для: {self.business.business_name}'


from django.db import models


class LookingForPremises(models.Model):
    BUSINESS_STAGE_CHOICES = [
        ('existing', 'Уже есть действующий бизнес'),
        ('new', 'Открываю впервые'),
    ]

    business_stage = models.CharField(
        'У вас уже есть бизнес или открываете впервые?',
        max_length=20,
        choices=BUSINESS_STAGE_CHOICES
    )
    whatsapp = models.CharField('Контакт (WhatsApp)', max_length=20)
    preferred_areas = models.CharField('Предпочтительные районы', max_length=255)

    min_square_meters = models.PositiveIntegerField('Минимальная площадь (м²)')
    max_square_meters = models.PositiveIntegerField('Максимальная площадь (м²)')

    format_description = models.CharField(
        'Формат помещения (столовая, кофейня, цех, ресторан и пр.)',
        max_length=255
    )

    price_per_m2_kgs = models.DecimalField(
        'Стоимость за м² в сомах',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    price_per_m2_usd = models.DecimalField(
        'Стоимость за м² в долларах',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    min_rent_duration_months = models.PositiveIntegerField('Минимальный срок аренды (мес)')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Запрос на помещение – {self.preferred_areas}'

    class Meta:
        verbose_name = 'Запрос на помещение под общепит'
        verbose_name_plural = 'Запросы на помещения под общепит'

