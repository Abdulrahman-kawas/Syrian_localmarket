import { useCallback, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, TouchableOpacity } from 'react-native';
import { useFocusEffect, useRouter } from 'expo-router';
import { ListingFeed } from '../../src/features/consumer';
import { myListings, type FeedProduct } from '../../src/api/endpoints';
import { useAuthStore } from '../../src/store/authStore';
import { theme } from '../../src/theme';
import i18n from '../../src/i18n';

export default function SellerListings() {
  const router = useRouter();
  const logout = useAuthStore((s) => s.logout);
  const [products, setProducts] = useState<FeedProduct[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    try {
      setProducts(await myListings());
    } catch {
      setProducts([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load]),
  );

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={theme.colors.light.primary} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {products.length === 0 ? (
        <View style={styles.center}>
          <Text style={styles.muted}>{i18n.t('noListings')}</Text>
          <TouchableOpacity onPress={() => router.push('/(seller)/create')}>
            <Text style={styles.link}>{i18n.t('createListing')}</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <ListingFeed products={products} onProductPress={(p) => router.push(`/listing/${p.id}`)} />
      )}
      <TouchableOpacity style={styles.signout} onPress={logout}>
        <Text style={styles.muted}>{i18n.t('signOut')}</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: theme.colors.light.bg },
  center: { flex: 1, alignItems: 'center', justifyContent: 'center', gap: 10 },
  muted: { color: theme.colors.light.textSoft },
  link: { color: theme.colors.light.primary, fontWeight: '600' },
  signout: { padding: 16, alignItems: 'center' },
});
