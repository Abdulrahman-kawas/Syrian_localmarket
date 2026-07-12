import { useState } from 'react';
import { View, StyleSheet, Alert } from 'react-native';
import { useRouter } from 'expo-router';
import { QRScanner } from '../../src/features/consumer';
import { scanQr } from '../../src/api/endpoints';
import { theme } from '../../src/theme';
import i18n from '../../src/i18n';

export default function ScanScreen() {
  const router = useRouter();
  const [busy, setBusy] = useState(false);

  async function onScan(code: string) {
    if (busy) return;
    setBusy(true);
    try {
      const res = await scanQr(code);
      Alert.alert(
        i18n.t('success'),
        `${i18n.t('scanToBuy')} — ${res.status}`,
        [{ text: 'OK', onPress: () => router.replace('/(consumer)/feed') }],
      );
    } catch (e) {
      Alert.alert(i18n.t('error'), e instanceof Error ? e.message : 'Error');
    } finally {
      setBusy(false);
    }
  }

  return (
    <View style={styles.container}>
      <QRScanner onScan={onScan} onCancel={() => router.replace('/(consumer)/feed')} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { backgroundColor: theme.colors.light.bg, flex: 1 },
});
