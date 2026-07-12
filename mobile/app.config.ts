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
  plugins: ['expo-router'],
};
