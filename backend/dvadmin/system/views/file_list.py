import hashlib
import mimetypes

from django.conf import settings
from rest_framework import serializers

from application import dispatch
from dvadmin.system.models import FileList
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.tooss import Tooss
from dvadmin.utils.viewset import CustomModelViewSet


class FileSerializer(CustomModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    def get_url(self, instance):
        # return 'media/' + str(instance.url)
        return instance.file_url or (f'media/{str(instance.url)}')

    class Meta:
        model = FileList
        fields = "__all__"

    def create(self, validated_data):
        # file_engine = dispatch.get_system_config_values("fileStorageConfig.file_engine") or 'local'
        file_engine = 'oss'

        file_backup = dispatch.get_system_config_values("fileStorageConfig.file_backup")
        file = self.initial_data.get('file')

        file_size = file.size
        validated_data['name'] = file.name
        validated_data['size'] = file_size
        md5 = hashlib.md5()
        with open(f'./media/files/messages/{file.name}', 'wb+') as f:
            print('00000000')
            for chunk in file.chunks():
                f.write(chunk)
            md5.update(chunk)
        validated_data['md5sum'] = md5.hexdigest()
        validated_data['engine'] = file_engine
        validated_data['mime_type'] = file.content_type

        if file_backup:
            validated_data['url'] = file
        if file_engine == 'oss':
            oss_file_url = Tooss.main(file, 'message_center', local=True, local_path=f'./media/files/messages/{file.name}')
            if oss_file_url:
                print(oss_file_url)
                print("oss_file_urloss_file_urloss_file_url")
                validated_data['file_url'] = oss_file_url[0]
            else:
                raise ValueError("上传失败")
        elif file_engine == 'cos':
            from dvadmin_cloud_storage.views.tencent import tencent_cos_upload
            file_path = tencent_cos_upload(file)
            if file_path:

                validated_data['file_url'] = file_path
            else:
                raise ValueError("上传失败")
        else:
            validated_data['url'] = file
        # 审计字段
        try:
            request_user = self.request.user
            validated_data['dept_belong_id'] = request_user.dept.id
            validated_data['creator'] = request_user.id
            validated_data['modifier'] = request_user.id
        except:
            pass
        return super().create(validated_data)


class FileViewSet(CustomModelViewSet):
    """
    文件管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = FileList.objects.all()

    serializer_class = FileSerializer
    filter_fields = ['name', ]
    permission_classes = []
