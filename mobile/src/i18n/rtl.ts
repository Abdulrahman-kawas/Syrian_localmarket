import { I18nManager } from 'react-native';

export const isRTL = I18nManager.isRTL;

export const setRTL = (enabled: boolean): void => {
  I18nManager.forceRTL(enabled);
  I18nManager.allowRTL(enabled);
};

export const toggleRTL = (): void => {
  const newRTL = !I18nManager.isRTL;
  I18nManager.forceRTL(newRTL);
  I18nManager.allowRTL(newRTL);
};
