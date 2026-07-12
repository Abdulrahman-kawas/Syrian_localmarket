import Expo from 'expo/config';

export default {
  ...Expo,
  name: 'LocalMarket',
  slug: 'localmarket',
  version: '0.1.0',
  orientation: 'portrait',
  icon: './assets/icon.png',
  userInterfaceStyle: 'automatic',
  splash: {
    image: './assets/splash.png',
    resizeMode: 'contain',
    backgroundColor: '#0F3D2E',
  },
  assetBundlePatterns: ['**/*'],
  ios: {
    supportsTablet: true,
    bundleIdentifier: 'com.localmarket.app',
    // Certificate pinning (iOS 14+, release builds — not Expo Go). Replace the
    // placeholder with the real SPKI SHA-256 pin (see docs/CERT_PINNING.md).
    infoPlist: {
      NSAppTransportSecurity: {
        NSPinnedDomains: {
          'api.localmarket.app': {
            NSIncludesSubdomains: true,
            NSPinnedCAIdentities: [
              { 'SPKI-SHA256-BASE64': 'REPLACE_WITH_REAL_SPKI_PIN_BASE64=' },
            ],
          },
        },
      },
    },
  },
  android: {
    adaptiveIcon: {
      foregroundImage: './assets/adaptive-icon.png',
      backgroundColor: '#0F3D2E',
    },
    package: 'com.localmarket.app',
  },
  web: {
    favicon: './assets/favicon.png',
  },
  plugins: [
    'expo-router',
    // Android certificate pinning via a network-security-config pin-set.
    [
      './plugins/withAndroidCertPinning',
      {
        host: 'api.localmarket.app',
        pins: ['REPLACE_WITH_REAL_SPKI_PIN_BASE64='],
      },
    ],
  ],
};
