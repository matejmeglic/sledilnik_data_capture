from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone


class Hospital(models.Model):
    name = models.CharField("Polno ime COVID bolnišnice", max_length=100)
    short_name = models.CharField("Kratica COVID bolnišnice", max_length=30)
    is_active = models.BooleanField(
        "Ali je bolnišnica trenutno aktivna?", default=False
    )

    class Meta:
        verbose_name = "Bolnišnica"
        verbose_name_plural = "Bolnišnice"
        ordering = ("-is_active", "name")

    def __str__(self):
        return self.short_name


class EmailLogRecipient(models.Model):
    email = models.EmailField()

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emaili"
        ordering = ("-email",)

    def __str__(self):
        return self.email


class Report_type(models.Model):
    name = models.CharField("Polno ime poročila", max_length=100)
    slug = models.SlugField("Kratica poročila", unique=True)
    is_active = models.BooleanField(
        "Ali je email poročilo trenutno aktivno?", default=False
    )
    recipients = models.ManyToManyField(EmailLogRecipient, verbose_name="Email naslovi")
    send_partial_report = models.TimeField(auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField("Zadnja sprememba", auto_now_add=True)

    class Meta:
        verbose_name = "Email poročanje in adrema"
        verbose_name_plural = "Email poročanja in adreme"
        ordering = ("slug",)

    def __str__(self):
        return self.slug


class Email_log(models.Model):
    timestamp = models.DateTimeField("Timestamp", auto_now_add=True)
    date_report_sent = models.DateField(
        ("Datum poslanega emaila"),
        default=django.utils.timezone.now,
        help_text="LLLL-MM-DD",
    )
    date_report_sent_for = models.DateField(
        ("Datum poročanja"), default=django.utils.timezone.now, help_text="LLLL-MM-DD",
    )
    report_type = models.ForeignKey(
        Report_type, null=True, blank=True, on_delete=models.SET_NULL
    )
    full_report_sent = models.BooleanField(
        "Popolno poročilo (vse aktivne bolnice)", default=False
    )
    partial_report_sent = models.BooleanField(
        "Delno poročilo (samo nekatere bolnice)", default=False
    )
    recipients = models.TextField("Email adrema", blank=True, null=True)

    class Meta:
        verbose_name = "Poslano sporočilo"
        verbose_name_plural = "Poslana sporočila"
        ordering = (
            "date_report_sent",
            "date_report_sent_for",
            "report_type",
            "full_report_sent",
            "partial_report_sent",
        )

    def __str__(self):
        return str(self.date_report_sent_for)


class ReportHOS(models.Model):
    def yesterday():
        return django.utils.timezone.now() - django.utils.timezone.timedelta(days=1)

    date_form_saved = models.DateTimeField(auto_now_add=True)
    report_type = models.CharField(
        "Tip poročila - short name", max_length=8, blank=True, null=True,
    )
    submitted_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL
    )
    date_reporting = models.DateField(
        ("Datum, za katerega poročamo"), default=yesterday, help_text="DD.MM.LLLL",
    )
    hospital = models.ForeignKey(
        Hospital, on_delete=models.SET_NULL, null=True, verbose_name="Bolnišnica"
    )
    total_hospitalized = models.PositiveIntegerField(
        "Število vseh hospitaliziranih COVID", null=True, blank=True
    )
    total_hospitalized_ICU = models.PositiveIntegerField(
        "Število hospitaliziranih COVID na intenzivni negi", null=True, blank=True
    )
    total_released = models.PositiveIntegerField(
        "Število odpuščenih pacientov COVID", null=True, blank=True
    )
    total_deaths = models.PositiveIntegerField(
        "Število smrtnih primerov s COVID", null=True, blank=True
    )
    deaths_info = models.CharField(
        "Informacije o preminulih",
        max_length=100,
        help_text="Spol M/Ž in starost umrlih, npr. M70 Ž85",
        blank=True,
        null=True,
    )
    remark = models.TextField("Opombe", blank=True, null=True)

    class Meta:
        verbose_name = "Poročilo bolnišnic"
        verbose_name_plural = "Poročila bolnišnic"
        ordering = ("-date_reporting", "hospital")

    def __str__(self):
        return str(self.date_form_saved)

