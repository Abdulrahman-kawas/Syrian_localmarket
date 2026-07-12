import { useEffect } from 'react';
import { View, ActivityIndicator, StyleSheet } from 'react-native';
import { useRouter } from 'expo-router';
import { useAuthStore } from '../src/store/authStore';
import { theme } from '../src/theme';

// Entry gate: route by auth + role once the token is hydrated.
export default function Index() {
  const router = useRouter();
  const { hydrated, token, user } = useAuthStore();

  useEffect(() => {
    if (!hydrated) return;
    if (!token) {
      router.replace('/(auth)/login');
    } else if (user?.role === 'seller') {
      router.replace('/(seller)/listings');
    } else {
      router.replace('/(consumer)/feed');
    }
  }, [hydrated, token, user, router]);

  return (
    <View style={styles.center}>
      <ActivityIndicator size="large" color={theme.colors.light.primary} />
    </View>
  );
}

const styles = StyleSheet.create({
  center: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: theme.colors.light.bg,
  },
});
