from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from BookLog import settings

class Author(models.Model):
  first_name = models.CharField(max_length=150, verbose_name="Имя")
  last_name = models.CharField(max_length=150, verbose_name="Фамилия")
  patronymic = models.CharField(max_length=150, verbose_name="Отчество", null=True, blank=True)
  birthday = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
  death = models.DateField(verbose_name="Дата смерти", null=True, blank=True)
  country = models.CharField(max_length=150, verbose_name="Страна", blank=True, null=True)

  def __str__(self):
    return f'{self.last_name} {self.first_name}'  # или любое поле, которое удобно показывать


class Genre(models.Model):
  title = models.CharField(max_length=200, verbose_name="Название")
  description = models.CharField(max_length=200, verbose_name="Описание")

  def __str__(self):
    return self.title
  
class Types(models.IntegerChoices):
  FICTION = 0, "Художественная"
  NON_FICTION = 1, "Нон-фикшн (не художественная)"

class Book(models.Model):
  title = models.CharField(max_length=200, verbose_name="Название")
  author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор", related_name="books")
  genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name="Жанр", related_name="books")
  logo = models.ImageField(verbose_name="Картинка профиля", upload_to="book_logos/", blank=True, null=True)
  symbols = models.IntegerField(verbose_name="Количество символов", null=True, blank=True)
  type = models.IntegerField(choices=Types.choices, verbose_name="Тип")

  def __str__(self):
    return f'{self.title} - {self.author}'

class BookLog(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга", related_name="book_logs")
  start = models.DateField(verbose_name="Начало чтения", null=True, blank=True)
  end = models.DateField(verbose_name="Конец чтения", null=True, blank=True)
  topic = models.TextField(verbose_name="Тема", null=True, blank=True)
  score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Оценка")
  three_sentences = models.TextField(verbose_name="Книга в 3-х предложениях", null=True, blank=True)
  new_knowledge = models.TextField(verbose_name="Новые знания", null=True, blank=True)
  transformed_me = models.TextField(verbose_name="Как книга изменила меня", null=True, blank=True)
  impressions = models.TextField(verbose_name="Впечатления", null=True, blank=True)
  ideas = models.TextField(verbose_name="Основные идеи", null=True, blank=True)
  heroes = models.TextField(verbose_name="Герои", null=True, blank=True)
  begin = models.TextField(verbose_name="Начало действия", null=True, blank=True)
  key_events = models.TextField(verbose_name="Ключевые события", null=True, blank=True)
  most_important_event = models.TextField(verbose_name="Самое главное событие", null=True, blank=True)
  result = models.TextField(verbose_name="Итог", blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
  updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

  def __str__(self):
    return f'{self.book} - {self.updated_at}'

class Quote(models.Model):
  book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга", related_name="quotes")
  note = models.TextField(verbose_name="Цитата")
  likes = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Like', related_name='liked_quotes', verbose_name="Понравилось")
  shared = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Share', related_name='shared_quotes', verbose_name="Поделились")
  privat = models.BooleanField(default=False, verbose_name="Приватность")
  book_log = models.ForeignKey(BookLog, on_delete=models.CASCADE, verbose_name="Запись читателького журнала", null=True, blank=True, related_name="quotes")

  def __str__(self):
    return f'{self.note}'

class Like(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="likes")
  quote = models.ForeignKey(Quote, on_delete=models.CASCADE, verbose_name="Цитата", related_name="like_records")
  moment = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")

  def __str__(self):
    return f'{self.quote} - {self.user}'

  class Meta:
    unique_together = ('user', 'quote')


class Share(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="shares")
  quote = models.ForeignKey(Quote, on_delete=models.CASCADE, verbose_name="Цитата", related_name="share_records")
  moment = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")
  destination = models.CharField(max_length=200, verbose_name="Куда поделились")

  def __str__(self):
    return f'{self.quote} - {self.user} - {self.destination}'
  
  class Meta:
    ordering = ['-moment']
    indexes = [models.Index(fields=['moment'])]
