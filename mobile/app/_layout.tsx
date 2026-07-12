import { useEffect } from 'react';
import { I18nManager } from 'react-native';
import { Stack } from 'expo-router';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import i18n from '../src/i18n';
import { useAuthStore } from '../src/store/authStore';

// Force RTL when the app locale is Arabic (default). Takes effect app-wide.
if (i18n.locale?.startsWith('ar') && !I18nManager.isRTL) {
  I18nManager.allowRTL(true);
  I18nManager.forceRTL(true);
}

export default function RootLayout() {
  const hydrate = useAuthStore((s) => s.hydrate);

  useEffect(() => {
    hydrate();
  }, [hydrate]);

  return (
    <SafeAreaProvider>
      <StatusBar style="dark" />
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="index" />
        <Stack.Screen name="(auth)" />
        <Stack.Screen name="(consumer)" />
        <Stack.Screen name="(seller)" />
        <Stack.Screen name="listing/[id]" options={{ headerShown: true, title: '' }} />
        <Stack.Screen name="chat/[id]" options={{ headerShown: true, title: 'Chat' }} />
      </Stack>
    </SafeAreaProvider>
  );
}
