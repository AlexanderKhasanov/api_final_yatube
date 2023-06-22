from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название группы',
        help_text='Придумайте название группы',
    )
    slug = models.SlugField(
        max_length=20,
        unique=True,
        verbose_name='Адрес для страницы группы',
        help_text=(
            'Укажите уникальный адрес для страницы задачи. Используйте только '
            'латиницу, цифры, дефисы и знаки подчёркивания'
        ),
    )
    description = models.TextField(
        verbose_name='Описание группы',
        help_text='Введите описание группы'
    )

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='group',
        verbose_name='Группа',
        help_text='Укажите группу, к которой относится пост'
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост, к которому оставляется комментарий'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Пользователь, который подписывается',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Пользователь, на которого подписываются',
    )

    class Meta:
        verbose_name = 'follow'
        verbose_name_plural = 'follows'
