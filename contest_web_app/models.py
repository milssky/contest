from django.conf import  settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Course(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название курса"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Ссылка на курс"
    )
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ("id",)


class Task(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        related_name="tasks",
        blank=False,
        null=False,
        verbose_name="Курс",
        help_text="Выберите курс для привязки задачи"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
        help_text="Введите название задачи"
    )
    task_text = models.TextField(
        blank=False,
        verbose_name="Условие задачи"
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    score = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        validators=[
            MinValueValidator(1, "Баллов не может быть меньше 1"),
            MaxValueValidator(10, "Баллов не может быть больше 10")
        ]
    )
    language = models.CharField(max_length=50)  # @TODO добавить выбор языка задачи

    def __str__(self):
        return f"{self.course}-{self.title}"

    class Meta:
        ordering = ("-pub_date",)
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"


class Attempt(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="attempts",
        on_delete=models.CASCADE
    )
    status = ...  # @TODO Наверное нужен enum
    task = models.ForeignKey(
        Task,
        related_name="tasks",
        on_delete=models.CASCADE
    )
    attempt_datetime = models.DateTimeField(auto_now_add=True)
    solution_text = models.TextField()

    def __str__(self):
        return f"{self.author} at {self.attempt_datetime}"

    class Meta:
        ordering = ("-attempt_datetime",)
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
