from django.urls import path, include
from rest_framework import routers

from dvadmin.system.views.activate_code import BatchGenerateCode, ActivationCodeManagement, GetActivateCodeTemp
from dvadmin.system.views.api_white_list import ApiWhiteListViewSet
from dvadmin.system.views.area import AreaViewSet
from dvadmin.system.views.bank_card import UsersBankCardWithdrawalView
from dvadmin.system.views.clause import PrivacyView, TermsServiceView
from dvadmin.system.views.contact import BusinessCooperationManage
from dvadmin.system.views.customer_account import OCICustomerInformationView, CustomerInfoDict
from dvadmin.system.views.customer_balance import CustomerBalance, CustomerBalancePublic
from dvadmin.system.views.customer_products import CPCustomerProductsView
from dvadmin.system.views.dashboard import DashBoardAPIView, LoginUserView, RegisteredUserView, UsersTotalView, \
    DatabaseTotalView
from dvadmin.system.views.datav import DataVViewSet
from dvadmin.system.views.dept import DeptViewSet
from dvadmin.system.views.dictionary import DictionaryViewSet
from dvadmin.system.views.digital_human_experience import DigitalHumanExperienceManage
from dvadmin.system.views.digital_human_personal_center import DigitalPersonalCenter, QRCodeManage
from dvadmin.system.views.digital_human_products import DigitalHumanProductManage
from dvadmin.system.views.digital_human_secret_key import DigitalHumanSecretKeyManage, AssignCustomer, ShortUrl
from dvadmin.system.views.distributor import DistributorLevelManage
from dvadmin.system.views.duration import OpEmpDurationView, OpEmpDurationDictView
from dvadmin.system.views.enterprise_info import EnterpriseInfoManage
from dvadmin.system.views.expertise_level import OpExpertiseLevelView, OpExpertiseLevelDictView
from dvadmin.system.views.file_list import FileViewSet
from dvadmin.system.views.hashrate_rules import HashratesRules
from dvadmin.system.views.industry import OpIndustryManage, OpIndustryManageDict
from dvadmin.system.views.login_log import LoginLogViewSet
from dvadmin.system.views.menu import MenuViewSet
from dvadmin.system.views.menu_button import MenuButtonViewSet
from dvadmin.system.views.message_center import MessageCenterViewSet
from dvadmin.system.views.messages import OmtMessageCenterManage, OmtMessageCenterOverviewManage
from dvadmin.system.views.modules import ModulesManage, ModulesDictManage
from dvadmin.system.views.occupation import OpOccupationView, OpOccupationDictView
from dvadmin.system.views.orders import POOrderManage
from dvadmin.system.views.payments import PpPaymentsManage
from dvadmin.system.views.pictures import PicturesManage
from dvadmin.system.views.operation_log import OperationLogViewSet
from dvadmin.system.views.oss import OSS
from dvadmin.system.views.products import ProductsManage
from dvadmin.system.views.question_edit import OpQuestionsEditView
from dvadmin.system.views.question_edit_user import OioInfoOptionsUserView, OqQuestionInfoUserView, \
    UQDUserQuestionDetailsView, OqQuestionInfoUserDictView, OioInfoOptionsUserDictView, \
    OqQuestionInfoUserDetailDictView, GetRelatedDocuments
from dvadmin.system.views.question_set import OpQuestionsSetView, OpQuestionsSetDictView
from dvadmin.system.views.role import RoleViewSet
from dvadmin.system.views.sd_models import SdModelsManage
from dvadmin.system.views.sec_occupation import OpSubOccuView, OpSubOccuDictView
from dvadmin.system.views.secret_key import SecretKeyManage, SecretKeyPublish
from dvadmin.system.views.speech_voice import VtTextToSpeechVoiceManage
from dvadmin.system.views.system_config import SystemConfigViewSet
from dvadmin.system.views.tab import OpTabManage, OpTabManageDict
from dvadmin.system.views.tech_assistant import UpProblemView
from dvadmin.system.views.user import UserViewSet
from dvadmin.system.views.users import UuUsersManage
from dvadmin.system.views.voice_clone import VtVoiceIdManagement
from dvadmin.system.views.question_edit_new import OiInfoTypesView, OqQuestionInfoView, OioInfoOptionsView, \
    OioInfoOptionsDictView, OiInfoTypesDictView, CCChatSquareView

system_url = routers.SimpleRouter()
system_url.register(r'menu', MenuViewSet)
system_url.register(r'menu_button', MenuButtonViewSet)
system_url.register(r'role', RoleViewSet)
system_url.register(r'dept', DeptViewSet)
system_url.register(r'user', UserViewSet)
system_url.register(r'operation_log', OperationLogViewSet)
system_url.register(r'dictionary', DictionaryViewSet)
system_url.register(r'area', AreaViewSet)
system_url.register(r'file', FileViewSet)
system_url.register(r'api_white_list', ApiWhiteListViewSet)
system_url.register(r'system_config', SystemConfigViewSet)
system_url.register(r'message_center', MessageCenterViewSet)
system_url.register(r'datav', DataVViewSet)



urlpatterns = [
    path('system_config/save_content/', SystemConfigViewSet.as_view({'put': 'save_content'})),
    path('system_config/get_association_table/', SystemConfigViewSet.as_view({'get': 'get_association_table'})),
    path('system_config/get_table_data/<int:pk>/', SystemConfigViewSet.as_view({'get': 'get_table_data'})),
    path('system_config/get_relation_info/', SystemConfigViewSet.as_view({'get': 'get_relation_info'})),
    path('login_log/', LoginLogViewSet.as_view({'get': 'list'})),
    path('login_log/<int:pk>/', LoginLogViewSet.as_view({'get': 'retrieve'})),
    path('dept_lazy_tree/', DeptViewSet.as_view({'get': 'dept_lazy_tree'})),
    path('clause/privacy.html', PrivacyView.as_view()),
    path('clause/terms_service.html', TermsServiceView.as_view()),
]

urlpatterns += system_url.urls
# 新增urlpatterns， 主要为chatai_admin 相关api

admin_urls = [
    path('batch_generate_code/', BatchGenerateCode.as_view(), name='批量生成激活码'),
    path('activate_code/', ActivationCodeManagement.as_view(), name='激活码管理'),
    path('get_code/', GetActivateCodeTemp.as_view(), name='外部用户获取激活码'),
    path('dashboard/', DashBoardAPIView.as_view(), name='Dashboard'),
    path('login_user_count/', LoginUserView.as_view(), name='登陆用户趋势'),
    path('reg_user_count/', RegisteredUserView.as_view(), name='注册用户趋势'),
    path('user_total/', UsersTotalView.as_view(), name='总用户数'),
    path('database_total/', DatabaseTotalView.as_view(), name='数据库使用情况'),
    path('oss/', OSS.as_view(), name='上传图片'),
    path('pictures/', PicturesManage.as_view(), name='图片管理'),
    path('secret_key/', SecretKeyManage.as_view(), name='密钥管理'),
    path('secret_key_pub/', SecretKeyPublish.as_view(), name='密钥发布'),
    path('contact/', BusinessCooperationManage.as_view(), name='商务合作'),
    path('product/', ProductsManage.as_view(), name='商品后台'),
    path('payments/', PpPaymentsManage.as_view(), name='支付后台'),
    path('orders/', POOrderManage.as_view(), name='订单后台'),
    path('users/', UuUsersManage.as_view(), name='用户后台'),
    path('tab/', OpTabManage.as_view(), name='tab栏管理'),
    path('tab_dict/', OpTabManageDict.as_view(), name='tab栏字典映射'),
    path('industry/', OpIndustryManage.as_view(), name='行业管理后台'),
    path('industry_dict/', OpIndustryManageDict.as_view(), name='行业管理后台字典映射'),
    path('occupation/', OpOccupationView.as_view(), name='职业管理后台'),
    path('occupation_dict/', OpOccupationDictView.as_view(), name='职业管理后台字典映射'),
    path('sec_occupation/', OpSubOccuView.as_view(), name='次级职业管理后台'),
    path('sec_occupation_dict/', OpSubOccuDictView.as_view(), name='次级职业管理后台字典映射'),
    path('duration/', OpEmpDurationView.as_view(), name='从业时间管理后台'),
    path('duration_dict/', OpEmpDurationDictView.as_view(), name='从业时间管理后台字典挺适合'),
    path('expertise_level/', OpExpertiseLevelView.as_view(), name='技能等级管理后台'),
    path('expertise_level_dict/', OpExpertiseLevelDictView.as_view(), name='技能等级管理后台字典映射'),
    path('modules/', ModulesManage.as_view(), name='模块管理后台'),
    path('modules_dict/', ModulesDictManage.as_view(), name='模块管理后台字典映射'),
    path('question_set/', OpQuestionsSetView.as_view(), name='问题集管理后台'),
    path('question_set_dict/', OpQuestionsSetDictView.as_view(), name='问题集构建查询字典'),
    path('question_edit/', OpQuestionsEditView.as_view(), name='问题集编辑管理后台'),
    path('tech_assistant/', UpProblemView.as_view(), name='技术支持'),
    path('approval_transfer/', UsersBankCardWithdrawalView.as_view(), name='审核转账'),
    path('messages/', OmtMessageCenterManage.as_view(), name='消息中心'),
    path('messages/get_content/', OmtMessageCenterManage.as_view(), name='消息中心-获取消息体'),
    path('messages_overview/', OmtMessageCenterOverviewManage.as_view(), name='消息中心-获取消息体'),
    path('info_type/', OiInfoTypesView.as_view(), name='消息中心-获取消息体'),
    path('info_type_dict/', OiInfoTypesDictView.as_view(), name='获取附加类型字典'),
    path('info_option/', OioInfoOptionsView.as_view(), name='获取自建文本框，选择器类型'),
    path('info_option_dict/', OioInfoOptionsDictView.as_view(), name='获取附加类型内容字典'),
    path('info_option_user/', OioInfoOptionsUserView.as_view(), name='获取用户建立文本框，选择器类型'),
    path('info_option_user_dict/', OioInfoOptionsUserDictView.as_view(), name='获取用户建立文本框，选择器类型'),
    path('info_question/', OqQuestionInfoView.as_view(), name='获取问题集拓展相关信息'),
    path('info_question_user/', OqQuestionInfoUserView.as_view(), name='获取用户建立问题集拓展相关信息'),
    path('info_question_user_dict/', OqQuestionInfoUserDictView.as_view(), name='获取用户建立问题集拓展相关信息'),
    path('info_question_user_detail/', UQDUserQuestionDetailsView.as_view(), name='删除用户建立问题集拓展相关详情信息'),
    path('info_question_user_detail_dict/', OqQuestionInfoUserDetailDictView.as_view(), name='获取用户建立问题集拓展相关详情信息字典映射'),
    path('get_documents/', GetRelatedDocuments.as_view(), name='获取相关文档'),
    path('question_square/', CCChatSquareView.as_view(), name='问答广场审核'),
    path('customer_products/', CPCustomerProductsView.as_view(), name='客户产品管理'),
    path('customer_info/', OCICustomerInformationView.as_view(), name='客户信息管理'),
    path('customer_info_dict/', CustomerInfoDict.as_view(), name='客户信息字典'),
    path('customer_balance/', CustomerBalance.as_view(), name='客户余额'),
    path('customer_balance_public/', CustomerBalancePublic.as_view(), name='客户余额'),
    path('enterprise/', EnterpriseInfoManage.as_view(), name='企业信息'),
    path('sd_models/', SdModelsManage.as_view(), name='stable diffusion 模型管理'),
    path('dhe/', DigitalHumanExperienceManage.as_view(), name='数字人客户反馈管理'),
    path('dh_products/', DigitalHumanProductManage.as_view(), name='数字人产品管理'),
    path('dh_secret/', DigitalHumanSecretKeyManage.as_view(), name='数字人密钥管理'),
    path('assign_customer/', AssignCustomer.as_view(), name='分配客户'),
    path('dh_personal_center/', DigitalPersonalCenter.as_view(), name='数字人个人中心'),
    path('qr_codes/', QRCodeManage.as_view(), name='获取二维码'),
    path('get_short_url/', ShortUrl.as_view(), name='get_short_url'),
    path('distributor/', DistributorLevelManage.as_view(), name='分销商'),
    path('hashrate_rules/', HashratesRules.as_view(), name='管理计费规则'),
    path('speech_voice/', VtTextToSpeechVoiceManage.as_view(), name='管理声音'),
    path('vt_voice_id/', VtVoiceIdManagement.as_view(), name='火山引擎声音克隆')
]

urlpatterns += admin_urls


