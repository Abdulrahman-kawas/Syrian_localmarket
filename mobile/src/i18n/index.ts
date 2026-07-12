import { I18n } from 'i18n-js';
import { ar } from './ar';
import { en } from './en';

const i18n = new I18n({
  ar,
  en,
});

i18n.defaultLocale = 'ar';
i18n.locale = 'ar';
i18n.enableFallback = true;

export default i18n;
