
from appium.webdriver.common.mobileby import MobileBy


appPackage = {
    'fake_location': 'com.lerist.fakelocation',
    'chrome': "com.android.chrome",
    'settings': 'com.android.settings',
    'gmail': 'com.google.android.gm',
}
appActivity = {
    'fake_location': '.ui.activity.MainActivity',
    'chrome': "com.google.android.apps.chrome.Main",
    'settings': '.Settings',
    'gmail': '.ConversationListActivityGmail',
    'gmail_wel': '.welcome.WelcomeTourActivity',
}

appBundleId = {
    'chrome': 'com.google.chrome.ios',
    'gmail': 'com.google.Gmail',
    'safari': 'com.apple.mobilesafari',
    'settings': 'com.apple.Preferences',
    'appstore': 'com.apple.AppStore',
}

android_base = {
    'text': lambda value: (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format(value)),
    'text_contains': lambda value: (
        MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{0}")'.format(value)),
    'text_view': lambda value: (MobileBy.XPATH, '//android.widget.TextView[@text="{0}"]'.format(value)),
    'button': lambda value: (
        MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").text("{0}")'.format(value)),
    'edittext': lambda value: (MobileBy.XPATH, '//android.widget.EditText[@text="{0}"]'.format(value)),
    'desc_contains': lambda value: (
        MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("{0}")'.format(value)),  # content-desc属性
}

ios_base = {
    'value': lambda v: (MobileBy.XPATH, '//*[@value="{}"]'.format(v)),
    'value_contains': lambda v: (MobileBy.XPATH, '//*[contains(@value,"{}")]'.format(v)),
    'name': lambda v: (MobileBy.XPATH, '//*[@name="{}"]'.format(v)),
    'name_contains': lambda v: (MobileBy.XPATH, '//*[contains(@name,"{}")]'.format(v)),
    'btn_name': lambda v: (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeButton" AND name=="{}"'.format(v)),
    'btn_name_contains': lambda v: (
        MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeButton" AND name CONTAINS "{}"'.format(v)),
    'switch_name': lambda v: (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeSwitch" AND name=="{}"'.format(v)),
    'switch_name_contains': lambda v: (
        MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeSwitch" AND name CONTAINS "{}"'.format(v)),
    'cell_name': lambda v: (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeCell" AND name=="{}"'.format(v)),
    'cell_name_contains': lambda v: (
        MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeCell" AND name CONTAINS "{}"'.format(v)),
}

'''
iOS键盘上的按键, 大小写敏感。特殊键shift, delete, more, space, @, ., Return, Next keyboard(切换文字, 比如中英文)大小写不敏感
'''
ios_keyboard = {
    'done': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label MATCHES "Done|完成"`]'),
    'key': lambda k: (MobileBy.ACCESSIBILITY_ID, '{0}'.format(k))
}


def scrollable(locators: [list, str]):
    if isinstance(locators, list):
        return (MobileBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().%s)' % '.'.join(locators))
    elif isinstance(locators, str):
        return (MobileBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().%s)' % locators)


def selector(locators: [list, str]):
    if isinstance(locators, list):
        return (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().%s' % '.'.join(locators))
    elif isinstance(locators, str):
        return (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().%s' % locators)


settings = {
    'nothing_en': (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("%s")' % 'Nothing'),
    'nothing_zh': (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("%s")' % '无'),
    'None': (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("%s")' % 'None'),
    'fake_location': (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('Fake Location')),
    'select_mock_app_en': (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("%s")' % 'Mock'),
    'select_mock_app_zh': (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("%s")' % '模拟位置'),
    'select_text_zh': '选择模拟位置信息应用',
    'select_text_en': 'Select mock location app',

    # ********* iOS ************
    'ios_setting_page_title': (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="Settings"]'),
    'ios_setting_search_field': (MobileBy.ACCESSIBILITY_ID, 'Search'),
    # 蓝牙页面元素：开启时，value属性为1，关闭时value属性为0
    'ios_bluetooth': (MobileBy.IOS_PREDICATE, 'type=="{0}" AND name=="{1}"'.format('XCUIElementTypeSwitch','Bluetooth')),
    'ios_bluetooth2': (MobileBy.XPATH, '//XCUIElementTypeSwitch[@name="Bluetooth"]'),
    # setting主页元素：On/Off元素，点击进入蓝牙页面
    'ios_bluetooth_item': (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="Bluetooth"]/following-sibling::XCUIElementTypeStaticText[1]'),
    'ios_setting_items': lambda x: (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeCell" AND name=="{0}"'.format(x)),
    'ios_setting_toggles': lambda x: (MobileBy.XPATH, '//XCUIElementTypeSwitch[@name="{0}"]'.format(x)),
    'ios_setting_wifi': (MobileBy.XPATH, '//XCUIElementTypeSwitch[@name="Wi-Fi"]'),
    'ios_back_to_current_app': (MobileBy.ACCESSIBILITY_ID, 'breadcrumb'),  # 这个记得要加approach = 'p'
    'ios_setting_items_title': lambda x: (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeOther" AND name=="{0}"'.format(x)),
    # 'ios_general': (MobileBy.IOS_PREDICATE, 'type=="{0}" AND name=="{1}"'.format('XCUIElementTypeCell', 'General')),
    'ios_general': (MobileBy.IOS_PREDICATE, 'type=="{0}" AND name=="{1}"'.format('XCUIElementTypeCell', '通用')),
    'ios_date&time': (MobileBy.IOS_PREDICATE, 'type=="{0}" AND name=="{1}"'.format('XCUIElementTypeCell', 'Date & Time')),
    'ios_profile&devicemanagement': (MobileBy.IOS_PREDICATE, 'type=="{0}" AND name CONTAINS "{1}"'.format('XCUIElementTypeCell', 'Device Management')),
    'ios_trust_app_btn': lambda x: (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeStaticText" AND value=="Trust “{0}”"'.format(x)),  # e.g. Trust “Fisher-Price, Inc.”
    'ios_trust_app_dialog_title': lambda x: (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeStaticText" AND value CONTAINS "Trust “iPhone Distribution: {0}”"'.format(x)),  # e.g. Trust “iPhone Distribution: Fisher-Price, Inc.” Apps on This iPhone
    'ios_trust_btn': (MobileBy.ACCESSIBILITY_ID, 'Trust'),
    # 24小时制的按钮，如果当前为12小时制，其value为0，否则为1
    'ios_24hr': (MobileBy.IOS_PREDICATE, 'type=="{0}" AND name=="{1}"'.format('XCUIElementTypeCell','24-Hour Time')),
    'ios_24hr_x': (MobileBy.XPATH, '//XCUIElementTypeCell[@name="24-Hour Time"]'),
}


app_store = {
    'continue': (MobileBy.IOS_PREDICATE, 'label == "继续" AND name == "继续" AND type == "XCUIElementTypeButton"'),  # 继续 弹窗页面
    'allow_when_using': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "使用App时允许"`]'),
    'app_item': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "App"`]'),
    'account': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "我的帐户"`]'),
    'search_item': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "搜索"`]'),
    'search_field': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeNavigationBar[`name == "搜索"`]/XCUIElementTypeSearchField'),
    'keyboard_continue': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "继续"`]'), # 点击searchfield后出现
    'keyboard_search_btn': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "Search"`]'), # 点击searchfield后出现
    'progress_circle': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeActivityIndicator[`label MATCHES "正在载入|进行中"`]'), # 加载搜索结果的按钮
    'retry': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "重试"`]'), # 搜索失败时
    'app': lambda a: (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label CONTAINS "{}"`]'.format(a)),  # Fisher-Price® Smart Connect™
    'navigate_search_btn': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeNavigationBar[`name == "搜索"`]`]'),  # app详情页面
    'reload_btn': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "重新下载"`]'),  # app详情页面
    'get_btn': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "获取"`]'),  # app详情页面first time download
    'upgrade_btn': (MobileBy.IOS_CLASS_CHAIN, ''),
    'in_process': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "正在载入"`]'),  # circle按钮
    'downloading': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "正在下载"`]'), # 暂停按钮
    'open_app': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "打开"`]'),

}


notification = {
    'ios_notification': lambda msg_title: (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeScrollView" AND (name CONTAINS "{0}" OR label CONTAINS "{0}")'.format(msg_title)),  # 某个app的通知，多个的时候通常会重叠在一起，需要点击展开。需传入name值，一般为展开的消息的app title，如：SMART CONNECT
    'ios_nt_msg': lambda c: (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeButton" AND name=="NotificationCell" AND label CONTAINS "{}"'.format(c)), # （右滑可删除）如消息： Animal projection on your My Child's Deluxe Soother is turning off soon.
    'ios_nt_clear': lambda msg_title: (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label BEGINSWITH "{}"`]/XCUIElementTypeButton[`label == "Clear"`][1]'.format(msg_title)),  # 向左滑动消息出现的Clear button
    'ios_nt_clear_all': (MobileBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "Clear All"`]'),  # 向左滑动消息出现的Clear All button
    'ios_clear_all_btn': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeButton" AND name=="clear-button" AND value=="Notification Center"'), # 清除所有app消息按钮（x）
    'ios_clear_btn': lambda app: (MobileBy.XPATH, '//XCUIElementTypeStaticText[@name="{}"]/../following::XCUIElementTypeButton[@name="clear-button"]'.format(app)), # 清除某个app消息按钮（x）,没有label值,如Smart Connect
    'ios_confirm_clear': (MobileBy.IOS_PREDICATE, 'type=="XCUIElementTypeButton" AND name=="clear-button" AND label=="Confirm Clear"'), # 点击x出现的clear按钮，通用
}

camera = {
    # App内嵌拍照界面
    'ios_capture': (MobileBy.ACCESSIBILITY_ID, 'PhotoCapture'),
    'ios_cancel_capture': (MobileBy.ACCESSIBILITY_ID, 'Cancel'),
    'ios_switch_camera': (MobileBy.ACCESSIBILITY_ID, 'FrontBackFacingCameraChooser'),
    # 闪光灯有三个value, 分别是Automatic,On, Off, 不能使用send_keys来设置, 需要点Flash图标然后再在下面的二级菜单中选择
    'ios_flash_light': (MobileBy.ACCESSIBILITY_ID, 'Flash'),
    'ios_flash_auto': (MobileBy.ACCESSIBILITY_ID, 'Auto'),
    'ios_flash_on': (MobileBy.ACCESSIBILITY_ID, 'On'),
    'ios_flash_off': (MobileBy.ACCESSIBILITY_ID, 'Off'),
    # 预览界面
    'ios_retake': (MobileBy.ACCESSIBILITY_ID, 'Retake'),
    'ios_use': (MobileBy.ACCESSIBILITY_ID, 'Use Photo'),
    # 剪切界面
    'ios_crop_use': (MobileBy.ACCESSIBILITY_ID, 'useButton'),
    'ios_crop_cancel': (MobileBy.ACCESSIBILITY_ID, 'cancelButton'),
}

albums = {
    # App相册界面(选取相)
    'ios_cancel': (MobileBy.ACCESSIBILITY_ID, 'Cancel'),
    # 各个相册, 使用时引用相册的名字即可, 系统默认的相册一般有: Camera Roll, Recently Added, Screenshots, 还有各个App自建的相册
    'ios_albums': lambda x: (MobileBy.ACCESSIBILITY_ID, '{0}'.format(x)),
    'ios_back_btn': (MobileBy.ACCESSIBILITY_ID, 'Photos'),  # 这个位于左上角的返回键, 是用于返回相册列表的
    # 相册里的相, 一般来说最新的相会出现在相册的最后, 可以引入last()来获取, 或者输入数字来获取第N张相, 比如输入200就会获得相册中第200张相
    # 这里要注意相册里可以显示的相是有限的, 选取了没显示的相点击第一次, 相册会自动跳转到被选择的相的可显示位置, 再点击一次才最终选择到这张相
    'ios_photos_by_position': lambda x: (MobileBy.XPATH, '//XCUIElementTypeCollectionView[@name="PhotosGridView"]/XCUIElementTypeCell[{0}]'.format(x)),

    # 剪切界面
    'ios_crop_use': (MobileBy.ACCESSIBILITY_ID, 'useButton'),
    'ios_crop_cancel': (MobileBy.ACCESSIBILITY_ID, 'cancelButton'),
}


fake_location = {
    'menu_btn': (MobileBy.ACCESSIBILITY_ID, 'Open navigation drawer'),
    'start_to_fake': (MobileBy.ID, 'com.lerist.fakelocation:id/f_fakeloc_tv_service_switch'),
    'add_btn': (MobileBy.ID, 'com.lerist.fakelocation:id/fab'),
    'current_coords': (MobileBy.ID, 'com.lerist.fakelocation:id/f_fakeloc_tv_current_latlong'),
    'running_mode': (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('运行模式')),
    'no_root_mode': (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{0}")'.format('NOROOT')),
    'root_mode': (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{0}")'.format('ROOT（推荐）')),
    'permission_allow': (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('允许')),
    'permission_allow_id': (MobileBy.ID, 'com.android.packageinstaller:id/dialog_container'),
    'title_choose_location': (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('选择位置')),
    'search_btn': (MobileBy.ID, 'com.lerist.fakelocation:id/m_item_search'),
    'search_box': (MobileBy.ID, 'com.lerist.fakelocation:id/l_search_panel_et_input'),
    'confirm_btn': (MobileBy.ID, 'com.lerist.fakelocation:id/a_map_btn_done'),
    'back_btn': (MobileBy.ACCESSIBILITY_ID, '转到上一层级'),
    'update_next_time': (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('下次再说')),
    'forward_toset': (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('前往设置')),
    'get_permission': (MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('前往授权')),

    # 通用元素-提示框&提示框的确认取消按钮
    'native_dialog': (MobileBy.ID, 'android:id/parentPanel'),
    'prompt_dialog': (MobileBy.ID, 'com.lerist.fakelocation:id/parentPanel'),
    'dialog_confirm_btn': (MobileBy.ID, 'android:id/button1'),
    'dialog_cancel_btn': (MobileBy.ID, 'android:id/button2'),
}
