import { useCallback, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { useFocusEffect, useRouter } from 'expo-router';
import { ConsumerMap } from '../../src/features/consumer';
import { nearbySellers } from '../../src/api/endpoints';
import { useLocation } from '../../src/hooks/useLocation';
import { theme } from '../../src/theme';
import i18n from '../../src/i18n';

type MapSeller = {
  id: string;
  shopName: string;
  type: 'shop' | 'factory';
  latitude: number;
  longitude: number;
};

// Fallback center (Damascus) until device location is available.
const DAMASCUS = { latitude: 33.5138, longitude: 36.2765 };

export default function MapScreen() {
  const router = useRouter();
  const { location } = useLocation();
  const [sellers, setSellers] = useState<MapSeller[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    const center = location?.coords ?? DAMASCUS;
    try {
      setSellers(await nearbySellers(center.latitude, center.longitude, 10));
    } catch {
      setSellers([]);
    } finally {
      setLoading(false);
    }
  }, [location]);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load]),
  );

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={theme.colors.light.primary} />
        <Text style={styles.muted}>{i18n.t('nearbyDeals')}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ConsumerMap
        sellers={sellers}
        onSellerPress={(s) => router.push(`/(consumer)/feed`)}
        onMapPress={() => {}}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  center: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: theme.colors.light.bg,
  },
  muted: { color: theme.colors.light.textSoft },
});
