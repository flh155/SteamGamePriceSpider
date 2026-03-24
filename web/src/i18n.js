import { createI18n } from 'vue-i18n'

// 中文语言包
const zhCN = {
  common: {
    appTitle: 'Steam 游戏价格助手',
    logoText: 'Steam 价格追踪',
    home: '首页',
    hotGames: '热门游戏 功能开发中',
    about: '关于 功能开发中',
    settings: '设置',
    logout: '退出登录',
    footer: '2026 Steam 价格追踪 数据来源 IsThereAnyDeal API',
    search: '搜索',
    cancel: '取消',
    confirm: '确认',
    save: '保存',
    delete: '删除',
    edit: '编辑',
    loading: '加载中',
    success: '成功',
    error: '错误',
    warning: '警告',
    tip: '提示',
    viewDetail: '查看详情'
  },
  initPassword: {
    subtitle: '首次使用，请设置管理员密码',
    confirmPasswordPlaceholder: '请确认管理员密码',
    submit: '设置密码',
    passwordRequirements: '密码安全要求',
    passwordLength: '密码长度至少 8 位，最多 32 位',
    passwordTypes: '必须包含以下四种字符中的至少两种',
    uppercase: '大写字母 A 到 Z',
    lowercase: '小写字母 a 到 z',
    numbers: '数字 0 到 9',
    specialChars: '常用符号',
    noSpaceChinese: '不能包含空格、中文或其他特殊字符',
    savePassword: '请妥善保管您的密码',
    alreadyInitializedTitle: '密码已初始化',
    alreadyInitializedMessage: '管理员密码已经完成初始化，无法再次设置',
    goToLogin: '前往登录',
    checking: '正在检查初始化状态'
  },
  login: {
    welcomeBack: '欢迎回来，请登录您的账户',
    passwordPlaceholder: '请输入管理员密码',
    login: '登录',
    loginSuccess: '登录成功',
    loginFailed: '登录失败，请检查密码',
    passwordRequired: '请输入密码',
    passwordMinLength: '密码长度至少 8 位',
    loading: '正在检查初始化状态'
  },
  home: {
    title: '查找 Steam 游戏价格',
    subtitle: '快速比较各平台价格，发现最佳优惠',
    searchPlaceholder: '输入游戏英文名称，例如 Elden Ring, Cyberpunk 2077',
    searching: '查询中，请稍后',
    searchSuccess: '查询成功',
    searchError: '查询失败，请重试',
    pleaseEnterGameName: '请输入游戏名称',
    noData: '暂无数据',
    apiKeyConfig: {
      title: '首次使用 请配置 API Key',
      warningText: '检测到您尚未配置 API Key，请先完成配置才能使用本系统',
      label: 'IsThereAnyDeal API Key',
      placeholder: '请输入你的 API Key',
      tip1: 'API Key 用于查询 Steam 游戏价格数据，请妥善保管',
      tip2: '你可以在 IsThereAnyDeal API 官网 获取',
      saveAndContinue: '保存并继续',
      pleaseConfigApiKey: '请先配置 API Key'
    },
    resultSection: {
      title: '搜索结果',
      coverImage: '封面图片',
      noImage: '暂无图片',
      currentLowestPrice: '当前最低价',
      lowestShop: '在售平台',
      historicalLowestPrice: '历史最低价',
      lowestShopHistory: '史低平台',
      steamCurrentPrice: 'Steam 当前价',
      steamShop: '在售平台 Steam'
    }
  },
  settings: {
    title: '系统设置',
    apiConfig: 'API 配置',
    apiKeyLabel: 'IsThereAnyDeal API Key',
    apiKeyPlaceholder: '请输入你的 API Key',
    apiKeyTip1: 'API Key 用于查询 Steam 游戏价格数据，请妥善保管',
    apiKeyTip2: '你可以在 IsThereAnyDeal API 官网 获取',
    saveApiKey: '保存 API Key',
    saveApiKeySuccess: 'API Key 保存成功',
    changePassword: '修改登录密码',
    currentPassword: '当前密码',
    currentPasswordPlaceholder: '请输入当前密码',
    newPassword: '新密码',
    newPasswordPlaceholder: '请输入新密码',
    confirmPassword: '确认新密码',
    confirmPasswordPlaceholder: '请再次输入新密码',
    passwordRequirement: '密码要求 8-32 位，包含大小写字母、数字、特殊符号中的至少两种',
    changePasswordAndRelogin: '修改密码并重新登录',
    passwordChangeSuccess: '密码修改成功，请重新登录',
    passwordRequired: '请输入密码',
    passwordMinLength: '密码长度至少为 8 位',
    passwordMaxLength: '密码长度不能超过 32 位',
    passwordNoSpace: '密码不能包含空格',
    passwordNoChinese: '密码不能包含中文字符',
    passwordStrength: '密码必须包含大写字母、小写字母、数字、特殊符号中的至少两种',
    passwordNotMatch: '两次输入的密码不一致'
  },
  language: {
    switchLanguage: '切换语言',
    chinese: '中文',
    english: 'English'
  }
}

// 英文语言包
const enUS = {
  common: {
    appTitle: 'Steam Game Price Assistant',
    logoText: 'Steam Price Tracker',
    home: 'Home',
    hotGames: 'Hot Games Coming Soon',
    about: 'About Coming Soon',
    settings: 'Settings',
    logout: 'Logout',
    footer: '2026 Steam Price Tracker Data Source IsThereAnyDeal API',
    search: 'Search',
    cancel: 'Cancel',
    confirm: 'Confirm',
    save: 'Save',
    delete: 'Delete',
    edit: 'Edit',
    loading: 'Loading',
    success: 'Success',
    error: 'Error',
    warning: 'Warning',
    tip: 'Tip',
    viewDetail: 'View Details'
  },
  initPassword: {
    subtitle: 'First time use, please set admin password',
    confirmPasswordPlaceholder: 'Please confirm admin password',
    submit: 'Set Password',
    passwordRequirements: 'Password Requirements',
    passwordLength: 'Password length must be between 8 and 32 characters',
    passwordTypes: 'Must contain at least two of the following four character types',
    uppercase: 'Uppercase letters A to Z',
    lowercase: 'Lowercase letters a to z',
    numbers: 'Numbers 0 to 9',
    specialChars: 'Special symbols',
    noSpaceChinese: 'Cannot contain spaces, Chinese characters, or other special characters',
    savePassword: 'Please keep your password safe',
    alreadyInitializedTitle: 'Password Already Initialized',
    alreadyInitializedMessage: 'Admin password has been initialized and cannot be set again',
    goToLogin: 'Go to Login',
    checking: 'Checking initialization status'
  },
  login: {
    welcomeBack: 'Welcome back, please log in to your account',
    passwordPlaceholder: 'Please enter admin password',
    login: 'Login',
    loginSuccess: 'Login successful',
    loginFailed: 'Login failed, please check your password',
    passwordRequired: 'Please enter password',
    passwordMinLength: 'Password must be at least 8 characters',
    loading: 'Checking initialization status'
  },
  home: {
    title: 'Find Steam Game Prices',
    subtitle: 'Quickly compare prices across platforms and find the best deals',
    searchPlaceholder: 'Enter game name in English, e.g. Elden Ring, Cyberpunk 2077',
    searching: 'Searching, please wait',
    searchSuccess: 'Search successful',
    searchError: 'Search failed, please try again',
    pleaseEnterGameName: 'Please enter game name',
    noData: 'No data',
    apiKeyConfig: {
      title: 'First Time Use Please Configure API Key',
      warningText: 'No API Key detected. Please configure it to use this system',
      label: 'IsThereAnyDeal API Key',
      placeholder: 'Please enter your API Key',
      tip1: 'API Key is used to query Steam game price data, please keep it secure',
      tip2: 'You can get it from IsThereAnyDeal API official website',
      saveAndContinue: 'Save and Continue',
      pleaseConfigApiKey: 'Please configure API Key first'
    },
    resultSection: {
      title: 'Search Results',
      coverImage: 'Cover Image',
      noImage: 'No Image Available',
      currentLowestPrice: 'Current Lowest Price',
      lowestShop: 'Available at',
      historicalLowestPrice: 'Historical Lowest Price',
      lowestShopHistory: 'Lowest at',
      steamCurrentPrice: 'Steam Current Price',
      steamShop: 'Available at Steam'
    }
  },
  settings: {
    title: 'System Settings',
    apiConfig: 'API Configuration',
    apiKeyLabel: 'IsThereAnyDeal API Key',
    apiKeyPlaceholder: 'Please enter your API Key',
    apiKeyTip1: 'API Key is used to query Steam game price data, please keep it secure',
    apiKeyTip2: 'You can get it from IsThereAnyDeal API official website',
    saveApiKey: 'Save API Key',
    saveApiKeySuccess: 'API Key saved successfully',
    changePassword: 'Change Login Password',
    currentPassword: 'Current Password',
    currentPasswordPlaceholder: 'Please enter current password',
    newPassword: 'New Password',
    newPasswordPlaceholder: 'Please enter new password',
    confirmPassword: 'Confirm New Password',
    confirmPasswordPlaceholder: 'Please enter new password again',
    passwordRequirement: 'Password requirement 8-32 characters, with at least two of uppercase, lowercase, numbers, special symbols',
    changePasswordAndRelogin: 'Change Password and Re-login',
    passwordChangeSuccess: 'Password changed successfully, please re-login',
    passwordRequired: 'Please enter password',
    passwordMinLength: 'Password must be at least 8 characters',
    passwordMaxLength: 'Password cannot exceed 32 characters',
    passwordNoSpace: 'Password cannot contain spaces',
    passwordNoChinese: 'Password cannot contain Chinese characters',
    passwordStrength: 'Password must contain at least two of uppercase, lowercase, numbers, special symbols',
    passwordNotMatch: 'The two passwords do not match'
  },
  language: {
    switchLanguage: 'Switch Language',
    chinese: '中文',
    english: 'English'
  }
}

// 创建 i18n 实例
const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('locale') || 'zh-CN',
  fallbackLocale: 'en-US',
  messages: {
    'zh-CN': zhCN,
    'en-US': enUS
  }
})

export default i18n