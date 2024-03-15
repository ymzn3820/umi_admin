💡 **「关于」**

## 声明
  后台使用了基于huge-dream的django-vue-admin平台
  源码地址：gitee地址(主推)：[https://gitee.com/liqianglog/django-vue-admin](https://gitee.com/liqianglog/django-vue-admin)👩‍👦‍👦

## 平台简介

* 🧑‍🤝‍🧑前端采用[D2Admin](https://github.com/d2-projects/d2-admin) 、[Vue](https://cn.vuejs.org/)、[ElementUI](https://element.eleme.cn/)。
* 👭后端采用 Python 语言 Django 框架以及强大的 [Django REST Framework](https://pypi.org/project/djangorestframework)。
* 👫权限认证使用[Django REST Framework SimpleJWT](https://pypi.org/project/djangorestframework-simplejwt)，支持多终端认证系统。
* 👬支持加载动态权限菜单，多方式轻松权限控制。


👩‍👦‍👦文档地址：[https://django-vue-admin.com](https://django-vue-admin.com)

## 内置功能

1.  👨‍⚕️菜单管理：配置系统菜单，操作权限，按钮权限标识、后端接口权限等。
2.  🧑‍⚕️部门管理：配置系统组织机构（公司、部门、角色）。
3.  👩‍⚕️角色管理：角色菜单权限分配、数据权限分配、设置角色按部门进行数据范围权限划分。
4.  🧑‍🎓权限权限：授权角色的权限范围。
5.  👨‍🎓用户管理：用户是系统操作者，该功能主要完成系统用户配置。
6.  👬接口白名单：配置不需要进行权限校验的接口。
7.  🧑‍🔧字典管理：对系统中经常使用的一些较为固定的数据进行维护。
8.  🧑‍🔧地区管理：对省市县区域进行管理。
9.  📁附件管理：对平台上所有文件、图片等进行统一管理。
10.  🗓️操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。
11.  🔌[插件市场 ](https://bbs.django-vue-admin.com/plugMarket.html)：基于Django-Vue-Admin框架开发的应用和插件。

##  插件市场 🔌

- Celery异步任务：[dvadmin-celery](https://gitee.com/huge-dream/dvadmin-celery)
- 升级中心后端：[dvadmin-upgrade-center](https://gitee.com/huge-dream/dvadmin-upgrade-center)
- 升级中心前端：[dvadmin-upgrade-center-web](https://gitee.com/huge-dream/dvadmin-upgrade-center-web)

## 准备工作
~~~
补全TODO配置部分
Python >= 3.8.0 (推荐3.8+版本)
nodejs >= 14.0 (推荐最新)
Mysql >= 5.7.0 (可选，默认数据库sqlite3，推荐8.0版本)
Redis(可选，最新版)
~~~

## 开始
    拉取项目：git clone https://github.com/ymzn3820/umi_admin.git
    构建：docker compose -f ai.yml build
    运行：docker compose -f ai.yml up -d
    检查：docker logs -f {containerId}, 如果没有报错信息，则运行成功。

    # 初始化后端数据(第一次执行即可)
    docker exec -ti dvadmin-django bash
    python manage.py makemigrations 
    python manage.py migrate
    python manage.py init_area
    python manage.py init
    exit
    
    前端地址：http://127.0.0.1:8080
    后端地址：http://127.0.0.1:8080/api
    # 在服务器上请把127.0.0.1 换成自己公网ip
    账号：superadmin 密码：admin123456
    
    # docker-compose 停止
    docker-compose down
    #  docker-compose 重启
    docker-compose restart
    #  docker-compose 启动时重新进行 build
    docker-compose up -d --build


### 访问项目

- 访问地址：[http://localhost:8080](http://localhost:8080) (默认为此地址，如有修改请按照配置文件)
- 账号：`superadmin` 密码：`admin123456`


##  联系我们: 
![联系我们](https://umi-intelligence.oss-cn-shenzhen.aliyuncs.com/static/com/message_center/1705734163826.jpg)




