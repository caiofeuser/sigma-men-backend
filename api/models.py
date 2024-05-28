from django.db import models
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes


@permission_classes([AllowAny])
class Survey(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    number_of_questions = models.IntegerField(default=0)

    def __str__(self):
        return self.name


@permission_classes([AllowAny])
class Question(models.Model):
    question = models.CharField(max_length=200)
    position = models.IntegerField(default=0)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    options = models.ManyToManyField('Option', related_name='options')

    def __str__(self):
        return self.question


@permission_classes([AllowAny])
class Partnerships(models.Model):
    display_button = models.BooleanField(default=False)

    # Override the save method to ensure only one instance exists
    def save(self, *args, **kwargs):
        self.pk = 1  # Set primary key to 1 to ensure only one instance
        super(Partnerships, self).save(*args, **kwargs)

    # Override the delete method to prevent deletion of the single instance
    def delete(self, *args, **kwargs):
        pass

    def __str__(self):
        return str(self.display_button)


@permission_classes([AllowAny])
class ContactInformation(models.Model):
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    instragram = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(ContactInformation, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    def __str__(self):
        return 'Contact Information'


@permission_classes([AllowAny])
class Track(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# class QuestionTrack(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     track = models.ForeignKey(Track, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.question.question + ' - ' + self.track.name

@permission_classes([AllowAny])
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.CharField(max_length=200)
    redirect_to_track = models.ForeignKey(
        Track, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.option + ' - ' + self.question.survey.name + ' - ' + self.question.question


@permission_classes([AllowAny])
class Result(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)

    def __str__(self):
        return self.survey.name + ' - ' + self.track.name


# @permission_classes([IsAuthenticated])
class Order(models.Model):
    user = models.ForeignKey('auth_api.CustomUserModel',
                             on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, default='Pending')
