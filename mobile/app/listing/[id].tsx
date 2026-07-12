import { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, Linking } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { ListingDetail } from '../../src/features/consumer';
import { getProduct, createConversation, type DetailProduct } from '../../src/api/endpoints';
import { theme } from '../../src/theme';

export default function ListingDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const [product, setProduct] = useState<DetailProduct | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        setProduct(await getProduct(String(id)));
      } catch (e) {
        setError(e instanceof Error ? e.message : 'Error');
      }
    })();
  }, [id]);

  if (error) {
    return (
      <View style={styles.center}>
        <Text style={styles.error}>{error}</Text>
      </View>
    );
  }

  if (!product) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={theme.colors.light.primary} />
      </View>
    );
  }

  return (
    <ListingDetail
      product={product}
      onCallSeller={() => {
        if (product.seller.phone) Linking.openURL(`tel:${product.seller.phone}`);
      }}
      onChatSeller={async () => {
        if (!product.seller.userId) return;
        try {
          const convo = await createConversation(product.seller.userId);
          router.push(`/chat/${convo.id}`);
        } catch {
          router.push('/(consumer)/chat');
        }
      }}
      onScanQR={() => router.push('/(consumer)/scan')}
    />
  );
}

const styles = StyleSheet.create({
  center: {
    alignItems: 'center',
    backgroundColor: theme.colors.light.bg,
    flex: 1,
    justifyContent: 'center',
  },
  error: { color: theme.colors.urgent, padding: 24, textAlign: 'center' },
});
