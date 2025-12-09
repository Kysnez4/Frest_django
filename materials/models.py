from django.db import models

from users.models import User


# Create your models here.
class Course(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    preview = models.ImageField(upload_to="course_preview/", null=True, blank=True)
    last_update = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ["name"]


class Lesson(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    name = models.CharField(max_length=100)
    description = models.TextField()
    preview = models.ImageField(upload_to="lesson_preview/", blank=True, null=True)
    video_url = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"
        ordering = ["name"]


class Subscribe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="subscribers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")  # Одна подписка на курс для пользователя
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"

    def __str__(self):
        return f"{self.user.email} subscribed to {self.course.name}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    date = models.DateField(auto_now_add=True)
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    stripe_product_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_session_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_payment_link = models.URLField(max_length=500, blank=True, null=True)
    stripe_payment_status = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Платеж {self.amount} от {self.user.email} ({self.date})"

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-date"]
