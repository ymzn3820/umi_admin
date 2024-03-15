import hashlib
import os
from pathlib import PurePath, PureWindowsPath, PurePosixPath

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from application import dispatch
from dvadmin.utils.models import CoreModel, table_prefix

STATUS_CHOICES = (
    (0, "禁用"),
    (1, "启用"),
)


class Users(CoreModel, AbstractUser):
    username = models.CharField(max_length=150, unique=True, db_index=True, verbose_name="用户账号",
                                help_text="用户账号")
    employee_no = models.CharField(max_length=150, unique=True, db_index=True, null=True, blank=True,
                                   verbose_name="工号", help_text="工号")
    email = models.EmailField(max_length=255, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    mobile = models.CharField(max_length=255, verbose_name="电话", null=True, blank=True, help_text="电话")
    avatar = models.CharField(max_length=255, verbose_name="头像", null=True, blank=True, help_text="头像")
    name = models.CharField(max_length=40, verbose_name="姓名", help_text="姓名")
    GENDER_CHOICES = (
        (0, "未知"),
        (1, "男"),
        (2, "女"),
    )
    gender = models.IntegerField(
        choices=GENDER_CHOICES, default=0, verbose_name="性别", null=True, blank=True, help_text="性别"
    )
    USER_TYPE = (
        (0, "后台用户"),
        (1, "前台用户"),
    )
    user_type = models.IntegerField(
        choices=USER_TYPE, default=0, verbose_name="用户类型", null=True, blank=True, help_text="用户类型"
    )
    post = models.ManyToManyField(to="Post", blank=True, verbose_name="关联岗位", db_constraint=False,
                                  help_text="关联岗位")
    role = models.ManyToManyField(to="Role", blank=True, verbose_name="关联角色", db_constraint=False,
                                  help_text="关联角色")
    dept = models.ForeignKey(
        to="Dept",
        verbose_name="所属部门",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="关联部门",
    )
    last_token = models.CharField(max_length=255, null=True, blank=True, verbose_name="最后一次登录Token",
                                  help_text="最后一次登录Token")

    def set_password(self, raw_password):
        super().set_password(hashlib.md5(raw_password.encode(encoding="UTF-8")).hexdigest())

    class Meta:
        db_table = table_prefix + "system_users"
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class Post(CoreModel):
    name = models.CharField(null=False, max_length=64, verbose_name="岗位名称", help_text="岗位名称")
    code = models.CharField(max_length=32, verbose_name="岗位编码", help_text="岗位编码")
    sort = models.IntegerField(default=1, verbose_name="岗位顺序", help_text="岗位顺序")
    STATUS_CHOICES = (
        (0, "离职"),
        (1, "在职"),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="岗位状态", help_text="岗位状态")

    class Meta:
        db_table = table_prefix + "system_post"
        verbose_name = "岗位表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Role(CoreModel):
    name = models.CharField(max_length=64, verbose_name="角色名称", help_text="角色名称")
    key = models.CharField(max_length=64, unique=True, verbose_name="权限字符", help_text="权限字符")
    sort = models.IntegerField(default=1, verbose_name="角色顺序", help_text="角色顺序")
    status = models.BooleanField(default=True, verbose_name="角色状态", help_text="角色状态")
    admin = models.BooleanField(default=False, verbose_name="是否为admin", help_text="是否为admin")
    DATASCOPE_CHOICES = (
        (0, "仅本人数据权限"),
        (1, "本部门及以下数据权限"),
        (2, "本部门数据权限"),
        (3, "全部数据权限"),
        (4, "自定数据权限"),
    )
    data_range = models.IntegerField(default=0, choices=DATASCOPE_CHOICES, verbose_name="数据权限范围",
                                     help_text="数据权限范围")
    remark = models.TextField(verbose_name="备注", help_text="备注", null=True, blank=True)
    dept = models.ManyToManyField(to="Dept", verbose_name="数据权限-关联部门", db_constraint=False,
                                  help_text="数据权限-关联部门")
    menu = models.ManyToManyField(to="Menu", verbose_name="关联菜单", db_constraint=False, help_text="关联菜单")
    permission = models.ManyToManyField(
        to="MenuButton", verbose_name="关联菜单的接口按钮", db_constraint=False, help_text="关联菜单的接口按钮"
    )

    class Meta:
        db_table = table_prefix + "system_role"
        verbose_name = "角色表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Dept(CoreModel):
    name = models.CharField(max_length=64, verbose_name="部门名称", help_text="部门名称")
    key = models.CharField(max_length=64, unique=True, null=True, blank=True, verbose_name="关联字符",
                           help_text="关联字符")
    sort = models.IntegerField(default=1, verbose_name="显示排序", help_text="显示排序")
    owner = models.CharField(max_length=32, verbose_name="负责人", null=True, blank=True, help_text="负责人")
    phone = models.CharField(max_length=32, verbose_name="联系电话", null=True, blank=True, help_text="联系电话")
    email = models.EmailField(max_length=32, verbose_name="邮箱", null=True, blank=True, help_text="邮箱")
    status = models.BooleanField(default=True, verbose_name="部门状态", null=True, blank=True, help_text="部门状态")
    parent = models.ForeignKey(
        to="Dept",
        on_delete=models.CASCADE,
        default=None,
        verbose_name="上级部门",
        db_constraint=False,
        null=True,
        blank=True,
        help_text="上级部门",
    )

    @classmethod
    def recursion_dept_info(cls, dept_id: int, dept_all_list=None, dept_list=None):
        """
        递归获取部门的所有下级部门
        :param dept_id: 需要获取的id
        :param dept_all_list: 所有列表
        :param dept_list: 递归list
        :return:
        """
        if not dept_all_list:
            dept_all_list = Dept.objects.values("id", "parent")
        if dept_list is None:
            dept_list = [dept_id]
        for ele in dept_all_list:
            if ele.get("parent") == dept_id:
                dept_list.append(ele.get("id"))
                cls.recursion_dept_info(ele.get("id"), dept_all_list, dept_list)
        return list(set(dept_list))

    class Meta:
        db_table = table_prefix + "system_dept"
        verbose_name = "部门表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class Menu(CoreModel):
    parent = models.ForeignKey(
        to="Menu",
        on_delete=models.PROTECT,
        verbose_name="上级菜单",
        null=True,
        blank=True,
        db_constraint=False,
        help_text="上级菜单",
    )
    icon = models.CharField(max_length=64, verbose_name="菜单图标", null=True, blank=True, help_text="菜单图标")
    name = models.CharField(max_length=64, verbose_name="菜单名称", help_text="菜单名称")
    sort = models.IntegerField(default=1, verbose_name="显示排序", null=True, blank=True, help_text="显示排序")
    ISLINK_CHOICES = (
        (0, "否"),
        (1, "是"),
    )
    is_link = models.BooleanField(default=False, verbose_name="是否外链", help_text="是否外链")
    is_catalog = models.BooleanField(default=False, verbose_name="是否目录", help_text="是否目录")
    web_path = models.CharField(max_length=128, verbose_name="路由地址", null=True, blank=True, help_text="路由地址")
    component = models.CharField(max_length=128, verbose_name="组件地址", null=True, blank=True, help_text="组件地址")
    component_name = models.CharField(max_length=50, verbose_name="组件名称", null=True, blank=True,
                                      help_text="组件名称")
    status = models.BooleanField(default=True, blank=True, verbose_name="菜单状态", help_text="菜单状态")
    cache = models.BooleanField(default=False, blank=True, verbose_name="是否页面缓存", help_text="是否页面缓存")
    visible = models.BooleanField(default=True, blank=True, verbose_name="侧边栏中是否显示",
                                  help_text="侧边栏中是否显示")

    class Meta:
        db_table = table_prefix + "system_menu"
        verbose_name = "菜单表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)


class MenuButton(CoreModel):
    menu = models.ForeignKey(
        to="Menu",
        db_constraint=False,
        related_name="menuPermission",
        on_delete=models.PROTECT,
        verbose_name="关联菜单",
        help_text="关联菜单",
    )
    name = models.CharField(max_length=64, verbose_name="名称", help_text="名称")
    value = models.CharField(max_length=64, verbose_name="权限值", help_text="权限值")
    api = models.CharField(max_length=200, verbose_name="接口地址", help_text="接口地址")
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
    )
    method = models.IntegerField(default=0, verbose_name="接口请求方法", null=True, blank=True,
                                 help_text="接口请求方法")

    class Meta:
        db_table = table_prefix + "system_menu_button"
        verbose_name = "菜单权限表"
        verbose_name_plural = verbose_name
        ordering = ("-name",)


class Dictionary(CoreModel):
    TYPE_LIST = (
        (0, "text"),
        (1, "number"),
        (2, "date"),
        (3, "datetime"),
        (4, "time"),
        (5, "files"),
        (6, "boolean"),
        (7, "images"),
    )
    label = models.CharField(max_length=100, blank=True, null=True, verbose_name="字典名称", help_text="字典名称")
    value = models.CharField(max_length=200, blank=True, null=True, verbose_name="字典编号",
                             help_text="字典编号/实际值")
    parent = models.ForeignKey(
        to="self",
        related_name="sublist",
        db_constraint=False,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name="父级",
        help_text="父级",
    )
    type = models.IntegerField(choices=TYPE_LIST, default=0, verbose_name="数据值类型", help_text="数据值类型")
    color = models.CharField(max_length=20, blank=True, null=True, verbose_name="颜色", help_text="颜色")
    is_value = models.BooleanField(default=False, verbose_name="是否为value值",
                                   help_text="是否为value值,用来做具体值存放")
    status = models.BooleanField(default=True, verbose_name="状态", help_text="状态")
    sort = models.IntegerField(default=1, verbose_name="显示排序", null=True, blank=True, help_text="显示排序")
    remark = models.CharField(max_length=2000, blank=True, null=True, verbose_name="备注", help_text="备注")

    class Meta:
        db_table = table_prefix + "system_dictionary"
        verbose_name = "字典表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        dispatch.refresh_dictionary()  # 有更新则刷新字典配置

    def delete(self, using=None, keep_parents=False):
        res = super().delete(using, keep_parents)
        dispatch.refresh_dictionary()
        return res


class OperationLog(CoreModel):
    request_modular = models.CharField(max_length=64, verbose_name="请求模块", null=True, blank=True,
                                       help_text="请求模块")
    request_path = models.CharField(max_length=400, verbose_name="请求地址", null=True, blank=True,
                                    help_text="请求地址")
    request_body = models.TextField(verbose_name="请求参数", null=True, blank=True, help_text="请求参数")
    request_method = models.CharField(max_length=8, verbose_name="请求方式", null=True, blank=True,
                                      help_text="请求方式")
    request_msg = models.TextField(verbose_name="操作说明", null=True, blank=True, help_text="操作说明")
    request_ip = models.CharField(max_length=32, verbose_name="请求ip地址", null=True, blank=True,
                                  help_text="请求ip地址")
    request_browser = models.CharField(max_length=64, verbose_name="请求浏览器", null=True, blank=True,
                                       help_text="请求浏览器")
    response_code = models.CharField(max_length=32, verbose_name="响应状态码", null=True, blank=True,
                                     help_text="响应状态码")
    request_os = models.CharField(max_length=64, verbose_name="操作系统", null=True, blank=True, help_text="操作系统")
    json_result = models.TextField(verbose_name="返回信息", null=True, blank=True, help_text="返回信息")
    status = models.BooleanField(default=False, verbose_name="响应状态", help_text="响应状态")

    class Meta:
        db_table = table_prefix + "system_operation_log"
        verbose_name = "操作日志"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


def media_file_name(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return PurePosixPath("files", h[:1], h[1:2], h + ext.lower())


class FileList(CoreModel):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="名称", help_text="名称")
    url = models.FileField(upload_to=media_file_name, null=True, blank=True, )
    file_url = models.CharField(max_length=255, blank=True, verbose_name="文件地址", help_text="文件地址")
    engine = models.CharField(max_length=100, default='local', blank=True, verbose_name="引擎", help_text="引擎")
    mime_type = models.CharField(max_length=100, blank=True, verbose_name="Mime类型", help_text="Mime类型")
    size = models.CharField(max_length=36, blank=True, verbose_name="文件大小", help_text="文件大小")
    md5sum = models.CharField(max_length=36, blank=True, verbose_name="文件md5", help_text="文件md5")

    def save(self, *args, **kwargs):
        if not self.md5sum:  # file is new
            md5 = hashlib.md5()
            for chunk in self.url.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        if not self.size:
            self.size = self.url.size
        if not self.file_url:
            url = media_file_name(self, self.name)
            self.file_url = f'media/{url}'
        super(FileList, self).save(*args, **kwargs)

    class Meta:
        db_table = table_prefix + "system_file_list"
        verbose_name = "文件管理"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class Area(CoreModel):
    name = models.CharField(max_length=100, verbose_name="名称", help_text="名称")
    code = models.CharField(max_length=20, verbose_name="地区编码", help_text="地区编码", unique=True, db_index=True)
    level = models.BigIntegerField(verbose_name="地区层级(1省份 2城市 3区县 4乡级)",
                                   help_text="地区层级(1省份 2城市 3区县 4乡级)")
    pinyin = models.CharField(max_length=255, verbose_name="拼音", help_text="拼音")
    initials = models.CharField(max_length=20, verbose_name="首字母", help_text="首字母")
    enable = models.BooleanField(default=True, verbose_name="是否启用", help_text="是否启用")
    pcode = models.ForeignKey(
        to="self",
        verbose_name="父地区编码",
        to_field="code",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="父地区编码",
    )

    class Meta:
        db_table = table_prefix + "system_area"
        verbose_name = "地区表"
        verbose_name_plural = verbose_name
        ordering = ("code",)

    def __str__(self):
        return f"{self.name}"


class ApiWhiteList(CoreModel):
    url = models.CharField(max_length=200, help_text="url地址", verbose_name="url")
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
    )
    method = models.IntegerField(default=0, verbose_name="接口请求方法", null=True, blank=True,
                                 help_text="接口请求方法")
    enable_datasource = models.BooleanField(default=True, verbose_name="激活数据权限", help_text="激活数据权限",
                                            blank=True)

    class Meta:
        db_table = table_prefix + "api_white_list"
        verbose_name = "接口白名单"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class SystemConfig(CoreModel):
    parent = models.ForeignKey(
        to="self",
        verbose_name="父级",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="父级",
    )
    title = models.CharField(max_length=50, verbose_name="标题", help_text="标题")
    key = models.CharField(max_length=200, verbose_name="键", help_text="键", db_index=True)
    value = models.JSONField(max_length=500, verbose_name="值", help_text="值", null=True, blank=True)
    sort = models.IntegerField(default=0, verbose_name="排序", help_text="排序", blank=True)
    status = models.BooleanField(default=True, verbose_name="启用状态", help_text="启用状态")
    data_options = models.JSONField(verbose_name="数据options", help_text="数据options", null=True, blank=True)
    FORM_ITEM_TYPE_LIST = (
        (0, "text"),
        (1, "datetime"),
        (2, "date"),
        (3, "textarea"),
        (4, "select"),
        (5, "checkbox"),
        (6, "radio"),
        (7, "img"),
        (8, "file"),
        (9, "switch"),
        (10, "number"),
        (11, "array"),
        (12, "imgs"),
        (13, "foreignkey"),
        (14, "manytomany"),
        (15, "time"),
    )
    form_item_type = models.IntegerField(
        choices=FORM_ITEM_TYPE_LIST, verbose_name="表单类型", help_text="表单类型", default=0, blank=True
    )
    rule = models.JSONField(null=True, blank=True, verbose_name="校验规则", help_text="校验规则")
    placeholder = models.CharField(max_length=100, null=True, blank=True, verbose_name="提示信息", help_text="提示信息")
    setting = models.JSONField(null=True, blank=True, verbose_name="配置", help_text="配置")

    class Meta:
        db_table = table_prefix + "system_config"
        verbose_name = "系统配置表"
        verbose_name_plural = verbose_name
        ordering = ("sort",)
        unique_together = (("key", "parent_id"),)

    def __str__(self):
        return f"{self.title}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # from application.websocketConfig import websocket_push
        # websocket_push("dvadmin", message={"sender": 'system', "contentType": 'SYSTEM',
        #                                    "content": '系统配置有变化~', "systemConfig": True})

        super().save(force_insert, force_update, using, update_fields)
        dispatch.refresh_system_config()  # 有更新则刷新系统配置

    def delete(self, using=None, keep_parents=False):
        res = super().delete(using, keep_parents)
        dispatch.refresh_system_config()
        from application.websocketConfig import websocket_push
        websocket_push("dvadmin", message={"sender": 'system', "contentType": 'SYSTEM',
                                           "content": '系统配置有变化~', "systemConfig": True})

        return res


class LoginLog(CoreModel):
    LOGIN_TYPE_CHOICES = (
        (1, "普通登录"),
        (2, "普通扫码登录"),
        (3, "微信扫码登录"),
        (4, "飞书扫码登录"),
        (5, "钉钉扫码登录"),
        (6, "短信登录")
    )
    username = models.CharField(max_length=150, verbose_name="登录用户名", null=True, blank=True,
                                help_text="登录用户名")
    ip = models.CharField(max_length=32, verbose_name="登录ip", null=True, blank=True, help_text="登录ip")
    agent = models.TextField(verbose_name="agent信息", null=True, blank=True, help_text="agent信息")
    browser = models.CharField(max_length=200, verbose_name="浏览器名", null=True, blank=True, help_text="浏览器名")
    os = models.CharField(max_length=200, verbose_name="操作系统", null=True, blank=True, help_text="操作系统")
    continent = models.CharField(max_length=50, verbose_name="州", null=True, blank=True, help_text="州")
    country = models.CharField(max_length=50, verbose_name="国家", null=True, blank=True, help_text="国家")
    province = models.CharField(max_length=50, verbose_name="省份", null=True, blank=True, help_text="省份")
    city = models.CharField(max_length=50, verbose_name="城市", null=True, blank=True, help_text="城市")
    district = models.CharField(max_length=50, verbose_name="县区", null=True, blank=True, help_text="县区")
    isp = models.CharField(max_length=50, verbose_name="运营商", null=True, blank=True, help_text="运营商")
    area_code = models.CharField(max_length=50, verbose_name="区域代码", null=True, blank=True, help_text="区域代码")
    country_english = models.CharField(max_length=50, verbose_name="英文全称", null=True, blank=True,
                                       help_text="英文全称")
    country_code = models.CharField(max_length=50, verbose_name="简称", null=True, blank=True, help_text="简称")
    longitude = models.CharField(max_length=50, verbose_name="经度", null=True, blank=True, help_text="经度")
    latitude = models.CharField(max_length=50, verbose_name="纬度", null=True, blank=True, help_text="纬度")
    login_type = models.IntegerField(default=1, choices=LOGIN_TYPE_CHOICES, verbose_name="登录类型",
                                     help_text="登录类型")

    class Meta:
        db_table = table_prefix + "system_login_log"
        verbose_name = "登录日志"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class MessageCenter(CoreModel):
    title = models.CharField(max_length=100, verbose_name="标题", help_text="标题")
    content = models.TextField(verbose_name="内容", help_text="内容")
    target_type = models.IntegerField(default=0, verbose_name="目标类型", help_text="目标类型")
    target_user = models.ManyToManyField(to=Users, related_name='user', through='MessageCenterTargetUser',
                                         through_fields=('messagecenter', 'users'), blank=True, verbose_name="目标用户",
                                         help_text="目标用户")
    target_dept = models.ManyToManyField(to=Dept, blank=True, db_constraint=False,
                                         verbose_name="目标部门", help_text="目标部门")
    target_role = models.ManyToManyField(to=Role, blank=True, db_constraint=False,
                                         verbose_name="目标角色", help_text="目标角色")

    class Meta:
        db_table = table_prefix + "message_center"
        verbose_name = "消息中心"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)


class MessageCenterTargetUser(CoreModel):
    users = models.ForeignKey(Users, related_name="target_user", on_delete=models.CASCADE, db_constraint=False,
                              verbose_name="关联用户表", help_text="关联用户表")
    messagecenter = models.ForeignKey(MessageCenter, on_delete=models.CASCADE, db_constraint=False,
                                      verbose_name="关联消息中心表", help_text="关联消息中心表")
    is_read = models.BooleanField(default=False, blank=True, null=True, verbose_name="是否已读", help_text="是否已读")

    class Meta:
        db_table = table_prefix + "message_center_target_user"
        verbose_name = "消息中心目标用户表"
        verbose_name_plural = verbose_name


class UUUsers(models.Model):
    user_code = models.CharField(max_length=64, default='', db_column='user_code', verbose_name='用户编号')
    mobile = models.CharField(max_length=64, default='', db_column='mobile', verbose_name='手机号')
    user_name = models.CharField(max_length=64, default='', db_column='user_name', verbose_name='用户名')
    nick_name = models.CharField(max_length=64, default='', db_column='nick_name', verbose_name='昵称')
    password = models.CharField(max_length=64, default='', db_column='password', verbose_name='密码')
    source = models.CharField(max_length=64, default='', db_column='source', verbose_name='来源')
    avatar_url = models.CharField(max_length=256, default='', db_column='avatar_url', verbose_name='头像地址')
    wx_union_id = models.CharField(max_length=64, default='', db_column='wx_union_id', verbose_name='微信wx_union_id')
    salt = models.CharField(max_length=10, default='', db_column='salt', verbose_name='加密字符')
    avatar_id = models.IntegerField(max_length=10, default=-1, db_column='avatar_id', verbose_name='avatar_id')
    user_status = models.BooleanField(default=True, db_column='user_status',
                                      verbose_name='用户状态')  # 使用BooleanField表示tinyint(1)
    create_by = models.CharField(max_length=64, default='', db_column='create_by', verbose_name='创建人')
    create_time = models.DateTimeField(null=True, db_column='create_time', verbose_name='创建日期')
    modify_time = models.DateTimeField(null=True, db_column='modify_time', verbose_name='最近修改日期')
    is_delete = models.BooleanField(default=False, db_column='is_delete',
                                    verbose_name='是否删除')  # 使用BooleanField表示tinyint(1)
    login_time = models.DateTimeField(null=True, db_column='login_time', verbose_name='最近登录日期')
    login_ip = models.CharField(null=True, db_column='login_ip', verbose_name='最近登录IP')
    source_url = models.CharField(null=True, db_column='source_url', verbose_name='注册来源')

    def to_dict(self):
        return {
            'user_code': self.user_code,
            'mobile': self.mobile,
            'user_name': self.user_name,
            'nick_name': self.nick_name,
            'password': self.password,
            'source': self.source,
            'avatar_url': self.avatar_url,
            'wx_union_id': self.wx_union_id,
            'salt': self.salt,
            'user_status': self.user_status,
            'create_by': self.create_by,
            'create_time': self.create_time,
            'modify_time': self.modify_time,
            'is_delete': self.is_delete,
            'login_time': self.login_time,
            'avatar_id': self.avatar_id,
            'login_ip': self.login_ip,
            'source_url': self.source_url,
        }

    class Meta:
        db_table = 'uu_users'
        verbose_name = '用户表'
        app_label = 'server'
        verbose_name_plural = verbose_name
        ordering = ("-create_time",)
        indexes = [
            models.Index(fields=['user_code'], name='uu_users_user_code_sjkqhwcvj_idx'),
            models.Index(fields=['mobile'], name='uu_users_mobile_sjkqhwcvj_idx'),
            models.Index(fields=['user_name'], name='uu_users_user_name_sjkqhwcvj_idx'),
            models.Index(fields=['create_time'], name='uu_users_create_time_sjkqhwcvj_idx'),
            models.Index(fields=['wx_union_id'], name='uu_users_wx_union_id_sjkqhwcvj_idx'),
        ]

    def __str__(self):
        fields = self._meta.fields
        field_values = [str(getattr(self, field.name)) for field in fields]
        return ', '.join(field_values)


class UUUsersTemp(models.Model):
    user_code = models.CharField(max_length=64, default='', db_column='user_code', verbose_name='用户编号')
    mobile = models.CharField(max_length=64, default='', db_column='mobile', verbose_name='手机号')
    user_name = models.CharField(max_length=64, default='', db_column='user_name', verbose_name='用户名')
    nick_name = models.CharField(max_length=64, default='', db_column='nick_name', verbose_name='昵称')
    password = models.CharField(max_length=64, default='', db_column='password', verbose_name='密码')
    source = models.CharField(max_length=64, default='', db_column='source', verbose_name='来源')
    avatar_url = models.CharField(max_length=256, default='', db_column='avatar_url', verbose_name='头像地址')
    wx_union_id = models.CharField(max_length=64, default='', db_column='wx_union_id', verbose_name='微信wx_union_id')
    salt = models.CharField(max_length=10, default='', db_column='salt', verbose_name='加密字符')
    avatar_id = models.IntegerField(max_length=10, default=-1, db_column='avatar_id', verbose_name='头像id')
    user_status = models.BooleanField(default=True, db_column='user_status',
                                      verbose_name='用户状态')  # 使用BooleanField表示tinyint(1)
    create_by = models.CharField(max_length=64, default='', db_column='create_by', verbose_name='创建人')
    create_time = models.DateTimeField(null=True, db_column='create_time', verbose_name='创建日期')
    modify_time = models.DateTimeField(null=True, db_column='modify_time', verbose_name='最近修改日期')
    is_delete = models.BooleanField(default=False, db_column='is_delete',
                                    verbose_name='是否删除')  # 使用BooleanField表示tinyint(1)
    login_time = models.DateTimeField(null=True, db_column='login_time', verbose_name='最近登录日期')

    def to_dict(self):
        return {
            'user_code': self.user_code,
            'mobile': self.mobile,
            'user_name': self.user_name,
            'nick_name': self.nick_name,
            'password': self.password,
            'source': self.source,
            'avatar_url': self.avatar_url,
            'wx_union_id': self.wx_union_id,
            'salt': self.salt,
            'user_status': self.user_status,
            'create_by': self.create_by,
            'create_time': self.create_time,
            'modify_time': self.modify_time,
            'is_delete': self.is_delete,
            'login_time': self.login_time,
            'avatar_id': self.avatar_id,
        }

    class Meta:
        db_table = 'uu_users_temp'
        verbose_name = '临时用户表'
        app_label = 'server'
        verbose_name_plural = verbose_name
        ordering = ("-create_time",)


class ActivateCode(models.Model):
    generated_by = models.CharField(max_length=255, default='', verbose_name='生成者id')
    consumed_by = models.CharField(max_length=255, default='', verbose_name='消费者id')
    activate_code = models.CharField(max_length=255, default='', verbose_name='激活码')
    activate_code_id = models.CharField(max_length=255, default='', verbose_name='激活码id')
    to_prod_id = models.IntegerField(default=0, verbose_name='对应产品id')
    status = models.SmallIntegerField(default=0, verbose_name='激活状态')
    desc = models.CharField(default=0, verbose_name='描述')
    code_type = models.SmallIntegerField(default=1, verbose_name='激活码类型')
    expired_date = models.DateTimeField(null=True, verbose_name='过期时间')
    is_delete = models.SmallIntegerField(default=0, verbose_name='删除状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'oa_activate_code'
        verbose_name = '激活码管理'
        app_label = 'admin'
        verbose_name_plural = verbose_name
        ordering = ("-created_at",)


class Products(models.Model):
    PROD_PLATFORM_CHOICES = [
        (1, 'PC'),
        (2, 'H5'),
        (3, '小程序'),
        (4, '全平台'),
    ]

    prod_id = models.IntegerField(unique=True, verbose_name='商品id')
    prod_name = models.CharField(max_length=255, verbose_name='商品名称')
    platform = models.IntegerField(choices=PROD_PLATFORM_CHOICES, verbose_name='platform')
    prod_description = models.TextField(null=True, blank=True, verbose_name='商品描述')
    prod_details = models.TextField(null=True, blank=True, verbose_name='商品详情')
    prod_origin_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='商品原价')
    continuous_annual_sub_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                                      verbose_name='连续订阅价格')
    prod_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='商品价格')
    valid_period_days = models.IntegerField(default=0, verbose_name='会员类产品有效期')
    prod_cate_id = models.IntegerField(verbose_name='商品类别ID')
    is_show = models.BooleanField(default=False, verbose_name='是否展示')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'pp_products'
        verbose_name = '商品表'
        app_label = 'server'
        verbose_name_plural = verbose_name
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=['prod_cate_id'], name='idx_products_category_id'),
        ]


class OpPictures(models.Model):
    TYPE_CHOICES = [
        (0, '其他'),
        (1, '公众号'),
        (2, '客服'),
        (3, '小程序'),
    ]

    pic_id = models.CharField(max_length=255, default='', verbose_name='图片id')
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=0)
    pic_size = models.FloatField(default=0, verbose_name='图片大小')
    pic_format = models.CharField(max_length=255, default='', verbose_name='图片格式')
    pic_url = models.CharField(max_length=255, verbose_name='图片地址')
    pic_desc = models.CharField(max_length=255, default=None, blank=True, null=True, verbose_name='图片描述')
    uploader_id = models.CharField(max_length=255, default='', verbose_name='上传者id')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'op_pictures'
        verbose_name = '图片表'
        app_label = 'server'
        verbose_name_plural = verbose_name
        ordering = ("-create_time",)


class OpenaiKey(models.Model):
    STATUS_CHOICES = [
        (1, '正常'),
        (2, '余额不足'),
    ]

    KEY_TYPE_CHOICES = [
        (0, '3.5'),
        (1, '4.0'),
    ]

    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=256, default='', verbose_name='key')
    server_ip = models.CharField(max_length=64, default='', verbose_name='key绑定的ip')
    o_status = models.IntegerField(default=1, choices=STATUS_CHOICES, verbose_name='状态')
    key_type = models.IntegerField(default=0, choices=KEY_TYPE_CHOICES, verbose_name='状态')
    desc = models.CharField(max_length=64, default='', verbose_name='描述')

    class Meta:
        db_table = 'oo_openai_key'
        verbose_name = 'openai key管理表'
        app_label = 'server'
        verbose_name_plural = verbose_name
        ordering = ("-id",)


class ObBusinessCooperation(models.Model):
    TYPE_CHOICES = (
        (0, 'Unknown'),
        (1, '城市运营商'),
        (2, '源码定制'),
        (3, 'api接口'),
    )

    STATUS_CHOICES = (
        (0, '待处理'),
        (1, '正在处理'),
        (2, '处理完成'),
        (3, '失效'),
    )

    DELETE_CHOICES = (
        (0, '正常'),
        (1, '删除'),
    )
    id = models.AutoField(primary_key=True, verbose_name='主键，自增')
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=0, verbose_name='类型')
    name = models.CharField(max_length=255, default='', verbose_name='姓名')
    user_id = models.CharField(max_length=255, default='', verbose_name='用户id')
    position = models.CharField(max_length=255, default='', verbose_name='职位')
    phone = models.CharField(max_length=20, default='', verbose_name='电话')
    referer = models.CharField(max_length=100, default='', verbose_name='来源')
    cooperation_details = models.TextField(verbose_name='合作明细')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    email = models.EmailField(max_length=255, default='', verbose_name='电子邮件字段')
    company = models.CharField(max_length=255, default='', verbose_name='公司名称字段')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0, verbose_name='状态字段')
    is_delete = models.PositiveSmallIntegerField(choices=DELETE_CHOICES, default=0, verbose_name='是否删除')

    class Meta:
        verbose_name = "商务合作"
        verbose_name_plural = "商务合作"
        db_table = 'ob_business_cooperation'
        ordering = ['-created_at']
        app_label = 'server'


class PpPayments(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='支付ID')
    order_id = models.CharField(max_length=255, default='0', verbose_name='订单id')
    user_id = models.CharField(max_length=255, default='0', verbose_name='用户ID')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default='0.00', verbose_name='支付金额')
    status = models.SmallIntegerField(default='0', verbose_name='支付状态: 3-失败, 1-成功, 2-退款,0-待付款, 4-失效')
    payment_method = models.SmallIntegerField(default='0', verbose_name='支付方式: 1-支付宝, 2-微信支付 3卡密兑换')
    pre_pay_id = models.CharField(max_length=191, default='', verbose_name='预支付id')
    pay_data = models.CharField(max_length=1000, default='', verbose_name='发起支付的url或者数据\n微信小程序为数据, 其余为url')
    pay_id = models.CharField(max_length=191, null=True, unique=True, verbose_name='支付id， 微信或者支付宝返回')
    is_delete = models.SmallIntegerField(default='0', verbose_name='是否删除: 0-未删除, 1-已删除')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "支付管理"
        verbose_name_plural = verbose_name
        db_table = 'pp_payments'
        ordering = ['-created_at']
        app_label = 'server'


class POOrder(models.Model):
    ORDER_STATUS_CHOICES = (
        (0, '默认状态'),
        (1, '待付款'),
        (2, '已付款'),
        (3, '已取消'),
        (4, '已过期'),
    )

    DELETE_CHOICES = (
        (0, '未删除'),
        (1, '已删除'),
    )

    id = models.AutoField(primary_key=True, verbose_name='订单ID')
    order_id = models.CharField(max_length=255, unique=True, default='0', verbose_name='订单id')
    user_id = models.CharField(max_length=255, default='0', verbose_name='用户ID')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总金额')
    status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=0, verbose_name='订单状态')
    is_delete = models.IntegerField(choices=DELETE_CHOICES, default=0, verbose_name='是否删除')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "订单管理"
        verbose_name_plural = verbose_name
        db_table = 'po_orders'
        ordering = ['-created_at']
        app_label = 'server'
        indexes = [
            models.Index(fields=['user_id'], name='idx_orders_user_id'),
        ]


class POOrderItem(models.Model):
    DELETE_CHOICES = (
        (0, '未删除'),
        (1, '已删除'),
    )

    id = models.AutoField(primary_key=True, verbose_name='订单商品关联ID')
    order_id = models.CharField(max_length=255, default='0', verbose_name='订单id')
    prod_id = models.IntegerField(default=0, verbose_name='商品ID')
    quantity = models.IntegerField(default=0, verbose_name='购买数量')
    price = models.DecimalField(max_digits=10, decimal_places=2, default='0.00', verbose_name='购买时的单价')
    is_delete = models.IntegerField(choices=DELETE_CHOICES, default=0, verbose_name='是否删除')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "订单商品关联"
        verbose_name_plural = verbose_name
        db_table = 'po_orders_items'
        ordering = ['-created_at']
        app_label = 'server'
        indexes = [
            models.Index(fields=['order_id'], name='idx_order_items_order_id'),
            models.Index(fields=['prod_id'], name='idx_order_items_product_id'),
        ]


class OpTab(models.Model):
    id = models.AutoField(primary_key=True)
    weight = models.IntegerField(default=0)
    tab_id = models.CharField(max_length=255, unique=True, default='')
    name = models.CharField(max_length=255, default='')
    icon = models.CharField(max_length=255, default='')
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_hidden = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = "tab栏表"
        verbose_name_plural = verbose_name
        db_table = 'op_tab'
        ordering = ['-created_at']
        app_label = 'admin'
        indexes = [
            models.Index(fields=['tab_id']),
        ]


class OpIndustry(models.Model):
    id = models.AutoField(primary_key=True)
    industry_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    naics_code = models.CharField(max_length=10, default='')
    sic_code = models.CharField(max_length=10, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = "行业表"
        verbose_name_plural = verbose_name
        db_table = 'op_industry'
        ordering = ['-created_at']
        app_label = 'admin'
        indexes = [
            models.Index(fields=['industry_id'], name='idx_industry')
        ]


class OpOccupation(models.Model):
    id = models.AutoField(primary_key=True)
    occu_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    industry_id = models.CharField(max_length=255, default='0')
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "职业表"
        verbose_name_plural = verbose_name
        db_table = 'op_occupation'
        ordering = ['-created_at']
        app_label = 'admin'
        indexes = [
            models.Index(fields=['occu_id'], name='idx_occu_id')
        ]


class OpSubOccu(models.Model):
    id = models.AutoField(primary_key=True)
    industry_id = models.CharField(max_length=255, default='')
    sub_occu_id = models.CharField(max_length=255)
    occu_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "次级职业"
        verbose_name_plural = verbose_name
        db_table = 'op_sub_occu'
        ordering = ['-created_at']
        app_label = 'admin'
        indexes = [
            models.Index(fields=['sub_occu_id'], name='idx_sub_occu_id')
        ]


class OpEmpDuration(models.Model):
    id = models.AutoField(primary_key=True)
    industry_id = models.CharField(max_length=255, default='')
    occu_id = models.CharField(max_length=255, default='')
    sub_occu_id = models.CharField(max_length=255, default='')
    emp_duration_id = models.CharField(max_length=255)
    emp_duration_name = models.CharField(max_length=255)
    emp_duration_desc = models.TextField(blank=True, null=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "从业时间"
        verbose_name_plural = verbose_name
        db_table = 'op_emp_duration'
        ordering = ['-created_at']
        app_label = 'admin'
        indexes = [
            models.Index(fields=['emp_duration_id'], name='emp_duration_id')
        ]


class OpExpertiseLevel(models.Model):
    id = models.AutoField(primary_key=True)
    industry_id = models.CharField(max_length=255, default='')
    occu_id = models.CharField(max_length=255, null=True, blank=True)
    sub_occu_id = models.CharField(max_length=255, null=True, blank=True)
    emp_duration_id = models.CharField(max_length=255, default='')
    expertise_level_id = models.IntegerField()
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "职业技能"
        verbose_name_plural = verbose_name
        db_table = 'op_expertise_level'
        ordering = ['-created_at']
        app_label = 'admin'
        indexes = [
            models.Index(fields=['expertise_level_id'], name='expertise_level_id')
        ]


class OpModules(models.Model):
    id = models.AutoField(primary_key=True)
    module_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=255, default='')
    interest_group = models.CharField(max_length=255, default='')
    interest_group_desc = models.CharField(max_length=255, default='')
    contact_qr_code = models.CharField(max_length=255, default='')
    contact_qr_code_desc = models.CharField(max_length=255, default='')
    industry_id = models.CharField(max_length=255, default='')
    occu_id = models.CharField(max_length=255, default='')
    sub_occu_id = models.CharField(max_length=255, default='')
    emp_duration_id = models.CharField(max_length=255, default='')
    expertise_level_id = models.CharField(max_length=255)
    is_delete = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "模块"
        verbose_name_plural = verbose_name
        db_table = 'op_modules'
        ordering = ['-created_at']
        app_label = 'admin'
        indexes = [
            models.Index(fields=['module_id'], name='module_id')
        ]


class OpQuestionsSet(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键ID')
    weight = models.IntegerField(verbose_name='权重', default=0)
    question_id = models.CharField(max_length=255, default='', verbose_name='问题ID')
    module_id = models.CharField(max_length=255, default='', verbose_name='所属模块ID')
    industry_id = models.CharField(max_length=255, default='0', verbose_name='所属行业ID')
    occupation_id = models.CharField(max_length=255, default='0', verbose_name='所属职业ID')
    sub_occu_id = models.CharField(max_length=255, default='0', verbose_name='所属二级职业ID')
    emp_duration_id = models.CharField(max_length=255, verbose_name='从业时间ID')
    expertise_level_id = models.CharField(max_length=255, default='', verbose_name='专业水平ID')
    title = models.CharField(max_length=255, default='', verbose_name='标题')
    content = models.TextField(blank=True, null=True, verbose_name='问题描述')
    example_question = models.TextField(blank=True, null=True, verbose_name='示例提问')
    content_hidden = models.TextField(blank=True, null=True, verbose_name='隐藏内容')
    is_hidden = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False, verbose_name='是否删除，0表示未删除，1表示已删除')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "问题集"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        app_label = 'admin'
        db_table = 'op_questions_set'
        indexes = [
            models.Index(fields=['question_id'], name='question_id_index'),
            models.Index(fields=['module_id'], name='module_id_index')
        ]


class OpQuestionsEdit(models.Model):
    id = models.AutoField(primary_key=True)
    question_id = models.CharField(max_length=255)
    field_id = models.CharField(max_length=255)
    field_name = models.CharField(max_length=255)
    content = models.CharField(max_length=255, default='')
    show_order = models.IntegerField(default=0)
    is_hidden = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "问题集编辑"
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        app_label = 'admin'
        db_table = 'op_questions_edit'
        indexes = [
            models.Index(fields=['question_id'], name='question_id')
        ]


class UpProblem(models.Model):
    QUESTION_TYPE = (
        (1, "使用问题"),
        (2, "产品错误"),
        (3, "产品建议"),
        (4, "不良内容"),
        (5, "购买问题"),
        (6, "其他问题"),
    )
    id = models.AutoField(primary_key=True)
    problem = models.CharField(max_length=512, default='', verbose_name='问题描述')
    question_type = models.IntegerField(default=0, verbose_name='问题类型', choices=QUESTION_TYPE)
    contact = models.CharField(max_length=256, default='', verbose_name='联系方式')
    create_by = models.CharField(max_length=64, default='', verbose_name='创建人')
    create_time = models.DateTimeField(null=True, verbose_name='创建日期')
    modify_time = models.DateTimeField(null=True, verbose_name='最近修改日期')
    status = models.BooleanField(default=False, verbose_name='是否删除1：处理完成，0：待处理')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除1：是，0：未删除')

    class Meta:
        db_table = 'up_problem'
        verbose_name = '问题反馈表'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
        app_label = 'server'


class UpProblemPicture(models.Model):
    id = models.AutoField(primary_key=True)
    problem = models.ForeignKey('UpProblem', on_delete=models.CASCADE, related_name='pictures', verbose_name='问题反馈表id')
    picture_url = models.CharField(max_length=256, default='', verbose_name='图片路由')
    picture_id = models.IntegerField(default=-1, verbose_name='图片路由')
    create_by = models.CharField(max_length=64, default='', verbose_name='创建人')
    create_time = models.DateTimeField(null=True, verbose_name='创建日期')
    modify_time = models.DateTimeField(null=True, verbose_name='最近修改日期')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除1：是，0：未删除')

    class Meta:
        db_table = 'up_problem_picture'
        verbose_name = '问题反馈图片表'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']
        app_label = 'server'


class UsersWithdrawalHistory(models.Model):
    user_code = models.CharField(max_length=64, default='', verbose_name='用户编号')
    card_code = models.CharField(max_length=64, default='', verbose_name='id号')
    order_no = models.CharField(max_length=64, default='', verbose_name='提现单号')
    withdrawal_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='提现金额')
    account_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name='到账金额')
    w_status = models.IntegerField(default=1, verbose_name='提现状态，1：审核中，2：已打款，3：已驳回')
    reason = models.CharField(max_length=256, default='', verbose_name='驳回原因')
    create_by = models.CharField(max_length=64, default='', verbose_name='创建人')
    create_time = models.DateTimeField(null=True, verbose_name='创建日期')
    modify_time = models.DateTimeField(null=True, verbose_name='最近修改日期')
    is_delete = models.IntegerField(default=0, verbose_name='是否删除1：是，0：未删除')

    class Meta:
        indexes = [
            models.Index(fields=['user_code', ]),
            models.Index(fields=['card_code', ]),
            models.Index(fields=['order_no', ]),
            models.Index(fields=['create_time', ]),
        ]
        verbose_name = '用户佣金提现记录表'
        verbose_name_plural = '用户佣金提现记录表'
        db_table = 'uw_users_withdrawal_history'
        ordering = ['-create_time']
        app_label = 'server'


class UsersBankCard(models.Model):
    user_code = models.CharField(max_length=64, default='', verbose_name='用户编号')
    name = models.CharField(max_length=64, default='', verbose_name='姓名')
    card_number = models.CharField(max_length=64, default='', unique=True, verbose_name='卡号')
    bank = models.CharField(max_length=128, default='', verbose_name='银行')
    bank_name = models.CharField(max_length=128, default='', verbose_name='开户行')
    mobile = models.CharField(max_length=64, default='', verbose_name='手机号')
    card_code = models.CharField(max_length=64, default='', unique=True, verbose_name='id号')
    create_by = models.CharField(max_length=64, default='', verbose_name='创建人')
    create_time = models.DateTimeField(null=True, verbose_name='创建日期')
    modify_time = models.DateTimeField(null=True, verbose_name='最近修改日期')
    is_delete = models.IntegerField(default=0, verbose_name='是否删除1：是，0：未删除')
    bank_no = models.CharField(max_length=128, default='', verbose_name='银行编号')

    class Meta:
        db_table = 'ub_users_bank_card'
        indexes = [
            models.Index(fields=['user_code', ]),
        ]
        verbose_name = '用户银行卡表'
        verbose_name_plural = '用户银行卡表'
        ordering = ['-create_time']
        app_label = 'server'


class OmtMessageCenter(models.Model):
    class Meta:
        db_table = 'omt_message_center'
        indexes = [
            models.Index(fields=['message_id', ]),
        ]
        verbose_name = '消息中心表'
        verbose_name_plural = verbose_name
        ordering = ['-weight']
        app_label = 'admin'

    id = models.AutoField(primary_key=True, verbose_name='唯一标识')
    message_id = models.IntegerField(db_index=True, verbose_name='消息ID')
    title = models.CharField(max_length=255, default='', verbose_name='标题')
    content = models.TextField(null=True, blank=True, verbose_name='内容')
    desc = models.TextField(null=True, blank=True, verbose_name='描述')
    creator = models.CharField(max_length=255, default='', verbose_name='创建者')
    cate = models.CharField(max_length=255, default='', verbose_name='分类')
    read_count = models.CharField(max_length=255, default='', verbose_name='阅读量')
    like_count = models.CharField(max_length=255, default='', verbose_name='点赞量')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    weight = models.IntegerField(default=0, verbose_name='权重, 数值越高， 排序越靠前')
    target_users = models.CharField(max_length=255, default='', verbose_name='目标用户')

    TARGET_TYPE_CHOICES = [
        ('0', '全部用户'),
        ('1', '普通用户'),
        ('2', 'vip'),
        ('3', '流量包会员'),
        ('4', '营销用户'),
    ]
    target_type = models.CharField(max_length=1, choices=TARGET_TYPE_CHOICES, default='0', verbose_name='目标类型')

    MESSAGE_TYPE_CHOICES = [
        (0, '系统消息'),
        (1, '站内信'),
        (2, '资讯'),
    ]
    message_type = models.IntegerField(choices=MESSAGE_TYPE_CHOICES, default=0, verbose_name='消息类型')
    read_count = models.IntegerField(default=0, verbose_name='阅读量')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')

    is_arousel = models.BooleanField(default=False, verbose_name='是否轮播')

    STATUS_CHOICES = [
        ('0', '未定义'),
        ('1', '使用中'),
        ('2', '暂停'),
        ('3', '删除'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='0', verbose_name='状态')
    image = models.CharField(max_length=255, default='', verbose_name='资讯首页图片')

    IS_READ = [
        ('0', '未读'),
        ('1', '已读')
    ]
    is_read = models.IntegerField(max_length=1, choices=IS_READ, default='0', verbose_name='是否已读')

    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')


class OiInfoTypes(models.Model):
    id = models.AutoField(primary_key=True)
    info_type_id = models.BigIntegerField()
    info_type_name = models.CharField(max_length=255, null=True, blank=True)
    info_type_name_cn = models.CharField(max_length=255, null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oi_info_types'
        indexes = [
            models.Index(fields=['info_type_id', ]),
        ]
        verbose_name = '补充信息类型表'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        app_label = 'admin'


class OioInfoOptions(models.Model):
    id = models.AutoField(primary_key=True)
    option_id = models.BigIntegerField(default=0)
    info_type_id = models.IntegerField(default=0)
    option_value = models.CharField(max_length=255, default='')
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oio_info_options'
        verbose_name = '补充信息选项表'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        app_label = 'admin'


class OioInfoOptionsUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=255, default='')
    option_id = models.BigIntegerField(default=0)
    info_type_id = models.IntegerField(default=0)
    option_value = models.CharField(max_length=255, default='')
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oio_info_options_user'
        verbose_name = '用户自建补充信息选项表'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        app_label = 'admin'


class OqQuestionInfo(models.Model):
    id = models.AutoField(primary_key=True)
    question_add_id = models.IntegerField(default=0)
    info_type_id = models.IntegerField(default=0)
    question_id = models.IntegerField(null=True, blank=True)
    option_ids = models.CharField(max_length=255, default='')
    title = models.CharField(max_length=255, default='')
    placeholder = models.CharField(max_length=255, default='')
    is_required = models.CharField(max_length=255, default=0)
    weight = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oq_question_info'
        ordering = ['-weight']
        verbose_name = '问题补充信息表'
        verbose_name_plural = verbose_name
        app_label = 'admin'


class OqQuestionInfoUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=255, default='')
    question_add_id = models.IntegerField(default=0)
    info_type_id = models.IntegerField(default=0)
    question_id = models.IntegerField(null=True, blank=True)
    option_ids = models.CharField(max_length=255, default='')
    title = models.CharField(max_length=255, default='')
    placeholder = models.CharField(max_length=255, default='')
    is_required = models.CharField(max_length=255, default=0)
    weight = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oq_question_info_user'
        ordering = ['-weight']
        verbose_name = '用户自建问题补充信息表'
        verbose_name_plural = verbose_name
        app_label = 'admin'


class CCChatSquare(models.Model):
    id = models.AutoField(primary_key=True)
    module_id = models.CharField(max_length=64, default='', blank=True, null=True)
    question_id = models.CharField(max_length=64, default='', blank=True, null=True)
    session_code = models.CharField(max_length=64, default='', blank=True, null=True)
    chat_group_code = models.CharField(max_length=64, default='', blank=True, null=True)
    question_code = models.CharField(max_length=64, default='', blank=True, null=True)
    s_status = models.IntegerField(default=1, blank=True, null=True)
    create_by = models.CharField(max_length=64, default='', blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    modify_time = models.DateTimeField(blank=True, null=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['create_by']),
            models.Index(fields=['module_id', 'question_id']),
            models.Index(fields=['session_code']),
        ]
        db_table = 'cc_chat_square'
        verbose_name = "问答广场主表"
        verbose_name_plural = "问答广场主表"
        app_label = 'server'


class CCChatPrompt(models.Model):
    id = models.AutoField(primary_key=True)
    question_code = models.CharField(max_length=64, default='', blank=True, null=True, unique=True)
    question_data = models.JSONField(null=True)

    class Meta:
        db_table = 'cc_chat_prompt'
        verbose_name = "问答广场提示词表"
        verbose_name_plural = "问答广场提示词表"
        app_label = 'server'


class CCChatMessages(models.Model):
    id = models.AutoField(primary_key=True)
    session_code = models.CharField(max_length=64, default='', blank=True, null=True, unique=True)
    session_data = models.JSONField(null=True)

    class Meta:
        db_table = 'cc_chat_messages'
        verbose_name = "问答广场消息表"
        verbose_name_plural = "问答广场消息表"
        app_label = 'server'


class CPCustomerProducts(models.Model):
    PLATFORM_CHOICES = (
        (0, '测试'),
        (1, 'PC'),
        (2, 'H5'),
        (3, '小程序'),
        (4, '全平台'),
        (5, 'API辅助'),
    )

    STATUS_CHOICES = (
        (0, '待启用'),
        (1, '正常'),
        (2, '下架'),
        (3, '暂停'),
    )

    id = models.AutoField(primary_key=True, verbose_name='商品ID')
    customer_id = models.BigIntegerField(verbose_name='客户ID', unique=True)
    prod_id = models.IntegerField(verbose_name='商品id', default=0)
    prod_name = models.CharField(max_length=255, default='', verbose_name='商品名称')
    platform = models.PositiveSmallIntegerField(choices=PLATFORM_CHOICES, verbose_name='平台')
    prod_desc = models.TextField(null=True, blank=True, verbose_name='商品描述')
    prod_description = models.CharField(max_length=255, null=True, blank=True)
    prod_details = models.TextField(null=True, blank=True, verbose_name='商品详情')
    prod_origin_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='商品原价')
    continuous_annual_sub_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                                      verbose_name='连续订阅价格')
    prod_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='商品价格')
    valid_period_days = models.IntegerField(default=0, verbose_name='会员类产品有效期')
    prod_cate_id = models.IntegerField(default=0, verbose_name='商品类别ID')
    status = models.PositiveSmallIntegerField(default=0, choices=STATUS_CHOICES, verbose_name='状态')
    is_show = models.BooleanField(default=False, verbose_name='是否前端展示')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'cp_customer_products'
        verbose_name = '客户产品'
        verbose_name_plural = verbose_name
        app_label = 'admin'


class OCICustomerInformation(models.Model):
    STATUS_CHOICES = (
        (0, '待启用'),
        (1, '正常'),
        (2, '欠费'),
        (3, '封禁'),
        (4, '暂停'),
    )

    id = models.AutoField(primary_key=True, verbose_name='主键ID')
    customer_id = models.BigIntegerField(verbose_name='客户ID')
    company_name = models.CharField(max_length=255, verbose_name='公司名称', db_index=True)
    address = models.CharField(max_length=255, verbose_name='地址')
    account = models.CharField(max_length=255, verbose_name='账号', db_index=True)
    password = models.CharField(max_length=255, verbose_name='密码')
    contact_person = models.CharField(max_length=255, verbose_name='联系人')
    contact_number = models.CharField(max_length=20, verbose_name='联系电话')
    status = models.PositiveSmallIntegerField(default=0, choices=STATUS_CHOICES, verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'oci_customer_information'
        verbose_name = '客户信息'
        verbose_name_plural = verbose_name
        app_label = 'admin'


class UQDUserQuestionDetails(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="主键")
    user_id = models.CharField(max_length=255, db_index=True, verbose_name="用户ID")
    question_id = models.IntegerField(default=0, db_index=True, verbose_name="问题ID")
    question_add_ids = models.CharField(max_length=255, default="", verbose_name="附加问题ID")
    industry_id = models.IntegerField(default=0, verbose_name="行业ID")
    module_id = models.IntegerField(default=0, verbose_name="模块ID")
    occu_id = models.IntegerField(default=0, verbose_name="职业ID")
    sec_occu_id = models.IntegerField(default=0, verbose_name="次要职业ID")
    occu_duration_id = models.IntegerField(default=0, verbose_name="职业持续时间")
    expertise_level_id = models.IntegerField(default=0, verbose_name="专业水平")
    character_avatar = models.CharField(max_length=255, default="", blank=True, verbose_name="角色头像")
    character_name = models.CharField(max_length=255, default="", blank=True, verbose_name="角色名字")
    character_greetings = models.CharField(max_length=255, default="", blank=True, verbose_name="角色问候语")
    is_public = models.IntegerField(default=0, verbose_name="是否公开")
    hint = models.CharField(max_length=255, default="", blank=True, verbose_name="角色提示")
    example_question = models.CharField(max_length=255, default="", blank=True, verbose_name="示例问题")
    character_desc = models.TextField(default="", blank=True, verbose_name="角色描述")
    character_achievements = models.TextField(max_length=255, default="", blank=True, verbose_name="角色成就")
    assistant_title = models.CharField(max_length=255, default="", blank=True, verbose_name="助手标题")
    assistant_content = models.TextField(max_length=255, default="", blank=True, verbose_name="助手内容")
    related_document = models.TextField(default="", blank=True, verbose_name="相关文档")
    is_delete = models.IntegerField(default=0, verbose_name="是否删除")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    status = models.IntegerField(default=0, verbose_name="状态")
    refuse_reason = models.CharField(max_length=255, default="", blank=True, verbose_name="拒绝理由")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "question_id": self.question_id,
            "question_add_ids": self.question_add_ids,
            "industry_id": self.industry_id,
            "module_id": self.module_id,
            "occu_id": self.occu_id,
            "sec_occu_id": self.sec_occu_id,
            "occu_duration_id": self.occu_duration_id,
            "expertise_level_id": self.expertise_level_id,
            "character_avatar": self.character_avatar,
            "character_name": self.character_name,
            "character_greetings": self.character_greetings,
            "is_public": self.is_public,
            "hint": self.hint,
            "example_question": self.example_question,
            "character_desc": self.character_desc,
            "character_achievements": self.character_achievements,
            "assistant_title": self.assistant_title,
            "assistant_content": self.assistant_content,
            "related_document": self.related_document,
            "is_delete": self.is_delete,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            "updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
            "status": self.status,
            "refuse_reason": self.refuse_reason,
        }

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['user_id'])
        ]
        db_table = 'uqd_user_question_details'
        verbose_name = '用户自建问题详情'
        verbose_name_plural = verbose_name
        app_label = 'admin'


class CEEnterpriseFiles(models.Model):
    code = models.CharField(max_length=64, default='', db_index=True, verbose_name='关联编号')
    file_url = models.CharField(max_length=256, default='', verbose_name='文件地址')
    file_category = models.SmallIntegerField(default=1, verbose_name='文件分类', choices=(
        (1, '企业文件'),
        (2, '项目文件'),
        (3, '资讯文件'),
        (4, '知识库文件'),
    ))
    group_code = models.CharField(max_length=64, default='', verbose_name='组编号')
    create_by = models.CharField(max_length=64, default='', verbose_name='创建人')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    modify_time = models.DateTimeField(auto_now=True, verbose_name='最近修改日期')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    file_name = models.CharField(max_length=256, default='', verbose_name='文件名称')

    class Meta:
        db_table = 'ce_enterprise_files'
        verbose_name = '企业文件表'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['code'])
        ]
        app_label = 'server'


class EnterpriseInfo(models.Model):
    company_code = models.CharField(max_length=64, unique=True, default='', verbose_name='公司编号')
    company_name = models.CharField(max_length=64, default='', verbose_name='公司名称')
    company_abbreviation = models.CharField(max_length=64, default='', verbose_name='简称')
    position = models.CharField(max_length=64, default='', verbose_name='职位')
    industry_code = models.CharField(max_length=20, default='', verbose_name='行业编号')
    registered_address = models.CharField(max_length=256, default='', verbose_name='注册地址')
    company_desc = models.CharField(max_length=512, default='', verbose_name='公司描述')
    company_url = models.CharField(max_length=256, default='', verbose_name='公司网址')
    ipc_code = models.CharField(max_length=256, default='', verbose_name='ipc备案号')
    company_mobile = models.CharField(max_length=64, default='', verbose_name='公司电话')
    company_mailbox = models.CharField(max_length=64, default='', verbose_name='公司邮箱')
    company_address = models.CharField(max_length=256, default='', verbose_name='公司地址')
    status = models.PositiveSmallIntegerField(default=1, verbose_name='状态，1：保存，2提交')
    create_by = models.CharField(max_length=64, default='', verbose_name='创建人')
    create_time = models.DateTimeField(null=True, verbose_name='创建日期')
    modify_time = models.DateTimeField(null=True, verbose_name='最近修改日期')
    is_delete = models.PositiveSmallIntegerField(default=0, verbose_name='是否删除1：是，0：未删除')

    class Meta:
        db_table = 'ce_enterprise_info'
        verbose_name = '企业表'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['company_code', 'create_by'])
        ]
        app_label = 'server'


class EnterpriseProjectInfo(models.Model):
    company_code = models.CharField(max_length=64, default='', verbose_name='企业编号')
    project_code = models.CharField(max_length=64, unique=True, default='', verbose_name='项目编号')
    category_name = models.CharField(max_length=64, default='', verbose_name='类目名称')
    project_name = models.CharField(max_length=64, default='', verbose_name='项目名称')
    brief_introduction = models.CharField(max_length=256, default='', verbose_name='简介')
    create_by = models.CharField(max_length=64, default='', verbose_name='创建人')
    create_time = models.DateTimeField(null=True, verbose_name='创建日期')
    modify_time = models.DateTimeField(null=True, verbose_name='最近修改日期')
    is_delete = models.PositiveSmallIntegerField(default=0, verbose_name='是否删除1：是，0：未删除')

    class Meta:
        db_table = 'ce_enterprise_project_info'
        verbose_name = '企业项目表'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['company_code', 'project_code'])
        ]
        app_label = 'server'


class EnterpriseInformationInfo(models.Model):
    company_code = models.CharField(max_length=64, default='', verbose_name='企业编号')
    information_code = models.CharField(max_length=64, unique=True, default='', verbose_name='资讯编号')
    label_code = models.CharField(max_length=20, default='', verbose_name='资讯信息标签编号')
    information_name = models.CharField(max_length=64, default='', verbose_name='资讯名称')
    content_desc = models.CharField(max_length=512, default='', verbose_name='内容描述')
    create_by = models.CharField(max_length=64, default='', verbose_name='创建人')
    create_time = models.DateTimeField(null=True, verbose_name='创建日期')
    modify_time = models.DateTimeField(null=True, verbose_name='最近修改日期')
    is_delete = models.PositiveSmallIntegerField(default=0, verbose_name='是否删除1：是，0：未删除')

    class Meta:
        db_table = 'ce_enterprise_information_info'
        verbose_name = '企业资讯表'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['company_code', 'information_code'])
        ]
        app_label = 'server'


class EnterpriseKnowledgeBase(models.Model):
    company_code = models.CharField(max_length=64, default='', verbose_name='企业编号')
    knowledge_code = models.CharField(max_length=64, unique=True, default='', verbose_name='知识库编号')
    category = models.CharField(max_length=64, default='', verbose_name='分类')
    category_name = models.CharField(max_length=64, default='', verbose_name='知识库名称')
    content_desc = models.CharField(max_length=512, default='', verbose_name='内容描述')
    purpose = models.CharField(max_length=512, default='', verbose_name='用途')
    create_by = models.CharField(max_length=64, default='', verbose_name='创建人')
    create_time = models.DateTimeField(null=True, verbose_name='创建日期')
    modify_time = models.DateTimeField(null=True, verbose_name='最近修改日期')
    is_delete = models.PositiveSmallIntegerField(default=0, verbose_name='是否删除1：是，0：未删除')

    class Meta:
        db_table = 'ce_enterprise_knowledge_base'
        verbose_name = '企业知识库表'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['company_code', 'knowledge_code'])
        ]
        app_label = 'server'


class EnterpriseLabel(models.Model):
    label_code = models.CharField(max_length=64, unique=True, default='', verbose_name='分类编号')
    label = models.CharField(max_length=64, default='', verbose_name='分类')
    label_type = models.PositiveSmallIntegerField(default=1, verbose_name='类型1行业，2资讯，3：分类')
    create_by = models.CharField(max_length=64, default='', verbose_name='创建人')
    create_time = models.DateTimeField(null=True, verbose_name='创建日期')
    modify_time = models.DateTimeField(null=True, verbose_name='最近修改日期')
    is_delete = models.PositiveSmallIntegerField(default=0, verbose_name='是否删除1：是，0：未删除')

    class Meta:
        db_table = 'ce_enterprise_label'
        verbose_name = '企业标签表'
        verbose_name_plural = verbose_name
        app_label = 'server'


class VdDigitalHumanExperience(models.Model):
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=256, default='', verbose_name='姓名')
    mobile = models.CharField(max_length=256, default='', verbose_name='手机', db_index=True)
    create_by = models.CharField(max_length=64, default='', verbose_name='创建人')
    create_time = models.DateTimeField(null=True, verbose_name='创建日期')
    modify_time = models.DateTimeField(null=True, verbose_name='最近修改日期')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除1：是，0：未删除')

    class Meta:
        db_table = 'vd_digital_human_experience'
        verbose_name = '数字体验记录表'
        verbose_name_plural = '数字体验记录表'
        app_label = 'server'


class DhDigitalHumanProduct(models.Model):
    # Constants for product types
    NO_MAN_LIVE_BROADCAST = 1
    SHORT_VIDEO_MATRIX = 2
    DIGITAL_HUMAN_LIVE_BROADCAST = 3

    PRODUCT_TYPE_CHOICES = (
        (NO_MAN_LIVE_BROADCAST, '无人直播'),
        (SHORT_VIDEO_MATRIX, '短视频矩阵'),
        (DIGITAL_HUMAN_LIVE_BROADCAST, '数字人直播'),
    )

    id = models.AutoField(primary_key=True)
    product_type = models.PositiveSmallIntegerField(choices=PRODUCT_TYPE_CHOICES, null=True, verbose_name="产品类型")
    download_link = models.CharField(max_length=1000, null=True, blank=True, verbose_name="下载地址")
    product_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="产品名称")
    tutorial = models.CharField(max_length=1000, null=True, blank=True, verbose_name="使用教程")
    usage_description = models.TextField(null=True, blank=True, verbose_name="使用说明")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.PositiveSmallIntegerField(default=0, verbose_name="是否删除")

    class Meta:
        db_table = 'dh_digital_human_product'
        verbose_name = '数字人产品'
        verbose_name_plural = '数字人产品列表'
        app_label = 'admin'


class DhDigitalHumanSecretKey(models.Model):
    # Constants for product types
    # You can define the product types as per the requirements.
    # For this example, I'm reusing the previous product types.
    NO_MAN_LIVE_BROADCAST = 1
    SHORT_VIDEO_MATRIX = 2
    DIGITAL_HUMAN_LIVE_BROADCAST = 3

    PRODUCT_TYPE_CHOICES = (
        (NO_MAN_LIVE_BROADCAST, '无人直播'),
        (SHORT_VIDEO_MATRIX, '短视频矩阵'),
        (DIGITAL_HUMAN_LIVE_BROADCAST, '数字人直播'),
    )

    id = models.AutoField(primary_key=True)
    product_type = models.PositiveSmallIntegerField(choices=PRODUCT_TYPE_CHOICES, verbose_name="产品类型")
    key_id = models.BigIntegerField(verbose_name="卡密ID")
    account = models.CharField(max_length=255, blank=True, verbose_name="账号")
    account_type = models.SmallIntegerField(max_length=1, blank=True, verbose_name="账号类型")
    password = models.CharField(max_length=255, blank=True, verbose_name="密码")
    mobile = models.CharField(max_length=255, blank=True, verbose_name="手机号")
    name = models.CharField(max_length=100, blank=True, verbose_name="姓名")
    secrey_key = models.CharField(max_length=255, default='', verbose_name="卡密")
    sign = models.CharField(max_length=100, default='', verbose_name="标识")
    seller_name = models.CharField(max_length=100, default='', verbose_name="所属销售人员")
    status = models.PositiveSmallIntegerField(verbose_name="状态")
    receive_time = models.DateTimeField(verbose_name="领取时间")
    valid_time = models.DateTimeField(verbose_name="有效时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = 'dh_digital_human_secret_key'
        verbose_name = '数字人秘钥'
        verbose_name_plural = '数字人秘钥列表'
        app_label = 'admin'


class ScpcSecretKeyPersonalCenter(models.Model):
    # Constants for product types
    # As you have not defined the product types, I'm leaving this commented out.
    # You can uncomment and define the product types as per your requirements.
    # For example:
    NO_MAN_LIVE_BROADCAST = 1
    SHORT_VIDEO_MATRIX = 2
    DIGITAL_HUMAN_LIVE_BROADCAST = 3

    PRODUCT_TYPE_CHOICES = (
        (NO_MAN_LIVE_BROADCAST, '无人直播'),
        (SHORT_VIDEO_MATRIX, '短视频矩阵'),
        (DIGITAL_HUMAN_LIVE_BROADCAST, '数字人直播'),
    )

    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100, blank=True, verbose_name="用户ID")
    sign = models.CharField(max_length=100, blank=True, verbose_name="分享者id")
    product_type = models.PositiveSmallIntegerField(null=True, choices=PRODUCT_TYPE_CHOICES,
                                                    verbose_name="产品类型")  # , choices=PRODUCT_TYPE_CHOICES
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")

    class Meta:
        db_table = 'scpc_secret_key_personal_center'
        verbose_name = '个人中心秘钥'
        verbose_name_plural = '个人中心秘钥列表'
        app_label = 'admin'


class UDDistributorLevel(models.Model):
    d_level = models.PositiveSmallIntegerField(default=1, help_text='分销等级1：金牌分销，2：钻石分销')
    commission_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text='佣金比例,计算时除100')
    desc = models.CharField(max_length=64, default='', help_text='等级描述')
    create_by = models.CharField(max_length=64, default='', help_text='创建人')
    create_time = models.DateTimeField(null=True, blank=True, help_text='创建日期')
    modify_time = models.DateTimeField(null=True, blank=True, help_text='最近修改日期')
    is_delete = models.BooleanField(default=False, help_text='是否删除1：是，0：未删除')

    class Meta:
        db_table = 'ud_distributor_level'
        verbose_name = '用户分销等级表'
        verbose_name_plural = '用户分销等级表'
        app_label = 'server'


class VtTextToSpeechVoice(models.Model):
    engine_code = models.CharField(max_length=20, default='', blank=True, verbose_name='引擎唯一编号')
    voice_code = models.CharField(max_length=20, unique=True, default='', blank=True, verbose_name='音色唯一编号')
    voice = models.CharField(max_length=64, default='', blank=True, verbose_name='音色')
    voice_name = models.CharField(max_length=64, default='', blank=True, verbose_name='音色名称')
    voice_logo = models.CharField(max_length=256, default='', blank=True, verbose_name='音色logo')
    speech_url = models.CharField(max_length=256, default='', blank=True, verbose_name='音色试听')
    language = models.CharField(max_length=64, default='', blank=True, verbose_name='语言')
    desc = models.CharField(max_length=256, default='', blank=True, verbose_name='描述')
    create_by = models.CharField(max_length=64, default='', blank=True, verbose_name='创建人')
    create_time = models.DateTimeField(null=True, blank=True, verbose_name='创建日期')
    modify_time = models.DateTimeField(null=True, blank=True, verbose_name='最近修改日期')
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'vt_text_to_speech_voice'
        verbose_name = '文本转语音音色表'
        verbose_name_plural = '文本转语音音色表'
        app_label = 'server'


class BaseModel(models.Model):
    """为模型类补充字段"""
    create_by = models.CharField(max_length=64, blank=True, null=True, default="", help_text="创建人唯一编号")
    create_time = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name="创建时间")
    modify_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_delete = models.IntegerField(blank=True, null=True, default=0, help_text="是否删除。1：删除，0：否")

    objects = models.Manager()

    class Meta:
        abstract = True
        app_label = 'server'

class VtVoiceId(BaseModel):
    """"""
    voice_id = models.CharField(max_length=64, blank=True, null=True, default="", verbose_name="第三方唯一声音id")
    voice_status = models.IntegerField(blank=True, null=True, default=1, help_text="状态1：待分配，2:已分配，3：已使用")
    user_code = models.CharField(max_length=64, blank=True, null=True, default="", verbose_name="使用者")

    class Meta:
        managed = False
        db_table = 'vt_voice_id'
        verbose_name = '声音id表'
        verbose_name_plural = verbose_name
        app_label = 'server'