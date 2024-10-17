from django.db import models


class UserProfile(models.Model):
    user_name = models.CharField(max_length=100, )  # 用户名
    nickname = models.CharField(max_length=100, blank=True, null=True)  # 昵称
    open_id = models.CharField(max_length=50, unique=True)  # 学号
    avatar = models.URLField(blank=True)  # 头像 URL

    # 四种正脸照片
    enrollment_photo = models.URLField(blank=True,null=True)  # 入学照片 URL
    current_photo = models.URLField(blank=True,null=True)  # 在校照片 URL
    graduation_photo = models.URLField(blank=True,null=True)  # 毕业照片 URL
    id_card_photo = models.URLField(blank=True,null=True)  # 身份证照片 URL

    grade = models.CharField(max_length=10)  # 年级，如2023级
    org_name = models.CharField(max_length=100)  # 所属学院
    org_id = models.CharField(max_length=50)  # 学院 ID
    class_id = models.CharField(max_length=50)  # 班级 ID
    major_id = models.CharField(max_length=50)  # 专业 ID
    uid = models.CharField(max_length=50)  # 用户唯一标识
    dormitory = models.CharField(max_length=100, blank=True)  # 宿舍
    phone_number = models.CharField(max_length=20, blank=True)  # 手机号

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = "用户档案"
        verbose_name_plural = "用户档案"


class Organization(models.Model):
    org_name = models.CharField(max_length=50)  # 学院名
    org_id = models.CharField(max_length=50, unique=True)  # 学院ID

    def __str__(self):
        return self.org_name


class Major(models.Model):
    major_name = models.CharField(max_length=50)  # 专业名称
    major_id = models.CharField(max_length=50, unique=True)  # 专业ID
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)  # 外键关联到学院

    def __str__(self):
        return self.major_name
