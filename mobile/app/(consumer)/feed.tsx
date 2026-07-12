import { useCallback, useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, RefreshControl, ScrollView } from 'react-native';
import { useFocusEffect, useRouter } from 'expo-router';
import { ListingFeed } from '../../src/features/consumer';
import { listProducts, updateLocation, type FeedProduct } from '../../src/api/endpoints';
import { useLocation } from '../../src/hooks/useLocation';
import { theme } from '../../src/theme';

export default function FeedScreen() {
  const router = useRouter();
  const { location } = useLocation();
  const [products, setProducts] = useState<FeedProduct[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setError(null);
    try {
      const query = location
        ? {
            lat: location.coords.latitude,
            lng: location.coords.longitude,
            radius: 10,
            sort: 'nearby',
          }
        : {};
      setProducts(await listProducts(query));
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Error');
    } finally {
      setLoading(false);
    }
  }, [location]);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load]),
  );

  // Share the consumer's location so the proximity timer can target them.
  useEffect(() => {
    if (!location) return;
    updateLocation(location.coords.latitude, location.coords.longitude).catch(() => {});
  }, [location]);

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={theme.colors.light.primary} />
      </View>
    );
  }

  if (error) {
    return (
      <ScrollView
        contentContainerStyle={styles.center}
        refreshControl={<RefreshControl refreshing={false} onRefresh={load} />}
      >
        <Text style={styles.error}>{error}</Text>
      </ScrollView>
    );
  }

  return (
    <View style={styles.container}>
      <ListingFeed products={products} onProductPress={(p) => router.push(`/listing/${p.id}`)} />
    </View>
  );
}

const styles = StyleSheet.create({
  center: {
    alignItems: 'center',
    backgroundColor: theme.colors.light.bg,
    flexGrow: 1,
    justifyContent: 'center',
  },
  container: { backgroundColor: theme.colors.light.bg, flex: 1 },
  error: { color: theme.colors.urgent, padding: 24, textAlign: 'center' },
});
