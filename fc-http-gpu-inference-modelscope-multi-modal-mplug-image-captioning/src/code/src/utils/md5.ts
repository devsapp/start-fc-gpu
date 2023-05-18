import CryptoJS from 'crypto-js';

export function md5(value: string) {
  return CryptoJS.MD5(value).toString();
}
