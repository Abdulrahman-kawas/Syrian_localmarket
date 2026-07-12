import { useState } from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { useRouter, Link } from 'expo-router';
import { Button, Input } from '../../src/components';
import { theme } from '../../src/theme';
import i18n from '../../src/i18n';
import { useAuthStore } from '../../src/store/authStore';

export default function LoginScreen() {
  const router = useRouter();
  const login = useAuthStore((s) => s.login);
  const isLoading = useAuthStore((s) => s.isLoading);
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  async function onSubmit() {
    setError(null);
    try {
      await login(identifier.trim(), password);
      router.replace('/');
    } catch {
      setError(i18n.t('loginFailed'));
    }
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>{i18n.t('login')}</Text>
      <Input
        label={i18n.t('emailOrPhone')}
        value={identifier}
        onChangeText={setIdentifier}
        autoCapitalize="none"
        keyboardType="email-address"
      />
      <Input
        label={i18n.t('password')}
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <Button title={i18n.t('login')} onPress={onSubmit} loading={isLoading} />
      <View style={styles.row}>
        <Text style={styles.muted}>{i18n.t('noAccount')} </Text>
        <Link href="/(auth)/signup" style={styles.link}>
          {i18n.t('signup')}
        </Link>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 24,
    gap: 14,
    backgroundColor: theme.colors.light.bg,
  },
  title: { fontSize: 26, fontWeight: '700', color: theme.colors.light.text, marginBottom: 8 },
  error: { color: theme.colors.urgent },
  row: { flexDirection: 'row', justifyContent: 'center', marginTop: 12 },
  muted: { color: theme.colors.light.textSoft },
  link: { color: theme.colors.light.primary, fontWeight: '600' },
});
