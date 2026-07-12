import { useState } from 'react';
import { Text, StyleSheet, ScrollView } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Button, Input } from '../../src/components';
import { theme } from '../../src/theme';
import i18n from '../../src/i18n';
import { useAuthStore } from '../../src/store/authStore';

export default function VerifyScreen() {
  const router = useRouter();
  const { identifier } = useLocalSearchParams<{ identifier: string }>();
  const verify = useAuthStore((s) => s.verify);
  const isLoading = useAuthStore((s) => s.isLoading);
  const [code, setCode] = useState('');
  const [error, setError] = useState<string | null>(null);

  async function onSubmit() {
    setError(null);
    try {
      await verify(String(identifier ?? ''), code.trim());
      router.replace('/');
    } catch {
      setError(i18n.t('verifyFailed'));
    }
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>{i18n.t('verify')}</Text>
      <Text style={styles.muted}>{i18n.t('enterCode')}</Text>
      <Input
        label={i18n.t('verificationCode')}
        value={code}
        onChangeText={setCode}
        keyboardType="number-pad"
        maxLength={10}
      />
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <Button title={i18n.t('verify')} onPress={onSubmit} loading={isLoading} />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.light.bg,
    flexGrow: 1,
    gap: 14,
    justifyContent: 'center',
    padding: 24,
  },
  error: { color: theme.colors.urgent },
  muted: { color: theme.colors.light.textSoft },
  title: { color: theme.colors.light.text, fontSize: 26, fontWeight: '700' },
});
