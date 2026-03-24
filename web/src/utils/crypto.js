import CryptoJS from 'crypto-js'

// 固定的 AES 加密密钥和 IV (与后端保持一致)
const SECRET_KEY = '7A4B2C9D8E1F6G3H5I0J2K4L8M6N0O2P'
const IV = '1A2B3C4D5E6F7G8H'

let isInitialized = false

function checkKeys() {
  if (!isInitialized) {
    throw new Error('加密密钥未初始化，请先调用 initKeys()')
  }
}

export async function initKeys() {
  // 固定密钥，无需从后端获取
  console.log('使用固定加密密钥')
  isInitialized = true
  return true
}

export function setKeys(secretKey, iv) {
  // 保留此函数以兼容，但不再使用
  console.warn('setKeys 已废弃，请使用固定密钥')
}

export function getKeys() {
  return { secretKey: SECRET_KEY, iv: IV }
}

export function encrypt(data) {
  try {
    checkKeys()
    const key = CryptoJS.enc.Utf8.parse(SECRET_KEY)
    const iv = CryptoJS.enc.Utf8.parse(IV)
    const encrypted = CryptoJS.AES.encrypt(data, key, {
      iv: iv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    }).toString()
    return encrypted
  } catch (error) {
    console.error('加密失败:', error)
    throw new Error('数据加密失败')
  }
}

export function decrypt(encryptedData) {
  try {
    checkKeys()
    const key = CryptoJS.enc.Utf8.parse(SECRET_KEY)
    const iv = CryptoJS.enc.Utf8.parse(IV)
    const decrypted = CryptoJS.AES.decrypt(encryptedData, key, {
      iv: iv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    })
    const result = decrypted.toString(CryptoJS.enc.Utf8)
    if (!result) {
      throw new Error('解密结果为空')
    }
    return result
  } catch (error) {
    console.error('解密失败:', error)
    throw new Error('数据解密失败')
  }
}