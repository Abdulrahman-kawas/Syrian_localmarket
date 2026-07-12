import { useState } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { useRouter, Link } from 'expo-router';
import { Button, Input } from '../../src/components';
import { theme } from '../../src/theme';
import i18n from '../../src/i18n';
import { useAuthStore } from '../../src/store/authStore';

type Role = 'consumer' | 'seller';

export default function SignupScreen() {
  const router = useRouter();
  const signup = useAuthStore((s) => s.signup);
  const isLoading = useAuthStore((s) => s.isLoading);
  const [role, setRole] = useState<Role>('consumer');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);

  async function onSubmit() {
    setError(null);
    try {
      await signup({
        email: email.trim(),
        phone: phone.trim(),
        password,
        role,
        verificationMethod: 'email',
      });
      router.replace({ pathname: '/(auth)/verify', params: { identifier: email.trim() } });
    } catch {
      setError(i18n.t('signupFailed'));
    }
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>{i18n.t('signup')}</Text>

      <Text style={styles.label}>{i18n.t('selectRole')}</Text>
      <View style={styles.roleRow}>
        {(['consumer', 'seller'] as Role[]).map((r) => (
          <TouchableOpacity
            key={r}
            style={[styles.rolePill, role === r && styles.rolePillActive]}
            onPress={() => setRole(r)}
          >
            <Text style={[styles.roleText, role === r && styles.roleTextActive]}>
              {r === 'consumer' ? i18n.t('consumer') : i18n.t('seller')}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <Input
        label={i18n.t('email')}
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
        keyboardType="email-address"
      />
      <Input label={i18n.t('phone')} value={phone} onChangeText={setPhone} keyboardType="phone-pad" />
      <Input label={i18n.t('password')} value={password} onChangeText={setPassword} secureTextEntry />
      {error ? <Text style={styles.error}>{error}</Text> : null}
      <Button title={i18n.t('signup')} onPress={onSubmit} loading={isLoading} />
      <View style={styles.row}>
        <Text style={styles.muted}>{i18n.t('haveAccount')} </Text>
        <Link href="/(auth)/login" style={styles.link}>
          {i18n.t('login')}
        </Link>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.light.bg,
    flexGrow: 1,
    gap: 12,
    justifyContent: 'center',
    padding: 24,
  },
  error: { color: theme.colors.urgent },
  label: { color: theme.colors.light.textSoft, fontSize: 13 },
  link: { color: theme.colors.light.primary, fontWeight: '600' },
  muted: { color: theme.colors.light.textSoft },
  rolePill: {
    alignItems: 'center',
    borderColor: theme.colors.light.line,
    borderRadius: 10,
    borderWidth: 1,
    flex: 1,
    paddingVertical: 12,
  },
  rolePillActive: {
    backgroundColor: theme.colors.light.primary,
    borderColor: theme.colors.light.primary,
  },
  roleRow: { flexDirection: 'row', gap: 10 },
  roleText: { color: theme.colors.light.text, fontWeight: '600' },
  roleTextActive: { color: theme.colors.light.onPrimary },
  row: { flexDirection: 'row', justifyContent: 'center', marginTop: 12 },
  title: { color: theme.colors.light.text, fontSize: 26, fontWeight: '700', marginBottom: 4 },
});
